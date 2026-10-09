# -*- coding: utf-8 -*-
"""공모사업(지원사업) 수집

두 갈래를 합친다.
 1) 검증해 둔 공모 목록 — grants_curated.json (공식 공고 주소가 있는 것만, 마감 지나면 자동으로 빠진다)
 2) 행정안전부 「대한민국 공공서비스(혜택) 정보」 오픈API — 공공데이터포털에서 **따로 활용신청**한 뒤 켜진다.
    신청 전에는 401 이 나고, 그때는 안내만 남기고 1) 만 쓴다.

규칙(프로젝트 CLAUDE.md 와 같다): 제목·기관·기간·링크까지만. 지원내용 같은 본문은 가져오지 않는다.
"""
import json
import os
import re
import sys
import time
from datetime import date

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import classify
import config

_DATE_RE = re.compile(r"(20\d{2})\s*[.\-/년]\s*(\d{1,2})\s*[.\-/월]\s*(\d{1,2})")
_ALWAYS = ("상시", "연중", "수시", "예산 소진", "예산소진")


def parse_deadline(text, today=None):
    """신청기한 글에서 마감일을 뽑는다.

    돌려주는 값: (deadline 'YYYY-MM-DD' 또는 '', expired 여부)
      · 날짜가 여럿이면(기간) 가장 늦은 날짜를 마감으로 본다.
      · 날짜가 없고 상시·연중·수시면 마감 없음('')으로 남긴다.
      · 가장 늦은 날짜가 오늘보다 앞서면 expired=True.
    """
    today = today or date.today()
    t = str(text or "")
    dates = []
    for y, m, d in _DATE_RE.findall(t):
        try:
            dates.append(date(int(y), int(m), int(d)))
        except ValueError:
            continue
    if dates:
        last = max(dates)
        return last.isoformat(), last < today
    return "", False


def _gov24_url(row):
    u = str(row.get("상세조회URL") or "").strip()
    if u.startswith("http"):
        return u
    sid = str(row.get("서비스ID") or "").strip()
    return f"https://www.gov.kr/portal/rcvfvrSvc/dtlEx/{sid}" if sid else "https://www.gov.kr/"


def _normalize_gov24(row, today=None):
    """공공서비스(혜택) 응답 한 건 → 공통 스키마. 응답 항목 이름은 공식 명세(odcloud Swagger) 기준."""
    sid = str(row.get("서비스ID") or "").strip()
    title = str(row.get("서비스명") or "").strip()
    org = str(row.get("소관기관명") or "").strip()
    deadline, expired = parse_deadline(row.get("신청기한"), today)
    posted = classify.ymd(row.get("등록일시"))
    posted_at = f"{posted[:4]}-{posted[4:6]}-{posted[6:8]}" if posted else ""
    return {
        "uid": f"gov24:{sid}",
        "kind": "grant",
        "source": "공공서비스(혜택)",
        "title": title,
        "org": org,
        "region": classify.detect_region(org, title),
        "posted_at": posted_at,
        "start_date": "",
        "end_date": "",
        "deadline": deadline,
        "budget": "",
        "place": "",
        "image": "",
        "url": _gov24_url(row),
        "summary": "",
        "license": "공공데이터포털 이용허락범위 제한 없음",
        "_expired": expired,
        "_utype": str(row.get("사용자구분") or ""),
    }


def _is_relevant(rec):
    """문화·행사 쪽 단체·업체가 받을 만한 것만. 개인 혜택은 뺀다(사용자구분 기준)."""
    t = rec["title"]
    if any(x in t for x in config.GRANT_EXCLUDE_KEYWORDS):
        return False
    return any(u in rec.get("_utype", "") for u in config.GRANT_USER_TYPES)


def load_curated(today=None, path=None):
    """grants_curated.json 에서 아직 마감 안 지난 것만."""
    path = path or config.GRANTS_CURATED
    today = today or date.today()
    try:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f).get("items", [])
    except (OSError, ValueError):
        return []
    out = []
    for r in rows:
        dl = str(r.get("deadline") or "")
        n = classify.days_left(dl, today) if dl else None
        if n is not None and n < 0:
            continue                      # 마감 지남
        title = str(r.get("title") or "").strip()
        if not title or not str(r.get("url") or "").startswith("http"):
            continue                      # 제목·공식 주소가 없는 건 싣지 않는다
        out.append({
            "uid": f"grant:{r.get('id') or classify._norm_title(title)[:40]}",
            "kind": "grant",
            "source": str(r.get("source") or "한국문화예술위원회"),
            "title": title,
            "org": str(r.get("org") or ""),
            "region": classify.detect_region(r.get("org"), title),
            "posted_at": str(r.get("posted_at") or ""),
            "start_date": str(r.get("start_date") or ""),
            "end_date": str(r.get("end_date") or ""),
            "deadline": dl,
            "budget": "",
            "place": "",
            "image": "",
            "url": str(r["url"]),
            "summary": classify.truncate(r.get("summary"), 200),
            "license": "확인 필요",
        })
    return out


def fetch_gov24(log=print, today=None):
    if not config.DATA_GO_KR_KEY:
        log("공모사업(공공서비스): DATA_GO_KR_KEY 가 없어 건너뜁니다.")
        return []
    seen = {}
    for kw in config.GRANT_KEYWORDS:
        for page in range(1, config.MAX_PAGES + 1):
            params = {"serviceKey": config.DATA_GO_KR_KEY, "page": page, "perPage": 100,
                      "returnType": "JSON", "cond[서비스명::LIKE]": kw}
            try:
                r = requests.get(config.GRANT_GOV24_URL, params=params,
                                 headers={"User-Agent": config.UA}, timeout=config.TIMEOUT)
            except Exception as e:
                log(f"공모사업(공공서비스) 호출 실패({kw} p{page}): {e}")
                break
            if r.status_code in (401, 403):
                log("공모사업(공공서비스): 이 키로는 아직 호출이 안 됩니다 — 공공데이터포털에서 "
                    "'행정안전부_대한민국 공공서비스(혜택) 정보' 활용신청(자동승인) 뒤 다시 실행하세요. "
                    "(검증해 둔 목록만 사용합니다)")
                return []
            try:
                r.raise_for_status()
                body = r.json()
            except Exception as e:
                log(f"공모사업(공공서비스) 응답 오류({kw} p{page}): {e}")
                break
            rows = body.get("data") or []
            for row in rows:
                rec = _normalize_gov24(row, today)
                if rec["uid"] != "gov24:" and rec["title"] and rec["uid"] not in seen:
                    seen[rec["uid"]] = rec
            total = int(body.get("matchCount") or body.get("totalCount") or 0)
            if not rows or page * 100 >= total:
                break
            time.sleep(config.REQUEST_DELAY)
        time.sleep(config.REQUEST_DELAY)
    out, standing = [], 0
    for rec in seen.values():
        expired = rec.pop("_expired")
        if not _is_relevant(rec) or expired:
            continue
        if not rec["deadline"]:
            standing += 1               # 상시·연중·미정 안내는 「접수 중인 공모」가 아니라서 싣지 않는다
            continue
        rec.pop("_utype", None)
        out.append(rec)
    log(f"공모사업(공공서비스): 기한이 정해진 {len(out)}건 (상시·연중 안내 {standing}건은 제외)")
    return out


def fetch(log=print):
    items = load_curated()
    log(f"공모사업(검증 목록): {len(items)}건")
    items += fetch_gov24(log)
    return items

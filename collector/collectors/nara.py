# -*- coding: utf-8 -*-
"""나라장터 용역 입찰공고 수집 (공공데이터포털 입찰공고정보서비스)

조회기간 제한(약 15일) 때문에 LOOKBACK_DAYS 를 CHUNK_DAYS 단위로 쪼개 호출한다.
"""
import os
import sys
import time
from datetime import datetime, timedelta

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import classify
import config


def _normalize(row):
    """API 응답 한 건을 공통 스키마로. 첫 실 수집 후 필드명이 문서와 다르면 여기부터 확인."""
    no = str(row.get("bidNtceNo", "")).strip()
    ord_ = str(row.get("bidNtceOrd", "00")).strip() or "00"
    title = str(row.get("bidNtceNm", "")).strip()
    org = str(row.get("dminsttNm") or row.get("ntceInsttNm") or "").strip()
    url = str(row.get("bidNtceDtlUrl") or row.get("bidNtceUrl") or "https://www.g2b.go.kr/").strip()
    return {
        "uid": f"nara:{no}-{ord_}",
        "kind": "bid",
        "source": "나라장터",
        "title": title,
        "org": org,
        "region": classify.detect_region(org, title),
        "posted_at": str(row.get("bidNtceDt", ""))[:16],
        "start_date": "",
        "end_date": "",
        "deadline": str(row.get("bidClseDt", ""))[:16],
        "budget": classify.parse_budget(row.get("presmptPrce") or row.get("asignBdgtAmt")),
        "place": "",
        "image": "",
        "url": url,
        "summary": "",
        "license": "나라장터 공개정보",
    }


def fetch(log=print):
    """LOOKBACK_DAYS 범위의 용역 공고를 받아 행사 관련만 돌려준다."""
    if not config.DATA_GO_KR_KEY:
        log("나라장터: DATA_GO_KR_KEY 가 없어 건너뜁니다.")
        return []

    out = []
    end = datetime.now()
    begin = end - timedelta(days=config.LOOKBACK_DAYS)
    cur = begin
    while cur < end:
        chunk_end = min(cur + timedelta(days=config.CHUNK_DAYS), end)
        for page in range(1, config.MAX_PAGES + 1):
            params = {
                "serviceKey": config.DATA_GO_KR_KEY,
                "numOfRows": 100,
                "pageNo": page,
                "inqryDiv": 1,
                "inqryBgnDt": cur.strftime("%Y%m%d") + "0000",
                "inqryEndDt": chunk_end.strftime("%Y%m%d") + "2359",
                "type": "json",
            }
            try:
                r = requests.get(f"{config.NARA_BASE}/{config.NARA_OP}",
                                 params=params, timeout=config.TIMEOUT)
                r.raise_for_status()
                body = r.json().get("response", {}).get("body", {})
            except Exception as e:
                log(f"나라장터 호출 실패({cur:%m/%d}~, p{page}): {e}")
                break
            rows = body.get("items") or []
            if isinstance(rows, dict):          # 1건이면 dict 로 오는 API가 있다
                rows = rows.get("item") or []
            if isinstance(rows, dict):
                rows = [rows]
            for row in rows:
                rec = _normalize(row)
                if rec["title"] and classify.is_event(rec["title"]):
                    out.append(rec)
            total = int(body.get("totalCount") or 0)
            if page * 100 >= total:
                break
            time.sleep(config.REQUEST_DELAY)
        cur = chunk_end
        time.sleep(config.REQUEST_DELAY)
    log(f"나라장터: 행사 관련 {len(out)}건")
    return out

# -*- coding: utf-8 -*-
"""공모사업 검증 목록(grants_curated.json) 검사기 — 주간 갱신 루틴의 관문

  python validate_grants.py                # 형식 검사
  python validate_grants.py --check-urls   # + 각 공고 주소를 한 번씩 열어 「근거 문장」이 실제로 있는지 대조
  python validate_grants.py --prune        # 마감이 14일 넘게 지난 항목을 파일에서 지운다
  python validate_grants.py --peek URL [키워드 …]   # 공식 공고 페이지 글자를 있는 그대로 보여 준다(근거 문장 베끼기용)

왜 이렇게 하나: 이 목록은 사람 없이 라이브에 오른다. 그래서 항목마다 공식 공고 페이지에서 베껴 온
`evidence`(근거 문장)를 두게 하고, 검사기가 그 문장이 **그 주소의 실제 페이지 글자에 있는지** 직접 확인한다.
(근거가 떨어진 두 곳에 있으면 「앞 조각 … 뒤 조각」처럼 …로 잇는다. 조각마다 페이지에 있어야 한다.)
지어낸 날짜나 제목은 여기서 걸린다. 페이지를 열 수 없거나(스크립트로만 그려지는 페이지 등) robots.txt 가
막는 곳은 검증 못 한 것으로 보고 싣지 않는다.

주소 열기 규칙(프로젝트 규칙과 같다): 연락처가 있는 User-Agent, 요청 간격 config.REQUEST_DELAY 이상,
robots.txt 준수, 항목당 한 번(같은 주소는 한 번만). 목록 페이지를 훑지 않는다.
"""
import json
import os
import re
import sys
import time
import urllib.robotparser
from datetime import date, timedelta
from urllib.parse import urlparse

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import config

BLOCK_HOSTS = ("blog.naver.com", "cafe.naver.com", "m.blog.naver.com", "post.naver.com", "instagram.com",
               "facebook.com", "youtube.com", "youtu.be", "tistory.com", "brunch.co.kr", "band.us",
               "twitter.com", "x.com", "threads.net", "kakao.com", "open.kakao.com", "medium.com",
               "bit.ly", "naver.me", "tinyurl.com")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2})?$")
_ID = re.compile(r"^[0-9a-z]+(-[0-9a-z]+)*$")
PRUNE_AFTER_DAYS = 14


def _strip_html(html):
    t = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("&nbsp;", " ").replace("&amp;", "&").replace("&middot;", "·")
    return t


def squash(s):
    """공백을 모두 없앤 비교용 글자."""
    return re.sub(r"\s+", "", str(s or ""))


def date_in_text(iso, text):
    """ISO 날짜(YYYY-MM-DD[ HH:MM])의 월·일이 text 에 흔한 꼴로 들어 있는지.
    예: 2026.11.5 · 2026. 11. 05. · 2026-11-05 · 11월 5일 · 11.5 · 11/5"""
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(iso or ""))
    if not m:
        return False
    y, mo, d = m.group(1), int(m.group(2)), int(m.group(3))
    t = squash(text)
    mm, dd = f"{mo}", f"{d}"
    pats = [
        rf"{y}[.\-/년]0?{mm}[.\-/월]0?{dd}(?!\d)",
        rf"(?<!\d)0?{mm}월0?{dd}일",
        rf"(?<![\d.])0?{mm}[./]0?{dd}(?!\d)",
    ]
    return any(re.search(p, t) for p in pats)


def check_static(item, today=None):
    """항목 하나의 형식 검사. 오류 문자열 목록."""
    E = []
    today = today or date.today()
    iid = str(item.get("id") or "")
    if not _ID.match(iid):
        E.append(f"id 는 영소문자·숫자·- 만: {iid!r}")
    title = str(item.get("title") or "").strip()
    if not (8 <= len(title) <= 120):
        E.append(f"title 길이 {len(title)}자 (8~120)")
    if not str(item.get("org") or "").strip():
        E.append("org(주관 기관)이 비어 있다")
    url = str(item.get("url") or "")
    host = (urlparse(url).hostname or "").lower()
    if not url.startswith("https://") or not host:
        E.append("url 은 https:// 로 시작하는 공식 공고 주소여야 한다")
    elif any(host == h or host.endswith("." + h) for h in BLOCK_HOSTS):
        E.append(f"블로그·SNS·단축 주소는 근거가 아니다: {host}")
    elif not host.endswith(".kr"):
        E.append(f"공식 기관 주소(.kr)가 아니다: {host}")
    for k in ("posted_at", "start_date", "end_date", "deadline"):
        v = str(item.get(k) or "")
        if v and not _DATE.match(v) and not (k in ("posted_at", "start_date", "end_date") and re.match(r"^\d{4}-\d{2}-\d{2}$", v)):
            E.append(f"{k} 형식이 YYYY-MM-DD[ HH:MM] 이 아니다: {v!r}")
    dl = str(item.get("deadline") or "")
    if not dl and not re.search(r"미정|예정", title + str(item.get("summary") or "")):
        E.append("deadline 이 없으면 제목이나 summary 에 「미정」·「예정」이 있어야 한다")
    if dl and _DATE.match(dl) and dl[:10] < (today - timedelta(days=PRUNE_AFTER_DAYS)).isoformat():
        E.append(f"마감이 {PRUNE_AFTER_DAYS}일 넘게 지났다(--prune 으로 지운다): {dl}")
    if len(str(item.get("summary") or "")) > 200:
        E.append("summary 는 200자 이하(본문 전재 금지)")
    ev = str(item.get("evidence") or "").strip()
    if not (12 <= len(ev) <= 240):
        E.append(f"evidence(공식 페이지에서 베껴 온 근거 문장) 길이 {len(ev)}자 (12~240)")
    elif dl and _DATE.match(dl) and not date_in_text(dl, ev):
        E.append(f"evidence 에 마감일({dl[:10]})이 보이지 않는다")
    ck = str(item.get("checked_at") or "")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", ck):
        E.append("checked_at(확인한 날) YYYY-MM-DD 가 필요하다")
    return E


def check_unique(items):
    ids = [i.get("id") for i in items]
    return [f"id 중복: {x}" for x in sorted({x for x in ids if ids.count(x) > 1})]


class Fetcher:
    """공식 공고 주소를 정중하게 한 번씩 연다 — robots.txt · 간격 · 같은 주소 캐시."""

    def __init__(self, delay=None):
        self.delay = config.REQUEST_DELAY if delay is None else delay
        self._robots, self._pages, self._last = {}, {}, 0.0
        self.s = requests.Session()
        self.s.headers["User-Agent"] = config.UA

    def _wait(self):
        gap = self.delay - (time.time() - self._last)
        if gap > 0:
            time.sleep(gap)
        self._last = time.time()

    def allowed(self, url):
        u = urlparse(url)
        base = f"{u.scheme}://{u.netloc}"
        if base not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                self._wait()
                r = self.s.get(base + "/robots.txt", timeout=15)
                if r.status_code == 200 and "<html" not in r.text[:300].lower():
                    rp.parse(r.text.splitlines())
                else:
                    rp.parse([])            # robots.txt 가 없으면 제한 없음
            except Exception:
                rp.parse([])
            self._robots[base] = rp
        return self._robots[base].can_fetch(config.UA, url)

    def text(self, url):
        """(상태, 글자). 상태: ok | robots | http-NNN | error"""
        if url in self._pages:
            return self._pages[url]
        if not self.allowed(url):
            res = ("robots", "")
        else:
            try:
                self._wait()
                r = self.s.get(url, timeout=config.TIMEOUT)
                if r.status_code != 200:
                    res = (f"http-{r.status_code}", "")
                else:
                    r.encoding = r.apparent_encoding or r.encoding
                    res = ("ok", _strip_html(r.text))
            except Exception as e:
                res = ("error", str(e)[:80])
        self._pages[url] = res
        return res


def check_online(items, fetcher=None):
    """항목별 (id, 오류 문자열) 목록. evidence 가 실제 페이지에 있어야 통과."""
    fetcher = fetcher or Fetcher()
    out = []
    for it in items:
        status, text = fetcher.text(it.get("url", ""))
        if status != "ok":
            out.append((it.get("id"), f"공고 페이지를 확인하지 못했다({status}) — 검증 불가라 싣지 않는다"))
            continue
        parts = [p for p in re.split(r"\s*…\s*", str(it.get("evidence") or "")) if p.strip()]
        if not parts or any(squash(p) not in squash(text) for p in parts):
            out.append((it.get("id"), "evidence 문장이 그 주소의 실제 페이지에 없다 — 베낀 문장이 아니거나 페이지가 바뀌었다"))
    return out


def load(path=None):
    with open(path or config.GRANTS_CURATED, encoding="utf-8") as f:
        return json.load(f)


def save(doc, path=None):
    with open(path or config.GRANTS_CURATED, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")


def prune(doc, today=None):
    """마감이 PRUNE_AFTER_DAYS 넘게 지난 항목을 뺀 새 doc 과 지운 id 목록."""
    today = today or date.today()
    cut = (today - timedelta(days=PRUNE_AFTER_DAYS)).isoformat()
    keep, gone = [], []
    for it in doc.get("items", []):
        dl = str(it.get("deadline") or "")[:10]
        (gone if dl and dl < cut else keep).append(it)
    new = dict(doc)
    new["items"] = keep
    return new, [i.get("id") for i in gone]


def peek(url, keywords=(), width=90):
    """공고 페이지를 정중하게 한 번 열어 글자를 있는 그대로 보여 준다. evidence 는 여기 나온 글자에서 베껴 쓴다."""
    f = Fetcher()
    status, text = f.text(url)
    print(f"상태: {status}  주소: {url}")
    if status != "ok":
        return 1
    flat = re.sub(r"\s+", " ", text).strip()
    print(f"글자 수: {len(flat)}" + ("  (거의 없음 — 스크립트로 그려지는 페이지일 수 있어 근거로 못 쓴다)" if len(flat) < 300 else ""))
    seen = 0
    for kw in keywords:
        for m in re.finditer(re.escape(kw), flat):
            seen += 1
            if seen > 12:
                break
            print(f"[{kw}] …{flat[max(0, m.start() - width):m.end() + width]}…")
    if not keywords:
        print(flat[:600])
    return 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "--peek":
        if len(argv) < 2:
            print("사용법: --peek URL [키워드 …]")
            return 2
        return peek(argv[1], argv[2:])
    path = config.GRANTS_CURATED
    doc = load(path)
    if "--prune" in argv:
        doc, gone = prune(doc)
        if gone:
            save(doc, path)
        print(f"지움 {len(gone)}건: {', '.join(gone) if gone else '-'}")
    items = doc.get("items", [])
    bad = 0
    for e in check_unique(items):
        print("✗", e); bad += 1
    for it in items:
        errs = check_static(it)
        if errs:
            bad += 1
            print(f"✗ {it.get('id')}")
            for e in errs:
                print("   -", e)
    if "--check-urls" in argv:
        for iid, e in check_online(items):
            bad += 1
            print(f"✗ {iid}\n   - {e}")
    print(f"\n{'실패 ' + str(bad) + '건' if bad else '모두 통과'} (항목 {len(items)}개)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

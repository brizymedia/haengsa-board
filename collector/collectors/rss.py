# -*- coding: utf-8 -*-
"""지자체 RSS 수집

원칙 (법적·운영상 제약 — 임의로 완화하지 말 것):
- 공식 RSS 만 읽는다. 게시판 HTML 직접 파싱은 금지.
- robots.txt 가 거부하면 건너뛴다. 이 확인 로직을 우회하지 말 것.
- 요약은 200자에서 자른다 (본문 전재 금지).
- license 는 기관별 공공누리 유형 확인 전까지 "확인 필요" 로 둔다.

피드 생사 확인:  python -m collectors.rss --check
"""
import hashlib
import os
import re
import sys
import time
import urllib.robotparser
from urllib.parse import urlparse

import feedparser
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import classify
import config

_robots_cache = {}


def robots_allows(url, ua=None):
    """해당 URL 수집을 robots.txt 가 허용하는지. 응답이 없으면 허용으로 본다."""
    ua = ua or config.UA
    host = urlparse(url).scheme + "://" + urlparse(url).netloc
    if host not in _robots_cache:
        rp = urllib.robotparser.RobotFileParser()
        try:
            r = requests.get(host + "/robots.txt", timeout=config.TIMEOUT,
                             headers={"User-Agent": ua})
            if r.status_code == 200:
                rp.parse(r.text.splitlines())
            else:
                rp.parse([])          # robots.txt 없음 → 허용
        except Exception:
            rp.parse([])
        _robots_cache[host] = rp
    return _robots_cache[host].can_fetch(ua, url)


def _strip_html(s):
    return re.sub(r"<[^>]+>", "", str(s or "")).strip()


def _normalize(feed_name, entry):
    title = _strip_html(entry.get("title", ""))
    link = str(entry.get("link", "")).strip()
    uid = "rss:" + hashlib.md5((link or title).encode("utf-8")).hexdigest()[:16]
    posted = ""
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    if t:
        posted = time.strftime("%Y-%m-%d", t)
    return {
        "uid": uid,
        "kind": "notice",
        "source": feed_name,
        "title": title,
        "org": "",
        "region": classify.detect_region(feed_name, title),
        "posted_at": posted,
        "start_date": "",
        "end_date": "",
        "deadline": "",
        "budget": "",
        "place": "",
        "image": "",
        "url": link,
        "summary": classify.truncate(_strip_html(entry.get("summary", "")), 200),
        "license": "확인 필요",
    }


def fetch(log=print):
    """등록된 모든 피드에서 행사 관련 항목만 모은다."""
    out = []
    for name, url in config.RSS_FEEDS:
        if not robots_allows(url):
            log(f"RSS [{name}]: robots.txt 가 수집을 거부해 건너뜁니다.")
            continue
        try:
            r = requests.get(url, timeout=config.TIMEOUT,
                             headers={"User-Agent": config.UA})
            r.raise_for_status()
            parsed = feedparser.parse(r.content)
        except Exception as e:
            log(f"RSS [{name}]: 읽기 실패 — {e}")
            continue
        kept = 0
        for entry in parsed.entries:
            rec = _normalize(name, entry)
            if rec["title"] and classify.is_event(rec["title"]):
                out.append(rec)
                kept += 1
        log(f"RSS [{name}]: {len(parsed.entries)}건 중 행사 관련 {kept}건")
        time.sleep(config.REQUEST_DELAY)
    return out


def check(log=print):
    """피드 생사 확인. 지자체가 홈페이지를 개편하면 RSS 가 조용히 죽는다."""
    ok = 0
    for name, url in config.RSS_FEEDS:
        try:
            r = requests.get(url, timeout=config.TIMEOUT,
                             headers={"User-Agent": config.UA})
            parsed = feedparser.parse(r.content)
            n = len(parsed.entries)
            alive = r.status_code == 200 and n > 0
            ok += 1 if alive else 0
            mark = "정상" if alive else "확인 필요"
            log(f"[{mark}] {name} — HTTP {r.status_code}, 항목 {n}건 · {url}")
        except Exception as e:
            log(f"[실패] {name} — {e} · {url}")
        time.sleep(config.REQUEST_DELAY)
    log(f"총 {len(config.RSS_FEEDS)}개 중 정상 {ok}개")
    return ok


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    else:
        for rec in fetch():
            print(rec["region"], "|", rec["title"])

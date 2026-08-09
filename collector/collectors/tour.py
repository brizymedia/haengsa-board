# -*- coding: utf-8 -*-
"""TourAPI 축제·공연·행사 수집 (한국관광공사 국문 관광정보 서비스, contentTypeId=15)

엔드포인트 버전이 KorService1 → KorService2 처럼 오른다.
호출이 갑자기 실패하면 config.TOUR_BASE 부터 확인할 것.
"""
import os
import sys
import time
from datetime import datetime, timedelta
from urllib.parse import quote

import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import classify
import config


def _normalize(row):
    """API 응답 한 건을 공통 스키마로. 첫 실 수집 후 필드명이 다르면 여기부터 확인."""
    title = str(row.get("title", "")).strip()
    addr = str(row.get("addr1", "")).strip()
    start = str(row.get("eventstartdate", ""))[:8]
    end = str(row.get("eventenddate", ""))[:8]
    fmt = lambda d: f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 else ""
    org = (addr.split()[0] + " " + addr.split()[1] if len(addr.split()) >= 2 else addr) or ""
    # TourAPI 는 개별 상세 URL 을 주지 않는다. 공사 공식 검색 페이지로 연결한다.
    url = "https://korean.visitkorea.or.kr/search/search_list.do?keyword=" + quote(title)
    return {
        "uid": f"tour:{row.get('contentid', '')}",
        "kind": "festival",
        "source": "TourAPI",
        "title": title,
        "org": (addr + " 일원") if addr else "",
        "region": classify.detect_region(addr, title),
        "posted_at": "",
        "start_date": fmt(start),
        "end_date": fmt(end),
        "deadline": fmt(end),          # 축제는 종료일을 마감으로 본다
        "budget": "",
        "place": (addr + " 일원") if addr else "",
        "image": str(row.get("firstimage", "")).strip(),
        "url": url,
        "summary": "",
        "license": "한국관광공사 TourAPI",
    }


def fetch(log=print):
    """오늘 이후 LOOKAHEAD_DAYS 안에 열리는 축제를 시도 구분 없이 받아온다."""
    if not config.DATA_GO_KR_KEY:
        log("TourAPI: DATA_GO_KR_KEY 가 없어 건너뜁니다.")
        return []

    out = []
    start = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    for page in range(1, config.MAX_PAGES + 1):
        params = {
            "serviceKey": config.DATA_GO_KR_KEY,
            "numOfRows": 100,
            "pageNo": page,
            "MobileOS": "ETC",
            "MobileApp": "haengsa-board",
            "_type": "json",
            # KorService1 의 listYN 은 KorService2 에서 폐지됐다 (넣으면 INVALID_REQUEST_PARAMETER_ERROR)
            "arrange": "A",
            "eventStartDate": start,
        }
        try:
            r = requests.get(f"{config.TOUR_BASE}/{config.TOUR_OP}",
                             params=params, timeout=config.TIMEOUT)
            r.raise_for_status()
            body = r.json().get("response", {}).get("body", {})
        except Exception as e:
            log(f"TourAPI 호출 실패(p{page}): {e}")
            break
        rows = (body.get("items") or {})
        rows = rows.get("item") if isinstance(rows, dict) else rows
        if not rows:
            break
        if isinstance(rows, dict):
            rows = [rows]
        horizon = (datetime.now() + timedelta(days=config.LOOKAHEAD_DAYS)).strftime("%Y-%m-%d")
        for row in rows:
            rec = _normalize(row)
            if rec["title"] and rec["start_date"] and rec["start_date"] <= horizon:
                out.append(rec)
        total = int(body.get("totalCount") or 0)
        if page * 100 >= total:
            break
        time.sleep(config.REQUEST_DELAY)
    log(f"TourAPI: 축제·행사 {len(out)}건")
    return out

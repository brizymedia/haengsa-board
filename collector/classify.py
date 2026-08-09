# -*- coding: utf-8 -*-
"""행사 판정 · 시도 추출 · 중복 제거 · 점수 · 정렬"""
import re
from datetime import date, datetime

import config

# 별칭은 긴 것부터 적는다. 같은 위치에서 겹치면 긴 별칭이 이긴다.
SIDO_ALIASES = [
    ("서울", ["서울특별시", "서울시", "서울"]),
    ("부산", ["부산광역시", "부산시", "부산"]),
    ("대구", ["대구광역시", "대구시", "대구"]),
    ("인천", ["인천광역시", "인천시", "인천"]),
    ("광주", ["광주광역시", "광주"]),
    ("대전", ["대전광역시", "대전시", "대전"]),
    ("울산", ["울산광역시", "울산시", "울산"]),
    ("세종", ["세종특별자치시", "세종시", "세종"]),
    ("경기", ["경기도", "경기"]),
    ("강원", ["강원특별자치도", "강원도", "강원"]),
    ("충북", ["충청북도", "충북"]),
    ("충남", ["충청남도", "충남"]),
    ("전북", ["전북특별자치도", "전라북도", "전북"]),
    ("전남", ["전라남도", "전남"]),
    ("경북", ["경상북도", "경북"]),
    ("경남", ["경상남도", "경남"]),
    ("제주", ["제주특별자치도", "제주도", "제주"]),
]


def is_event(title):
    """제목만 보고 행사 관련 여부를 판정한다."""
    t = str(title or "")
    if not t:
        return False
    if any(x in t for x in config.EXCLUDE_KEYWORDS):
        return False
    return any(k in t for k in config.EVENT_KEYWORDS)


def detect_region(*texts):
    """*가장 앞에 나온* 시·도명을 채택한다. 기관명이 관례상 시·도로 시작하기 때문.

    이래야 '광주광역시 북구'는 광주로, '경기도 광주시'는 경기로 갈린다.
    길이나 가중치 기반으로 바꾸면 회귀한다 — tests.py 가 잡는다.
    앞 인자(기관명)에서 먼저 찾고, 없으면 다음 인자(제목)로 넘어간다.
    """
    for text in texts:
        t = str(text or "")
        if not t:
            continue
        best = None  # (위치, -별칭길이, 시도)
        for sido, aliases in SIDO_ALIASES:
            for a in aliases:
                pos = t.find(a)
                if pos < 0:
                    continue
                cand = (pos, -len(a), sido)
                if best is None or cand < best:
                    best = cand
        if best:
            return best[2]
    return ""


def ymd(s):
    """날짜 문자열에서 YYYYMMDD 여덟 자리만 뽑는다. 못 뽑으면 None."""
    d = re.sub(r"\D", "", str(s or ""))[:8]
    return d if len(d) == 8 else None


def days_left(s, today=None):
    """마감까지 남은 일수. 오늘 마감이면 0, 지났으면 음수, 날짜가 없으면 None."""
    d = ymd(s)
    if not d:
        return None
    today = today or date.today()
    target = date(int(d[:4]), int(d[4:6]), int(d[6:8]))
    return (target - today).days


def parse_budget(v):
    """'240,000,000원' 따위를 '240000000' 문자열로. 숫자가 없으면 ''."""
    d = re.sub(r"\D", "", str(v or ""))
    return d.lstrip("0") or "" if d else ""


def truncate(s, n=200):
    """RSS 요약은 200자에서 자른다 — 본문 전재 금지 규칙."""
    s = str(s or "").strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def _norm_title(s):
    """중복 판정용 제목 정규화: 공백·기호 제거."""
    return re.sub(r"[\s\W_]+", "", str(s or ""), flags=re.UNICODE)


def dedupe(items):
    """같은 (정규화 제목, 지역) 은 하나만 남긴다. 출처 우선순위 nara > tour > rss."""
    prio = {"nara": 0, "tour": 1, "rss": 2}
    seen = {}
    for r in items:
        key = (_norm_title(r.get("title")), r.get("region", ""))
        p = prio.get(str(r.get("uid", "")).split(":", 1)[0], 9)
        if key not in seen or p < seen[key][0]:
            seen[key] = (p, r)
    return [v[1] for v in seen.values()]


def score(rec, today=None):
    """노출 우선순위. 마감이 임박할수록, 사업비가 클수록 위로. 지난 건 아래로."""
    s = 0
    n = days_left(rec.get("deadline"), today)
    if n is not None:
        if n < 0:
            s -= 90 if rec.get("kind") == "festival" else 70
        elif n == 0:
            s += 50
        elif n <= 3:
            s += 40
        elif n <= 7:
            s += 30
        elif n <= 14:
            s += 20
        else:
            s += 10
    b = int(parse_budget(rec.get("budget")) or 0)
    if b >= 200_000_000:
        s += 15
    elif b >= 100_000_000:
        s += 10
    elif b >= 50_000_000:
        s += 5
    p = days_left(rec.get("posted_at"), today)
    if p is not None and -3 <= p <= 0:   # 최근 사흘 내 게시
        s += 5
    return s


def finalize(items, today=None):
    """점수·남은 일수 채우고 정렬해 돌려준다."""
    for r in items:
        r["score"] = score(r, today)
        r["days_left"] = days_left(r.get("deadline"), today)
    def sort_key(r):
        n = r["days_left"]
        return (-r["score"], 9999 if n is None else (9998 if n < 0 else n))
    return sorted(items, key=sort_key)

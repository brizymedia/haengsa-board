# -*- coding: utf-8 -*-
"""예시 데이터 생성 — API 키 없이 화면·검증을 돌려보기 위한 것.

실 데이터와 같은 스키마로 오늘 날짜 기준 121건을 만들어
../site/data/events.json 에 mock:true 로 저장한다. 운영 후 삭제해도 된다.
"""
import random
from datetime import date, timedelta

import classify
import store

SIDO = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종",
        "강원", "경기", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]

GU = {"서울": ["마포구", "성동구", "종로구"], "부산": ["기장군", "중구"],
      "대구": ["수성구", "중구"], "인천": ["강화군", "연수구", "중구"],
      "광주": ["북구", "동구"], "대전": ["유성구", "대덕구"],
      "울산": ["남구", "울주군"], "세종": [""],
      "강원": ["춘천시", "강릉시", "평창군"], "경기": ["수원시", "고양시", "남양주시", "가평군"],
      "충북": ["청주시", "제천시", "단양군"], "충남": ["천안시", "보령시", "부여군"],
      "전북": ["전주시", "군산시", "무주군"], "전남": ["순천시", "담양군", "광양시"],
      "경북": ["포항시", "안동시", "영주시"], "경남": ["통영시", "하동군"], "제주": ["제주시", "서귀포시"]}

THEME = ["벚꽃", "단풍", "불꽃", "빙어", "머드", "장미", "국화", "허브",
         "한지", "재즈", "야행", "해변", "청년", "매화", "감귤", "해맞이"]

BID_FORM = ["2026 {c} {t}축제 행사대행 용역", "{c} {t}거리 야시장 운영 대행",
            "2026 {c} {t}문화제 총괄기획 및 운영용역", "{c} {t}페스티벌 조명·특수효과 임차",
            "2026 {c} 신년음악회 무대 연출", "제{n}회 {c}시민의날 기념식 무대·음향 설치",
            "제{n}회 {c} 생활체육대회 대행용역", "2026 {c} 청소년 한마당 행사 운영용역",
            "{c} 관광 홍보 부스 설치 및 운영", "2026 {c} 농특산물 박람회 부대시설 설치"]

FEST_FORM = ["2026 {c} {t}축제", "{c} {t}문화제", "2026 {c} {t}페스티벌",
             "{c} {t}빛축제", "{c} 전통연희 한마당"]

RSS_FORM = ["2026 {c} {t}축제 부대행사 운영자 모집 공고", "2026 {c} 지역축제 안전관리계획 고시",
            "{c} 문화행사 프리마켓 셀러 모집 공고", "{c} {t}행사 교통통제 안내 공고"]

BUDGETS = [18, 24, 35, 42, 68, 95, 120, 185, 240]   # 백만원 단위


def _pick_city(rng):
    sido = rng.choice(SIDO)
    gu = rng.choice(GU[sido])
    org = (sido + " " + gu).strip()
    city = (gu or sido).replace("시", "").replace("군", "").replace("구", "") \
        if gu and gu[-1] in "시군" else (gu or sido)
    return sido, org, city or sido


def generate(today=None, seed=2037):    # 이 시드에서 중복 제거 후 정확히 121건이 나온다
    rng = random.Random(seed)
    today = today or date.today()
    items = []

    for i in range(55):     # 나라장터 입찰
        sido, org, city = _pick_city(rng)
        form = rng.choice(BID_FORM)
        title = form.format(c=city, t=rng.choice(THEME), n=rng.randint(4, 40))
        posted = today - timedelta(days=rng.randint(0, 25))
        deadline = posted + timedelta(days=rng.randint(7, 22))
        items.append({
            "uid": f"nara:2026{i:07d}-00", "kind": "bid", "source": "나라장터",
            "title": title, "org": org, "region": classify.detect_region(org, title),
            "posted_at": posted.strftime("%Y-%m-%d") + " 09:00",
            "start_date": "", "end_date": "",
            "deadline": deadline.strftime("%Y-%m-%d") + " 10:00",
            "budget": str(rng.choice(BUDGETS) * 1_000_000), "place": "", "image": "",
            "url": "https://www.g2b.go.kr/", "summary": "",
            "license": "나라장터 공개정보",
        })

    for i in range(44):     # TourAPI 축제
        sido, org, city = _pick_city(rng)
        title = rng.choice(FEST_FORM).format(c=city, t=rng.choice(THEME))
        start = today + timedelta(days=rng.randint(-9, 88))
        end = start + timedelta(days=rng.randint(1, 9))
        items.append({
            "uid": f"tour:28{i:05d}", "kind": "festival", "source": "TourAPI",
            "title": title, "org": org + " 일원", "region": classify.detect_region(org, title),
            "posted_at": "", "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"), "deadline": end.strftime("%Y-%m-%d"),
            "budget": "", "place": org + " 일원", "image": "",
            "url": "https://korean.visitkorea.or.kr/", "summary": "",
            "license": "한국관광공사 TourAPI",
        })

    for i in range(22):     # 지자체 RSS 고시
        sido, org, city = _pick_city(rng)
        title = rng.choice(RSS_FORM).format(c=city, t=rng.choice(THEME))
        posted = today - timedelta(days=rng.randint(0, 17))
        has_deadline = rng.random() < 0.6
        deadline = (posted + timedelta(days=rng.randint(0, 21))).strftime("%Y-%m-%d") + " 18:00" \
            if has_deadline else ""
        items.append({
            "uid": f"rss:{i:016x}", "kind": "notice", "source": f"{sido} 고시공고",
            "title": title, "org": org, "region": classify.detect_region(org, title),
            "posted_at": posted.strftime("%Y-%m-%d"), "start_date": "", "end_date": "",
            "deadline": deadline, "budget": "", "place": "", "image": "",
            "url": "https://www.example.go.kr/",
            "summary": "행사 운영과 관련한 세부 사항은 원문 공고문을 확인하시기 바랍니다.",
            "license": "확인 필요",
        })

    items = classify.dedupe(items)
    return classify.finalize(items, today)


if __name__ == "__main__":
    items = generate()
    path = store.export_json(items, mock=True)
    print(f"예시 데이터 {len(items)}건 → {path}")

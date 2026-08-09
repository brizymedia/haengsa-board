# -*- coding: utf-8 -*-
"""수집기 단위 테스트 30항목 — 분류·지역·일수·중복·저장

  cd collector && python tests.py
"""
import json
import os
import tempfile
import unittest
from datetime import date

import classify
import store
from collectors import nara, rss, tour

TODAY = date(2026, 8, 10)


class TestIsEvent(unittest.TestCase):
    def test_01_festival_keyword(self):
        self.assertTrue(classify.is_event("2026 강화 한지축제 개최 안내"))

    def test_02_bid_keyword(self):
        self.assertTrue(classify.is_event("2026 세종 야행축제 행사대행 용역"))

    def test_03_stage_keyword(self):
        self.assertTrue(classify.is_event("신년음악회 무대 연출"))

    def test_04_exclude_construction(self):
        self.assertFalse(classify.is_event("축제장 진입도로 포장공사"))

    def test_05_exclude_cleaning(self):
        self.assertFalse(classify.is_event("청사 청소용역 입찰공고"))

    def test_06_plain_notice(self):
        self.assertFalse(classify.is_event("물품 구매 입찰 공고"))

    def test_07_empty_title(self):
        self.assertFalse(classify.is_event(""))


class TestDetectRegion(unittest.TestCase):
    def test_08_simple(self):
        self.assertEqual(classify.detect_region("서울 마포구"), "서울")

    def test_09_gwangju_metro(self):
        # 광주광역시 → 광주
        self.assertEqual(classify.detect_region("광주광역시 북구"), "광주")

    def test_10_gyeonggi_gwangju(self):
        # 경기도 광주시 → 앞에 나온 경기 채택. 길이·가중치 기반으로 되돌리면 회귀한다.
        self.assertEqual(classify.detect_region("경기도 광주시"), "경기")

    def test_11_long_alias(self):
        self.assertEqual(classify.detect_region("전라남도 순천시"), "전남")

    def test_12_jeonbuk_special(self):
        self.assertEqual(classify.detect_region("전북특별자치도 전주시"), "전북")

    def test_13_org_before_title(self):
        # 기관명에서 먼저 찾고, 제목은 그다음이다
        self.assertEqual(classify.detect_region("부산 해운대구", "서울 페스티벌 대행"), "부산")

    def test_14_fallback_to_title(self):
        self.assertEqual(classify.detect_region("", "강원 강릉시 행사 대행"), "강원")

    def test_15_none(self):
        self.assertEqual(classify.detect_region("한국문화재단"), "")


class TestDates(unittest.TestCase):
    def test_16_days_left_today(self):
        self.assertEqual(classify.days_left("2026-08-10 18:00", TODAY), 0)

    def test_17_days_left_future(self):
        self.assertEqual(classify.days_left("2026-08-15", TODAY), 5)

    def test_18_days_left_past(self):
        self.assertEqual(classify.days_left("2026-08-01", TODAY), -9)

    def test_19_days_left_none(self):
        self.assertIsNone(classify.days_left("", TODAY))

    def test_20_ymd_formats(self):
        self.assertEqual(classify.ymd("2026-08-10 18:00"), "20260810")
        self.assertIsNone(classify.ymd("상시"))


class TestHelpers(unittest.TestCase):
    def test_21_parse_budget(self):
        self.assertEqual(classify.parse_budget("240,000,000원"), "240000000")
        self.assertEqual(classify.parse_budget(""), "")

    def test_22_truncate_200(self):
        s = "가" * 300
        out = classify.truncate(s, 200)
        self.assertLessEqual(len(out), 200)
        self.assertTrue(out.endswith("…"))


class TestDedupe(unittest.TestCase):
    def _rec(self, uid, title, region):
        return {"uid": uid, "title": title, "region": region}

    def test_23_same_title_region(self):
        out = classify.dedupe([self._rec("nara:1", "가평 머드축제", "경기"),
                               self._rec("rss:2", "가평 머드축제", "경기")])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["uid"], "nara:1")   # 출처 우선순위 nara > rss

    def test_24_different_region_kept(self):
        out = classify.dedupe([self._rec("rss:1", "중구 불꽃축제", "부산"),
                               self._rec("rss:2", "중구 불꽃축제", "대구")])
        self.assertEqual(len(out), 2)

    def test_25_normalized_spacing(self):
        out = classify.dedupe([self._rec("tour:1", "가평 머드축제", "경기"),
                               self._rec("rss:2", "가평  머드축제!", "경기")])
        self.assertEqual(len(out), 1)


class TestScore(unittest.TestCase):
    def test_26_expired_negative(self):
        r = {"kind": "bid", "deadline": "2026-08-01", "budget": ""}
        self.assertLess(classify.score(r, TODAY), 0)

    def test_27_today_beats_far(self):
        near = {"kind": "bid", "deadline": "2026-08-10", "budget": ""}
        far = {"kind": "bid", "deadline": "2026-09-30", "budget": ""}
        self.assertGreater(classify.score(near, TODAY), classify.score(far, TODAY))

    def test_28_sort_order(self):
        items = [{"uid": "a", "kind": "bid", "title": "지난 공고", "region": "서울",
                  "deadline": "2026-08-01", "budget": "", "posted_at": ""},
                 {"uid": "b", "kind": "bid", "title": "오늘 마감", "region": "서울",
                  "deadline": "2026-08-10", "budget": "", "posted_at": ""}]
        out = classify.finalize(items, TODAY)
        self.assertEqual(out[0]["uid"], "b")
        self.assertEqual(out[0]["days_left"], 0)
        self.assertEqual(out[-1]["days_left"], -9)


class TestStoreAndNormalize(unittest.TestCase):
    def test_29_store_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            db = os.path.join(td, "t.db")
            con = store.open_db(db)
            rec = {"uid": "nara:x-00", "title": "테스트"}
            store.upsert(con, [rec], now="2026-08-01 05:00:00")
            store.upsert(con, [rec], now="2026-08-10 05:00:00")
            # first_seen 은 보존되고 last_seen 만 갱신된다
            self.assertEqual(store.first_seen(con, "nara:x-00"), "2026-08-01 05:00:00")
            out = store.export_json([rec], path=os.path.join(td, "e.json"), mock=True)
            with open(out, encoding="utf-8") as f:
                data = json.load(f)
            self.assertTrue(data["mock"])
            self.assertEqual(data["count"], 1)
            con.close()

    def test_30_source_normalize(self):
        n = nara._normalize({"bidNtceNo": "20260001", "bidNtceOrd": "01",
                             "bidNtceNm": "2026 광주 충장축제 행사대행 용역",
                             "dminsttNm": "광주광역시 동구",
                             "bidNtceDt": "2026-08-01 09:00",
                             "bidClseDt": "2026-08-20 10:00",
                             "presmptPrce": "120000000"})
        self.assertEqual(n["uid"], "nara:20260001-01")
        self.assertEqual(n["region"], "광주")
        self.assertEqual(n["kind"], "bid")
        t = tour._normalize({"contentid": "999", "title": "화천 산천어축제",
                             "addr1": "강원특별자치도 화천군",
                             "eventstartdate": "20260901", "eventenddate": "20260910"})
        self.assertEqual(t["region"], "강원")
        self.assertEqual(t["start_date"], "2026-09-01")
        self.assertEqual(t["deadline"], "2026-09-10")
        r = rss._normalize("전남 고시공고", {"title": "<b>광양 전어축제</b> 안내",
                                             "link": "https://gwangyang.go.kr/1",
                                             "summary": "본문 " * 200})
        self.assertEqual(r["region"], "전남")
        self.assertEqual(r["license"], "확인 필요")
        self.assertLessEqual(len(r["summary"]), 200)


if __name__ == "__main__":
    unittest.main(verbosity=1)

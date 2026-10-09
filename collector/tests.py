# -*- coding: utf-8 -*-
"""수집기 단위 테스트 42항목 — 분류·지역·일수·중복·저장·공모사업

  cd collector && python tests.py
"""
import json
import os
import tempfile
import unittest
from datetime import date

import classify
import config
import store
import validate_grants as vg
import run as runmod
from collectors import grant, nara, rss, tour

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


class TestGrant(unittest.TestCase):
    def test_31_deadline_range_takes_last_date(self):
        # 기간이면 가장 늦은 날짜가 마감
        self.assertEqual(grant.parse_deadline("2026.10.08 ~ 2026.11.05", TODAY), ("2026-11-05", False))
        self.assertEqual(grant.parse_deadline("2026년 9월 1일부터 2026년 9월 30일까지", TODAY), ("2026-09-30", False))

    def test_32_deadline_expired_and_always(self):
        self.assertEqual(grant.parse_deadline("2026-07-31까지", TODAY), ("2026-07-31", True))
        self.assertEqual(grant.parse_deadline("상시신청", TODAY), ("", False))
        self.assertEqual(grant.parse_deadline("", TODAY), ("", False))

    def test_33_curated_drops_expired_keeps_open(self):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "g.json")
            rows = [
                {"id": "a", "title": "열린 공모", "org": "서울 문화재단", "deadline": "2026-09-01 15:00", "url": "https://x.kr/a", "evidence": "열린 공모 접수 2026.9.1 15시 마감"},
                {"id": "b", "title": "지난 공모", "org": "서울 문화재단", "deadline": "2026-08-01", "url": "https://x.kr/b", "evidence": "지난 공모 2026.8.1 마감"},
                {"id": "c", "title": "일정 미정 공모", "org": "", "deadline": "", "url": "https://x.kr/c", "evidence": "일정 미정 공모 별도공모"},
                {"id": "d", "title": "주소 없는 공모", "org": "", "deadline": "2026-09-01", "url": "", "evidence": "주소 없는 공모 2026.9.1"},
                {"id": "e", "title": "근거 없는 공모", "org": "", "deadline": "2026-09-01", "url": "https://x.kr/e"},
            ]
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"items": rows}, f, ensure_ascii=False)
            out = grant.load_curated(TODAY, p)
        self.assertEqual([r["uid"] for r in out], ["grant:a", "grant:c"])   # 지난 것 · 주소 없는 것 · 근거 없는 것은 빠진다
        self.assertEqual(out[0]["kind"], "grant")
        self.assertEqual(out[0]["region"], "서울")
        self.assertEqual(out[0]["license"], "확인 필요")

    def test_34_shipped_curated_file_is_valid(self):
        # 저장소에 들어 있는 검증 목록 자체의 형식 점검 — 날짜에 흔들리지 않게 오늘을 고정해서 본다
        with open(config.GRANTS_CURATED, encoding="utf-8") as f:
            rows = json.load(f)["items"]
        self.assertGreaterEqual(len(rows), 1)
        self.assertEqual(vg.check_unique(rows), [])
        for r in rows:
            self.assertEqual(vg.check_static(r, today=date(2026, 10, 10)), [], r.get("id"))

    def test_35_gov24_normalize_and_relevance(self):
        row = {"서비스ID": "WF0001", "서비스명": "지역 문화예술 행사 지원", "소관기관명": "경기도 문화재단",
               "신청기한": "2026.08.01 ~ 2026.09.15", "사용자구분": "개인||법인/시설/단체",
               "지원내용": "본문 " * 100, "등록일시": "20260801120000"}
        n = grant._normalize_gov24(row, TODAY)
        self.assertEqual(n["uid"], "gov24:WF0001")
        self.assertEqual(n["kind"], "grant")
        self.assertEqual(n["deadline"], "2026-09-15")
        self.assertEqual(n["region"], "경기")
        self.assertEqual(n["posted_at"], "2026-08-01")
        self.assertEqual(n["summary"], "")                     # 본문(지원내용)은 가져오지 않는다
        self.assertTrue(n["url"].startswith("https://www.gov.kr/"))
        self.assertTrue(grant._is_relevant(n))
        # 개인만 받는 혜택은 뺀다(사용자구분 기준)
        person = grant._normalize_gov24({"서비스ID": "WF0002", "서비스명": "청년 문화예술패스",
                                         "사용자구분": "개인"}, TODAY)
        self.assertFalse(grant._is_relevant(person))
        # 제외 단어 · 글자만 겹친 「공공연」(실응답에서 「공연」 검색에 섞여 나왔다)
        for bad_title in ("공연장 직원 채용 지원", "공공연 연구인력 파견지원사업", "기획공연 관람료 할인"):
            bad = grant._normalize_gov24({"서비스ID": "WF0003", "서비스명": bad_title,
                                          "사용자구분": "법인/시설/단체"}, TODAY)
            self.assertFalse(grant._is_relevant(bad), bad_title)

    def test_37_gov24_keeps_only_open_dated_items(self):
        # 실응답은 상시·연중 안내가 대부분이다 — 마감일이 적히고 안 지난 것만 싣는다
        rows = [
            {"서비스ID": "A", "서비스명": "문화행사 운영단체 지원", "소관기관명": "서울특별시", "사용자구분": "법인/시설/단체",
             "신청기한": "2026.08.01~2026.09.10"},
            {"서비스ID": "B", "서비스명": "문화행사 상시 지원", "소관기관명": "서울특별시", "사용자구분": "법인/시설/단체",
             "신청기한": "상시신청"},
            {"서비스ID": "C", "서비스명": "문화행사 지난 지원", "소관기관명": "서울특별시", "사용자구분": "법인/시설/단체",
             "신청기한": "2026.01.02~2026.01.09"},
            {"서비스ID": "D", "서비스명": "문화행사 개인 지원", "소관기관명": "서울특별시", "사용자구분": "개인",
             "신청기한": "2026.08.01~2026.09.10"},
        ]

        class FakeResp:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"data": rows, "matchCount": len(rows)}

        orig = (grant.requests.get, grant.time.sleep, config.DATA_GO_KR_KEY, config.GRANT_KEYWORDS)
        try:
            grant.requests.get = lambda *a, **k: FakeResp()
            grant.time.sleep = lambda s: None
            config.DATA_GO_KR_KEY = "test-key"
            config.GRANT_KEYWORDS = ["행사"]
            out = grant.fetch_gov24(log=lambda m: None, today=TODAY)
        finally:
            grant.requests.get, grant.time.sleep, config.DATA_GO_KR_KEY, config.GRANT_KEYWORDS = orig
        self.assertEqual([r["uid"] for r in out], ["gov24:A"])
        self.assertNotIn("_utype", out[0])
        self.assertNotIn("_expired", out[0])

    def test_36_grant_scoring_and_dedupe(self):
        soon = {"uid": "grant:a", "kind": "grant", "title": "공모 가", "region": "", "deadline": "2026-08-12 15:00"}
        none = {"uid": "grant:b", "kind": "grant", "title": "공모 나", "region": "", "deadline": ""}
        past = {"uid": "grant:c", "kind": "grant", "title": "공모 다", "region": "", "deadline": "2026-08-01"}
        out = classify.finalize([none, past, soon], TODAY)
        self.assertEqual([r["uid"] for r in out], ["grant:a", "grant:b", "grant:c"])
        self.assertEqual(out[0]["days_left"], 2)
        self.assertIsNone(out[1]["days_left"])
        # 같은 제목은 검증 목록(grant)이 공공서비스(gov24)를 이긴다
        a = {"uid": "gov24:1", "kind": "grant", "title": "같은 제목", "region": ""}
        b = {"uid": "grant:x", "kind": "grant", "title": "같은 제목", "region": ""}
        self.assertEqual(classify.dedupe([a, b])[0]["uid"], "grant:x")


class TestGrantValidator(unittest.TestCase):
    GOOD = {"id": "arko-x-1", "title": "2027 테스트 공모 사업 안내", "org": "한국문화예술위원회", "posted_at": "2026-10-08",
            "start_date": "2026-10-08", "end_date": "2026-11-05", "deadline": "2026-11-05 15:00", "summary": "",
            "url": "https://arko.or.kr/content/6220", "evidence": "공연예술 : 공연장기획제작지원 - 2026. 10. 8. (목)~11. 5. (월) 15시 마감",
            "checked_at": "2026-10-10"}

    def test_38_date_in_text_common_forms(self):
        for t in ("2026.11.5", "2026. 11. 05.", "2026-11-05", "11월 5일까지", "~11. 5. (월) 15시", "11/5"):
            self.assertTrue(vg.date_in_text("2026-11-05 15:00", t), t)
        for t in ("2026.11.15", "2026.1.5", "12월 5일", "11.25"):
            self.assertFalse(vg.date_in_text("2026-11-05", t), t)

    def test_39_static_checks(self):
        t = date(2026, 10, 10)
        self.assertEqual(vg.check_static(self.GOOD, t), [])
        def bad(**kw):
            d = dict(self.GOOD); d.update(kw); return vg.check_static(d, t)
        self.assertTrue(bad(url="http://arko.or.kr/x"))                    # https 아님
        self.assertTrue(bad(url="https://blog.naver.com/abc/123"))         # 블로그는 근거가 아니다
        self.assertTrue(bad(url="https://example.com/notice"))             # .kr 공식 주소 아님
        self.assertTrue(bad(evidence=""))                                  # 근거 없음
        self.assertTrue(bad(evidence="공연장기획제작지원 접수 중 마감 안내문 확인"))  # 근거에 마감일이 없음
        self.assertTrue(bad(checked_at=""))
        self.assertTrue(bad(deadline="2026/11/05"))                        # 날짜 형식
        self.assertTrue(bad(summary="가" * 201))                           # 본문 전재 금지
        self.assertTrue(bad(deadline="2026-09-01", evidence="2026.9.1 마감 안내문 전문 확인"))  # 14일 넘게 지남
        self.assertTrue(bad(deadline="", title="마감일이 없는 공모 사업 안내"))             # 미정·예정 표기 없음
        self.assertEqual(bad(deadline="", title="2027 별도 공모 예정 안내 사업"), [])
        self.assertTrue(vg.check_unique([self.GOOD, dict(self.GOOD)]))

    def test_40_prune_old_items(self):
        doc = {"items": [dict(self.GOOD, id="old", deadline="2026-09-01"), dict(self.GOOD, id="new"),
                         dict(self.GOOD, id="tbd", deadline="")]}
        new, gone = vg.prune(doc, date(2026, 10, 10))
        self.assertEqual(gone, ["old"])
        self.assertEqual([i["id"] for i in new["items"]], ["new", "tbd"])

    def test_41_online_check_compares_evidence_with_page(self):
        class FakeFetcher:
            def __init__(self, pages): self.pages = pages
            def text(self, url): return self.pages.get(url, ("http-404", ""))
        page = "공연예술 :  (공연예술창작주체)  공연장기획제작지원 -\n 2026. 10. 8. (목)~11. 5. (월) 15시 마감"
        ok = dict(self.GOOD, evidence="공연예술 : (공연예술창작주체) 공연장기획제작지원 - 2026. 10. 8. (목)~11. 5. (월) 15시 마감", id="ok")
        split = dict(self.GOOD, evidence="공연장기획제작지원 … 11. 5. (월) 15시 마감", id="split")      # … 로 이은 두 조각
        fake = dict(self.GOOD, evidence="공연장기획제작지원 - 2026. 10. 8. (목)~11. 6. (화) 15시 마감", id="fake")  # 지어낸 날짜
        gone = dict(self.GOOD, url="https://arko.or.kr/none", id="gone")
        robots = dict(self.GOOD, url="https://blocked.or.kr/x", id="robots")
        f = FakeFetcher({self.GOOD["url"]: ("ok", page), "https://blocked.or.kr/x": ("robots", "")})
        errs = dict(vg.check_online([ok, split, fake, gone, robots], fetcher=f))
        self.assertEqual(sorted(errs), ["fake", "gone", "robots"])      # ok · split 은 통과
        self.assertIn("실제 페이지에 없다", errs["fake"])
        self.assertIn("확인하지 못했다", errs["robots"])

    def test_42_refresh_keeps_other_kinds(self):
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, "e.json")
            old = {"generated_at": "x", "mock": False, "count": 3, "items": [
                {"uid": "nara:1", "kind": "bid", "title": "입찰", "region": ""},
                {"uid": "tour:1", "kind": "festival", "title": "축제", "region": ""},
                {"uid": "grant:old", "kind": "grant", "title": "옛 공모", "region": ""}]}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(old, f, ensure_ascii=False)
            orig = runmod.SOURCES["grant"]
            try:
                runmod.SOURCES["grant"] = lambda: [{"uid": "grant:new", "kind": "grant", "title": "새 공모", "region": "", "deadline": "2026-09-01"}]
                self.assertEqual(runmod.refresh("grant", path=path), 0)
            finally:
                runmod.SOURCES["grant"] = orig
            with open(path, encoding="utf-8") as f:
                new = json.load(f)
        self.assertEqual(sorted(r["uid"] for r in new["items"]), ["grant:new", "nara:1", "tour:1"])
        self.assertEqual(new["count"], 3)


if __name__ == "__main__":
    unittest.main(verbosity=1)

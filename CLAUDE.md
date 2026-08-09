# CLAUDE.md

이 파일은 Claude Code가 이 저장소에서 작업할 때 읽는 안내서입니다.

## 프로젝트

전국 지자체가 공개한 **행사 관련 입찰공고·축제 일정·고시**를 하루 한 번 모아
보여주는 정적 사이트. 운영 주체는 (주)브리지미디어 큰길이벤트기획.

```
나라장터 API ─┐
TourAPI     ─┼→ 분류·지역판정·중복제거 → SQLite → events.json → 정적 사이트
지자체 RSS   ─┘
```

백엔드 서버 없음. GitHub Actions가 매일 05시(KST) 수집하고 Pages로 배포한다.

## 구조

```
collector/              배치 수집기 (Python, 외부 의존성 requests·feedparser뿐)
  config.py             API 키·지역코드·키워드 사전   ← 대부분의 튜닝은 여기
  collectors/nara.py    나라장터 용역 입찰공고
  collectors/tour.py    TourAPI 축제·행사 (contentTypeId=15)
  collectors/rss.py     지자체 RSS (robots.txt 확인 포함)
  classify.py           행사 판정·시도 추출·중복 제거·정렬
  store.py              SQLite 저장·JSON 내보내기
  run.py                실행 진입점 (--dry-run, --only 지원)
  mockgen.py            예시 데이터 생성 (API 키 없이 확인용)
  tests.py              단위 테스트 30항목

site/                   배포 대상. 이 폴더가 곧 사이트다
  index.html            알림판 — 검색·필터·정렬·페이지 이동
  calendar.html         축제 달력 — 월별
  about.html            이용안내·출처·저작권
  assets/style.css      공통 스타일
  assets/app.js         공통 스크립트 (외부 라이브러리 없음)
  data/events.json      배치 산출물 (gitignore 됨)

serve.py                로컬 미리보기 서버
build_single.py         미리보기.html 한 파일로 합치기
verify.py               브라우저 자동 검증 24항목 (playwright)
.github/workflows/deploy.yml   매일 수집 + Pages 배포
```

## 검증

**코드를 고쳤으면 반드시 아래 셋을 통과시킬 것.**

```bash
cd collector && python tests.py     # 30항목: 분류·지역·일수·중복·저장
cd .. && python serve.py 8899 &     # 서버를 띄운 뒤
python verify.py                    # 24항목: 브라우저 실동작
```

`verify.py`는 `http://localhost:8899` 를 본다. 포트를 바꾸면 파일 안 `BASE` 도 바꿀 것.
playwright가 없으면 `pip install playwright && python -m playwright install chromium`.

## 지켜야 할 규칙

이건 취향이 아니라 **법적·운영상 제약**이다. 임의로 완화하지 말 것.

- **본문 전재 금지.** 제목·기관·기간·링크까지만. RSS 요약은 200자에서 자른다.
- **공공누리 유형 확인.** 제1유형만 상업적 이용이 자유롭다. RSS 수집분은
  `license` 를 `확인 필요` 로 둔다. 임의로 다른 값을 채우지 말 것.
- **robots.txt 준수.** `collectors/rss.py` 의 확인 로직을 우회하지 말 것.
- **요청 간격.** `config.REQUEST_DELAY` 를 1초 미만으로 낮추지 말 것.
- **출처 표기.** 각 페이지 하단 고지와 `about.html` 을 지우지 말 것.
- **게시판 HTML 직접 파싱 금지.** 공식 RSS와 공개 API만 쓴다.

## 알아둘 것

- **한글 줄바꿈.** `body { word-break: keep-all }` 이 걸려 있다. 빼면 "찾아보세/요"
  처럼 낱자가 떨어진다.
- **지역 판정.** `classify.detect_region()` 은 *가장 앞에 나온* 시·도명을 채택한다.
  기관명이 관례상 시·도로 시작하기 때문. 이래야 광주광역시와 경기도 광주시가
  갈린다. 길이나 가중치 기반으로 되돌리면 회귀한다 (tests.py가 잡는다).
- **나라장터 조회기간 제한.** 약 15일이라 `config.CHUNK_DAYS=14` 로 쪼개 호출한다.
- **TourAPI 버전.** 엔드포인트가 `KorService1 → KorService2` 처럼 올라간다.
  호출이 갑자기 실패하면 `config.TOUR_BASE` 부터 확인.
- **file:// 에서는 fetch가 막힌다.** 그래서 `build_single.py` 가 데이터를 문서에
  심은 `미리보기.html` 을 만든다. `app.js` 의 `window.__EVENTS__` 분기가 그것.
- **sticky 필터 바.** 지역 칩 17개가 줄바꿈하면 모바일 화면을 덮는다.
  `.frow.scrollx` 로 한 줄 가로 스크롤을 유지할 것.
- **id 중복.** `#genAt`, `#total`, `#mockflag` 는 문서당 하나만 있어야 한다.
  `build_single.py` 가 달력 쪽 것을 제거한다.

## 남은 작업

1. **GitHub에 올리고 Pages 띄우기** — README 상단 5단계 참조.
   저장소 생성 → `git remote add` → `git push` → Pages Source를 GitHub Actions로
   → 시크릿 `DATA_GO_KR_KEY` 등록.
2. ~~문의처 교체~~ — 완료. `about.html`·`config.UA` 에 gilcaro@naver.com / 1533-7295 반영.
3. **RSS 피드 확충** — 2026-08 조사 결과 정책브리핑은 RSS 를 중단했고 광양시 등
   다수 지자체도 RSS 를 제공하지 않는다. 피드는 각 지자체 RSS 안내 페이지에서
   확인된 주소만 넣고 `python -m collectors.rss --check` 로 검증할 것.
   RSS 가 없는 곳은 공공데이터포털의 지자체 고시공고 오픈API 활용을 검토.
5. **키워드 튜닝** — 실데이터 수집 후 `run.py` 출력 상위 항목을 보며
   `EVENT_KEYWORDS` / `EXCLUDE_KEYWORDS` 조정. 서비스 품질의 대부분이 여기서 갈린다.

## 아직 안 한 것

- 실제 API 키로 수집해 본 적 없음. 지금까지 검증은 전부 예시 데이터 기준.
  첫 실 수집 후 응답 필드명이 문서와 다를 수 있으니 `_normalize()` 를 확인할 것.
- 신규 공고 알림(카카오 알림톡·이메일) 미구현.
- 검색엔진 최적화(sitemap.xml, 개별 공고 페이지) 미구현.

## 말투

한국어로 응답. 사용자는 개발 전문가가 아니므로 명령어는 복사해서 바로 쓸 수 있게
제시하고, 무엇을 왜 하는지 한 줄로 덧붙일 것.

# 파일 지도 — brizymedia/hd-event

경로는 레포 루트 기준. 줄 수는 2026-10-28 클론 기준.
「원본」= 손으로 고치는 파일, 「생성물」= 스크립트가 쓰는 파일(손 수정 금지).

## 루트

| 파일 | 줄 | 구분 | 역할 |
|---|---|---|---|
| `index.html` | 425 | 원본 | 대문 한 장. JSON-LD(Organization+LocalBusiness, WebSite), 14구획, 문의 폼 |
| `portfolio.html` | 137 | 원본 | 포트폴리오 전체 + 필터 7개 + 라이트박스. **stories/ · areas/ 의 틀** |
| `quote.html` | 1994 | 생성물(port_docs) | 자동 견적서. 손님 화면 / `?admin=1` 관리자(발행 · 저장함) |
| `quote-catalog.js` | 113 | 생성물(port_docs `CATALOG`) | 견적 품목표 `CATALOG`(7묶음 34품목, 전부 `price:null`) + 견적 코드 풀이 `견적풀기()` — quote.html · schedule.html 공용 |
| `contract.html` | 1227 | 생성물 | 전자계약서(용역 / 출연 두 종류), 서명 패드, PDF |
| `statement.html` | 504 | 생성물 | 거래명세서(인쇄 · PDF) |
| `schedule.html` | 853 | 생성물 | 월간 행사 일정 + 행사별 체크리스트(직원 공유) |
| `upload.html` | 1261 | 생성물 | 현장 사진 올리기 + 블로그 · 인스타 문구 자동 작성 |
| `office.html` | 160 | 생성물(port_docs `office()` + admin_gate) | 대표 전용 업무 문서함, 서버 연결 상태 표시, 관리자 잠금 |
| `admin-lock.js` | 85 | 생성물 | `?admin=1` 화면 잠금(계약 서버 `boxList` 로 암호 확인) |
| `llms.txt` | 30 | 머리=원본, 「## 블로그」 절=생성물 | AI 검색 안내문 |
| `rss.xml` | 14 | 생성물(build-blog) | 블로그 RSS 2.0, 최근 50편 |
| `sitemap.xml` | 42 | 생성물(make_pages 전체 → build-blog 가 /blog/ 줄만 덧붙임) | |
| `robots.txt` | — | 원본 | 전체 허용, `/contract.html /statement.html /upload.html /schedule.html /office.html` Disallow, Sitemap 줄 |
| `CNAME` | 1 | 원본 | `www.hdplan.co.kr` |
| `<32자 hex>.txt` | 1 | 원본 | IndexNow 키 파일(값 = 파일 이름) |
| `.gitignore` | — | | `_raw/ .DS_Store Thumbs.db` |
| `README.md` | — | | 납품 메모 · 확인할 것 · 업무 도구 표 · 블로그 요약(일부 낡음, SKILL.md 15장) |

## assets/

| 경로 | 역할 |
|---|---|
| `assets/style.css` (545줄) | 공통 스타일. 1~460행 대문 · 공통, 463행~ 「행사 이야기 · 지역 페이지 · 바닥글 링크(2026-10-03)」 추가분 |
| `assets/app.js` (239줄) | 공통 스크립트. 맨 위 `FORM_ENDPOINT` · `SMS_TO` · `COMPANY` · `NOTICES` · `WORKS` · `UP_LIST` · `UP_IMG` · `UP_CAT`, 맨 아래 관리자 모드 입구 |
| `assets/img/favicon.svg` | 네모 마크(업무 화면 머리 로고로도 씀) |
| `assets/img/logo-h-white.png` | 가로 로고(어두운 바탕용) — 메일 머리 · JSON-LD logo |
| `assets/img/hero_poster.webp` | 히어로 1장 · og:image · 영상 포스터 · 블로그 사진 |
| `assets/img/slider1~5.webp` | 슬라이드 · 카드 배경(slider1 · slider4 는 얼굴 → 블로그 제외) |
| `assets/img/sys/h1_1~8, h2_1~5, h3_1~3.webp` | 시스템 · 무대 사진 16장(워터마크 없음, h1_1 은 자료 화면) |
| `assets/img/works/w1~w19.webp` | 포트폴리오 19장 — **프로이벤트 워터마크** |
| `assets/img/biz/b1~b8.webp` | 사업분야 원본 8장 — **워터마크**(대문에서는 안 씀, 이야기 페이지 일부가 씀) |
| `assets/img/stamp-hd.png` | **없음.** 생기면 계약서 · 명세서에 직인이 찍힌다 |
| `assets/video/hero_md.mp4` (약 6MB) · `hero_sm.mp4` (약 2.9MB) | 현장 스케치 영상(프로이벤트 몽타주) |

## 생성 폴더

| 경로 | 만드는 것 | 내용 |
|---|---|---|
| `stories/index.html` + 5편 (`assembly-playzone`, `corporate-festival`, `fire-academy-sports`, `childrens-day`, `groundbreaking-ceremony`) | `tools/make_pages.py` | 행사 이야기 |
| `areas/index.html` + 9곳 (`geumcheon guro gwangmyeong gwanak yeongdeungpo mapo gangnam songpa namyangju`) | `tools/make_pages.py` | 지역 페이지 |
| `blog/index.html`, `blog/<지역 slug>/index.html`(9), `blog/<한글 slug>/index.html`(10), 24편 넘으면 `blog/page/N/` | `scripts/build-blog.mjs` | 블로그 |

## _blog/ (블로그 원본 — 공개 안 됨)

| 파일 | 역할 |
|---|---|
| `_blog/GUIDE.md` | 글쓰기 규칙 6장(순서 · 금지 · JSON 형식 · 회사 사실 · 사진 · 좋은 글 기준) |
| `_blog/posts/*.json` | 글 원본 10편(2026-10-13) |
| `_blog/regions.json` | 지역 9곳: slug · 이름 · 시군 · 도 · 비중 · 서비스페이지 · 이동 · 동네 · 많은행사 · 주의 · 현장기록 |
| `_blog/keywords.json` | 주제 14개 틀(`{지역}` 자리) + 지역전용 1개 + 검색량 · 보정(비어 있음) |
| `_blog/photos.json` | 쓸 수 있는 사진 묶음(보이는것 · 쓰임 · 제외) |
| `_blog/sources.json` | 사람이 확인한 공식 출처 7개(확인일 2026-09-11)와 각 `사실` 범위 |
| `_blog/indexnow-key.txt` | IndexNow 키(루트 txt 와 같은 값) |

## scripts/ · tools/

| 파일 | 실행 | 하는 일 |
|---|---|---|
| `scripts/build-blog.mjs` (427) | `node scripts/build-blog.mjs` | blog/ 재생성, rss.xml, sitemap · llms.txt 블로그 부분. 다른 두 스크립트가 함수를 import |
| `scripts/blog-check.mjs` (257) | `node scripts/blog-check.mjs [--new 파일…]` | 글 검사, 실패 시 exit 1 |
| `scripts/blog-plan.mjs` (87) | `node scripts/blog-plan.mjs [--json] [--n 5]` | 다음 글 지역 · 주제 고르기 |
| `tools/make_pages.py` (215) | `python tools/make_pages.py` | stories/ · areas/ · sitemap.xml 전체 |
| `tools/port_docs.py` (514) | `python tools/port_docs.py [큰길이벤트 레포 경로]` (기본 `~/Documents/클로드코드`) | 업무 화면 7개 + 서버 코드 2개 + office.html 을 큰길이벤트 원본에서 치환 이식, 끝에 `admin_gate.apply()` |
| `tools/admin_gate.py` (90) | port_docs 가 부름 | office.html 에 관리자 잠금 씌우기. 「고객사 레포마다 같은 내용, 원본은 바로기획 tools/admin_gate.py」 |

## apps-script/

| 파일 | 역할 |
|---|---|
| `apps-script/contract/Code.gs` (457) | 계약 · 견적 보관함 · 행사 일정 서버 (`VERSION '2026-10-02b'`) |
| `apps-script/contract/README.md` | 설치 · 배포 · BOX_PW · 사용 흐름 · 문제 해결 · 데이터 위치 |
| `apps-script/gallery/Code.gs` (421) | 사진 업로드 → GitHub `photos` 가지 |
| `apps-script/gallery/README.md` | 토큰 만들기 · 스크립트 속성 3개 · 배포 · 문제 해결 |

## 레포 밖에 있는 것

- `https://www.ai-make.co.kr/stats/stats.js` — 유입 통계(모든 공개 페이지). 큰길브리지 서버.
- 공용 문의 서버(Apps Script) — 코드 없음, 주소만(`references/backend.md`).
- 큰길이벤트 원본 레포 — `port_docs.py` 의 입력. 경로 기본값 `~/Documents/클로드코드`.
- GitHub `photos` 가지 — 이 클론에는 `main` 만 받아져 있었다.

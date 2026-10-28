# 파일 지도 — brizymedia/pro-event

기준: main 브랜치 커밋 `af0912d` (2026-10-28, 커밋은 이것 하나뿐). 줄 수는 그 시점 `wc -l`.
경로는 모두 레포 루트 기준. **결과물(생성 파일)은 손으로 고치지 말 것** 표시가 붙은 것은 생성기를 고친다.

## 루트

| 파일 | 줄 | 하는 일 | 손수정 |
|---|---|---|---|
| `index.html` | 394 | 대문 한 장. 커튼·히어로·고객 띠·소개·사업분야·포트폴리오·프로세스·시스템·영상·섭외·견적문의·푸터·라이트박스. 생성 페이지(stories·areas·blog)의 머리글·바닥글 **원본** | O (고친 뒤 생성기 재실행) |
| `assets/style.css` | 551 | 전체 스타일. 460행부터는 생성 페이지용(`.phead` `.story` `.scard` `.area3` `.callband` 등) | O |
| `assets/app.js` | 282 | 대문 + 생성 페이지 공통 스크립트(외부 라이브러리 없음). 요소가 있을 때만 동작 | O |
| `admin-lock.js` | 85 | `?admin=1` 화면 잠금(견적·계약·명세서) | port_docs 로 옮겨 옴 |
| `quote-catalog.js` | 110 | 견적 품목표 `CATALOG` + 견적 코드(#q=) 푸는 규칙. quote·schedule 가 같이 씀 | port_docs 가 `CATALOG` 부분을 덮어씀 → `tools/port_docs.py` 의 `CATALOG` 를 고친다 |
| `quote.html` | 1994 | 자동 견적서(손님) / `?admin=1` 견적서 발행·저장함 | port_docs 결과물 |
| `contract.html` | 1227 | 전자계약서 (`?admin=1` 작성, `?c=…&s=…` 손님 서명) | port_docs 결과물 |
| `statement.html` | 504 | 거래명세서 (`?admin=1`) | port_docs 결과물 |
| `schedule.html` | 853 | 행사 일정 · 체크리스트 (보관함/직원 암호) | port_docs 결과물 |
| `upload.html` | 1268 | 현장 사진 올리기 + 블로그·인스타 글 만들기 | port_docs 결과물 |
| `office.html` | 160 | 대표 전용 업무 문서함(관리자 모드) | **port_docs 가 통째로 생성** |
| `llms.txt` | 77 | AI 검색 안내문. 「## 블로그」 절은 build-blog 가 다시 씀(함정 참고) | 위쪽만 손수정 |
| `sitemap.xml` | 41 | 대문·견적·stories·areas(make_pages) + blog(build-blog) | 생성 |
| `rss.xml` | 14 | 블로그 RSS | 생성 |
| `robots.txt` | 11 | 업무 화면 Disallow + Sitemap | O |
| `README.md` | — | 제작 기록(히어로 영상 컷 표, 업무 도구 표, 블로그) — 일부 낡음(SKILL.md 함정 참고) | O |
| `.gitignore` | 1 | `_raw/` 만 | — |

`.github/workflows/` 는 **없다**. 배포는 GitHub Pages(브랜치 배포로 보임 — 설정값은 확인 필요).

## assets/img

| 경로 | 내용 |
|---|---|
| `logo.png` (220×50) | 가로 로고(흰 글씨, 어두운 바탕용) |
| `favicon.svg` | 파비콘 겸 업무 화면 네모 마크(`port_docs.LOGO_FILE`) |
| `hero_poster.webp` (1600×900) | 히어로 포스터·og:image. photos.json 설명: 야외 축제 드론 촬영 |
| `works/w1~w19.webp` (긴 변 1400~1600) | 포트폴리오. 번호↔글 매핑 정본은 `app.js` 의 `WORKS` |
| `biz/b1~b8.webp` (1600×900) | 사업분야 무대 사진. 출처는 README 「납품 전에 바꿀 것 4」 |
| `sys/h1_*, h2_*, h3_*.webp` (1200×900) | 음향(h1)·조명(h2)·무대(h3). 대문은 h1_7 · h2_4 · h3_1 사용 |
| `stories/cy1~6, ot1~6.webp` (900×675) | 네이버 블로그 pro_event 원문 사진(cy=창용초 운동회 2026-09, ot=동남보건대 OT 2026-03) |
| `slider1~5.webp`, `con*_*.png/webp`, `og_old.jpg`, `ft_logo.png` | 원본 사이트에서 가져온 것. 대문 HTML 에서는 안 씀. slider1·3·4 등은 블로그 사진 목록(`_blog/photos.json`)에 있음 |
| `stamp-pro.png` | **없음.** 생기면 계약서·명세서에 직인이 찍힘(지금은 404 → 「(인)」) |

## assets/video

| 파일 | 규격(ffprobe 확인) | 용도 |
|---|---|---|
| `hero.mp4` | 1920×1080, 25fps, 26.92초, H.264 High yuv420p, 약 3.3Mbps, 11.0MB, 오디오 없음, moov 앞쪽(faststart) | 넓은 화면 |
| `hero_md.mp4` | 1280×720, 같은 길이, 약 1.8Mbps, 6.0MB | 중간 |
| `hero_sm.mp4` | 854×480, 같은 길이, 약 0.85Mbps, 2.9MB | 폰 |

마스터 `_raw/master_1080.mp4` 와 원본 영상·AI 컷은 `_raw/`(gitignore) — **레포에 없다.**

## 생성 페이지

| 폴더 | 만드는 것 | 명령 |
|---|---|---|
| `stories/` | 행사 이야기 5편 + `index.html` | `python tools/make_pages.py` |
| `areas/` | 지역 9곳(gangnam, seocho, yeongdeungpo, gangseo, yangcheon, seongbuk, suwon, hwaseong, chuncheon) + `index.html` | 같은 명령 |
| `blog/` | 글 10개(`blog/<한글slug>/index.html`), 지역 모음 `blog/<region>/`, 목록 `blog/index.html`(24개 넘으면 `blog/page/N/`) | `node scripts/build-blog.mjs` (매번 `blog/` 를 지우고 새로 만듦) |

## 원본 데이터 `_blog/` (밑줄 폴더라 Pages(Jekyll)가 공개하지 않음)

| 파일 | 내용 |
|---|---|
| `GUIDE.md` | 블로그 작업 규칙서(쓸 수 있는 회사 사실, 금지 표현, JSON 형식) — **글 쓰기 전에 반드시 읽기** |
| `regions.json` | 지역 9: slug·이름·시군·도·비중·서비스페이지·이동·동네·많은행사·주의·현장기록 |
| `keywords.json` | 주제 틀(`{지역}` 치환)·지역전용·검색량(미조사)·성수기 |
| `photos.json` | 블로그에 쓸 수 있는 사진 묶음 45개. `제외` 가 있으면 금지(얼굴 등) |
| `sources.json` | 공식 출처 7개(기상청 특보 기준 등)와 그 `사실` 범위 |
| `posts/<date>-<slug>.json` | 글 원본 10개(전부 2026-10-28) |

## 도구

| 파일 | 줄 | 하는 일 |
|---|---|---|
| `tools/make_pages.py` | 224 | `STORIES` · `AREAS` 표 → stories/ · areas/ + sitemap.xml(블로그 줄 보존) |
| `tools/port_docs.py` | 530 | 큰길이벤트 원본 레포의 업무 화면을 이 회사용으로 치환 복사 + `office.html` 생성. 인자: 원본 레포 경로(기본 `~/Documents/클로드코드`) |
| `tools/admin_gate.py` | 90 | `office.html` 에 잠금 화면 주입(port_docs 가 호출). 바로기획 것이 원본 |
| `scripts/build-blog.mjs` | 373 | `_blog/posts` → blog/ · rss.xml · sitemap(blog 부분) · llms.txt(블로그 절) |
| `scripts/blog-check.mjs` | 260 | 글 검사(금지 표현·사진·근거·출처·중복 30%). 실패 시 exit 1 |
| `scripts/blog-plan.mjs` | 87 | 다음에 쓸 지역·주제 추천(`--json`, `--n 5`) |

## apps-script/

| 파일 | 내용 |
|---|---|
| `apps-script/contract/Code.gs` (457) + `README.md` | 계약 서버: 계약 저장·서명·PDF·메일·대장 + 견적 보관함 + 행사 일정 |
| `apps-script/gallery/Code.gs` (421) + `README.md` | 사진 서버: photos 브랜치에 사진·photos.json 커밋 |

자세한 것은 `backend.md`.

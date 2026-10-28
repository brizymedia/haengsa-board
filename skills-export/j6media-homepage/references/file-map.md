# 파일 지도 — brizymedia/j6media

기준: `main` 커밋 `8708190` (2026-10-12, 커밋 1개 — 「관리자 화면 잠금 · 서명 뒤 단추 · 사진 목록 갱신 다시하기 (큰길이벤트 b6e70d5 옮김)」).
레포 전체 188 파일, 글 파일 약 12,500줄. 줄 수는 `wc -l` 값.

「만드는 쪽」: **손** = 직접 고침 / **생성** = `tools/make_pages.py` / **이식** = `tools/port_docs.py`(큰길이벤트 원본에서) / **서버** = Apps Script 가 씀.

## 뿌리

| 파일 | 줄 | 만드는 쪽 | 하는 일 |
|---|---|---|---|
| `index.html` | 217 | 손 | 대문. 머리 · 모바일 시트 · 히어로 영상 · 섹션 9개 · 바닥글 · 폰 하단 단추 · 맨 위로 · 라이트박스 틀 |
| `about.html` | 169 | 손 | 회사소개 — 인사말 · 숫자 4칸 · 연혁 · 회사 정보 표 · 오시는 길(그림 지도 카드 + 네이버 지도 링크) |
| `service.html` | 158 | 손 | 하는 일 6분야(앵커 `#church #corp #gov #school #show #install`) + 설치 사례 15곳 + 사진 3장 |
| `equipment.html` | 132 | 손 | 음향 시스템 8칸 · 조명 시스템 5칸(+상담 칸, night 섹션) · 취급 브랜드 로고 14 |
| `portfolio.html` | 129 | 손 | 현장 사진(필터 8 + `#pfGrid`, JS 가 채움) + 블로그 글 목록 `#blogList` (data-limit 10) |
| `notice.html` | 118 | 손 | 탭 3(`#btabs`): 공지 `#noticeBoard` · 게시판(블로그 목록, limit 15) · 자료실 `#fileBoard`. **생성기 셸 원본** |
| `contact.html` | 144 | 손 | 연락 방법 4 · 문의 전 체크리스트(`#ready`) · 문의 폼 `#quoteForm` · FAQ 6(`#faq`, JSON-LD FAQPage) |
| `quote.html` | 1994 | 이식 | 자동 견적서. 손님 화면 / `?admin=1` 대표 화면(견적서 저장함 · 계약 · 명세서 · 일정으로 넘기기) |
| `quote-catalog.js` | 106 | 이식(CATALOG 는 port_docs 안 표) | 견적 품목표 `CATALOG` + 견적 코드 풀기 `견적풀기()` · `견적줄설명()` — quote · schedule 공용 |
| `contract.html` | 1227 | 이식 | 전자계약서. `?admin=1` 작성 → 서명 링크 → 고객 서명 패드 → 서버 PDF |
| `statement.html` | 504 | 이식 | 거래명세서. `#t=` 로 견적 내용을 받아 인쇄 · PDF |
| `schedule.html` | 853 | 이식 | 행사 일정(월간표) · 행사별 체크리스트. 계약 서버의 일정 파일을 대표 · 직원이 같이 봄 |
| `upload.html` | 1264 | 이식 | 사진 올리기 → photos 가지, 대표 썸네일 2장, 블로그 · 인스타 글 초안 만들기, 올린 사진 수정 · 삭제 |
| `office.html` | 160 | 이식(`office()` + `admin_gate.apply`) | 대표 전용 업무 문서함 — 도구 카드 · 업무 흐름 7단계 · 서버 연결 상태 · 암호 안내. 대표 암호 잠금 |
| `admin-lock.js` | 85 | 이식 | `?admin=1` 화면 잠금(견적 · 계약 · 명세서). `data-server` `data-key` `data-name` 속성으로 설정 |
| `llms.txt` | 32 | 손 | AI 검색용 회사 요약(주소 · 장비 · 브랜드 · 하는 일 · 주요 페이지 링크) |
| `sitemap.xml` | 27 | 생성 | 대문 + 서브 6 + quote + 이야기 6 + 지역 10 = 24 URL. `make_pages.py` 가 통째로 다시 씀 |
| `robots.txt` | 11 | 손 | 업무 화면 5개 Disallow, Sitemap 주소(github.io) |
| `CNAME` | — | 손 | `www.j6media.co.kr` |
| `.nojekyll` | 0 | 손 | Jekyll 끄기 |
| `README.md` | 25 | 손 | 업무 도구 표 · 이식기 · 서버 · 직인 안내 |

## assets/

| 파일 | 줄 | 하는 일 |
|---|---|---|
| `assets/style.css` | 591 | 공통 스타일 전부. 업무 화면은 안 씀. 캐시 꼬리표 `?v=6` |
| `assets/app.js` | 388 | 공통 스크립트 + 데이터 칸. 꼬리표 `?v=20261004`. 끝에 「관리자 모드」 링크 IIFE |
| `assets/edit.js` | 295 | 사장님 수정 모드. 꼬리표 `?v=1`. 손으로 쓴 7쪽에만 포함 |
| `assets/img/SOURCES.md` | 55 | 사진 · 영상 · 로고 · og · 브랜드 로고 출처 기록 |
| `assets/img/logo-h.svg` / `logo-h-white.svg` / `logo-h-white.png` | — | 가로 로고(183×48). 마크는 PNG 를 SVG 안에 data URI 로 심음. 흰 것은 어두운 바탕(대문 히어로 · 바닥글 · 메일 머리) |
| `assets/img/logo-mark.svg` · `logo.png`(512) · `favicon.svg` · `apple-touch-icon.png`(180) | — | 마크. 업무 화면 머리는 `logo-mark.svg` |
| `assets/img/og.jpg` | — | 1200×630 공유 이미지(w41 + 로고) |
| `assets/img/works/w1~w57.webp` | 57장 | 1600px 현장 사진 |
| `assets/img/works/t1~t57.webp` | 57장 | 800px 썸네일 |
| `assets/img/brands/*.png` | 13장 | 브랜드 로고(KANALS 는 파일 없음 — 글자로 표시) |
| `assets/video/hero.mp4` | — | H.264 1920×1080 30fps 21.8초 약 7.0MB |
| `assets/video/hero_sm.mp4` | — | H.264 960×540 약 2.4MB (폭 900 미만) |
| `assets/video/hero_sm.webm` | — | VP9 960×540 약 2.9MB (mp4 못 트는 브라우저) |
| `assets/video/hero_poster.webp` | — | 1920×1080 포스터 · preload |
| `assets/img/stamp-j6.png` | **없음** | 생기면 계약서 · 명세서에 직인으로 찍힘 |

## stories/ · areas/ (전부 생성, 각 108~109줄)

| 파일 | 내용 |
|---|---|
| `stories/index.html` | 행사 이야기 목록(카드 큰 2열) |
| `stories/wonju-oakvalley-retreat.html` | 원주 오크밸리리조트 그랜드볼룸 교회 전가족수련회 (2026.08) |
| `stories/bucheon-fantastic-portal.html` | 부천국제판타스틱영화제 30주년 「판타스틱 포털」 제막식 (2026.06.09) |
| `stories/hanabok-seminar.html` | 하나복 본강좌 (2026.06, 곤지암 소망수양관) |
| `stories/dream-interpretation-exhibition.html` | 강신욱 작가 「꿈의 해석」 Genelec 27대 (2023.09, 삼성역 C스퀘어) |
| `stories/imundong-church-remodeling.html` | 이문동교회 본당 + 주일학교 6곳 리모델링 (2024~2025) |
| `areas/index.html` | 운영 지역 목록(이동 시간 줄) |
| `areas/{namyangju,guri,seoul,yangju,pocheon,gapyeong,gwangju,goyang,bucheon}.html` | 지역 9곳 |

## apps-script/

| 파일 | 줄 | 하는 일 |
|---|---|---|
| `apps-script/contract/Code.gs` | 457 | 계약 서버 — 계약 저장 · 서명 · PDF · 메일 · 대장, 견적서 보관함, 행사 일정 (이식) |
| `apps-script/contract/README.md` | 111 | 설치 · 배포 · 연결 · 보관함 암호 · 문제 해결 |
| `apps-script/gallery/Code.gs` | 421 | 사진 업로드 서버 — GitHub Contents API 로 photos 가지에 저장, photos.json 관리 (이식) |
| `apps-script/gallery/README.md` | 123 | 토큰 만들기 · 속성 · 권한 · 배포 · 문제 해결 |

## tools/

| 파일 | 줄 | 하는 일 |
|---|---|---|
| `tools/make_pages.py` | 236 | 이야기 · 지역 페이지 + sitemap. 데이터 표 `STORIES` `AREAS` `SERVICES` |
| `tools/port_docs.py` | 522 | 업무 화면 이식기. 「회사 설정」 칸 + 공통 치환 규칙 + 화면별 `*_extra()` + `office()` |
| `tools/admin_gate.py` | 90 | office.html 에 `<!--GATE-->` 잠금 화면 · CSS · JS 를 넣음(여러 번 돌려도 한 번만) |
| `tools/apply_edits.py` | 118 | 사장님 수정 JSON 반영(대상 `PAGES` 7쪽, 사진은 `assets/img/` 만) |

## 없는 것 (찾지 말 것)

`.github/workflows/`, `blog/`, `_blog/`, `scripts/`, `gallery.html`, `stats.js`(외부 주소로만 부름), 자동 검증 스크립트, 패키지 파일(package.json 등).

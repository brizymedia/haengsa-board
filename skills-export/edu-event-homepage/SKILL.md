---
name: edu-event-homepage
description: 「이벤트와 교육연구소」(인천 남동구, 소장 황윤수 — 운동회·교회·기업·축제 행사 + 감정교육·리더십·과학실험 마술수업 등 교육) 홈페이지 brizymedia/edu-event 를 처음부터 다시 만들거나 이어서 고칠 때 쓴다. 「이벤트와 교육연구소」「교육연구소」「이벤트와교육연구소」「edu-event」「황윤수」「황윤수 소장」 홈페이지 · build_site.py · 행사|교육 2분할 히어로 · 포트폴리오 사진(PHOTO_SETS · WORKS) · 운동회 실적 학교 94곳 · 공지 관리자(notice-admin) · 사장님 수정 모드(?edit=) · apply_edits · 견적서 · 전자계약서 · 거래명세서 · 행사 일정 · 사진 올리기 · 블로그(_blog) 작업이면 먼저 읽는다.
---

# 이벤트와 교육연구소 홈페이지 (brizymedia/edu-event)

큰길브리지(주식회사 브리지미디어)가 납품한 고객 홈페이지. 정적 HTML/CSS/JS(외부 라이브러리 없음, 글꼴만 CDN)
+ Google Apps Script 서버 2개(계약 · 갤러리+공지) + 공용 문의 서버(레포 밖).
**공개 페이지 HTML 은 손으로 쓰지 않고 `tools/build_site.py` 한 파일이 만든다** — 이것이 다른 고객 사이트(HD기획 · 힐링엔터 등)와 가장 다른 점이다.

이 문서는 2026-10-28, 커밋 `c0c4773`(2026-10-27 「대표님이 보낸 현장 사진 87장 · 영상 6개 반영」) 기준으로 코드를 직접 읽고 썼다.
코드에서 확인 못 한 것은 「확인 필요」로 적었다. 코드 복사본은 넣지 않았다 — 사이트 전체는 레포를 받아서 쓴다.

```bash
git clone https://github.com/brizymedia/edu-event.git      # 기본 가지는 master (README 의 「main」과 다름)
cd edu-event && python -m http.server 8820                  # → http://localhost:8820  (file:// 로 열면 글꼴·스크립트가 안 됨)
```

세부 자료(필요할 때만 읽기):

| 파일 | 내용 |
|---|---|
| `references/content.md` | **build_site.py 자료 구조** — 회사 정보 상수 · EVENT_CATS · EDU · PHOTO_SETS · WORKS · REVIEWS · TIMELINE · FAQ · 함수 지도, 사진 · 영상 넣는 법 |
| `references/file-map.md` | 파일 하나하나의 역할 · 원본/생성물 구분 · 자산 목록 |
| `references/design-tokens.md` | 색 hex · 글꼴 · 반응형 기준 · 컴포넌트 클래스 · 업무 화면 색 |
| `references/sections.md` | 페이지별 섹션 순서와 문구 출처 |
| `references/workflows.md` | 업무 화면(견적 · 계약 · 명세서 · 일정 · 사진 올리기 · 문서함) 흐름, 공지 관리자, 사장님 수정 모드 |
| `references/backend.md` | Apps Script 2개 action · 스크립트 속성 · photos 가지 · 배포 규칙 |
| `references/blog-system.md` | `_blog` 원본 → `build-blog.mjs` → `/blog/`, 검사기 규칙, 새 글 쓰는 순서 |

---

## 1. 회사 정보 (사이트에 공개된 것만)

| 항목 | 값 |
|---|---|
| 상호 | 이벤트와 교육연구소 (영문 `Event & Education institute`) |
| 대표 | 황윤수 — 사이트 호칭은 **「소장」** (대표 소개 페이지 이름만 「대표 소개」) |
| 주소 | 인천광역시 남동구 문화서로62번길 17, 3층 302호 (`build_site.py ADDR`. port_docs · company.json 은 「문화서로 62번길」 띄어쓰기 — 통일 안 됨) |
| 사업자등록번호 | 578-03-01411 (계약서 KB-20261009-273 기준, 바닥글 공개) |
| 전화 | 사이트 전체에 010 휴대폰 번호 하나. **이 스킬에는 적지 않는다** — `build_site.py TEL` · `port_docs.py TEL` · `assets/app.js SMS_TO` 에 있다. README: 「기존 시안의 대표 번호 — 대표 확인 필요」 |
| 이메일 | ihaha2040@gmail.com (기존 시안의 대표 메일 — 대표 확인 필요) |
| 채널 | 카카오톡 채널 `pf.kakao.com/_XVrSs` (상담 링크 `/chat`) · 네이버 블로그 `blog.naver.com/event_edu` |
| 슬로건 | 「즐거움을 기획하고, 성장을 교육합니다」 / 「행사로 마음을 모으고, 교육으로 사람을 키웁니다」 |
| 비전 · 미션 | 비전 「다음세대가 행복한 세상」 · 미션 「즐거움과 성장이 함께하는 현장」 |
| 사이트 숫자 | 20년(현장 경력) · 94곳(2011년부터 운동회를 맡긴 학교 — 서울 45 · 경기 37 · 인천 9 · 그 밖 3, `assets/data/schools.json`) · 대상별 행사 5 · 교육 6 |
| 활동 지역 | 서울 · 인천 · 경기 (JSON-LD `areaServed`, llms.txt) |
| 소장 이력(공개) | 인하대 교육대학원 석사(심리치료상담 전공) · 이벤트 PD · 레크리에이션 전문가 · 인천 동구 · 서구 진로체험센터 전문강사 · 전) 감정놀이연구소 인천지사 대표 · 전) 이벤트비전 수석실장 · 저서 『메타버스, 즐기는 자가 먼저다』 · 논문 「감정놀이 프로그램이 유아의 정서지능에 미치는 영향」 (전체는 `build_site.py build_ceo`) |

- 기획안의 「누적 행사 ○○회 · 함께한 기관 ○○곳」은 수치를 못 받아 **쓰지 않았다**. 숫자를 새로 만들지 말 것.
- 후기 4개 · 카톡 캡처(`review-kakao.webp`)는 기존 시안 것 — 공개 동의 확인 필요(README).
- 계약 담당자 연락처 · 계좌 · 서버 비밀값 · 수정 모드 열쇠는 이 스킬에 적지 않는다. 계좌는 `port_docs.py` 가 빈칸으로 만든다.
- 납품 근거: 큰길브리지 계약 KB-20261009-273(회사형, 2026-10-10 서명, 오픈 예정 2026-10-20). 관리: 큰길브리지 1533-7295 · www.ai-make.co.kr.

## 2. 레포 · 도메인 · 배포

- 레포 `brizymedia/edu-event`. 로컬 클론은 **얕은 클론(커밋 1개)**, 원격 기본 가지 **`master`**. README 는 「Pages(main 루트)」라고 적었으니 실제 Pages 설정 가지는 **확인 필요**.
- 도메인 **미정**. `BASE = 'https://brizymedia.github.io/edu-event'`(canonical · og · sitemap · JSON-LD · 블로그 절대주소 모두 이 값). `CNAME` 파일 없음.
- **검색 차단 상태**: `build_site.py NOINDEX = True` → 모든 페이지 `noindex,nofollow` + `robots.txt` `Disallow: /`.
- 배포: GitHub Pages 가 레포를 그대로 서비스(빌드 단계 · `.github/workflows/` 없음). 생성기는 사람이 로컬에서 돌리고 결과를 커밋.
- `photos` 고아 가지(사진 업로드 · 공지 저장소)는 클론에 없다 — 만들어졌는지 **확인 필요**(README 오픈 체크리스트 3번).
- 유입 통계: 모든 페이지 `https://www.ai-make.co.kr/stats/stats.js` `data-site="edu"`(큰길브리지 서버, 레포 밖. 현황판 SITE 목록에 추가 필요 — README).

**오픈할 때(README 순서)**: ① 도메인 정해지면 `build_site.py BASE` · `port_docs.py HOME` 바꾸고 두 스크립트 재실행 → CNAME 은 DNS 가 산 뒤 커밋 ② `NOINDEX = False` → 재실행 ③ photos 고아 가지(빈 `photos/photos.json` · `photos/notices.json`) ④ Apps Script 2개 배포 → `/exec` 주소를 `port_docs.py CONTRACT_URL · GALLERY_URL` → `port_docs.py` **와** `build_site.py` 재실행 ⑤ 공용 문의 서버에 대표 메일 수신 추가 ⑥ stats 현황판 등록 ⑦ 서치어드바이저 · 서치콘솔(소유 확인 태그는 `page()` 의 `EDIT_META` 옆에 넣어야 재생성 때 안 사라짐).

## 3. 파일 지도 (요약 — `references/file-map.md`)

```
tools/build_site.py   ★ 공개 페이지 생성기 (회사 정보 · 자료 · 템플릿 함수 전부)
  → index about ceo event education portfolio contact notice notice-admin 404 .html + sitemap.xml robots.txt llms.txt
tools/blog_shell.py   build_site 의 BASE · 머리글 · 바닥글 · 상담 띠를 JSON 으로 내보냄 (build-blog.mjs 가 부름)
scripts/build-blog.mjs → blog/ (매번 지우고 새로) · rss.xml · sitemap.xml 의 /blog/ 줄 · llms.txt 「## 블로그」 절
scripts/blog-check.mjs  blog-plan.mjs     블로그 검사기 · 남은 주제
_blog/                블로그 원본 (posts/*.json, GUIDE.md, company/keywords/photos/sources.json)
tools/port_docs.py    → quote.html quote-catalog.js contract.html statement.html schedule.html upload.html admin-lock.js
                        office.html apps-script/{contract,gallery}/Code.gs  (원본 = 큰길이벤트 레포, 이 레포에 없음)
tools/admin_gate.py   office.html 에 관리자 잠금 화면(<!--GATE-->) 씌움 (port_docs 가 마지막에 부름)
tools/apply_edits.py  사장님 수정 모드 결과(JSON)를 HTML 에 반영
assets/style.css      공통 스타일(손 수정 OK)   assets/app.js  공통 스크립트   assets/edit.js  수정 모드   assets/blog.css
assets/data/          notices.json(정적 공지) · schools.json(실적 학교 94곳)  ← build_site 가 읽음
assets/img/           로고 4종 · favicon.png · og.jpg · hero-event/edu.webp · ceo.webp · g01~g10 · p/<접두어>NN.webp(87) · story-2011 · review-kakao
assets/video/         sci-v1~5 · magic-v1 (.mp4 + 같은 이름 .jpg 포스터)
```

| 고칠 것 | 고치는 곳 | 다시 돌릴 것 |
|---|---|---|
| 공개 페이지 글 · 사진 배치 · 메뉴 · 바닥글 | `tools/build_site.py` (상수 또는 `build_*()` 함수) | `python tools/build_site.py` → `node scripts/build-blog.mjs` |
| 포트폴리오 사진 목록 · 분류 | `build_site.py PHOTO_SETS` · `WORKS_OLD` · `PF_FILTERS` | 위와 같음 |
| 실적 학교 | `assets/data/schools.json` | 위와 같음 |
| 정적 공지 | `assets/data/notices.json` | 위와 같음 (서버 연결 뒤엔 `notice-admin.html`) |
| 색 · 간격 · 반응형 | `assets/style.css` | `VER` 을 올렸다면 build_site + build-blog |
| 블로그 글 | `_blog/posts/<날짜>-<slug>.json` | `node scripts/blog-check.mjs --new <파일>` → `node scripts/build-blog.mjs` |
| 견적 품목 · 업무 화면 회사 설정 · 서버 주소 | `tools/port_docs.py` 「회사 설정」 | `python tools/port_docs.py <큰길이벤트 레포>` (+ 서버 주소를 바꿨으면 build_site) |

## 4. 디자인 체계 (요약 — `references/design-tokens.md`)

- 콘셉트(`style.css` 머리 주석): **「로고의 아치 · 산호 · 연두에서 출발한 디자인」**. 크림 바탕 + 산호(코랄) + 연두(라임), 둥근 아치 모양 반복.
- 핵심 토큰: `--ink #3D3938` · `--soft #6B6461` · `--cream #FFF9F1`(바탕, theme-color) · `--sand #F7EEE2`(교차 섹션) · `--coral #FA8A7A` · `--coral-ink #C8432F`(글자 · 주 단추) · `--coral-bg #FFE9E4` · `--lime #CFE5A3` · `--lime-ink #3F7A2A` · `--lime-bg #EEF6DC` · `--sun #F4A55A` · `--mint #A8D8C4` · `--sky #8CC3EA` · `--grape #B79AE0` · `--r-lg 32px` · `--r-md 22px` · 스프링 이징 `cubic-bezier(.32,.72,0,1)`.
- 글꼴: 제목 **Jua**(Google Fonts, `--display`, weight 400) · 본문 **Pretendard Variable v1.3.9 dynamic-subset**(jsDelivr). 둘 다 `style.css` 맨 위 `@import`. 본문 17px / 1.75. `body{word-break:keep-all}`.
- 반응형 기준: **1060**(메뉴 → 햄버거) · **900**(히어로 1열) · 860 · 760(하단 고정 상담 단추 `.dock` 등장, 숫자 2열) · 640 · 560 · 480. `.wrap` = `min(1200px, 100% - 40px)`.
- 머리글: **떠 있는 알약**(`.hdr .pill`, fixed top 14px, 블러 반투명 크림) — 로고 이미지 `logo-h.png` + 메뉴 5개 + 산호 전화 단추. 스크롤 30px 넘으면 `.solid`.
- 반복 컴포넌트: 알약 꼬리표 `.eb`(점 + 대문자 영문, `.lime` 변형), `.h2` + `.hl`(산호)/`.hl-l`(연두) 강조, 단추 `.btn`(안에 둥근 화살표 `.ar`, 변형 coral · lime · line · white · sm), 더블 베젤 카드 `.bz>.in`, 등장 효과 `.rv`(+`.d1~d4` 지연, 위로 46px + 블러 8px), CTA 띠 `.cta`(어두운 상자 + 오른쪽 아래 산호 · 연두 반원 아치), 서브 머리 `.phead`(모래 바탕 + 연두 원 · 산호 반원).

### 행사 | 교육 2분할 히어로 (`index.html .hero`)

- `grid-template-columns:1fr 1fr`, 높이 `100svh`. 왼쪽 `a.pane.ev`(→event.html, `hero-event.webp`, 산호→어두운 갈색 그라데이션 덮개, 꼬리표 EVENT, 「행사로 마음을 모읍니다」), 오른쪽 `a.pane.ed`(→education.html, `hero-edu.webp`, 연두→어두운 녹색, EDUCATION, 「교육으로 사람을 키웁니다」).
- 가운데 아래 `.core .arch` — **세 겹 아치**(산호 → 흰 → 연두, `border-radius:999px 999px 0 0`)에 `<h1>`「즐거움을 기획하고, 성장을 교육합니다」+ 단추 3개(행사 보기 · 교육 보기 · 견적 문의). 등장 `@keyframes rise`.
- 색종이 `.confetti`(app.js 가 폰 16개 / PC 30개 생성, `fall` 애니메이션), PC(hover + 901px 이상)는 포인터 따라 두 사진이 반대로 살짝 움직임. `prefers-reduced-motion` 이면 둘 다 끔.
- **900px 이하**: 1열, 아치가 `order:-1` 로 맨 위(크림 바탕, 머리글 아래 84px), 그 아래 행사 · 교육 사진 패널이 차례로(각 `max(60vw,330px)`), SCROLL 표시 숨김.
- 사진 초점: `.pane.ev img{object-position:16% 60%}` · `.pane.ed img{object-position:60% 30%}` — 사진을 바꾸면 여기도 본다.

## 5. 페이지 구성 (요약 — `references/sections.md`)

메뉴(`NAV`): 회사 소개 · 행사 · 교육 · 포트폴리오 · 견적 문의. 폰 메뉴 하단 보조: 대표 소개 · 공지사항 · 자동 견적서 · 블로그 · 네이버 블로그.

- **index**: 2분할 히어로 → 흐르는 띠(TICKER 14개) → 숫자 4 → 두 개의 파트(행사 · 교육 카드) → 대상별 5 → 대표 요약 → 갤러리 6 → 후기 3 → 공지 4 → CTA
- **about**: 소개 → 비전 · 미션 → 핵심 가치 3 → 왜 우리인가요 7 → 오시는 길 → CTA
- **ceo**: 인사말(아치 사진) → 이력 4칸 → 무대 위의 소장(사진 3) → 운동장에서 보낸 20년(2011 사진 + 연표 4) → CTA
- **event**: 대상 5개 탭(sticky) → 대상별 블록 5(큰 사진 + 썸네일 2~3, 소개, 프로그램 칩, 「이 행사 견적 문의」) → 진행 방식 4 → CTA
- **education**: 교육 카드 6 → 수업 현장(영상 5 + 사진 6) → 회차(1 · 4 · 8회, 어두운 섹션) → CTA
- **portfolio**: 분류 필터 + 사진 97장(18장씩 「더 보기」) → 마술 공연 영상 1 → 실적 학교 94곳(지역 4 접이식) → 후기 4 + 카톡 캡처 → CTA
- **contact**: 견적 문의 폼 + 옆 카드 4(전화 · 카톡 · 자동 견적서 · 오시는 길) → FAQ 5(FAQPage JSON-LD)
- **notice** · **notice-admin** · **404**

## 6. 스크립트 기능 (`assets/app.js`, 외부 라이브러리 없음)

1. 머리글 `.solid` 토글, 폰 메뉴 `.mbtn` ↔ `#sheet`(Esc 닫기, body 스크롤 잠금).
2. `.rv` 등장(IntersectionObserver + 0.4/1.5초 재검사 + 6초 뒤 화면 3배 안 강제 표시).
3. 히어로 색종이 · 포인터 시차. 4. `[data-n]` 숫자 올라가기(1.5초). 5. 띠 글자 두 번 이어붙여 무한 흐름.
6. 포트폴리오: `.filters [data-f]` 필터(분류는 `data-c` 공백 구분 여러 개), 18장씩 `#pfMore`, 해시(`#church` 등)로 필터 열기, `#pfEmpty`.
   `photos` 가지 `photos.json`(raw.githubusercontent, 5분 캐시 꼬리표)을 읽어 업로드 사진을 **앞에** 붙이고 필요한 필터 단추를 추가. 이미지는 jsDelivr `@photos`.
7. 라이트박스 `.lb`: `.gal` · `.pf` 의 figure 클릭/Enter → 크게, 캡션은 `data-t`.
8. 공지: `.notes[data-live]` 가 `photos` 가지 `notices.json`(2분 캐시 꼬리표)을 읽어 **서버 공지 + 정적 공지(`data-static`)** 순으로 다시 그림(대문은 `data-max=4`).
9. 문의 폼 `#qform`: `?type=` 으로 문의 종류 미리 선택, 숨은 `website` 칸 함정, 이름 · 연락처 · 동의 필수 → 공용 문의 서버로 JSON POST(`text/plain`) → `{ok:true}` 면 `#qdone`. 실패하면 내용 복사 + 폰은 `sms:` 문자 앱, PC 는 전화 안내.
10. 바닥글 끝 「관리자 모드」 링크 → `office.html`(app.js 경로에서 기준 주소 계산, 블로그에서도 맞음).

## 7. build_site.py 로 고치는 법 (핵심 — 자세히 `references/content.md`)

```bash
python tools/build_site.py          # ⚠ Python 3.12 이상 필요 (아래 함정 1)
node scripts/build-blog.mjs         # 반드시 이어서 — sitemap.xml · llms.txt 의 블로그 부분 복구
git diff --stat                     # 의도한 파일만 바뀌었는지
```

- 파일 맨 위 **「회사 정보」**(NAME · CEO · BIZNO · ADDR · TEL · EMAIL · KAKAO · NBLOG · BASE · NOINDEX · VER · EDIT_HASH · MAP · NAV) → **「자료」**(EVENT_CATS · AUD_SHORT · EDU · WORKS_OLD · PHOTO_SETS · PF_FILTERS · REVIEWS · TIMELINE · TICKER · FAQ, + schools.json · notices.json) → **「조각」**(btn · header · footer · jsonld_biz · page · phead · cta_band · gal_fig) → 페이지별 `build_*()`.
- 문구가 상수에 없으면 해당 `build_*()` 안의 f-string HTML 을 직접 고친다(about 소개문 · 인사말 · 비전 등은 함수 안에 있다).
- `page()` 가 `<head>`(title · description · noindex · theme-color · 수정 모드 메타 · canonical · og) + 머리글 + 바닥글 + 스크립트 3개(app.js · edit.js · stats.js)를 매번 새로 쓴다. **결과 HTML 에 직접 넣은 것은 다음 실행 때 사라진다.**
- 재현성(이 분석에서 확인): 임시 복사본에서 Python 3.12 로 돌린 결과 **HTML 10개는 레포와 바이트 단위로 같았다**. 차이는 `sitemap.xml` 날짜(lastmod=오늘)와, build-blog 전 단계의 블로그 줄 · llms.txt 블로그 절 누락뿐 — build-blog 를 이어 돌리면 날짜 외 차이 없음. 즉 지금(c0c4773)은 **build_site.py 가 진짜 원본**이다.

### ⚠ 「사장님 수정 반영 뒤 덮어쓰기」 함정

사장님이 `?edit=열쇠` 로 고친 글 · 사진은 `tools/apply_edits.py` 가 **HTML 에 직접** 반영한다(build_site.py 는 안 고친다).
그 상태에서 build_site.py 를 돌리면 사장님 수정이 **전부 원래대로 덮어써진다**(README 「고치는 법」에 명시).

안전한 순서:
1. `python tools/apply_edits.py 수정파일.json` → 출력의 「수동 확인」 건은 손으로.
2. **같은 문구를 build_site.py 의 상수/함수에도 옮긴다**(사진은 같은 파일 이름으로 덮였으니 코드 수정 불필요).
3. 임시로 `python tools/build_site.py` 를 돌려 `git diff` 가 비어야(=build_site 가 반영본과 같아야) 정상. 차이가 남으면 2번이 덜 된 것.
4. 2번을 못 하면 그 뒤로는 HTML 이 원본 — build_site.py 를 돌리지 말고 HTML 을 직접 고친다(README 방침). 이 경우 메뉴 · 바닥글 바꾸기가 10쪽 수작업이 된다.

## 8. 사진 · 영상 (자세히 `references/content.md`)

- 대표님 카톡 사진(폴더별) → `assets/img/p/<접두어>NN.webp`(두 자리, 1부터). README 기준 **긴 변 1400px WebP**. 실제 파일은 긴 변 1280px(55장) · 1400px(24장) 등 — 카톡 압축 원본(1280px)이라 키우지 않은 것으로 보인다. **변환 스크립트는 레포에 없다**(확인 필요).
- 접두어 7종(`PHOTO_SETS`, 장수와 파일 수가 정확히 맞아야 함): `school` 29 초등학교 운동회 · `church` 23 교회 전교인 명랑운동회 · `sci` 12 과학실험 마술수업(분류 edu) · `magic` 8 마술 공연 · `gov` 5 관공서 체육대회(corp gov) · `corp` 4 기업 레크리에이션 · `univ` 6 대학 축제 공연(local).
- 기존 시안 사진 `g01~g10.webp`(900~1200px) 은 `WORKS_OLD` 로 여러 분류를 달아 그대로 둠. 「성탄 축하 행사 매직쇼」 교회 분류는 짐작(README).
- 새 묶음 추가: 파일 넣기 → `PHOTO_SETS` 한 줄 → (새 분류면) `PF_FILTERS` · `_mix()` 의 `order` → build_site. 개별 사진을 대문 · 행사 · 교육 페이지에 쓰려면 코드(`'p/school09'` 같은 문자열)를 해당 함수 목록에 넣는다. **WORKS 에 없는 코드를 `gal_fig(W(...))` 로 쓰면 StopIteration 으로 생성이 멈춘다**(`thumbs()` 는 괜찮음).
- 영상: `assets/video/<이름>-vN.mp4` + 같은 이름 `.jpg` 포스터. 현재 h264 + aac, 짧은 변 406~432px, sci 6~22초 · magic 102초(7.8MB). 전부 `preload="none"` + `controls`. 인코딩 설정은 확인 필요.
- 히어로 사진은 `hero-event.webp` · `hero-edu.webp`(1280×721) — 원본 고화질을 받으면 교체(README).
- 얼굴: 아이 얼굴이 나오는 사진이 많다 → 학교 · 학부모 공개 동의 확인(README). 블로그는 `_blog/photos.json` 목록(g01~g10 · story-2011, g09 제외)만 쓸 수 있다 — p/ 사진은 아직 블로그 목록에 없다.

## 9. 업무 화면 · 공지 관리자 · 수정 모드 (자세히 `references/workflows.md`)

- 업무 화면 7개(quote · contract · statement · schedule · upload · office + admin-lock.js)는 큰길이벤트 원본을 `port_docs.py` 로 치환한 **생성물**. 손 수정 금지. 흐름: 문의 → `quote.html?admin=1` 견적 · 저장함 → `contract.html?admin=1` 서명 링크 → `schedule.html` → `upload.html` → `statement.html?admin=1`.
- 손님용 `quote.html` 카탈로그 35품목(7묶음) 전부 `price:null` — **「총액이 바로 나온다」고 쓰지 말 것.**
- ⚠ **서버 주소가 비어 있다**(`port_docs.py CONTRACT_URL = ''`, `GALLERY_URL = ''`). 그래서 지금은 `?admin=1` 화면이 **잠기지 않고**, `office.html` 은 「서버 연결 전」이라 **열 수 없고**, `notice-admin.html` 은 「공지 서버가 연결되지 않았습니다」, 사진 올리기 · 저장함 · 짧은 계약 링크가 안 된다.
- **공지 관리자** `notice-admin.html`(build_site 생성, 인라인 스크립트): 비밀번호 = 사진 올리기 암호(`UPLOAD_PW`), 기기 `sessionStorage edu-notice-pw`. 갤러리 서버에 `notice-list / notice-save / notice-delete` → `photos` 가지 `photos/notices.json`(최대 80개). 서버 주소는 **build_site 가 `port_docs.py` 의 `GALLERY_URL` 줄을 정규식으로 읽어** 넣는다 → 주소를 넣으면 build_site 도 다시 돌려야 한다.
- **사장님 수정 모드** `assets/edit.js`: 주소 `?edit=열쇠` → 열쇠의 SHA-256 이 `<meta name="edu-edit">`(= `build_site.py EDIT_HASH`)와 같을 때만 켜짐(`?edit=off` 끝). 글자 클릭 편집(레이아웃 · 순서 불가), 사진 클릭 교체(1920px JPEG 로 축소), 기기 IndexedDB `edu-edit` 에 보관, 「수정 내용 보내기」 → 글은 공용 문의 서버로 메일, 사진이 있으면 `이벤트와 교육연구소-수정요청-YYYYMMDDHHMM.json` 파일 공유/저장. 큰길브리지가 `apply_edits.py` 로 반영. 열쇠 원문은 어디에도 없다(문자로 따로 전달). 열쇠를 바꾸려면 새 열쇠의 sha256 을 `EDIT_HASH` 에 넣고 build_site. notice-admin · 404 · 블로그에는 메타가 없어 수정 모드가 안 켜진다.

## 10. 백엔드 (요약 — `references/backend.md`)

| 서버 | 쓰는 곳 | 코드 | 스크립트 속성 |
|---|---|---|---|
| 공용 문의 서버(큰길브리지, 레포 밖) | 문의 폼 · 자동 견적서 문의 · 수정 모드 글 전송 | 없음 | — (대표 메일 수신 추가 필요) |
| 계약 서버 `edu-contract` | 계약 저장 · 서명 · PDF · 견적 저장함 · 행사 일정 · 관리자 잠금(`boxList`) | `apps-script/contract/Code.gs` | `BOX_PW` · `CREW_PW` |
| 갤러리 서버 | 사진 올리기 → `photos` 가지 + **공지 3 action** | `apps-script/gallery/Code.gs` | `UPLOAD_PW` · `GITHUB_TOKEN` · `GITHUB_REPO` |

배포: 형님(큰길브리지) 구글 계정, 웹 앱 · 실행=나 · 액세스=모든 사용자. 고치면 「배포 관리 → 연필 → 새 버전」(새 배포는 주소가 바뀜). Code.gs 가 말하는 `README.md` 는 **이 레포에 없다**.

## 11. 블로그 (요약 — `references/blog-system.md`)

HD기획 `_blog` 체계를 **지역 글 → 주제 글**로 바꿔 옮긴 것. 10편(2026-10-21, event 5 · edu 5), 주소 `/blog/` · `/blog/event/` · `/blog/edu/` · `/blog/<slug>/`, **링크는 전부 상대 주소**(하위 경로 github.io 에서도 맞음).
머리글 · 바닥글 · BASE · noindex 는 `blog_shell.py` 가 build_site 에서 가져온다 — 메뉴를 바꾸면 build_site → build-blog 순으로.
현재(2026-10-28 실행): `blog-check` **통과(주의 1건 — 매직쇼 글 2493자)**, `blog-plan` 「모든 주제를 썼습니다」 → 새 글은 `keywords.json` 에 주제부터 추가.
회사 사실은 `_blog/company.json` 문장 안에서만, 허용 숫자 `94곳 · 45곳 · 37곳 · 9곳 · 3곳 · 20년 · 2011년 · 1회 · 4회 · 8회`.

## 12. 검증 절차 (고치면 반드시)

```bash
# 1) 문법
for f in assets/app.js assets/edit.js admin-lock.js quote-catalog.js scripts/*.mjs; do node --check "$f"; done
python -m py_compile tools/build_site.py tools/blog_shell.py tools/port_docs.py tools/apply_edits.py tools/admin_gate.py
# 2) 생성 · 재현성 — 원본만 고쳤다면 diff 는 고친 부분 + sitemap 날짜뿐이어야 한다
python tools/build_site.py && node scripts/build-blog.mjs && git diff --stat
# 3) 블로그
node scripts/blog-check.mjs           # 「통과」
# 4) 화면 — 서버 띄우고 375px · 1280px
python -m http.server 8820
```
- 375px: 가로 스크롤 0, 히어로가 아치 → 행사 사진 → 교육 사진 순, 하단 `.dock`(전화 · 카톡)이 마지막 내용을 가리지 않음(`body{padding-bottom:84px}`), 포트폴리오 1열, 폼 1열, 이벤트 탭이 머리글 아래 붙음.
- 1280px: 알약 머리글에 메뉴 5개 + 전화 단추 한 줄, 히어로 좌우 2분할 + 가운데 아치, 숫자 4열, 대상 5열.
- 콘솔 오류 0 — 단 `contract.html?admin=1` · `statement.html?admin=1` 의 `stamp-edu.png` 404 는 직인 파일이 아직 없어서 나는 **알려진 오류**. 업무 화면은 서버 주소가 비어 있어 「연결 전」 안내가 정상.
- 이 분석에서 Playwright(Chromium)로 공개 10쪽 + 블로그 2쪽 + 업무 6쪽을 375 · 1280 두 폭으로 열어 봤다: **가로 넘침 0, 콘솔 오류는 위 직인 404 뿐**. 외부 글꼴 · stats.js 로드 여부는 이 환경 네트워크 제약으로 확인 못 함.

## 13. 함정과 같이 고칠 곳

1. **Python 3.12 이상 필수.** `build_site.py` `header()` 의 f-string 안 역슬래시(`\"page\"`) 때문에 3.11 이하에서는 SyntaxError. `build-blog.mjs` 는 `python` 명령으로 `blog_shell.py`(→ build_site import)를 부르므로 **PATH 의 `python` 이 3.12+** 여야 한다(이 분석 환경에서는 `python`=3.11 이라 실패 → 3.12 를 앞에 두고 성공).
2. **build_site 뒤엔 반드시 build-blog.** `build_meta()` 가 sitemap.xml · llms.txt 를 통째로 새로 써서 블로그 항목이 빠진다.
3. **apply_edits 뒤 build_site 덮어쓰기**(7장). 또한 `apply_edits.py` 는 `open(path,'w',encoding='utf-8')`(newline 지정 없음)로 쓰므로 Windows 에서 돌리면 파일 전체가 CRLF 로 바뀔 수 있다 — `git diff` 로 확인(build_site 는 `newline='\n'`).
4. **회사 정보가 여러 곳**: `build_site.py`(회사 정보) · `port_docs.py`(회사 설정, 업무 화면 · 서버) · `assets/app.js`(SMS_TO · COMPANY) · `assets/edit.js`(OUR_*) · `_blog/company.json` · `apps-script/contract/Code.gs COMPANY_EMAIL` · README. 전화 · 메일이 바뀌면 전부.
5. **서버 주소 넣은 뒤 두 스크립트 모두**: `port_docs.py`(업무 화면 · office · admin-lock) + `build_site.py`(notice-admin).
6. `port_docs.py` 는 큰길이벤트 원본 레포(기본 `~/Documents/클로드코드`)가 있어야 돈다 — 이 레포만으로는 업무 화면을 다시 만들 수 없다.
7. **없는 파일 참조**: 업무 화면 6쪽의 `<link rel="icon" href="assets/img/favicon.svg">`(파일 없음, favicon.png 만 있음) · `assets/img/stamp-edu.png`(직인 미수령). `quote.html` 메뉴 「행사 이야기」→ `stories/`(이 사이트에 없음), quote 바닥글 「관리자 모드」 `href="/office.html"`(루트 절대 경로 — github.io/edu-event 하위 경로에서 깨짐). 모두 port_docs 치환 규칙으로 고쳐야 한다.
8. **메일 수신처**: `quote.html 견적_수신_이메일` · `contract.html 회사_수신_이메일`(FormSubmit 폴백)이 대표 메일이 아니라 **큰길브리지 관리 계정**. 계약 서버 `MANAGER_EMAIL` 도 같은 계정(의도: 사본). 공용 문의 서버도 아직 큰길 메일로만 간다(README) — 그런데 `office.html` 은 「문의가 대표 메일로 갑니다」라고 표시한다(불일치).
9. `office.html` 안내는 「저장 파일 받기」인데 실제 edit.js 단추는 「수정 내용 보내기」 · 「수정 파일만 저장」. edit.js 「보내는 분」 기본값이 다른 사람 이름으로 들어 있다(edit.js `#es-who` 기본값) — 다른 고객 사이트에서 옮긴 흔적으로 보임, **확인 필요**.
10. 공지 이중 출처: 정적(`notices.json` → HTML 에 구워짐 + `data-static`) + 서버(`photos/notices.json`). 화면은 서버 것 + 정적 것을 이어 붙이므로, 정적 공지를 서버에 다시 쓰면 두 번 보인다. 서버 연결 뒤엔 정적 공지를 정리할 것.
11. 캐시 꼬리표 `VER='1'`(style.css · app.js · edit.js · blog.css 공통). CSS/JS 를 고쳐 배포하면 `VER` 을 올리고 build_site → build-blog.
12. 바닥글 연도(`datetime.date.today().year`) · sitemap lastmod 가 실행 날짜를 따른다 → 다시 돌리면 그 줄들이 바뀌는 것은 정상.
13. 사진 올리기 분류는 6개(kinder · school · corp · local · church · edu). `gov` · `magic` 은 build_site 에만 있고, 업로드 사진은 모르는 분류면 `school` 로 붙는다.
14. 갤러리 Code.gs 주석의 `gallery.html` · `repository_dispatch(photos-updated)` 는 큰길 원본 흔적 — 받는 워크플로 없음(포트폴리오는 photos.json 을 직접 읽으므로 동작 지장 없음).
15. 업무 화면 일부 localStorage 키가 큰길 이름 그대로(`kg_contract_co`, `kg_stmt_bank`), `schedule.html` 주석에 「형님 암호」. 출처가 달라 충돌은 없다.
16. 블로그 검사기 「견적 낱말」 같은 HD 규칙은 이 사이트 검사기에 없다(대신 company.json 근거 · 효과 표현 금지). HD 스킬을 그대로 따르지 말 것.

## 14. 처음부터 다시 만드는 순서

1. 레포 생성(기본 가지 확인) · 로고 PNG 4종(`logo-arch` · `logo-h` · `logo-h-white` · `logo-mark`) + `favicon.png` 256px + `og.jpg` 1200×630.
2. `assets/style.css` — 토큰 · 알약 머리글 · 2분할 히어로 · 공통 컴포넌트(`references/design-tokens.md`).
3. `tools/build_site.py` — 회사 정보 → 자료 → 조각(`page()` · `header()` · `footer()`) → `build_*()` 10개 → `build_meta()`(`references/content.md`, `references/sections.md`). `assets/data/schools.json` · `notices.json`.
4. `assets/app.js` 10기능 · `assets/edit.js`(EDIT_HASH 와 짝) · `tools/apply_edits.py`.
5. 사진 · 영상 변환 → `assets/img/p/` · `assets/video/` → `PHOTO_SETS`.
6. `python tools/build_site.py` (3.12+).
7. 블로그: `_blog/` 자료 5개 + `tools/blog_shell.py` + `scripts/` 3개 + `assets/blog.css` → 글 → `blog-check` → `build-blog`.
8. 업무 도구: 큰길이벤트 원본 레포로 `python tools/port_docs.py <경로>` → admin_gate 자동.
9. Apps Script 2개 배포 → 속성 5개 → 주소를 port_docs 에 → port_docs + build_site 재실행 → photos 고아 가지.
10. 검증(12장) → 커밋 · 푸시 → Pages → 오픈 체크리스트(2장).

## 15. 확인 필요 목록

- 사이트 전화 · 메일이 대표 것이 맞는지(계약서의 담당자 연락처와 다름 — README).
- Pages 가 `master` 를 서비스하는지(README 는 main), `photos` 고아 가지 존재 여부, 도메인.
- Apps Script 2개 배포 여부(코드상 주소 빈칸) · 공용 문의 서버의 대표 메일 수신 추가 여부 · stats 현황판 등록.
- 사진 변환 방법(스크립트 없음) · 영상 인코딩 설정 · 히어로 원본 고화질.
- 아이 얼굴 · 후기 · 카톡 캡처 공개 동의, 「성탄 축하 행사 매직쇼」 교회 분류, 교회 프로그램 실제 운영 여부, 교육 · 행사 상세(시간 · 인원 · 준비물).
- 직인 `stamp-edu.png`, 대표 계좌(port_docs 빈칸).
- edit.js 「보내는 분」 기본 이름(다른 사람 이름)의 출처, office.html 문구 불일치(8 · 9번 함정).
- 얕은 클론이라 커밋 이력 · 이전 버전과의 차이는 못 봄.

## 16. 지켜야 할 것

- 사실만. 확인 못 한 숫자 · 후기 · 실적 · 교육 효과는 쓰지 않는다(기획안의 ○○ 숫자 포함). 모르면 「확인 필요」.
- 교육 문구에서 효과 단정 · 의학 표현 금지(「심리치료상담」 전공 표기만 예외 — 블로그 GUIDE 2장).
- 비밀값(암호 · 토큰 · 수정 모드 열쇠) · 계좌 · 개인 휴대폰을 코드 · 문서 · 커밋에 넣지 않는다.
- 생성물 HTML 손 수정 금지 — 공개 페이지는 build_site.py, 블로그는 `_blog` + build-blog, 업무 화면은 port_docs.py. 예외는 7장의 「사장님 수정 반영 뒤」 상황뿐.
- 다른 회사 이름을 공개 글에 쓰지 않는다.

# 페이지별 섹션 — 이벤트와 교육연구소

모든 공개 페이지 공통: 건너뛰기 링크 → 알약 머리글 → 폰 메뉴 `#sheet` → `<main id="main">` → 바닥글 → `.dock` → 라이트박스 → app.js · edit.js · stats.js.
서브 페이지는 `phead()` 머리(빵부스러기 · 영문 꼬리표 · h1 · 설명)로 시작하고 대부분 `cta_band()` 로 끝난다.
`.sec.sand` 로 흰/모래 바탕을 번갈아 쓴다. 문구 출처: 콘텐츠 기획안(README) + 기존 시안.

## index.html — `build_index()`

| # | 섹션 | 내용 |
|---|---|---|
| 1 | `.hero` | 2분할(행사 · 교육 사진 링크) + 가운데 아치 h1 + 단추 3 + 색종이 + SCROLL (SKILL.md 4장) |
| 2 | `.ticker` | TICKER 14개 흐름 |
| 3 | `#numbers` BY THE NUMBERS | 「숫자로 보는 연구소」 20년 · 94곳 · 5개 · 6개 (`data-n` 올라가기) |
| 4 | `#parts` TWO PARTS (sand) | 「두 개의 파트」 행사 카드(p/school11, 칩 5, 행사 자세히) · 교육 카드(p/sci01, 칩 5, 교육 자세히) |
| 5 | `#audience` FOR YOU | 「어떤 행사를 준비하세요?」 대상 5카드 → `event.html#<id>` |
| 6 | `#ceo` CEO (sand) | 아치 사진 + 「마음을 읽는 MC, 성장을 돕는 교육자」 + 이력 3줄 + 대표 소개 단추 |
| 7 | `#gallery` PORTFOLIO | 「최근 행사 갤러리」 6장(p/school09 w t · p/sci10 · p/church21 · p/univ02 w · p/corp01 · p/magic04) + 네이버 블로그 안내 |
| 8 | `#reviews` REVIEWS (sand) | 「“내년에도 꼭 와주세요”」 후기 3 |
| 9 | `#notice` NOTICE | 공지 4(`data-live="index" data-max="4"`) |
| 10 | `.cta` | 「행사 날짜가 정해지셨나요?」 |

`<head>` 에 LocalBusiness JSON-LD + `hero-event.webp` preload. h1 은 아치 안 하나뿐(패널 제목은 h2).

## about.html — `build_about()` (cur=about)
phead 「즐거움을 기획하고, 성장을 교육합니다」 → INTRO(2단: 「사람이 모이는 자리에는 언제나 두 가지가 필요합니다」 + 본문 3문단) → VISION & MISSION (sand, 더블 베젤 2) → CORE VALUES 3(마음을 읽는 진행 · 20년 현장 경험 · 원스톱 운영) → WHY US 7 (sand, 체크 목록) → `#map` LOCATION(주소 · 전화 · 메일 · 네이버 지도) → CTA.

## ceo.html — `build_ceo()` (cur=about)
phead(빵부스러기 회사 소개 › 대표 소개) → GREETING(아치 사진 + 인사말 5문단 + 서명) → CAREER (sand) 4칸(현재 · 학력 · 주요 경력 5 · 저서 · 논문) → ON STAGE 사진 3(p/corp01 · corp03 · corp04) → STORY (sand) 「운동장에서 보낸 20년」(story-2011 사진 + 연표 4) → CTA 「소장과 직접 상담하세요」.

## event.html — `build_event()`
phead 「행사로 마음을 모읍니다」 → 대상 탭 5(sticky) + 블록 5(`article.cat#<id>`: 큰 사진 + 썸네일, 번호 · 제목 · 「대상 — 소개」 · 프로그램 칩 · (kinder 만 구성 예시) · 「이 행사 견적 문의」) → HOW IT WORKS (sand) 「상담부터 사진 전달까지」 4(사전 상담 · 현장 답사 / 우천 · 돌발 / 소장 직접 진행 / 현장 사진) → CTA.

## education.html — `build_edu()`
phead 「교육으로 사람을 키웁니다」(`.hl-l` 연두) → PROGRAMS 「교육 프로그램 6가지」 카드 6(아이콘 · 이름 · 대상 · 소개 · 기대효과 · 교육 문의) → `#class` CLASS (sand) 「수업 현장」 영상 5 + 사진 6(p/sci01 w t · sci07 · sci08 · sci04 w · sci10 · sci06) → COURSE (`.sec.dark`) 「회차는 필요에 맞게」 1회 특강 · 4회 과정 · 8회 과정 + 교육 문의 → CTA 「우리 기관에 맞는 교육이 궁금하세요?」.

## portfolio.html — `build_portfolio()`
phead 「저희가 다녀온 행사」 → 필터(사진 있는 분류만) + `.pf` 97장(18장씩 「사진 더 보기」, `#pfEmpty`) + 네이버 블로그 안내 → `#video` VIDEO (sand) magic-v1 → `#record` TRACK RECORD 「해마다 다시 불러주시는 학교들」 지역 4 `<details>`(학교명 + 진행 연도) → `#reviews` 후기 4 + 카톡 캡처 → CTA.
업로드 사진(photos 가지)은 app.js 가 런타임에 맨 앞에 붙인다.

## contact.html — `build_contact()`
phead 「행사 날짜가 정해지셨나요? 지금 견적을 받아보세요」 → `#form`: 폼(문의 종류 7 · 성함* · 연락처* · 기관 · 이메일 · 날짜 · 인원 · 장소 · 요청사항 · 숨은 website · 개인정보 동의) + 완료 상자 `#qdone` / 옆 카드 4 → FAQ (sand) 5. `<head>` 에 FAQPage JSON-LD. CTA 띠 없음.
문의 종류: 유치원 · 어린이집 행사 / 초등학교 운동회 · 행사 / 기업체 · 기관 행사 / 지자체 · 축제 / 교회 행사 / 교육 프로그램 / 기타.

## notice.html — `build_notice()`
phead → `ul.notes[data-live="page"]`(각 `li#n<i>`, 내용 `b` 있으면 아래 줄) → CTA. 대문 공지 링크는 `notice.html#n<i>`.

## notice-admin.html — `build_notice_admin()`
phead(ADMIN) → 서버 없으면 안내 상자 / 있으면 로그인 → 작성 폼(날짜 · NEW · 제목 · 내용) + 올린 공지 목록(수정 · 삭제). 자세히 `workflows.md`.

## 404.html
「페이지를 찾을 수 없어요」 + 처음으로. (GitHub Pages 가 루트 404.html 을 쓴다.)

## 블로그 (build-blog.mjs)
`/blog/` 목록 · `/blog/event/` · `/blog/edu/` 분야 모음 · 글 쪽. 머리글 · 바닥글은 build_site 것 그대로(현재 메뉴 표시 없음), 끝에 CTA 「행사 · 교육 상담이 필요하신가요?」. 글 쪽에 BreadcrumbList · BlogPosting · (FAQ 있으면) FAQPage JSON-LD.

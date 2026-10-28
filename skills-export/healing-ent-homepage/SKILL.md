---
name: healing-ent-homepage
description: 힐링엔터테인먼트(서울 노원, 대표 MC 이현호) 홈페이지 brizymedia/healing-ent 를 고치거나 처음부터 다시 만들 때 쓴다. 「힐링엔터」「힐링MC」「이현호 MC」「healing-ent」 홈페이지 · 견적서 · 전자계약서 · 거래명세서 · 행사 일정 · 사진 올리기 · 행사 준비 블로그 · 지역 페이지 · 행사 이야기 · 히어로 영상 · 사장님 수정 모드 작업이면 먼저 읽는다.
---

# 힐링엔터테인먼트 홈페이지 (brizymedia/healing-ent)

큰길브리지(주식회사 브리지미디어)가 납품한 고객 홈페이지. 정적 HTML/CSS/JS(외부 라이브러리 없음, 구글 폰트만)
+ Google Apps Script 서버 3개(문의 · 계약 · 갤러리) + Node/Python 생성기로 블로그 · 지역 · 행사 이야기 페이지를 만든다.
이 문서는 2026-10-28 커밋 `8ecc69b` 기준으로 코드를 직접 읽고 쓴 것이다. 코드에서 확인 못 한 것은 「확인 필요」로 적었다.

세부 자료(필요할 때만 읽기):
- `references/file-map.md` — 파일 하나하나가 하는 일, 원본이 어디서 왔는지
- `references/design-tokens.md` — 색 hex · 글꼴 · 반응형 기준 · 컴포넌트 클래스
- `references/sections.md` — 페이지별 섹션 순서와 문구 출처
- `references/workflows.md` — 업무 화면(견적 · 계약 · 명세서 · 일정 · 사진 올리기 · 문서함) 흐름과 상태 저장, 생성기
- `references/backend.md` — Apps Script 서버 3개의 action · 스크립트 속성 · 배포 규칙
- `references/photo-video-pipeline.md` — 네이버 블로그 사진 받기 · 히어로 영상 만들기
- `scripts/` — `make_hero.py` · `decode_img.py` · `post_images.py` (공통 도구 복사본)

---

## 1. 회사 정보 (사이트에 공개된 것만)

| 항목 | 값 |
|---|---|
| 상호 | 힐링엔터테인먼트 (영문 Healing Entertainment, 로고 영문 「Healing」) |
| 대표 | 이현호 (대표 MC · 행사기획 전문가) |
| 주소 | 서울특별시 노원구 덕릉로 595 |
| 사업자등록번호 | 222-22-01111 (바닥글 · 회사소개 공개) |
| 사이트 표기 전화 · 문자 | 010-5620-2153 (사이트 전체가 이 번호. 제출 자료에 다른 번호가 있었으나 표기 번호로 통일함 — 다른 번호는 쓰지 말 것) |
| 이메일 | leehh2153@gmail.com |
| 영업 | 행사 연중무휴 · 상담 평일 10~18시 · 행사 중엔 통화 어려움 → 문자 · 카톡 안내 |
| 채널 | 인스타 mc_hyunholee · 네이버 블로그 leehh2153 · 유튜브 @healingevent · 네이버 플레이스 naver.me/GQGHLRaB · 리틀리 litt.ly/healingmc · 카톡 오픈채팅 open.kakao.com/me/vvipevent |
| 슬로건 | 「재미 · 감동 · 추억이 남는 행사를 만듭니다.」 / 「담당자는 편안하고, 참가자는 즐거운 행사」 |
| 시그니처 | 「대동놀이」 (모두가 함께하는 마무리 프로그램) |
| 사이트 숫자 | 20년(2006~) · 3,000회+ · 100+ 기업 · 공공기관 고객사 · 25개국 60개 지역 해외 워크숍 · 50만 명 규모 행사 총괄 |

- 숫자 출처: 고객 제출 자료 · 대표 MC 프로필 PDF(2026-09-27 수령). 해외는 PDF 에 「20개 나라 50개 지역」이었으나 형님(큰길브리지 대표) 지시로 사이트 전체를 25개국 60개 지역으로 통일했다(시안 README 기록).
- **블로그(`blog/`)에서는 위 숫자를 쓰지 않는다** — `_blog/GUIDE.md` 가 「대표 확인 전」이라 금지하고 `blog-check.mjs` 가 막는다. 대문 · 회사소개에는 있다. 이 차이를 일부러 유지한다.
- 대표 MC 자격 9종(회사소개): 국민안전교육 전문인력 · KEMA CPR · AED · 레크리에이션 지도자 1급 · 웃음치료사 1급 · 리더십강사 1급 · 국외여행인솔자(T/C) · 펀마스터 강사 · 수상구조원 · 래프팅 강사.
- 비밀(사장님 수정 모드 열쇠 원문 · 서버 암호 · GitHub 토큰 · 계좌)은 이 스킬에 적지 않는다. 계좌는 사이트에서도 지웠다(`port_docs.py` 가 빈 값으로 바꿈).

## 2. 고객 요청 · 큰길브리지 원칙 (어기면 납품 불가)

- **색:** 화이트 + 블루 기본, 오렌지 · 옐로 포인트. 홈페이지는 **어두운 배경 · 네온 금지**, 유아적인 디자인 금지.
  히어로 영상 위 덮개도 검정이 아니라 **파란 그라데이션**이다(style.css 주석 「검정 아님」).
  예외: 업무 화면(견적 · 계약 · 명세서 · 일정 · 사진 올리기 · 문서함 · 관리자 잠금)은 큰길이벤트 원본을 옮긴 것이라
  짙은 남색 `#0C1838` 바탕 + 오렌지다. 손님이 보는 홈페이지가 아니므로 그대로 둔다.
- **없는 사실 금지:** 확인 안 된 후기 · 별점 · 만족도 · 재의뢰율 · 「안전사고 ZERO」 · 거래처 이름 금지. 후기 섹션은 없고
  「재섭외가 이어지는 이유」(자료 문구) + 「블로그 행사 이야기」 카드로 대신했다. 블로그 원글 제목의 「참여율 98%」 같은 수치도 순화했다.
- **가격표 금지:** 「정해진 가격표 대신 맞춤 견적」. `quote-catalog.js` 모든 품목이 `price:null` — 손님 견적서에 금액이 안 나온다.
  블로그에 「총액이 바로 나온다」고 쓰지 않는다.
- **사진:** 고객 본인 네이버 블로그(leehh2153) · 대표 MC 프로필 PDF 의 실제 행사 사진만. AI 그림 · 인포그래픽 · 글자판 · 남의 사진 금지.
  학생 · 아이는 원경 · 뒷모습 위주, 얼굴 큰 사진 금지. 출처는 `assets/img/SOURCES.md` 에 한 줄씩.
- **문장:** 합니다체, 쉬운 말. `body{word-break:keep-all}` 유지(빼면 한글 낱자가 끊긴다).
- **대표 MC 다른 소속**(여행사 · 유아 업체 · 협회 직함)은 회사소개 「현 직책」에만 있고, 블로그에는 쓰지 않는다(GUIDE 규칙).
- 비밀(토큰 · 암호)은 코드에 넣지 않는다 — 서버 「스크립트 속성」에만.

## 3. 레포 · 도메인 · 배포

- 레포: `brizymedia/healing-ent` (main 브랜치). 사진 올리기 결과는 **`photos` 브랜치**에 쌓인다(main 아님).
  현재 클론은 깊이 1(커밋 1개)이라 이력은 `git log` 로 못 본다. 이력은 커밋 메시지 본문 · 시안 README 에 있다.
- 주소: **https://brizymedia.github.io/healing-ent/** (GitHub Pages, `.nojekyll` 있음 → `_blog/` 도 공개된다. 비밀 적지 말 것).
  전용 도메인 없음(「Healing」 이름으로 새로 잡을 예정 — 확인 필요).
- 배포: main 에 push 하면 Pages 가 반영. **`.github/workflows` 는 이 레포에 없다.** 갤러리 서버 주석의
  「6시간마다 도는 자동 작업」 · `photos-updated` 디스패치를 받을 워크플로도 이 레포에선 확인 안 됨(확인 필요). 갤러리는
  `portfolio.html` 이 photos 브랜치의 `photos/photos.json` 을 직접 읽어서 워크플로 없이도 보인다.
- 사이트가 하위 경로(`/healing-ent/`)에 있으므로 **모든 내부 링크는 상대 경로**. 블로그 원본 JSON 은 `/quote.html` 처럼 루트 기준으로 쓰고
  `build-blog.mjs` 가 깊이에 맞게 `../../` 로 바꾼다. `robots.txt` 는 루트가 아니라 지금은 검색 로봇이 읽지 않는다(파일 주석).
- 도메인을 바꾸면 같이 고칠 곳: 모든 html 의 canonical · og:url · og:image · JSON-LD, `llms.txt`, `sitemap.xml`, `rss.xml`,
  `robots.txt`, `scripts/build-blog.mjs` 의 `SITE`, `tools/make_pages.py` 의 `BASE`, `tools/port_docs.py` 의 `HOME` · `MAIL_LOGO`, `upload.html` 의 `홈주소`.
- 유입 통계: 모든 공개 페이지 `<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="healing">` (큰길브리지 유입 서버).

## 4. 파일 지도 (요약 — 자세히는 references/file-map.md)

```
index.html about.html service.html portfolio.html video.html notice.html contact.html   공개 7쪽 (edit.js · es-edit 메타 있음)
quote.html + quote-catalog.js     자동 견적서(손님) / ?admin=1 견적 발행 · 저장함
contract.html  statement.html     전자계약서 / 거래명세서 (?admin=1, noindex)
schedule.html  upload.html  office.html   행사 일정 · 사진 올리기 · 대표 전용 업무 문서함 (noindex)
admin-lock.js                     ?admin=1 화면 잠금 (계약 서버 BOX_PW 로 확인)
assets/style.css  assets/app.js  assets/edit.js
assets/img/  (logo-h.svg · logo-h-white.svg/.png · logo-mark.svg · favicon.svg · og.jpg · mc-lee*.webp · works/w1~w28 · b1~b4 · th/ · sig/9장 · SOURCES.md)
assets/video/ hero.mp4 · hero_sm.mp4 · hero_sm.webm · hero_poster.webp      assets/files/healing-checklist.pdf
stories/ (5편+목록)  areas/ (9지역+목록)   ← python tools/make_pages.py 가 만든다
blog/ (글 10편 + 지역 모음 9 + 목록) · rss.xml   ← node scripts/build-blog.mjs 가 만든다 (원본 _blog/)
apps-script/contract · apps-script/gallery   서버 코드 + 설치 README
tools/ port_docs.py · admin_gate.py · make_pages.py · apply_edits.py      scripts/ build-blog · blog-check · blog-plan (.mjs)
llms.txt · sitemap.xml · robots.txt · rss.xml · .nojekyll · README.md
```

**손으로 고치면 안 되는 결과물:** `blog/` · `rss.xml`(build-blog 가 매번 지우고 새로 씀), `stories/` · `areas/`(make_pages),
업무 화면 6종 + `quote-catalog.js` + `admin-lock.js` + `apps-script/*/Code.gs`(port_docs 가 큰길이벤트 원본에서 다시 옮김).
고칠 거면 생성기 안의 표나 규칙을 고친 뒤 다시 돌린다.

## 5. 디자인 체계 (요약 — references/design-tokens.md)

- 색: `--blue #1B5CF2` · `--blue2 #3D8BFF` · `--blue-d #1448C8` · `--navy #132F6B` · `--ink #1A2440` · `--sub #56627E` ·
  `--sky #EEF4FF` · `--sky2 #F6F9FF` · `--line #DCE5F5` · `--or #FF8A1E` · `--or-d #E8730A` · `--ye #FFC23A` · `--ye-l #FFF4D6`. theme-color `#1B5CF2`.
- 글꼴: Noto Sans KR 400~900(본문 · 제목) + Outfit 600~800(숫자 · 영문 `--en`). 구글 폰트 한 줄.
- 반경 `--r 18px` · `--r-s 12px`, 버튼은 알약형(999px) 높이 52px. 그림자는 파란 기운(`rgba(27,92,242,.10)`).
- 반응형: 1320 · 1180 · 1120(메뉴 9개 한 줄 유지) → **1024 이하 햄버거** → 960 → **760 이하 폰**(머리 62px, 하단 고정 4단추) → 600.
- 핵심 컴포넌트: 히어로 `.stage`(둥근 30px 무대 + 영상 + 파란 덮개 + 노란 거대한 「20」) · 서비스 5칸 `.svc5`(히어로에 -84px 겹침) ·
  키워드 띠 `.marq` · 카드 `.cards` · MC 프로필 `.mc` · 대표 실적 `.sigt` · 갤러리 `.gal` + 라이트박스 `.lb` · 영상 `.vids/.vgrid` ·
  서브 머리 `.ph-head` · CTA 띠 `.band`(파랑 그라데이션 + 노랑 · 오렌지 원) · 바닥 `.ft` · 폰 하단 `.quick` · 등장 `.rv(.d1~d4)`.
- 제목 강조 `<em>` = 파란 글자 + 노란 형광 밑줄(`linear-gradient(transparent 68%, --ye-l 68%)`). eyebrow 앞 오렌지 · 옐로 점 두 개.
- 캐시 깨기: 모든 페이지가 `style.css?v=24` · `app.js?v=20261004` · `edit.js?v=1`. CSS · JS 를 고치면 **모든 html 의 숫자를 함께 올린다**
  (stories · areas 는 notice.html 틀을 복사하므로 notice.html 을 고친 뒤 make_pages 를 다시 돌리면 따라간다).

## 6. 섹션 구성 (요약 — references/sections.md)

대문 `index.html`: 히어로(현장 영상 + 「20년 경력의 행사 전문 기업, 힐링엔터테인먼트」 + 숫자 4 + CTA) → 서비스 5칸 → 키워드 띠 →
하는 일 카드 5 → MC 이현호 프로필(자격 9) → 대표 실적 4 → 진행 방식이 다릅니다(강점 3) → 현장 사진 10 →
재섭외가 이어지는 이유 + 블로그 행사 이야기 4 → 진행 5단계 → 영상(홍보영상 + 4편 + 채널 카드) → 공지 · 오시는 길 → 빠른 견적 폼 → 바닥글.
서브: 회사소개(인사말 · 숫자 5 · MC 프로필 상세 · 일하는 방식 3 · 회사 정보) · 하는 일(5분야 + 이런 행사도 6 + 비용 안내 + 진행 순서) ·
현장 갤러리(대표 실적 8분야 + 사진 필터 5) · 영상(분류 단추 + 44편) · 공지(공지 · 게시판 · 자료실 탭, `#notice/#blog/#files`) · 견적문의(연락 4 + 폼 + FAQ 4).

## 7. 스크립트 기능 (`assets/app.js`, 외부 라이브러리 없음)

맨 위 「사장님 · 큰길브리지가 고치는 곳」에 설정과 데이터가 모여 있다:
`FORM_ENDPOINT`(공용 문의 서버) · `SMS_TO` · `COMPANY` · `KAKAO_URL` · `PROMO_ID`(홍보영상 bIoatdv9iYw) · `VCATS`(영상 분류 8) ·
`VIDEOS`(44편, `s:true`=쇼츠) · `NOTICES`(공지, `n`=NEW · `pin`=고정) · `FILES`(자료실) · `WORKS`(사진 28장 ↔ 제목 · 장소 · 분류) · `BLOG`(네이버 글 21편).

기능: 카톡 단추 주소 넣기 → 유튜브(썸네일 먼저, 누르면 youtube-nocookie 재생, 쇼츠는 세로 창) → 머리 그림자 · 햄버거 시트 · 맨 위로 ·
현재 메뉴 `.act` → 히어로 영상(폭 × DPR < 900 이면 `hero_sm.mp4`, H.264 못 틀면 `hero_sm.webm`, reduced-motion 이면 포스터만, 재생/정지 단추) →
숫자 올라가기(rAF 대신 setInterval — 백그라운드 탭에서도 끝값 도달) → 키워드 띠 복제 → `.rv` 등장 → 갤러리(WORKS + photos 브랜치 photos.json 합침,
필터 · 개수 · 라이트박스 ← → Esc 스와이프) → 공지 · 게시판 · 자료실(10개씩 더 보기) → 문의 폼 → 바닥글 「관리자 모드」 링크(→ office.html).

문의 폼(`form.qform`): 스팸 함정 `website` 칸, 성함 · 연락처 · 동의 필수 → `FORM_ENDPOINT` 에 `text/plain` JSON POST.
서버가 `{ok:true}` 일 때만 성공. 실패 · 빈 주소면 **폰은 문자 앱(sms:010-5620-2153, 본문 채움), PC 는 클립보드 복사 + 번호 안내**.
공용 문의 서버는 `page` 주소의 레포 이름(healing-ent)으로 회사를 알아보고 leehh2153@gmail.com + 큰길브리지로 메일을 보낸다(app.js 주석. 서버 코드는 이 레포에 없음).

## 8. 업무 화면 (요약 — references/workflows.md)

전부 `tools/port_docs.py` 가 **큰길이벤트기획 레포(기본 `~/Documents/클로드코드`)** 에서 옮겨 회사 정보 · 색 · 예시 문구 · 서버 주소를 바꾼 결과다.

- `quote.html` 손님 화면: 품목 체크 → 수량 · 일수만 수정 → 「이 견적으로 문의 보내기」(문의 서버 → 실패 시 FormSubmit → mailto). 금액 · 직인 · 인쇄 가림.
- `quote.html?admin=1`: 견적 발행 · 고객 메일용 복사 · 「계약서 작성」(→ `contract.html?admin=1#c=…`) · 「거래명세서」(→ `statement.html?admin=1#t=…`) ·
  저장함(이 기기 `healing-quote-box-v1`, 50개) + 폰 · PC 같이 보기(계약 서버 `boxList/boxPut/boxDel`, 암호 BOX_PW). 견적 상태는 주소 `#q=` 코드.
- `contract.html?admin=1`: 행사 대행 / 출연 계약서 2종, 취소 위약표 · 특약 → 「고객 서명 링크」 `contract.html?c=<ID>&s=<배포ID>` → 고객 폰 서명 →
  서버가 PDF · 드라이브 · 양측 메일 · 계약 대장. 서버 없으면 긴 링크 + 메일 폴백. 계약번호 `HL-YYYYMMDD-XXX`. 직인 파일이 없으면 「(인)」만.
- `statement.html?admin=1`: 거래명세서, 서버 없음, 인쇄 · PDF.
- `schedule.html`: 행사 일정 · 체크리스트(목록 · 월간 · 행사 하나 `#e=`), 계약 서버 `sched*`, 직원 암호 CREW_PW 또는 대표 암호.
- `upload.html`: 폰에서 사진 → 1600px 워터마크 사본 → 갤러리 서버 → photos 브랜치 → 현장 갤러리. 대표 썸네일(정사각 · 가로) · 블로그 · 인스타 글 자동 작성.
- `office.html`: 대표 전용 문서함(도구 카드 · 서버 연결 상태 · 암호 안내). `admin_gate.py` 잠금(BOX_PW).
- 잠금: `admin-lock.js` 가 `?admin=1` 화면만 덮고 계약 서버에 `{action:'boxList', pw}` 를 보내 확인. 암호는 페이지에 없다.

## 9. Apps Script 백엔드 (요약 — references/backend.md)

| 서버 | 주소(웹 앱 /exec) | 쓰는 곳 |
|---|---|---|
| 공용 문의 서버(큰길브리지 소유, 코드 이 레포에 없음) | `https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec` | app.js 폼 · quote.html 손님 문의 · edit.js 수정 메일 |
| 계약 서버 `apps-script/contract` | `https://script.google.com/macros/s/AKfycbwm8qkj9FgIwX3NOJiLdkTwJp8F8ncf1UwRqn-XJMg2HYXIOYBuZjleIiUt_J2DvL1O/exec` | contract · quote 저장함 · schedule · admin-lock · office |
| 갤러리 서버 `apps-script/gallery` | `https://script.google.com/macros/s/AKfycbw5HFoNVKAbu8xUcPGE6BUjHIM98vgc_cCGe98PlTZpfL4_c8oWktLuOsKcm0ggerTVLw/exec` | upload.html |

배포 규칙: 실행 = 나, 액세스 = **모든 사용자**. 코드를 고치면 **배포 관리 → 연필 → 새 버전**(새 배포를 만들면 주소가 바뀐다).
암호 · 토큰은 스크립트 속성에만: 계약 `BOX_PW`(대표) · `CREW_PW`(직원), 갤러리 `UPLOAD_PW` · `GITHUB_TOKEN` · `GITHUB_REPO`.
서버 주소를 바꾸면 `tools/port_docs.py` 의 `CONTRACT_URL` · `GALLERY_URL` 을 고치고 다시 돌린다(app.js · edit.js 의 문의 서버 주소는 손으로).

## 10. 생성기와 실행 명령

```bash
cd healing-ent
python3 tools/make_pages.py                       # stories/ 5편 + areas/ 9지역 + sitemap.xml (블로그 항목은 남김)
node scripts/blog-plan.mjs                        # 다음에 쓸 글(지역 · 주제 · 키워드) 추천 (--json, --n 5)
node scripts/blog-check.mjs --new _blog/posts/<파일>.json   # 새 글 엄격 검사 — 통과할 때까지 고친다
node scripts/blog-check.mjs                       # 전체 글 검사
node scripts/build-blog.mjs                       # blog/ 새로 만들기 + rss.xml · sitemap.xml · llms.txt 블로그 부분 갱신
python3 tools/port_docs.py <큰길이벤트 레포 경로>   # 업무 화면 6종 · 서버 코드 · office.html 다시 옮기기 (원본 레포 필요)
python3 tools/apply_edits.py <수정파일.json 또는 메일본문.txt>   # 사장님 수정 반영 → git diff 확인 → push
```

- `make_pages.py`: 머리 · 바닥을 `notice.html` 에서 빌려 온다. 내용은 파일 안 `STORIES`(5) · `AREAS`(9) 표만 고친다.
  AREAS 의 분 · km 는 본사 → 구청 · 시청 OSRM(2026-10-03, 5분 반올림). `done` 은 프로필 · 블로그에 기록된 행사만.
- 블로그: 규칙서 `_blog/GUIDE.md` 를 먼저 읽는다. 원본 `_blog/posts/<날짜>-<slug>.json`, 자료 `regions.json` · `keywords.json` · `photos.json` · `sources.json`.
  검사기는 사이트 숫자(20년 · 3,000회 · 50만 · 25개국 · 100+ 등) · 재의뢰 · 안전사고 ZERO · 가격 · 목록에 없는 사진 · 손으로 만든 공식 출처 주소 · 견적서에 없는 품목 · 지역 이름만 바꾼 글(30% 중복)을 막는다.
  블로그 HTML 은 `style.css` 를 쓰지 않고 `build-blog.mjs` 안의 `CSS`(남색 상단 바) 를 쓴다.

## 11. 사장님 수정 모드 (`assets/edit.js`)

- 켜기: `사이트주소/?edit=<열쇠>` — 열쇠의 SHA-256 이 공개 7쪽의 `<meta name="es-edit" content="…">` 와 같을 때만 켜진다. 끄기 `?edit=off`.
  열쇠 원문은 큰길브리지 내부 기록(시안 폴더 README)에만 있다. 새로 만들면 해시를 7쪽 메타에 모두 넣는다.
- 글자는 누르고 고침(Enter = 줄바꿈, 붙여넣기는 글자만), 사진은 눌러 갤러리에서 고름(1920px · 0.86 으로 줄임). 레이아웃 · 색 · 순서는 못 건드림.
  건너뛰는 곳: `#gal,#pfGrid,#boardBlog,#boardFiles,.marq,.lb,.done,.quick,form,#tabs`.
- 고친 것은 IndexedDB `es-edit` 에 페이지별 보관 → 「수정 내용 보내기」 = 문의 서버로 글 수정 메일 + 사진 있으면 `힐링엔터테인먼트-수정요청-YYYYMMDDHHMM.json` 공유/내려받기.
- 반영: `python3 tools/apply_edits.py 파일` — 7쪽에서 원문을 찾아 바꾸고, 못 찾으면 `assets/app.js`(NOTICES · FILES) 에서 찾는다. 못 찾은 것은 「수동 확인」.
- stories · areas 는 make_pages 가 es-edit 메타 · edit.js 를 빼므로 수정 모드가 없다. 블로그도 없다.

## 12. 히어로 영상 · 사진 (요약 — references/photo-video-pipeline.md)

- 영상: 실제 현장 사진 7장(w2 · w4 · w3 · w5 · w7 · w12 · w1)을 `scripts/make_hero.py` 로 천천히 확대 · 이동 + 0.8초 교차 전환 → 23.2초 무음.
  `hero.mp4` 1920×1080 · `hero_sm.mp4` 960×540 · `hero_poster.webp`. **AI 영상 금지**(한글 · 간판을 뭉갬).
  `hero_sm.webm`(VP9 960×540)은 make_hero.py 가 만들지 않는다 — ffmpeg 로 따로 만든다(명령은 reference 참고, 원래 쓴 옵션은 확인 필요).
- 사진: 네이버는 이 환경에서 직접 못 받는다 → Firecrawl 로 RSS · 모바일 글을 긁고 `post_images.py` 로 weserv 주소 → 다시 Firecrawl `rawHtml` →
  `decode_img.py` 로 webp. `works/` 긴 변 1600px, `works/th/` 800px. 새 사진은 `SOURCES.md` 와 `app.js WORKS` 와 `_blog/photos.json` 에 같이 적는다.

## 13. 검증 (고치면 반드시)

```bash
cd healing-ent && python3 -m http.server 8903 &      # file:// 로 열면 영상 · fetch 가 안 된다
```
1. playwright 로 공개 7쪽 + quote · stories/index · areas/index · blog/index 를 **375×812 · 1280×800** 으로 열어
   콘솔 오류 0, `document.documentElement.scrollWidth <= innerWidth`, 깨진 이미지 0(`img.naturalWidth>0`).
   (외부 stats.js · 유튜브 썸네일 · 구글 폰트가 막힌 환경의 네트워크 오류는 구분해서 본다.)
2. 대문 영상 `video.readyState>=2`, 숫자 20 · 3,000 끝값, 햄버거 시트, 갤러리 필터 · 라이트박스(← → Esc), 공지 탭 `#blog`, 영상 분류 단추 · 재생 창,
   문의 폼 제출(서버 실패 시 대체 문구), 1025~1320px 에서 메뉴 9개가 한 줄인지.
3. 문법: `node --check assets/app.js assets/edit.js admin-lock.js quote-catalog.js` · `node --check scripts/*.mjs` ·
   `python3 -m py_compile tools/*.py scripts/*.py`. 업무 화면 인라인 스크립트는 브라우저 콘솔로 확인.
4. 블로그를 건드렸으면 `node scripts/blog-check.mjs` 통과 후 `build-blog.mjs`. 스크린샷은 직접 Read 로 보고 겹침 · 넘침을 고친다.
5. 서버는 끈다. git 커밋 · 푸시는 지시가 있을 때만.

## 14. 함정과 같이 고칠 곳

- **메뉴 9개:** 1025~1320px 에서 두 줄로 꺾였던 적이 있다 → `nowrap` + 단계별 여백(1320 · 1180 · 1120). 메뉴를 늘리면 다시 확인.
  메뉴는 각 html 머리글 · 폰 시트(`.sheet`) · 바닥 `.ftl` 세 곳 + make_pages(notice.html 틀) + build-blog 템플릿 + port_docs `NAV_SITE` 에 따로 있다.
- **같은 origin 공유:** brizymedia.github.io 아래 다른 고객 사이트와 localStorage · IndexedDB 를 함께 쓴다. 대부분 `healing-` 앞글자로 나눴지만
  `contract.html` 의 `kg_contract_co` · `statement.html` 의 `kg_stmt_bank` 는 큰길 이름 그대로고, edit.js 는 DB 이름 `es-edit` + 파일 이름(`index.html`)을 키로 쓴다 →
  다른 고객 사이트와 섞일 수 있다(실제 충돌 여부 확인 필요).
- **폴백 메일 수신자:** `quote.html` 의 `견적_수신_이메일` · `contract.html` 의 `회사_수신_이메일` 이 `gilauto325@gmail.com`(큰길브리지)이다. 서버 실패 시 FormSubmit 경로. 의도인지 확인 필요.
- **숫자 · 문구 변경:** 히어로 · 회사소개 · 서비스 · 대표 실적 · `llms.txt` · JSON-LD · og description · `_blog/GUIDE.md` 4장 · `make_pages.py` 표가 서로 같은 사실을 따로 들고 있다. 하나 바꾸면 전부.
- **전화 · 메일 바꾸기:** 각 html(머리 · 시트 · 히어로 CTA · 연락 · 폼 · 바닥 · 하단 단추) · app.js `SMS_TO` · JSON-LD · llms.txt · make_pages `TEL` · build-blog `TEL` · GUIDE · port_docs `TEL/EMAIL` · Code.gs `COMPANY_EMAIL`.
- **사진 분류 slug** `school · corp · fest · stage` 는 app.js `WORKS c` · `UP_CAT` · portfolio 필터 `data-f` · port_docs `UPLOAD_CATS` 가 같아야 한다.
- 업무 화면을 손으로 고치면 다음 `port_docs.py` 실행 때 사라진다 → 규칙을 port_docs 에 넣는다. 끝에 「남은 큰길 흔적」이 `없음` 인지 본다.
  `port_docs.py` 의 `NAV_SITE` 는 업무 화면 메뉴의 `/blog/` 를 `notice.html`(「공지 · 블로그」)로 바꾼다 — `blog/` 가 생기기 전 규칙이라 지금 홈페이지 메뉴(공지 / 블로그 따로)와 다르다.
- `make_pages.py` 는 sitemap 을 새로 쓰되 `/blog/` 항목만 남긴다. 순서: make_pages → build-blog.
- `apps-script/gallery/README.md` 의 `scripts/prepare-gallery-photos.mjs` 는 이 레포에 없다(큰길 원본 이야기).
- `assets/img/mc-lee-studio.webp`(대문 · 회사소개 프로필)는 SOURCES.md 에 없다 — 출처 확인 필요(`mc-lee.webp` 는 프로필 PDF 2쪽).
- robots.txt 의 `Disallow:` 는 하위 경로 사이트라 지금은 효과 없다. 업무 화면은 페이지 안 `noindex` 로 막는다(quote.html 은 손님용이라 index).

## 15. 처음부터 다시 만드는 순서

1. 자료 모으기: 회사 정보(1장) · 대표 MC 프로필 PDF · 네이버 블로그 RSS(`rss.blog.naver.com/leehh2153.xml`) · 리틀리 영상 목록. 자료끼리 다르면 README 「확인할 것」.
2. 틀: `assets/style.css` 토큰(5장) → 공개 7쪽 공통 머리(로고 · 메뉴 9 · 전화 · 빠른 견적 · 햄버거) · 시트 · 바닥 · 하단 4단추 · 맨 위로.
3. 사진: photo-video-pipeline 순서로 works 28장 + th, sig 9장, SOURCES.md. 히어로 영상 make_hero.py + webm.
4. 대문 섹션(6장 순서) → 서브 6쪽. app.js 데이터 배열(VIDEOS · NOTICES · FILES · WORKS · BLOG) 채우기. 로고 SVG · og.jpg(1200×630).
5. 검색: 각 쪽 title · description · canonical · og, 대문 LocalBusiness JSON-LD, llms.txt, sitemap, robots.
6. 업무 화면: 큰길이벤트 레포를 받아 `python3 tools/port_docs.py <경로>` (회사 설정 칸만 이 회사 값). 서버 2개 설치(backend.md) 후 주소 넣고 다시 실행.
7. `python3 tools/make_pages.py` → `_blog` 자료 · 글 → `blog-check` → `build-blog`.
8. 수정 모드 열쇠 해시 7쪽 메타, edit.js · apply_edits.py.
9. 13장 검증 → README 갱신 → (지시 있을 때) 커밋 · 푸시.

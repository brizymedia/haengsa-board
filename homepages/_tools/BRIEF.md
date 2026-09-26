# 고객 홈페이지 제작 공통 지침 (큰길브리지 납품물)

작업자는 이 문서를 먼저 끝까지 읽는다. 고객별 자료는 각자 받은 작업 지시에 있다.

## 1. 무엇을 만드나
- 계약한 이벤트 · 행사 회사의 **기업형(회사형) 홈페이지** — 여러 페이지, 정적 HTML/CSS/JS, 서버 · 빌드 도구 · 외부 라이브러리 없음(구글 폰트만 허용).
- 결과물 위치: `/home/user/haengsa-board/homepages/<slug>/` 한 폴더에 전부. 모든 경로는 상대 경로(나중에 고객별 레포로 그대로 옮긴다). 다른 폴더는 건드리지 말 것. **git 커밋 · 푸시 금지**(총괄이 한다).

## 2. 참고할 우리 납품물 (읽고 분석해서 이어받을 것)
| 레포(읽기 전용 클론) | 배울 점 |
|---|---|
| `/home/user/brizymedia/es-company` | **기본 틀.** 가장 최근 납품(다섯 페이지 · 히어로 슬라이더 · 가치 탭 · 서비스 · 갤러리 라이트박스 · 공지 · 문의 폼 · FORM_ENDPOINT 비었을 때 문자/복사 대체 · 사장님 수정 모드 edit.js · JSON-LD · og). README 의 「납품 전 확인」 형식도 그대로 따른다 |
| `/home/user/brizymedia/hd-event` | es-company 의 원형(나인엠씨 구조). 섹션 순서 · 프로세스 5단계 · 포트폴리오 필터 |
| `/home/user/brizymedia/pro-event` | 영상 히어로 · 커튼 · 카운터 · 사업분야 무대 · 섭외 |
| `/home/user/brizymedia/goodfriend-event` | 스크롤 인터랙션 14종(진행률 바 · 등장 · 마퀴 · 단어 점등 · 가로 스크롤) — 유아 · 체육 업체에 어울림 |
| `/home/user/brizymedia/keungil-event` | 큰길이벤트.com (형님 회사). 바로기획이 참고 사이트로 지목 |
| `/home/user/claude-skills/*/SKILL.md` | 회사 규칙 · 함정 모음. `brizymedia-common` 은 꼭 읽기 |

**es-company 를 복사해 색 · 글꼴만 바꾸지 말 것.** 틀(파일 구성 · 스크립트 기능 · 폼 · 수정 모드)은 이어받되, 대문 레이아웃 · 히어로 연출 · 색 · 글꼴 · 섹션 구성은 고객의 업종과 요청 분위기에 맞게 다시 설계해서 다섯 회사 사이트가 서로 달라 보여야 한다.

## 3. 페이지 구성 (기업형 기본)
`index.html`(대문) · `about.html`(회사 · 대표 소개, 연혁, 오시는 길) · `service.html`(하는 일 상세) · `portfolio.html`(현장 사진 필터 · 라이트박스) · `notice.html`(**공지 · 게시판 · 자료실** 탭 — 글 목록은 `assets/app.js` 맨 위 `NOTICES` · `FILES` 배열, 사장님 수정 모드로 글 고침) · `contact.html`(견적 문의 폼 + 자주 묻는 질문). 고객이 요청한 페이지(채용 · 영상 · 가격표 등)가 있으면 추가.
- 모바일 하단 고정 단추: 전화 · 문자 · (카톡 채널이 있으면) 카톡 · 견적문의.
- 문의 폼: `FORM_ENDPOINT = ''` 로 두고 es-company 와 같은 대체 동작(폰=문자 앱, PC=복사 + 전화 안내).
- 사장님 수정 모드: es-company `assets/edit.js` 를 가져와 열쇠(meta 해시)만 새로 만든다. 열쇠는 README 에 적는다.
- 검색: title · description · canonical 은 비우지 말고, `LocalBusiness` JSON-LD, og 태그(og:image 는 `assets/img/og.jpg` 1200×630 을 만들어 쓴다). **시안 단계라 모든 페이지에 `<meta name="robots" content="noindex,nofollow">`** — README 「오픈할 때 바꿀 것」에 제거를 적는다.
- 하단: 상호 · 대표 · 주소 · 전화 · 사업자번호 · 「제작 큰길브리지」 링크(es-company 푸터 참고).
- `body { word-break: keep-all }` (한글 낱자 끊김 방지). 폰 375px · 데스크톱 1280px 둘 다 가로 스크롤 없이.

## 4. 사진 — 고객 본인의 네이버 블로그 사진만
이 환경은 네이버(blog · pstatic)에 직접 접속이 막혀 있다. **Firecrawl 도구로 우회한다** (`mcp__Firecrawl-cd3a0493__firecrawl_scrape`, 안 되면 `mcp__Firecrawl__firecrawl_scrape`).
1. 글 목록: `https://rss.blog.naver.com/<블로그ID>.xml` 을 formats `["rawHtml"]` 로 긁는다 → 최근 글 50편의 제목 · 링크 · 대표 사진 · 태그 · 요약.
2. 행사 · 현장 글을 골라 `https://m.blog.naver.com/<블로그ID>/<글번호>` 를 formats `["html"]` 로 긁는다. 결과가 크면 도구가 파일로 저장하고 경로를 알려 준다 → `python3 /home/user/haengsa-board/homepages/_tools/post_images.py <그 파일>` 이 사진 주소 목록(weserv 주소)을 준다.
3. 사진 한 장 = 그 weserv 주소를 formats `["rawHtml"]` 로 긁기 → 저장된 파일 경로를 `python3 /home/user/haengsa-board/homepages/_tools/decode_img.py <파일> <저장경로.webp>` 로 푼다(1600px webp). 받은 사진은 `Read` 로 직접 보고 고른다.
- **쓰지 말 것**: 인포그래픽 · 글자판 · 캡처 · 남의 뉴스 사진 · AI 생성 그림 · 아이 얼굴이 크게 나온 근접 사진(유아 업체는 뒷모습 · 원경 위주) · 다른 회사 워터마크.
- 목표 15~30장(히어로 6~8 · 서비스 · 갤러리). 출처는 `assets/img/SOURCES.md` 에 「파일명 — 글 제목 — 글 주소」.
- 파일 크기: 긴 변 1600px 이하 webp, 갤러리 썸네일은 800px 로 따로 만들어도 좋다(PIL).
- Firecrawl 호출은 한 번에 여러 개 병렬로 보내도 된다.

## 5. 히어로 영상
`python3 /home/user/haengsa-board/homepages/_tools/make_hero.py <사이트>/assets/video <사진1> … <사진7>` — 가로 사진 6~8장으로 천천히 확대 · 이동 + 교차 전환 영상(hero.mp4 1920×1080, hero_sm.mp4 폰용, hero_poster.webp). 글자가 큰 사진(현수막 정면)은 되도록 피한다. `<video autoplay muted loop playsinline poster>` + 폰은 hero_sm(`<source media>` 대신 JS 로 폭 보고 고르는 es/pro 방식). `prefers-reduced-motion` 이면 포스터만.

## 6. 절대 규칙 (어기면 납품 불가)
- **없는 사실을 만들지 않는다.** 후기 · 만족도 · 누적 건수 · 거래처 이름은 고객이 준 자료와 블로그에 있는 것만. 실제 후기가 없으면 후기 섹션은 넣지 않거나 「블로그 행사 이야기」로 대신한다(README 에 적기).
- 고객이 「넣지 말 것」 · 「피할 것」이라고 한 것(색 · 가격표 등)은 지킨다.
- 전화번호 · 주소 · 사업자번호는 받은 자료 그대로. 자료끼리 다르면 README 「확인할 것」에 적는다.
- 비밀(토큰 · 키)은 코드에 넣지 않는다.

## 7. 검증 (끝내기 전에 반드시)
```bash
cd /home/user/haengsa-board/homepages/<slug> && python3 -m http.server <포트> &   # 포트는 작업 지시에 있음
```
playwright(파이썬, `pip` 설치됨, 크로미움은 `executable_path='/opt/pw-browsers/chromium'` 없으면 기본값)로:
1. 모든 페이지를 375×812 · 1280×800 으로 열어 **콘솔 오류 0**, 가로 넘침 없음(`document.documentElement.scrollWidth <= innerWidth`), 깨진 이미지 0(`img.naturalWidth>0`).
2. 대문 히어로 영상이 재생되는지(`video.readyState>=2`), 메뉴 · 탭 · 라이트박스 · 문의 폼 제출(대체 동작)을 실제로 눌러 본다.
3. 전체 화면 스크린샷을 `/tmp/claude-0/shots/<slug>/` 에 저장하고 **직접 Read 로 보면서** 디자인을 다듬는다(겹침 · 빈칸 · 글자 넘침).
끝나면 서버를 끈다.

## 8. README.md (각 사이트 폴더)
es-company README 형식: 계약 정보 · 구조 · 보기 · 회사 정보(자료 기준) · 사진 출처 요약 · **납품 전 확인할 것(대표에게 물어볼 것)** · 사장님 수정 모드 열쇠 · 오픈할 때 바꿀 것.

## 9. 보고 (작업 끝에 총괄에게)
만든 페이지 목록, 쓴 사진 수, 영상 길이 · 용량, 검증 결과(오류 수), 고객에게 확인할 것 목록, 못 한 것. 짧게.

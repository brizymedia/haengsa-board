# 업무 화면 흐름 · 상태 저장 · 생성기

업무 화면 6종(quote · contract · statement · schedule · upload · office) + `quote-catalog.js` + `admin-lock.js` + 서버 코드는
`python3 tools/port_docs.py [큰길이벤트 레포 경로]`(기본 `~/Documents/클로드코드`)가 큰길이벤트기획 원본에서 옮긴 결과다.
**결과 HTML 을 손으로 고치지 말고 port_docs.py 안의 규칙(회사 설정 · `*_extra()` 함수)으로 넣는다.** 원본 레포는 이 환경에 없다(확인 필요: 다른 PC 경로).

## 0. port_docs.py 가 하는 일

1. `common()` — 큰길 회사명 · 대표 · 사업자번호 · 주소 · 전화 · 메일 · 계좌(빈 값) · 계약번호 앞글자 `KG-`→`HL-` · 기기 저장 이름 `keungil-*`→`healing-*` · 예시 문구(`EXAMPLES`) · 색(`COLORS`) 바꾸기.
2. 검색엔진 소유확인 태그 제거, 메뉴 주소 바꾸기(`nav()` · `NAV_SITE`), 「KG」 네모 로고 → `assets/img/logo-mark.svg`, 직인 → `assets/img/stamp-healing.png`(없으면 「(인)」), 서버 주소 넣기(`servers()`).
3. 페이지별 손질: quote(직인 줄 제거 · 제목/설명) · catalog(`CATALOG` 통째 교체) · contract(가짜 도장 대신 「(인)」, noindex) · statement(직인 없으면 지움) · upload(갤러리 칸 · 지역표 · photos 주소 · 문구, noindex).
4. `port_servers()` — Code.gs 2개 옮김(계약 서버에 `MANAGER_EMAIL` 큰길브리지 사본 수신 추가). `office()` — 문서함 생성 → `admin_gate.apply()` 잠금.
5. 각 파일마다 「남은 큰길 흔적」(`큰길 · 김동길 · 광양 · 브리지미디어 · 큰길 계좌번호 앞자리 · xn--wk0 · keungil · KG<`)을 출력 → `없음` 이어야 한다.

## 1. 자동 견적서 `quote.html` + `quote-catalog.js`

- **품목표** `CATALOG` 8묶음: 행사 기획 · 진행(p1~p8) · MC · 레크리에이션(f1 대표 MC 이현호 진행 · f6 · f8 대동놀이 · f5 스탭) · 공연 섭외(f2 가수 · f4 댄스 · f7 DJ) · 음향(a1~a4) · 무대 · 조명(b1~b4) · 게임도구 · 이벤트 존(h3 · h1 에어바운스 · h8 · h2 물놀이 · h7 경품) · 천막 · 테이블(d3 · d12 · d9) · 기타(g4 · g1 · g2 · g3 출장비 「서울 · 경기 외 지역」).
  **모든 `price:null`** → 금액 없음. `qty:true` 는 수량 칸. 블로그 검사기도 이 품목 이름으로 「견적서에 없는 약속」을 거른다.
- **손님 화면**(주소에 `admin=1` 없음): body `.cust`, 직인 · 인쇄 · 행 추가 · 할인 숨김, 품목명 · 규격 · 단위 · 단가 잠금(다른 데 비교견적으로 못 쓰게).
  「이 견적으로 문의 보내기」 → 공용 문의 서버(`서버접수`) → 실패하면 FormSubmit(`formsubmit.co/ajax/` + `견적_수신_이메일`) → 그것도 실패하면 mailto. 수신 메일 변수는 `gilauto325@gmail.com`(큰길브리지) — 확인 필요.
- **관리자 화면** `quote.html?admin=1`(admin-lock 으로 잠김): 견적 작성 · 고객 메일용 서식 복사(`고객발송`) ·
  「계약서 작성」 → `contract.html?admin=1#c=<b64u JSON>`(번호 `HL-YYYYMMDD-XXX`, 고객 · 행사 · 품목 · 할인) ·
  「거래명세서」 → `statement.html?admin=1#t=…` · 「일정에 넣기」 → `schedule.html#new=…`.
- **상태:** 견적 전체가 주소 `#q=<코드>`(`encodeState()`)에 들어간다 — 서버에 견적 본문은 없다. 짧은 주소용 `?q=` 형식도 읽는다.
- **저장함:** localStorage `healing-quote-box-v1`(최대 50). 「연결하기」로 암호(BOX_PW)를 넣으면 `healing-quote-box-pw` 에 기억하고
  계약 서버 `boxList · boxPut · boxDel` 로 폰 · PC 목록을 합친다(서버 쪽 최대 100, 드라이브 `_data/견적서-보관함.json`). 담기는 것은 코드 · 제목 · 고객 · 금액뿐.

## 2. 전자계약서 `contract.html?admin=1`

- 종류: **행사 대행 계약서**(service, 제1~14조) / **출연 계약서**(cast — 갑 · 을이 뒤집힘, 미성년 출연자 법정대리인 동의). 취소 위약 기본표 `CANCEL_DEF`(행사 대행: 30일 전 없음 · 29~15일 10% · 14~7일 30% · 6일~당일 50%).
- 왼쪽 관리자 패널(`data-k` 바인딩) → 오른쪽 종이 미리보기. 회사 정보 · 서버 주소 · 계좌는 localStorage `kg_contract_co`(큰길 이름 그대로 — 같은 origin 다른 사이트와 섞일 수 있음, 확인 필요).
- 「고객 서명 링크 만들기」: 서버가 있으면 `store` → 짧은 링크 `contract.html?c=<ID>&s=<배포ID>`. 없으면 계약 전체를 해시에 담은 긴 링크(약 1,400자).
- 고객 화면: 링크 열기 → 계약서 확인 → 손서명 → 동의 2개 → 「서명하고 계약서 보내기」 → `sign` → 서버가 PDF(도장 + 서명) → 드라이브 `힐링엔터테인먼트 계약서/연도/` → 회사 · 고객 · 큰길브리지 메일 → 「계약 대장」 시트 기록. 다시 열면 「서명 완료」 + PDF 링크.
  서버가 없으면 FormSubmit 으로 `회사_수신_이메일`(gilauto325) 에 서명 통보만.
- 직인: `assets/img/stamp-healing.png`(투명 PNG, 600px 이상 권장) — 지금 레포에 없음 → 「(인)」만 표시. 가짜 도장은 그리지 않는다. PDF 를 위해 data URI 로 바꿔 보낸다.
- 문서 확인 코드 SHA-256, 서명 시각 · 기기 정보 기록(전자서명법 제3조 근거 안내는 contract README).

## 3. 거래명세서 `statement.html?admin=1`
서버 없음. 견적서 상태(`#q=` / `#t=`)를 받아 품목 · 금액을 채움 → 편집 표 → 인쇄 · PDF. 계좌는 localStorage `kg_stmt_bank`. 직인 파일이 없으면 이미지를 지운다.

## 4. 행사 일정 · 체크리스트 `schedule.html`
- 계약 서버의 `행사일정.json`(최대 300건) 하나를 대표 · 직원이 함께 본다. 암호: 직원 `CREW_PW` 또는 대표 `BOX_PW`. localStorage `healing-sched-pw` · `healing-sched-who`(누가).
- 화면: 목록 · 월간 일정표 · 행사 하나(`#e=<id>`) · 체크리스트(`schedCheck`). 저장 `schedSave` · 삭제 `schedDel`.
- 견적서에서 넘어온 새 행사 `#new=<b64u>` 자동 채움. 「저장해 둔 견적서에서 가져오기」는 대표 암호일 때만(보관함은 BOX_PW 전용).

## 5. 사진 올리기 `upload.html` (폰용)
1. 처음 한 번: 갤러리 서버 웹 앱 주소(기본값 `GALLERY_URL` 박혀 있음) → localStorage `healing_srv`.
2. 01 행사 정보: 갤러리 항목(`school 학교행사 · corp 기업 · 단체 워크숍 · fest 지역축제 · stage 무대 · 음향`) · 행사명 · 행사일 · 장소 · 설명.
3. 02 사진 고르기: 여러 장, 워터마크(오른쪽 위, 웹 사본에만) · 긴 변 1600px 사본. 「대표로」 고른 사진에 행사명 · 날짜 · 장소를 얹은 썸네일 2장(정사각 = 블로그 대표 · 갤러리 칸 표지 / 가로형 = 카톡 공유 · 글 표지), 휴대폰 저장 가능.
4. 03 올리기: 업로드 비밀번호(UPLOAD_PW, 기억 시 `healing_pw`) → 서버 `photo`(장마다) → `cover` → `finish`(photos.json 갱신). 행사 기억 `healing_ev`, 마지막 항목 `healing_cat`.
5. 04 블로그 · 인스타 글: 행사명 · 장소 · 설명에서 지역(`지역표`: 노원 · 도봉 · 강북 · 성북 · 중랑 · 동대문 · 은평 · 의정부 · 남양주 · 구리 · 서울 · 경기)과 장비(`장비표`)를 읽어 제목 후보 · 본문 · 인스타 문구 · 서명 블록을 만든다. 홈페이지 · 갤러리 · 견적 링크 자동.
6. 05 올린 행사 고치기 · 지우기: `edit` · `delete`.
- 결과: photos 브랜치 `photos/<분류>/<eventId>-001.jpg` + `photos/photos.json`. `portfolio.html` 이
  `https://raw.githubusercontent.com/brizymedia/healing-ent/photos/photos/photos.json` 을 읽고 사진은 `https://cdn.jsdelivr.net/gh/brizymedia/healing-ent@photos/` 로 보여 준다(1~2분 캐시).
- 원본은 폰에만 남는다(드라이브 안 씀).

## 6. 대표 전용 업무 문서함 `office.html`
바닥글 맨 끝 작은 「관리자 모드」 링크(app.js 가 붙임) → office.html. `admin_gate.py` 잠금 화면(대표 암호 BOX_PW, 직원 암호로는 안 열림, 맞으면 이 기기에 기억 · 세션 `healing-office`).
카드: 견적서 발행 · 손님용 견적서 · 전자계약서 · 거래명세서 · 행사 일정 · 사진 올리기 · 행사 이야기 · 지역 페이지 · llms.txt · 사이트맵 · 유입 현황(ai-make.co.kr/stats).
계약 · 갤러리 서버에 GET 해서 「연결됨 · 저장함 암호 ✓ · 직원 암호 ✓」를 보여 준다. 「잠그기」 단추.

## 7. 관리자 잠금 `admin-lock.js`
`<script src="admin-lock.js" data-server='<계약 서버>' data-key='healing-quote-box-pw' data-name='힐링엔터테인먼트'>` 를 quote · contract · statement 머리에 둔다.
`?admin=1` 일 때만 화면을 덮고 `{action:'boxList', pw}` 로 확인. 맞으면 localStorage 에 기억(일정 열쇠 `healing-sched-pw` 도 비어 있으면 같이). 서버 주소가 비면 잠그지 않는다. 손님 화면 · 서명 링크는 그대로 열린다.

## 8. 행사 이야기 · 지역 페이지 `tools/make_pages.py`
- 틀: `notice.html` 의 `<main>` 앞뒤를 잘라 쓰고 title · description · canonical · og 를 바꾸며 `es-edit` 메타 · edit.js · `class="act"` 를 뺀다. 내부 주소에 `../` 를 붙이고 `@@` 표시를 실제 경로로 바꾼다(`fix_same_folder`).
- `STORIES`: slug · title · cat · date(`dlabel`) · place · area · lead · facts · body(3문단) · photos(works 이름) · blog(네이버 글 번호) · quote(현재 미사용).
- `AREAS`: slug · name · min · km · hq/city · done · photos. `SERVICES` 6.
- 끝에 sitemap.xml 을 다시 쓴다: 공개 8쪽(대문 · about · service · portfolio · video · notice · contact · quote) + stories · areas + 기존 `/blog/` 항목 유지.

## 9. 행사 준비 블로그 `_blog/` → `blog/`
순서(GUIDE 1장): `blog-plan` → regions.json 의 그 지역 이동 · 동네 · 많은행사 · 주의 · 현장기록 읽기 → sources.json 범위 안에서만 기준 · 법 인용 → photos.json 에서 표지 1 + 본문 2~3(같은 묶음 2장 금지) →
`_blog/posts/<date>-<slug>.json` 작성(`근거` 3개 이상) → `blog-check --new` 통과 → `build-blog` → 커밋 · 푸시.
글 JSON 칸: slug · date · region · topic · title(15~50자) · description(70~160자) · keyword{main,sub} · lead(80~420자) · points(3~5) · cover{path,alt,caption} · sections(4~8, blocks: p · ul · ol · table · img · tip) · faq(2~6) · 근거 · sources.
꾸밈은 `**굵게**` · `[글자](/주소|https://…)` 뿐. 본문 1800자 이상(2500 권장), 표 1개 이상, 내부 링크 2개 이상(`/quote.html` 필수).

## 10. 사장님 수정 반영 `tools/apply_edits.py`
입력: 수정 파일 JSON 또는 메일 본문(`{"v":1` 블록을 찾아냄). 대상 페이지 7쪽만. 원문 innerHTML(정규화 비교, `occ` 번째)을 새 글로 바꾸고, 못 찾으면 app.js 에서 찾고, 그래도 없으면 「수동 확인」.
사진은 `assets/img/` 아래 경로만 허용, 같은 파일 이름으로 덮어쓴다(PIL 있으면 EXIF 회전 · 폭 1920 이하 · webp q82 / jpg q86, 없으면 원본 그대로). 메일로 온 수정에는 사진이 없다(수정 파일로 받아야 함). 끝나면 `git diff` 로 확인.

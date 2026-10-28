# 자주 하는 일 — 절차와 명령

모든 명령은 레포 루트(`j6media/`)에서. 끝나면 SKILL.md §13 검증 → `git add` → `git commit` → `git push`(Pages 가 바로 배포).

## 1. 공지 올리기 · 자료실 추가

`assets/app.js` 맨 위 `NOTICES` 배열에 한 줄 추가(순서 무관 — 날짜 내림차순 + `top` 우선으로 정렬됨).

```js
{ d: '2026.11.01', t: '제목', n: true /* NEW 표시 */, top: false /* 맨 위 고정 */, b: '본문\n줄바꿈은 \\n' },
```

자료실은 `FILES` 에 `{ d, t, k: 'LINK'|'PAGE'|'FILE', u: '주소' }`. `FILE` 이면 단추 글자가 「내려받기」. 파일 자체는 레포에 올리고 상대 주소로.
고친 뒤 모든 HTML 의 `app.js?v=` 를 같은 새 값으로 올린다(`grep -rln "app.js?v=20261004" . | xargs sed -i 's/app.js?v=20261004/app.js?v=새값/'`).

## 2. 블로그 새 글 목록에 넣기

`assets/app.js` 의 `BLOG` 배열 **맨 앞**에 `{ d: "YYYY.MM.DD", t: "글 제목", u: "https://blog.naver.com/martin301/글번호" }`.
자동 수집기는 없다. portfolio(10개씩) · notice 게시판 탭(15개씩)에 「더 보기」로 나온다.

## 3. 현장 사진 추가 (레포에 직접)

1. 원본을 긴 변 1600px webp(`assets/img/works/w58.webp`)와 800px 썸네일(`t58.webp`)로 만든다. 예:
   `ffmpeg -i 원본.jpg -vf "scale='if(gt(iw,ih),1600,-2)':'if(gt(iw,ih),-2,1600)'" -q:v 80 assets/img/works/w58.webp`
   (같은 방식으로 800 → t58). 원래 변환 도구 · 품질값은 기록이 없다 — 확인 필요.
2. `assets/app.js` `WORKS` 에 `{ i: 58, t: '제목', o: '분야 · 지역 · 연도', c: 'church' }` (c 는 공백으로 여러 개: `'install church'`).
3. `assets/img/SOURCES.md` 에 출처 줄 추가(블로그 글 주소 또는 「대표님 원본 YYYY-MM-DD」).
4. 대문에 보이려면 `index.html` `#gal` 의 `data-pick` 번호 목록을 고친다(8장, 1번이 큰 칸).

## 4. 현장 사진 추가 (대표가 폰으로 — upload.html)

1. 대표가 `upload.html` 에서 처음 한 번 서버 주소(이미 박혀 있음) · 사진 비밀번호(`UPLOAD_PW`)를 넣는다(기기에 `j6_srv` `j6_pw` 저장).
2. 사진 칸 고르기 → 행사명 · 날짜 · 장소 · 설명 → 사진 선택(워터마크 기본 켬) → 올리기.
3. 화면이 사진마다 `action:'photo'`(1600px JPEG 0.82, 워터마크) → `action:'cover'`(정사각 1080 · 가로 1200×630 대표 썸네일) → `action:'finish'`(photos.json 앞에 추가) 순으로 보낸다.
   finish 만 실패하면 다음에 누를 때 그것부터 다시 보낸다(최근 커밋 「사진 목록 갱신 다시하기」).
4. `portfolio.html` 이 `https://raw.githubusercontent.com/brizymedia/j6media/photos/photos/photos.json?t=5분단위` 를 읽어 WORKS 앞에 붙인다.
   사진 주소는 `https://cdn.jsdelivr.net/gh/brizymedia/j6media@photos/<path>` — jsDelivr 캐시 때문에 늦게 보일 수 있다.
5. 같은 화면 아래에 블로그 제목 후보 · 본문 · 인스타 글(해시태그)이 만들어진다 — 대표가 복사해 네이버 블로그 · 인스타에 올린다.
   그 블로그 글 주소를 받으면 §2 처럼 `BLOG` 에 넣는다.

레포에서 할 일은 없다(main 에 커밋되지 않음). 사진 설명 오타는 upload.html 목록에서 고치기(`action:'edit'`) · 지우기(`action:'delete'`).

## 5. 행사 이야기 한 편 추가

1. `tools/make_pages.py` 의 `STORIES` 에 dict 하나 추가:
   `slug`(영문 파일명) · `title` · `cat`(교회행사/기업행사/지자체 행사/전시 · 공연/설치 …) · `date` · `place` · `area`(AREAS slug 또는 None) ·
   `lead`(한두 문장) · `facts`[(이름, 값)…] · `body`[문단…] · `photos`[works 번호, 첫 장이 표지] · `blog`(블로그 글 번호 또는 '') · `quote`[품목 id](현재 미사용).
2. **사실만** — 대표 블로그 원문 · 사이트 글 · 대표 확인분(파일 머리 주석의 규칙).
3. `python tools/make_pages.py` → `stories/` · `areas/`(지역 카드도 갱신) · `sitemap.xml` 다시 생성.
4. 필요하면 `llms.txt` 「하는 일」 줄에도 반영.

## 6. 지역 페이지 추가 · 수정

`AREAS` 에 `dict(slug, name, hall='○○시청', min=분, km=거리, done=['그 지역에서 한 일'…], photos=[번호 3개])`.
`hq=True` 는 사무실 지역(남양주) 하나뿐. 이동 시간은 별내 사무실 좌표(37.6524324, 127.1293090)→시청 · 군청, 막히지 않을 때, 5분 반올림.
`python tools/make_pages.py`. llms.txt 「운영 지역」 줄과 `port_docs.py` 의 `UPLOAD_REGIONS` · `UPLOAD_PAIRS`(지역 이름 목록)도 맞춰 둘 것.

## 7. 견적 → 계약 → 일정 → 명세서 (대표 업무 흐름)

`office.html` 의 흐름 7단계: 문의 메일 → 견적서 발행 · 저장 → 전자계약 서명 → 행사 일정 · 체크리스트 → 행사 진행 → 사진 올리기 · 블로그 글 → 거래명세서.

1. **견적**: `quote.html?admin=1`(대표 암호 잠금). 품목 체크 · 수량 · 일수 · 단가 · 할인 입력.
   - 「링크」: 주소 `quote.html#q=<코드>` — 코드는 `{i:정보, r:[id 또는 [id,수량]…], d:할인}` 를 base64url 한 것(`encodeState`). 푸는 규칙은 `quote-catalog.js 견적풀기()`.
   - 「손님에게 보내기」: 지메일 웹 / 메일 앱 / 일반 mailto 중 고름(폰 지메일 웹은 쓰기 창이 막혀 메일 앱으로).
   - 「견적서 저장함」: 이 기기 `j6-quote-box-v1` + (암호 연결 시) 계약 서버 `boxList/boxPut/boxDel` 로 폰 · PC 공유. 전화번호로도 찾기. 지우기는 두 번 눌러야.
2. **계약**: 「이 견적으로 계약서 작성」 → `contract.html?admin=1#c=<base64url 계약 JSON>`(`{v, no:'J6-YYYYMMDD-XXX', date, cl, ev, items, m:{disc}}`).
   계약 종류(행사 용역 / 출연) · 지급조건 · 취소규정(기본표 `CANCEL_DEF`) · 특약 확인 → 「고객 서명 링크 만들기」:
   서버 있으면 `action:'store'` → 짧은 링크 `contract.html?c=<ID>&s=<배포ID>`, 없으면 상태 전체를 담은 긴 링크.
   고객이 폰에서 서명 + 동의 2개 → `action:'sign'`(서명 PNG + 렌더된 HTML) → 서버가 PDF · 드라이브 저장 · 메일(회사 · 큰길브리지 · 고객) · 대장 기록.
   같은 링크를 다시 열면 「서명 완료」와 PDF 링크.
3. **일정**: 견적서 「일정으로」 → `schedule.html#new=<base64url>`(제목 · 날짜 · 장소 · 고객 · 담당 · 인원 · 비고 · 견적코드 · 품목→체크리스트).
   schedule 은 암호(대표 BOX_PW 또는 직원 CREW_PW) + 이름을 이 기기에 저장(`j6-sched-pw` `j6-sched-who`). 행사 화면 `#e=<id>`, 견적서 다시 열기는 `quote.html?admin=1#q=<견적코드>`.
   저장해 둔 견적서(저장함)에서 행사를 가져올 수도 있다.
4. **명세서**: 견적서 「이 견적으로 거래명세서 작성」 → `statement.html?admin=1#t=<base64url>`(`{v, no, issued, cl, ev, rows[{on,name,spec,qty,unit,days,price}], vat:'별도', paid, memo}`, 할인은 음수 줄).
   편집하면 주소 `#t=` 가 계속 갱신된다(그 주소가 곧 저장본). 계좌는 이 기기 `kg_stmt_bank` 에만 저장 — 레포에는 계좌를 적지 않는다.

## 8. 사장님 수정 요청 반영

```bash
# 메일로 온 경우: 메일 본문 전체를 수정.txt 로 저장 / 파일로 온 경우: 제이식스미디어-수정요청-….json
python tools/apply_edits.py 수정.txt
git diff                      # 바뀐 곳 확인. 「수동 확인」 줄은 손으로 고친다
pip install pillow            # 사진이 들어 있을 때 (없으면 원본 그대로 저장됨)
```

- 대상 페이지는 `PAGES` 7개뿐. 생성 · 업무 화면 수정 요청은 「반영 대상이 아닌 페이지」로 건너뛴다.
- 메일 본문 JSON 에는 사진 데이터가 없다(「수정 파일 참조」). 사진은 반드시 수정 파일(.json)로 받아야 한다.
- 반영 뒤 대표에게 문자로 알리는 것이 약속된 절차(edit.js 안내 문구).
- 새 열쇠를 줄 때: 열쇠 문자열의 SHA-256(소문자 hex 64자)을 7쪽 `<meta name="es-edit" content="…">` 에 모두 넣는다. 열쇠 원문은 레포 · 문서에 남기지 않는다.

## 9. 업무 화면 다시 옮기기 (큰길이벤트 원본이 바뀌었을 때)

```bash
python tools/port_docs.py ~/Documents/클로드코드     # 인자 = 큰길이벤트 레포 경로 (기본값과 같으면 생략)
git diff --stat
```

- 출력의 「남은 큰길 흔적」이 `없음` 이어야 한다(`TRACES`: 큰길 · 김동길 · 광양 · 브리지미디어 · 계좌 일부 · keungil · KG · 녹동 · 고흥 · 전남 · 드론).
- 손으로 고친 것은 다음 이식 때 사라진다. 바꿀 것은 `port_docs.py` 의 「회사 설정」(문구 · 색 · 예시 · CATALOG · 사진 칸 · 지역표 · 메뉴) 또는 `*_extra()` 함수에 규칙으로 넣는다.
- 서버 코드(`apps-script/*/Code.gs`)도 같이 다시 써진다 → 바뀌었으면 Apps Script 편집기에 붙여 넣고 **새 버전으로 재배포**.
- `office.html` 은 `office()` 가 통째로 다시 만들고 `admin_gate.apply()` 가 잠금을 씌운다.

## 10. 히어로 영상 · og 이미지 교체

SKILL.md §11 의 규격대로 만들고 같은 파일 이름으로 덮어쓴다(`hero.mp4 hero_sm.mp4 hero_sm.webm hero_poster.webp`).
사진 목록을 `assets/img/SOURCES.md` 「히어로 영상」 칸에 적는다. og.jpg 는 1200×630, 바꾸면 같은 칸에 기록.
캐시 때문에 바로 안 바뀌어 보이면 `index.html` 의 `data-src` 뒤에 `?v=날짜` 를 붙이는 방법이 있다(현재는 꼬리표 없음).

## 11. 새 서브 페이지 만들기

notice.html 을 복사 → title · description · canonical · og · BreadcrumbList · phead · main 교체 → 대문 + 서브 6쪽(+ 새 페이지) 메뉴 · 시트 · 바닥 `.ftl` 에 링크 →
`make_pages.py` 의 `sitemap()` `pages` 목록에 추가 후 실행 → `apply_edits.py` `PAGES` 에 추가(수정 모드 쓰려면 es-edit 메타 + edit.js 포함) → llms.txt 「주요 페이지」.

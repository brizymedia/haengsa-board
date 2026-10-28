# 업무 화면 흐름과 상태 저장

업무 화면 7개는 큰길이벤트 원본을 `tools/port_docs.py` 로 치환해 옮긴 **생성물**이다(2026-10-03, README).
고칠 때는 `port_docs.py` 「회사 설정」을 고치고 `python tools/port_docs.py <큰길이벤트 레포 경로>` 로 다시 만든다.
port_docs.py 는 끝에 남은 큰길 흔적(`큰길 · 김동길 · 광양 · 브리지미디어 · 788101 · xn--wk0 · keungil · KG<`)을 파일마다 출력한다.

## 전체 흐름 (office.html 의 7단계)

```
① 문의 메일 알림(대문 폼 · 견적 문의 → 공용 문의 서버 → 대표 메일 + 큰길브리지)
② quote.html?admin=1  견적서 발행 · 저장함
③ contract.html?admin=1 → 서명 링크 → 고객 폰 서명 → PDF 메일
④ schedule.html  행사 일정 · 체크리스트(직원 공유)
⑤ 행사 진행
⑥ upload.html  사진 올리기 + 블로그 · 인스타 글
⑦ statement.html?admin=1  거래명세서
```

## 화면 사이 데이터 넘기기 (서버 없이 주소로)

모두 `btoa(unescape(encodeURIComponent(JSON)))` 를 base64url(`+`→`-`, `/`→`_`, `=` 제거)로 바꾼 코드.

| 출발 → 도착 | 주소 | 담기는 것 |
|---|---|---|
| 견적 상태 | `quote.html#q=…` (또는 `?q=`) | `{ i: 고객정보 9칸 배열, r: 줄[], d: 할인 }` — 줄은 품목 id 문자열 / `[id,qty,days,price]` / 완전형 7칸 |
| 견적 → 계약 | `contract.html?admin=1#c=…` | 계약 전체 상태(항목명 · 규격까지 완전형) |
| 견적 → 명세서 | `statement.html?admin=1#t=…` | 명세서 상태 |
| 견적 → 일정 | `schedule.html#new=…` | 새 행사(품목이 체크리스트가 됨) |
| 일정 한 건 | `schedule.html#e=<id>` | 서버 행사 id |
| 계약 짧은 링크 | `contract.html?c=<ID>&s=<배포ID>` | 서버가 발급한 ID, `s` 는 Apps Script 배포 ID(고객 기기에서 서버를 찾게) |
| 계약 긴 링크(서버 없을 때) | `contract.html?s=<배포ID>#c=…` | |
| 계약 미리보기 | `contract.html?preview=1#c=…` | 서명 저장 안 됨 |

견적 코드 풀이 규칙은 `quote-catalog.js` 의 `견적풀기()` 한 곳(quote · schedule 공용). 고객정보 칸 순서 `org name tel email title date place people memo`(짧은 키 `o n t e m d p c x`).

## quote.html — 자동 견적서

- **손님 화면**(`admin` 없음): 고객정보 입력 → 카탈로그 체크(수량) → 견적서 미리보기 → 「보내기」. 금액 · 할인 · 직인 · 표 수정 안내를 숨긴다(`손님가리기()`). 카탈로그가 전부 `price:null` 이라 금액은 「협의」.
  - 보내기: 공용 문의 서버(`문의서버`)로 POST(`service:'[HD기획] 자동 견적서 문의'`) → 실패하면 FormSubmit(`formsubmit.co/ajax/<수신 메일>`) → 그래도 실패하면 `mailto:` 열기 제안.
  - ⚠ 이 수신 메일(`견적_수신_이메일`)은 큰길브리지 관리 계정으로 되어 있다. HD기획 메일로 받아야 하는지 확인 필요.
- **관리자 화면** `?admin=1`(admin-lock.js 잠금): 단가 입력 · 할인 · 부가세 10% · 합계, 행 추가, 인쇄, 링크 복사, **고객에게 보내기**(서식 있는 견적 HTML 을 클립보드에 → 지메일 웹/메일 앱 열기, 폰은 메일 앱), 계약서 작성 · 거래명세서 작성 · 행사 일정 등록 단추, 붙여넣은 링크/코드에서 견적 불러오기(`#admin-paste`).
- **견적서 저장함**: localStorage `hd-quote-box-v1`(최대 50개, 코드 · 제목 · 고객 · 전화 · 금액). 「연결하기」에 보관함 암호를 넣으면 계약 서버 `boxList`(올릴 목록 합치기) · `boxPut` · `boxDel` 로 폰 · PC 가 같은 목록(서버 최대 100). 암호는 `hd-quote-box-pw`. 지우기는 두 번 눌러야 함. 전화번호는 기호를 지우고 찾는다.
- 견적 유효기간 표기 「발행일로부터 30일」.

## contract.html — 전자계약서

- 종류 2개: `service`(용역, 우리=을) · `cast`(출연, 우리=갑, 개인 출연이면 원천세 3.3% 계산).
- 모드: `admin`(작성) · `customer`(서명) · `signed`(서명 완료) · `preview`.
- 관리자: 갑 정보 · 행사 · 품목 · 지급조건(계약금 %) · 부가세 별도/포함 · 취소 규정 표(`CANCEL_DEF` 종류별 기본값) · 특약 → 「고객 서명 링크 만들기」 = 서버 `store` → 짧은 링크, 실패하면 긴 링크. 문자 · 메일 · 복사 · 공유.
- 회사 기본값은 localStorage `kg_contract_co`(이름이 큰길 접두사 그대로).
- 고객: 계약서 확인 → 성명 · 연락처 · 이메일 · 서명 패드(canvas, DPR 3까지) · 동의 2개 → 서버 `sign`(문서 SHA-256 해시 · 서명 PNG · PDF용 HTML) → 서버가 PDF 생성 · 드라이브 저장 · 회사 + 고객 + 관리자 메일 · 대장 기록. 서버가 없으면 공용 문의 서버로 서명 정보만 보내고 고객에게 PDF 저장 안내.
- 직인: `assets/img/stamp-hd.png` 가 있으면 찍고, 없으면 「(인)」(가짜 도장은 그리지 않음).
- 계약 번호 `HD-YYYYMMDD-XXX`.
- 서버 폴백 메일(`회사_수신_이메일`)도 큰길브리지 관리 계정 — 확인 필요.

## statement.html — 거래명세서

- `?admin=1` 잠금. 견적서 「이 견적으로 거래명세서 작성」으로 `#t=` 가 넘어온다. 손으로도 작성.
- 공급자(`우리`): HD기획 · 엄원식 · 사업자번호 빈칸 · 주소 · 전화 · 이메일. 기본 계좌 `''`(비움). 입력한 계좌는 localStorage `kg_stmt_bank`.
- 번호 `HD-YYYYMMDD-XXX`, 부가세 별도/포함, 받은 돈(`paid`), 인쇄(`window.print()`) · PDF · 손님용 주소(admin 제거). 상태는 `#t=` 로 주소에 계속 저장.

## schedule.html — 행사 일정 · 체크리스트

- 계약 서버의 `_data/행사일정.json` 하나를 대표와 직원이 같이 본다(최대 300건).
- 암호: 직원 암호 `CREW_PW` 또는 대표 암호 `BOX_PW` 둘 다 일정은 열림(서버 `crewCheck_`). 기기 저장 `hd-sched-pw`, 이름(누가 체크했는지)도 기기에 저장.
- 서버 액션: `schedList` · `schedSave`(품목을 안 건드렸으면 빼고 보내 직원 체크를 덮어쓰지 않음) · `schedCheck`(그 항목만) · `schedDel`.
- 월간 일정표 + 행사별 체크리스트. 견적서에서 `#new=` 로 넘어오면 품목이 체크 항목이 된다. 저장해 둔 견적서에서 가져오기는 보관함 암호(`boxList`)가 있어야 함.

## upload.html — 사진 올리기 + 글

단계: 「처음 한 번만 설정」(서버 주소, 지금은 `서버주소_기본` 에 박혀 있음) → 01 행사 정보 → 02 사진 고르기 → 03 올리기 → 04 블로그 · 인스타 글 자동 작성 → 05 올린 행사 고치기 · 지우기.
- 사진은 브라우저에서 긴 변 1600px · JPEG 0.82 로 줄임(워터마크 체크박스 선택). 대표 썸네일은 정사각 · 가로 두 장(0.88).
- 서버 액션: `photo`(한 장씩) · `cover` · `finish`(photos.json 갱신) · `edit` · `delete`. 비밀번호 `UPLOAD_PW`, 기기 저장은 「암호 저장」 체크 시 `hd_pw`. 그 밖의 기기 저장 `hd_srv` · `hd_cat` · `hd_ev`.
- 사진 칸(slug): `corp` 기업행사 · 송년회 / `sport` 체육대회 · 워크숍 / `gov` 지자체 · 관공서 · 학교 / `fest` 축제 · 놀이존 · 물놀이 / `cer` 기공식 · 의전 · 개관식 — **portfolio.html 필터 `data-f` 와 같아야 한다.**
- 지역 찾기 표(행사명 · 장소 글자 → 금천 · 구로 · 영등포 · 관악 · 동작 · 강남 · 송파 · 마포 · 광명 · 남양주 · 안양 · 부천 · 인천 · 서울).
- 04 단계: 블로그 제목 후보 · 본문 · 서명 블록 · 인스타 문구 · 해시태그(블로그 15개 · 인스타 30개) 자동 생성, 「사진과 함께 공유」 = 폰 공유창. **사이트 `/blog/` 와는 별개**(네이버 블로그 · 인스타용 문구).
- 올린 사진은 `portfolio.html` 이 `https://raw.githubusercontent.com/brizymedia/hd-event/photos/photos/photos.json` 을 5분 단위 캐시 깨기로 읽고, 이미지는 `https://cdn.jsdelivr.net/gh/brizymedia/hd-event@photos/<path>` 로 보여 준다(1~2분 지연).

## office.html — 대표 전용 문서함

- `noindex,nofollow`, robots.txt Disallow, 공개 링크 없음(푸터 「관리자 모드」로만).
- 카드 3묶음: 견적 · 계약(견적서 발행 · 손님용 견적서 · 전자계약서 · 거래명세서) / 행사 준비(일정 · 사진 올리기) / 홈페이지 · 검색(행사 이야기 · 지역 페이지 · llms.txt · 사이트맵 · 유입 현황 ai-make.co.kr/stats/).
- 서버 연결 상태: 계약 서버 GET → `box: ready/no-pw`, `sched: ready/no-pw` 표시. 갤러리 서버 GET → `설정완료`.
- 암호 안내(값은 어디에도 없음), 「홈페이지 글 · 사진 고치기 `?edit=열쇠`」 안내(처리 코드는 이 레포에 없음 — 확인 필요).
- 잠금: `tools/admin_gate.py` 가 씌운 `#gate`. 대표 암호만(`boxList`), 맞으면 `hd-quote-box-pw` 저장(+ 일정 암호 없으면 같이), `sessionStorage hd-office`.

## admin-lock.js

```html
<script src="admin-lock.js" data-server='<계약 서버 /exec>' data-key='hd-quote-box-pw' data-name='HD기획'></script>
```
`<head>` 에 넣는다. `?admin=1` 이고 서버 주소가 있을 때만 잠근다(손님 화면 · 서명 링크는 열림). 화면 전체를 덮는 암호 창 → `{action:'boxList', pw}` ok 면 해제, 기기에 저장, 다음부터는 조용히 확인.
쓰는 곳: quote.html · contract.html · statement.html.

# 업무 화면 · 공지 관리자 · 사장님 수정 모드

## 1. 업무 화면 (port_docs.py 이식물)

quote · quote-catalog.js · contract · statement · schedule · upload · admin-lock.js 는 큰길이벤트기획 원본을 `tools/port_docs.py` 가 문자열 치환으로 옮긴 결과다.
`office.html` 은 port_docs 의 `office()` 가 새로 만들고 `admin_gate.apply()` 가 잠금 화면을 씌운다. **결과 파일을 손으로 고치지 말고** port_docs 「회사 설정」/치환 규칙을 고친 뒤
`python tools/port_docs.py <큰길이벤트 레포 경로>` 로 다시 만든다(원본 레포가 없으면 다시 만들 수 없다). 실행 끝에 파일마다 「남은 큰길 흔적」을 출력한다.

### office.html 의 7단계 흐름
```
① 문의 메일 알림 → ② quote.html?admin=1 견적서 발행 · 저장 → ③ contract.html?admin=1 전자계약 서명
→ ④ schedule.html 행사 일정 · 체크리스트 → ⑤ 행사 진행 → ⑥ upload.html 사진 올리기 · 블로그 글 → ⑦ statement.html?admin=1 거래명세서
```
office 카드 묶음: 견적 · 계약(견적서 발행 · 손님용 자동 견적서 · 전자계약서 · 거래명세서) / 행사 준비(일정 · 사진 올리기) / 홈페이지 · 검색(공지사항 관리 · 포트폴리오 · llms.txt · sitemap · 유입 현황 ai-make.co.kr/stats/).
「서버 연결 상태」 칸: 계약 서버 GET(`box`·`sched` 가 `ready` 인지) · 갤러리 서버 GET. 주소가 비면 「아직 연결 전 — 서버 배포 대기」.
「암호 안내」: 보관함 암호(대표) · 직원 암호(일정만) · 사진 올리기 암호 — 어디에도 적혀 있지 않음.

### 화면 사이 데이터 (주소 해시)
| 주소 | 내용 |
|---|---|
| `quote.html#q=…` | 견적 상태 코드(풀이는 `quote-catalog.js 견적풀기()` — quote · schedule · statement 공용) |
| `contract.html?admin=1#c=…` | 견적 → 계약 |
| `statement.html?admin=1#t=…` | 견적 → 거래명세서 |
| `schedule.html#new=…` / `#e=<id>` | 견적 → 새 행사 / 행사 한 건 |
| `contract.html?c=<ID>&s=<배포ID>` | 서버가 발급한 짧은 서명 링크(서버 있을 때) · `?preview=1#c=` 미리보기 |

번호 앞글자 `EE-`(견적 · 계약 · 명세서 `EE-YYYYMMDD-XXX`).

### quote.html
- 손님 화면: 고객 정보 → 카탈로그(35품목, 7묶음: 행사 진행 8 · 공연 3 · 체험 · 놀이 4 · 교육 프로그램 6 · 음향 · 조명 · 장비 8 · MC · 섭외 3 · 기타 3) 체크 → 보내기. **모든 품목 `price:null`** — 금액 · 직인 숨김(`손님가리기()`).
- 보내기: 공용 문의 서버(`service:'[이벤트와 교육연구소] 자동 견적서 문의'`) → 실패 시 FormSubmit(`견적_수신_이메일` = 큰길브리지 관리 계정) → mailto.
- `?admin=1`: 금액 입력 · 저장함(계약 서버 `boxList/boxPut/boxDel`, 기기 `edu-quote-box-pw` · `edu-quote-box-v1`) · 계약 · 명세서 · 일정으로 넘기기. admin-lock.js 가 잠금(서버 주소가 비면 잠그지 않음 — **현재 상태**).
- 견적 품목을 바꾸려면 `port_docs.py CATALOG`(id 를 바꾸면 기존 견적 코드가 안 풀림).
- 메뉴에 큰길 원본의 「행사 이야기」(`stories/`) 링크가 남아 있다(이 사이트엔 없음), 바닥글 관리자 링크는 `/office.html` 절대 경로.

### contract.html
- `?admin=1`: 작성 → 서버 `store`(짧은 ID) → 서명 링크. 서버가 없으면 긴 링크(`#c=`).
- 고객: 링크 열기 → 서명 → `sign` → 서버가 PDF 만들어 드라이브 저장 · 메일(`COMPANY_EMAIL` 대표 메일 + `MANAGER_EMAIL` 큰길 + 고객).
- 직인 `assets/img/stamp-edu.png`(없음 → 「(인)」, 콘솔 404). FormSubmit 폴백 `회사_수신_이메일` 도 큰길 관리 계정.
- 기기 저장 키 `kg_contract_co`(큰길 이름 그대로).

### statement.html
견적에서 넘어오거나 직접 작성 → 인쇄 · PDF. 공급자 칸 직인(없으면 이미지 제거). 기기 키 `kg_stmt_bank`. 계좌 기본값은 비움.

### schedule.html
월간 일정표 + 행사별 체크리스트. 계약 서버 `schedList/schedSave/schedCheck/schedDel`. 대표 암호(BOX_PW) 또는 직원 암호(CREW_PW, 일정만). 기기 `edu-sched-pw` · `edu-sched-who`. 품목 하나만 체크하는 `schedCheck` 로 서로 덮어쓰지 않게 함.

### upload.html (사진 올리기)
- 업로드 비밀번호(UPLOAD_PW, 기기 `edu_pw` 선택 저장) → 분류 6개(kinder · school · corp · local · church · edu, `port_docs UPLOAD_CATS`) · 행사명 · 날짜 · 장소 · 설명 → 사진을 **긴 변 1600px JPEG(품질 .82)** 로 줄이고 오른쪽 위 「이벤트와 교육연구소」 워터마크(선택) → 갤러리 서버 `photo` × n → `finish`(photos.json 갱신). 원본은 폰에만.
- 블로그 · 인스타 글 초안과 정사각 대표 이미지를 만들어 줌(지역표 = 인천 구 · 부천 · 김포 · 서울 · 경기 등, `UPLOAD_REGIONS`).
- 갤러리 서버 주소 `서버주소_기본`(= GALLERY_URL)이 현재 빈칸.
- 포트폴리오는 app.js 가 photos.json 을 읽어 붙인다(5분 캐시 꼬리표).

## 2. 공지 관리자 (notice-admin.html — build_site 생성)

```
대표님 → notice-admin.html → 비밀번호(= UPLOAD_PW) → sessionStorage edu-notice-pw
  → 갤러리 서버 {action:'notice-list'|'notice-save'|'notice-delete', pw, …}
  → photos 가지 photos/notices.json  {updated, notices:[{id,d,t,b,n}]}  (최대 80개, 제목 120자 · 내용 1500자, < > 제거)
홈페이지(index · notice) ← app.js 가 raw.githubusercontent …/photos/photos/notices.json 을 2분 캐시 꼬리표로 읽음
  → 서버 공지 + 정적 공지(data-static = assets/data/notices.json) 순으로 다시 그림
```
- 서버 주소는 build_site 가 `tools/port_docs.py` 의 `GALLERY_URL = '…'` 줄을 정규식으로 읽어 페이지 스크립트에 넣는다 → **주소를 넣으면 build_site 를 다시 돌려야** 이 화면이 열린다. 빈칸이면 「아직 공지 서버가 연결되지 않았습니다 … 큰길브리지(1533-7295)에 공지 내용을 알려 주세요」.
- 날짜 기본값은 오늘(`YYYY.MM.DD`), NEW 표시 선택, 목록에서 수정 · 삭제(confirm).
- 「몇 분 안에」 반영 = raw.githubusercontent 캐시 + 2분 꼬리표 때문.
- 정적 공지와 서버 공지가 겹치면 두 번 보인다. 서버 연결 후 `notices.json` 을 비우거나 정리하고 build_site.
- 서버 연결 전 공지 수정: `assets/data/notices.json`(`{d, t, n?, b?}`) → build_site → build-blog.

## 3. 사장님 수정 모드 (assets/edit.js + tools/apply_edits.py)

계약 항목 「직접 수정 가능한 CMS 세팅 + 교육」(README: es-company 방식).

### 켜기
- 모든 공개 페이지(notice-admin · 404 제외)의 `<meta name="edu-edit" content="<sha256>">` (= `build_site.py EDIT_HASH`).
- 주소 `?edit=열쇠` → `sessionStorage edu-edit-key` 에 보관 → sha256(열쇠) 가 메타와 같을 때만 편집 모드. 틀리면 아무 일도 없다. `?edit=off` 로 끝. 열쇠는 문자로 따로 전달(레포 · 문서에 없음).
- 열쇠 바꾸기: 새 열쇠의 sha256(소문자 hex 64자)을 `EDIT_HASH` 에 → build_site → build-blog → 배포.

### 편집
- 글: `h1~h4, p, li, b, small, span, a, label, summary, dt, dd, address, figcaption, em, time, i, td, th` 중 안쪽이 글자(+인라인 태그)뿐인 「잎」 요소를 `contenteditable`. 갤러리 · 포트폴리오 · 필터 · 공지 목록 · 숫자 · 띠 · 색종이 · 폼 · 실적 학교 등은 제외(`SKIP`). Enter = 줄바꿈, 붙여넣기는 글자만. 편집 중 본문 링크 이동 막음.
- 사진: `main` 안 `img`(또는 배경 이미지) 클릭 → 파일 고르기 → 긴 변 1920px JPEG(.86) dataURL.
- 기기 IndexedDB `edu-edit`(페이지별 `{texts, images}`)에 자동 보관 → 다른 페이지로 옮겨 다녀도 유지. 「이 페이지 되돌리기」.
- 각 글 변경은 `{sel: CSS 경로, old: 원래 innerHTML, new, occ: 같은 원문 중 몇 번째}`.

### 보내기
- 「수정 내용 보내기」 → 보내는 분 · 연락처(필수) · 남길 말 → 공용 문의 서버로 글 수정 요약 + `[JSON — tools/apply_edits.py 에 그대로 넣으면 반영됩니다]` 블록(사진 데이터는 빼고) 메일.
- 사진이 있으면 `이벤트와 교육연구소-수정요청-YYYYMMDDHHMM.json`(`{v:1, site:'edu-event', at, who, tel, memo, pages:{페이지:{texts:[…], images:[{src,data}]}}}`)을 폰 공유창 / 다운로드 → 카톡 · 메일로 큰길브리지에.
- ⚠ 「보내는 분」 기본값이 다른 사람 이름으로 들어 있다(`#es-who`)(다른 고객 사이트 흔적으로 보임 — 확인 필요). office.html 은 「저장 파일 받기」라고 안내하지만 실제 단추 이름은 「수정 파일만 저장」.

### 반영 (큰길브리지)
```bash
python tools/apply_edits.py 수정파일.json        # 또는 메일 본문을 저장한 .txt (JSON 블록 {"v":1 … 을 찾아냄)
git diff                                         # 확인
```
- 대상 페이지 8개(index · about · ceo · event · education · portfolio · contact · notice). 원문을 그대로 찾고, 없으면 공백 차이 무시 정규식으로, 그래도 없으면 「수동 확인」 목록.
- 새 글 안의 `<script|style|iframe>` 은 지움. 사진은 `assets/img/` 아래 · `..` 없는 경로만, PIL 로 1920px 이하 · 원래 확장자(webp q82 / jpg q86 / png)로 덮어씀(PIL 없으면 원본 그대로 저장).
- ⚠ 반영 후 **build_site.py 를 그냥 돌리면 반영분이 사라진다** → SKILL.md 7장 순서대로 build_site.py 에도 옮길 것.
- ⚠ HTML 을 `newline` 지정 없이 다시 쓴다 → Windows 에서 CRLF 로 바뀔 수 있음.

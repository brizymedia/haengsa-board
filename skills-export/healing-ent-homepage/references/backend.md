# Apps Script 백엔드

세 서버 모두 Google Apps Script 웹 앱. 브라우저는 `fetch(주소, {method:'POST', headers:{'Content-Type':'text/plain;charset=utf-8'}, body: JSON.stringify({...})})`
(text/plain 이라 CORS 사전요청이 없다) 로 부르고, 응답 `{ok:true, …}` 일 때만 성공으로 친다.
이 문서에는 **주소만** 적는다. 암호 · 토큰은 각 프로젝트의 「⚙ 프로젝트 설정 → 스크립트 속성」에만 있다.

## 배포 규칙 (세 서버 공통)
- 배포 → 새 배포 → 유형 **웹 앱** → 실행: **나** → 액세스: **모든 사용자**(고객 폰에서 열어야 하므로).
- 코드를 고친 뒤: **배포 → 배포 관리 → 연필 → 버전: 새 버전 → 배포.** 저장만 하면 반영 안 됨. 「새 배포」를 만들면 주소가 바뀐다 → 쓰는 곳을 전부 고쳐야 한다.
- 권한 승인: 「고급 → 안전하지 않은 페이지로 이동 → 허용」.
- 계약 서버 `VERSION` 상수(지금 `2026-10-02b`)를 고칠 때마다 올린다 → GET 응답으로 배포 확인.

## 1. 공용 문의 서버 (큰길브리지 소유)
- 주소: `https://script.google.com/macros/s/AKfycbwvQ4UJRZklRX7bZB6C0s1yZgSvBAMCVccT580L_1BtiVDyh0DIxShCAvN9McZIB0b7FA/exec`
- 코드는 **이 레포에 없다**(확인 필요: 큰길브리지 쪽 저장소). app.js 주석: 서버가 `page` 주소의 레포 이름(healing-ent)으로 회사를 알아보고 leehh2153@gmail.com + 큰길브리지로 메일.
- 쓰는 곳: `assets/app.js FORM_ENDPOINT`(필드 name · tel/phone · type · date · region · people · msg · message · service `[힐링엔터테인먼트] … 문의` · at · page · website(스팸 함정 빈 값)),
  `quote.html 문의서버`(name · phone · email · service · message · at · page · website), `assets/edit.js SEND_ENDPOINT`(사장님 수정 메일, 사진은 빼고 보냄).
- 2026-09-30 FormSubmit 이 CORS 응답을 끊어 견적 문의가 막힌 뒤 이 서버를 먼저 쓰게 됐다(quote.html 주석).

## 2. 계약 서버 `apps-script/contract/Code.gs` (457줄, service `healing-contract`)
- 주소: `https://script.google.com/macros/s/AKfycbwm8qkj9FgIwX3NOJiLdkTwJp8F8ncf1UwRqn-XJMg2HYXIOYBuZjleIiUt_J2DvL1O/exec` (port_docs 주석: 2026-10-03 배포, gilauto325 계정)
- 상수: `ROOT_FOLDER_NAME '힐링엔터테인먼트 계약서'` · `SHEET_NAME '계약 대장'` · `COMPANY_EMAIL leehh2153@gmail.com` · `MANAGER_EMAIL gilauto325@gmail.com`(큰길브리지 사본, 빼려면 '') ·
  `ALLOW_RESIGN false` · `BOX_FILE '견적서-보관함.json'` · `BOX_MAX 100` · `SCHED_FILE '행사일정.json'` · `SCHED_MAX 300`.
- 스크립트 속성: `BOX_PW`(대표 — 견적 저장함 · 관리자 화면 · 문서함 · 일정), `CREW_PW`(직원 — 일정만).
- `doGet`: `?id=` 면 계약 읽기, 아니면 `{ok, service, version, box:'ready'|'no-pw', sched:'ready'|'no-pw', time}` (office.html 상태 표시가 이걸 본다).
- `doPost` action (LockService 20초):

| action | 하는 일 | 암호 |
|---|---|---|
| `ping` | 살아 있나 | — |
| `store` | 계약 저장 → ID 발급 (`_data/ID.json`) | — |
| `sign` | 고객 서명 → PDF(도장 + 서명) · 드라이브 `연도/` · 메일(회사 · 매니저 · 고객) · 대장 기록 | — |
| `boxList` · `boxPut` · `boxDel` | 견적 저장함 목록 | BOX_PW (admin-lock · office 가 `boxList` 로 암호 확인) |
| `schedList` · `schedSave` · `schedCheck` · `schedDel` | 행사 일정 · 체크리스트 | CREW_PW 또는 BOX_PW |

- 데이터: 드라이브 `힐링엔터테인먼트 계약서/_data/`(ID.json — 지우면 링크가 깨짐, 견적서-보관함.json, 행사일정.json), `연도/계약서_….pdf` · `서명_….png`, 스프레드시트 「계약 대장」.
- 한도: Gmail 무료 하루 100통. PDF 가 안 만들어지면 도장 이미지 크기를 줄인다(README 문제 해결 표).

## 3. 갤러리 서버 `apps-script/gallery/Code.gs` (421줄)
- 주소: `https://script.google.com/macros/s/AKfycbw5HFoNVKAbu8xUcPGE6BUjHIM98vgc_cCGe98PlTZpfL4_c8oWktLuOsKcm0ggerTVLw/exec`
- 스크립트 속성: `UPLOAD_PW` · `GITHUB_TOKEN`(fine-grained, `brizymedia/healing-ent` 만, Contents Read and write) · `GITHUB_REPO = brizymedia/healing-ent`.
- 편집기에서 한 번 실행: `권한받기`(UrlFetch 권한) → `점검`(속성 3개 · photos 브랜치 연결 로그). 드라이브 · 메일 권한은 쓰지 않는다.
- 상수: 브랜치 `photos`, 폴더 `photos`, 목록 `photos/photos.json`.
- `doPost` action: `photo`(사진 1장 → `photos/<분류>/<eventId>-NNN.jpg`) · `cover`(정사각 · 가로 썸네일) · `finish`(목록 갱신) · `edit`(행사 정보 수정) · `delete`(사진 삭제). 뒤 셋은 잠금 안에서.
- `갤러리다시만들기()`: GitHub `repository_dispatch` `photos-updated` 를 보낸다. 이걸 받는 워크플로는 **이 레포에 없다**(확인 필요). 갤러리는 photos.json 을 직접 읽으므로 없어도 보인다.
- 문제 해결: 401 토큰 틀림/만료 · 403 권한 없음 · 404 레포 오타 · 「다른 업로드가 처리 중」 = 두 기기 동시 업로드.

## 4. 서버 주소를 바꿀 때 고칠 곳
- 계약 서버: `tools/port_docs.py CONTRACT_URL` → `python3 tools/port_docs.py <원본>` 다시 실행(quote · contract · schedule · admin-lock data-server · office 가 따라감).
  원본 레포가 없으면 손으로: quote.html(`보관서버`, admin-lock 태그) · contract.html(`서버주소_기본`, admin-lock 태그) · statement.html(admin-lock 태그) · schedule.html(`서버`) · office.html(`서버`, `C`).
- 갤러리 서버: `GALLERY_URL` → 같은 방법(upload.html `서버주소_기본` · office.html `G`). 기기에 저장된 `healing_srv` 는 기본값보다 뒤에 읽힌다(기본값이 있으면 기본값 우선).
- 문의 서버: `assets/app.js FORM_ENDPOINT` · `assets/edit.js SEND_ENDPOINT` · `quote.html 문의서버`.

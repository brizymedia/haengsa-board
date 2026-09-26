/* 행사ON 홈페이지 — 공통 스크립트 (외부 라이브러리 없음)
   ─────────────────────────────────────────────────────────────
   글 목록은 이 파일 맨 위 배열만 고치면 된다.
     NOTICES  공지사항 (notice.html 「공지」 탭 · 대문 공지)
     FILES    자료실  (notice.html 「자료실」 탭)
     BLOG     블로그 글 목록 (notice.html 「블로그」 탭 · 대문 · 행사 사진)
     WORKS    행사 사진 (대문 갤러리 · portfolio.html)
   ───────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  /* ---------- 문의 폼 전송처 · 연락처 ----------
     FORM_ENDPOINT 가 비어 있으면: 휴대폰은 문자 앱이 열리고(받는 번호 SMS_TO),
     PC 는 문의 내용을 복사해 주고 전화 · 문자를 안내한다.
     문의 서버(Apps Script) 주소를 넣으면 그쪽으로 JSON 이 간다(서버가 이메일로 전달). */
  var FORM_ENDPOINT = '';
  var SMS_TO = '010-9441-5542';
  var TEL = '1800-7947';
  var COMPANY = '행사ON';
  /* 카카오톡 채널 주소 (예: https://pf.kakao.com/_xxxxx). 넣으면 폰 하단 · 문의 페이지에 카톡 단추가 생긴다. */
  var KAKAO_URL = '';

  /* ---------- 공지사항 (새 글은 맨 앞에. pin: 위에 고정, n: NEW 표시) ---------- */
  var NOTICES = [
    { d: '2026.09.26', t: '행사ON 새 홈페이지를 준비하고 있습니다', n: true, pin: true,
      b: '스타컴퍼니가 행사ON 으로 이름을 바꾸면서 홈페이지도 새로 만들고 있습니다.\n하는 일 · 품목 · 행사 사진 · 블로그 글을 한곳에서 보실 수 있습니다.\n문의는 대표전화 1800-7947 (24시) 또는 「예약 · 문의」 페이지로 남겨 주세요.' },
    { d: '2026.09.26', t: '스타컴퍼니 → 「행사ON」 브랜드 리뉴얼 안내', n: true,
      b: '법인명 스타컴퍼니소상공인협동조합은 그대로이고, 브랜드 이름만 「행사ON」 으로 바꾸었습니다.\n블로그 · 유튜브에 남아 있는 「스타컴퍼니」 도 같은 회사입니다.\n행사가 필요한 순간 ON, 행사ON 으로 찾아 주세요.' },
    { d: '2026.09.26', t: '가을 학교축제 · 학예발표회 · 체육대회 음향 · 조명 상담 안내',
      b: '가을은 학교 축제 · 학예발표회 · 체육대회가 몰리는 시기입니다.\n행사 날짜가 정해지면 먼저 연락 주세요. 체육관 · 강당 · 운동장 조건에 맞춰 음향 · 조명 · 무대 구성을 제안드립니다.' },
    { d: '2026.09.26', t: '대표전화 1800-7947 · 24시 상담',
      b: '대표전화 1800-7947 은 24시간 상담합니다.\n문자는 010-9441-5542 로 보내 주세요. 행사 날짜 · 장소 · 인원을 적어 주시면 더 빨리 안내드립니다.' }
  ];

  /* ---------- 자료실 (파일이 준비되면 href 에 파일 경로를 넣는다. 비어 있으면 「요청하기」) ---------- */
  var FILES = [
    { t: '온라인 견적 요청서', s: '가격표에서 품목을 골라 바로 요청서를 만들 수 있습니다.', k: 'WEB', href: 'price.html', btn: '작성하기' },
    { t: '사업자등록증 사본', s: '학교 · 기관 계약 서류용. 요청하시면 보내 드립니다.', k: 'PDF', href: '', btn: '요청하기' },
    { t: '사회적기업 인증서 사본', s: '요청하시면 보내 드립니다.', k: 'PDF', href: '', btn: '요청하기' },
    { t: '회사 소개 · 행사 구성 안내', s: '준비 중입니다. 필요하시면 요청해 주세요.', k: 'PDF', href: '', btn: '요청하기' }
  ];

  /* ---------- 행사 사진 (assets/img/p 원본 · assets/img/t 썸네일) ----------
     c: school 학교행사 · sports 체육대회 · apt 아파트 · water 물놀이·에어바운스 · system 무대·음향·조명 · rental 천막·렌탈 · corp 기업·기관 */
  var WORKS = [
    { f: 'stage-jw-0', t: '대형 LED 와 조명으로 만든 공연 무대', o: '토탈 시스템 · 중원대학교 박물관 행사', c: 'system corp', u: 'https://blog.naver.com/hoon0170800/224419910650' },
    { f: 'school-yh-2', t: '학교 체육관 동아리 발표회 무대 조명', o: '학교축제 · 아산 온양용화고', c: 'school system', u: 'https://blog.naver.com/hoon0170800/224418933345' },
    { f: 'apt-lh-1', t: '아파트 추석 주민행사 공연 무대 · 음향', o: '아파트 · 아산 배방 LH15단지', c: 'apt system', u: 'https://blog.naver.com/hoon0170800/224416024254' },
    { f: 'water-apt-5', t: '워터슬라이드와 대형 에어풀장', o: '아파트 물놀이행사', c: 'water apt', u: 'https://blog.naver.com/hoon0170800/224317748152' },
    { f: 'tent-incheon-3', t: '운동장 가장자리를 따라 이어진 캐노피 천막', o: '체육대회 · 인천 서구 체육회', c: 'rental sports', u: 'https://blog.naver.com/hoon0170800/224418956512' },
    { f: 'stage-jw-6', t: '외줄트러스 · LED · 조명 · 음향 설치', o: '토탈 시스템 · 중원대학교 박물관 행사', c: 'system corp', u: 'https://blog.naver.com/hoon0170800/224419910650' },
    { f: 'corp-dk-7', t: '기업 체육대회 MC · 게임 진행', o: '기업 체육대회 · 당진 (4일간)', c: 'sports corp', u: 'https://blog.naver.com/hoon0170800/224407480300' },
    { f: 'water-sch-2', t: '학교 운동장 물놀이 바운스 · 에어풀장', o: '학교 물놀이행사', c: 'water school', u: 'https://blog.naver.com/hoon0170800/224317639604' },
    { f: 'fest-agri-0', t: '야외음악당 라인어레이 · 디지털 콘솔 운영', o: '지역축제 · 아산시 도시농업축제', c: 'system', u: 'https://blog.naver.com/hoon0170800/224405061050' },
    { f: 'apt-lh-6', t: '단지 산책로를 따라 세운 체험부스 천막', o: '아파트 · 아산 배방 LH15단지', c: 'apt rental', u: 'https://blog.naver.com/hoon0170800/224416024254' },
    { f: 'school-yh-1', t: '체육관 무대 음향 · 조명 세팅', o: '학교축제 · 아산 온양용화고', c: 'school system', u: 'https://blog.naver.com/hoon0170800/224418933345' },
    { f: 'water-apt-15', t: '아파트 단지 안 에어풀장 · 물놀이 바운스', o: '아파트 물놀이행사', c: 'water apt', u: 'https://blog.naver.com/hoon0170800/224317748152' },
    { f: 'tent-incheon-1', t: '체육대회 천막 · 테이블 · 의자 한 번에', o: '체육대회 · 인천 서구 체육회', c: 'rental sports', u: 'https://blog.naver.com/hoon0170800/224418956512' },
    { f: 'yearend-3', t: '기업 송년회 트러스 · 음향 · 무빙 조명', o: '기업행사 · 송년회', c: 'corp system', u: 'https://blog.naver.com/hoon0170800/223987888365' },
    { f: 'school-bb-1', t: '발표회 핀마이크 12채널 · 조명 콘솔 운영', o: '학예발표회 · 아산 배방초', c: 'school system', u: 'https://blog.naver.com/hoon0170800/224415445790' },
    { f: 'truss-photo-1', t: '입학식 포토존 트러스 · 레드카펫', o: '학교행사 · 포토존 트러스', c: 'school rental', u: 'https://blog.naver.com/hoon0170800/224091218910' },
    { f: 'corp-dk-12', t: '기업 체육대회 운동장 천막 세팅', o: '기업 체육대회 · 당진', c: 'sports corp rental', u: 'https://blog.naver.com/hoon0170800/224407480300' },
    { f: 'water-sch-1', t: '학교 물놀이 워터슬라이드 · 에어풀장', o: '학교 물놀이행사', c: 'water school', u: 'https://blog.naver.com/hoon0170800/224317639604' },
    { f: 'stage-jw-18', t: '트러스 조명 · 무대 덱 설치', o: '토탈 시스템 · 중원대학교 박물관 행사', c: 'system', u: 'https://blog.naver.com/hoon0170800/224419910650' },
    { f: 'apt-lh-9', t: '아파트 단지 부스 천막 · 테이블 · 의자', o: '아파트 · 아산 배방 LH15단지', c: 'apt rental', u: 'https://blog.naver.com/hoon0170800/224416024254' },
    { f: 'water-apt-0', t: '아파트 바닥분수 물놀이 행사장', o: '아파트 물놀이행사', c: 'water apt', u: 'https://blog.naver.com/hoon0170800/224317748152' },
    { f: 'fest-agri-6', t: '야외 무대 좌우 라인어레이 스피커', o: '지역축제 · 아산시 도시농업축제', c: 'system', u: 'https://blog.naver.com/hoon0170800/224405061050' }
  ];

  /* ---------- 블로그 현장 이야기 카드 (대문) ---------- */
  var STORIES = [
    { f: 'apt-lh-1', d: '2026.09.18 · 아산 배방', t: '아파트 주민행사, 단지가 하나의 축제장이 되는 날', p: '추석을 맞은 LH15단지 주민행사. 어르신 댄스 · 장구 공연과 초청가수 무대를 위해 음향 · 무대 · 백드롭 · 트러스 · 천막을 구성했습니다.', u: 'https://blog.naver.com/hoon0170800/224416024254' },
    { f: 'corp-dk-12', d: '2026.09.10 · 당진', t: '공장을 멈추지 않는 4일간의 기업 체육대회', p: '1조부터 4조까지 하루 한 조씩. 천막 · 음향 · 테이블 · 의자에 MC · 운영 스태프 · 게임장비까지 4일 동안 함께 운영했습니다.', u: 'https://blog.naver.com/hoon0170800/224407480300' },
    { f: 'stage-jw-6', d: '2026.09.22 · 토탈 시스템', t: '무대 · 외줄트러스 · LED · 조명 · 음향을 하나의 시스템으로', p: '무대 크기, LED 영상, 조명 위치, 음향, 출연자 동선까지 함께 고려해 하나의 행사 시스템으로 구성한 현장입니다.', u: 'https://blog.naver.com/hoon0170800/224419910650' }
  ];

  /* ---------- 블로그 글 목록 (2026-09-26 RSS 기준 49편 — 새 글은 맨 앞에 한 줄 추가) ---------- */
  var BLOG = [
    {d: "2026.09.23", t: "충남 행사 음향렌탈｜충남교육행정 어울림한마당 체육대회 음향 현장", u: "https://blog.naver.com/hoon0170800/224421093207"},
    {d: "2026.09.23", t: "공주 초등학교 학예발표회 음향·조명｜귀산초등학교 예술제 현장", u: "https://blog.naver.com/hoon0170800/224421057008"},
    {d: "2026.09.23", t: "세종 초등학교 학예발표회 음향·조명｜늘봄초등학교 축제 현장", u: "https://blog.naver.com/hoon0170800/224421003878"},
    {d: "2026.09.23", t: "아산·천안 초등학교 학예발표회 음향·조명 업｜남창초등학교 행사 현장", u: "https://blog.naver.com/hoon0170800/224420990257"},
    {d: "2026.09.22", t: "천안 학교축제 음향·조명 렌탈｜천안여자상업고등학교 축제 현장", u: "https://blog.naver.com/hoon0170800/224419997162"},
    {d: "2026.09.22", t: "행사 무대·LED전광판·음향·조명 렌탈｜트러스까지 토탈 행사 시스템", u: "https://blog.naver.com/hoon0170800/224419910650"},
    {d: "2026.09.22", t: "아산 대형 현수막 트러 설치｜천안 행사 사진 전시벽·전시 구조물 제작", u: "https://blog.naver.com/hoon0170800/224419845838"},
    {d: "2026.09.21", t: "충남 천막렌탈｜체육대회·축제 행사 캐노피천막 테이블 의자 대여", u: "https://blog.naver.com/hoon0170800/224418956512"},
    {d: "2026.09.21", t: "아산 학교축제 음향렌탈｜온양용화고등학교 축제 음향·조명 현장", u: "https://blog.naver.com/hoon0170800/224418933345"},
    {d: "2026.09.18", t: "아산 아파트행사｜배방 LH15단지 주민축제 현장, 우리 아파트가 하나의 축제장이 됩니다", u: "https://blog.naver.com/hoon0170800/224416024254"},
    {d: "2026.09.18", t: "당진 체육대회 행사대행｜성당·교회 명랑운동회 MC·음향·천막까지", u: "https://blog.naver.com/hoon0170800/224415476385"},
    {d: "2026.09.17", t: "아산 음향·조명 업체｜배방초등학교 발표회 핀마이크 12채널 운영 현장", u: "https://blog.naver.com/hoon0170800/224415445790"},
    {d: "2026.09.17", t: "논산 초등학교 학예발표회 업체｜채운초등학교 조명·옥타부스 설치 현장", u: "https://blog.naver.com/hoon0170800/224415292024"},
    {d: "2026.09.15", t: "천안중학교 체육대회 현장 후기｜음향·천막·MC·게임도구·프로그램까지", u: "https://blog.naver.com/hoon0170800/224412401648"},
    {d: "2026.09.14", t: "예산고등학교 체육대회·학교축제 3년연속진행업체 | 학교행사 음향·조명·천막·테이블·의자설치", u: "https://blog.naver.com/hoon0170800/224411467895"},
    {d: "2026.09.12", t: "평택 송탄 고등학교 체육대회 행사업체｜음향·천막·물놀이·게임장비 토탈 설치현장 후", u: "https://blog.naver.com/hoon0170800/224409329172"},
    {d: "2026.09.11", t: "아산 개소식 행사대행｜음향·레드카펫·테이프커팅식 준비부터 진행까지", u: "https://blog.naver.com/hoon0170800/224408257723"},
    {d: "2026.09.11", t: "아산 행사무대조명 렌탈｜김미성 시의원 의정보고회 무대조명,핀마이 설치 현장", u: "https://blog.naver.com/hoon0170800/224408230525"},
    {d: "2026.09.10", t: "당진 기업체육대회 업체｜동국제강 4일간 기업행사 기획·운영 현장후기", u: "https://blog.naver.com/hoon0170800/224407480300"},
    {d: "2026.09.08", t: "아산 축제 음향렌탈 업체｜도시농업축제 야외무대 라인어레이 음향 현장", u: "https://blog.naver.com/hoon0170800/224405061050"},
    {d: "2026.09.07", t: "아산 고등학교 축제 음향·조명 업체｜온양여고 2025 온화제 현장 후기", u: "https://blog.naver.com/hoon0170800/224403911643"},
    {d: "2026.09.07", t: "남양주 초등학교 학예발표회 업체｜미금초 음향,조명,무대막,풍선장식 현장후기", u: "https://blog.naver.com/hoon0170800/224403870932"},
    {d: "2026.09.03", t: "아산 초등학교 학예발표회/염티초등학교 음향,조명렌탈 행사후기", u: "https://blog.naver.com/hoon0170800/224399938953"},
    {d: "2026.09.03", t: "용인 초등학교 체육대회 업체,용마초등학교 운동회 현장후기", u: "https://blog.naver.com/hoon0170800/224399855636"},
    {d: "2026.06.19", t: "아산 물놀이장 추천 가족모임,생일파티,바베큐가능한 단독대관 공간", u: "https://blog.naver.com/hoon0170800/224321071777"},
    {d: "2026.06.17", t: "교회,성당물놀이행사 실제 설치사례 모음 / 워터슬라이드,에어풀장 운영후기", u: "https://blog.naver.com/hoon0170800/224318766164"},
    {d: "2026.06.16", t: "아파트물놀이행사 전문업체 스타컴퍼니 실제운영 현장공개", u: "https://blog.naver.com/hoon0170800/224317748152"},
    {d: "2026.06.16", t: "2026 학교 물놀이 행사 전문업체 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224317639604"},
    {d: "2026.05.27", t: "전국 교회,성당 물놀이행사,여름행사 전문 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224298096575"},
    {d: "2026.04.27", t: "여름물놀이 행사 고민되신다면? (아파트,교회,청소년시설추천)", u: "https://blog.naver.com/hoon0170800/224266957235"},
    {d: "2026.03.31", t: "아파트 물놀이 행사 비용 공개 / 업체선택꿀팁! - 후기포함", u: "https://blog.naver.com/hoon0170800/224236103331"},
    {d: "2026.03.17", t: "초등학교물놀이행사,물놀이에어바운스,렌탈대여-스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224219788211"},
    {d: "2026.03.09", t: "천안,아산,서산,당진,세종,보령,예산,평택 기업회사체육대회는-스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224210315899"},
    {d: "2026.02.24", t: "아산초등학교체육대회,운동회 대행용역은 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224194322075"},
    {d: "2026.01.28", t: "천안초등학교체육대회,운동회-대행용역업체 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224162821581"},
    {d: "2026.01.20", t: "천안,아산초등학교체육대회,운동회대행,용역업체는 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224153685678"},
    {d: "2025.12.10", t: "천안,아산,당진,서산,태안,홍성,보령,청양,예산,공주,계룡,논산,금산,부여,서천 졸업식,입학식포토존 렌탈,대여-스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224104945658"},
    {d: "2025.11.28", t: "학교졸업식,입학식 포토존 트러스렌탈 전문 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224091218910"},
    {d: "2025.09.16", t: "초등학교학예발표회 음향,조명렌탈 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/224010501315"},
    {d: "2025.09.02", t: "천안,아산,서산,당진,세종,청주,대전 중학교,고등학교 축제 음향조명렌탈- 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223992815999"},
    {d: "2025.08.29", t: "기업,회사 송년회 망년회 MC 음향,조명,노래방기계 렌탈 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223987888365"},
    {d: "2025.08.29", t: "청소년센터,청소년수련관,청소년문화의집 체육대회,운동회 후기 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223987815031"},
    {d: "2025.08.28", t: "중,고등학교 축제 음향,조명렌탈대여 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223986745450"},
    {d: "2025.08.21", t: "초등학교 체육대회 대행업체 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223978675292"},
    {d: "2025.08.18", t: "초등학교발표회,예술제 행사에 필요한 음향,조명,무대막,풍선장식 등 모든물품을 한번에렌탈 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223974410161"},
    {d: "2025.08.14", t: "갈산중학교 축제 현장속으로 음향,조명렌탈 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223970751919"},
    {d: "2025.08.14", t: "한서대학교 항공관광학과 학술제 무대조명렌탈 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223970731684"},
    {d: "2025.08.04", t: "기업체육대회,회사체육대회 대행업체 - 스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223958583216"},
    {d: "2025.07.22", t: "트러스,미니트러스,포토존트러스,시상식트러스,무대백월트러스,입학식졸업식트러스,포토존 전국렌탈-스타컴퍼니", u: "https://blog.naver.com/hoon0170800/223943034819"}
  ];

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var P = 'assets/img/p/', T = 'assets/img/t/';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var ARR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M9 7h8v8"/></svg>';

  /* ---------- 머리 · 모바일 메뉴 · 맨 위로 ---------- */
  var hd = $('#hd'), totop = $('#totop');
  function onScroll() { var y = window.scrollY; if (hd) hd.classList.toggle('stuck', y > 8); if (totop) totop.classList.toggle('on', y > 700); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (totop) totop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  var cur = (location.pathname.split('/').pop() || 'index.html');
  $$('.hd .menu a, .sheet nav a').forEach(function (a) { if (a.getAttribute('href') === cur) a.classList.add('act'); });

  var burger = $('#burger'), sheet = $('#sheet');
  function closeSheet() { sheet.classList.remove('on'); burger.classList.remove('x'); burger.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; }
  if (burger && sheet) {
    burger.addEventListener('click', function () {
      var on = sheet.classList.toggle('on'); burger.classList.toggle('x', on); burger.setAttribute('aria-expanded', on ? 'true' : 'false');
      document.body.style.overflow = on ? 'hidden' : '';
    });
    $$('a, .x', sheet).forEach(function (a) { a.addEventListener('click', closeSheet); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && sheet.classList.contains('on')) closeSheet(); });
  }

  /* ---------- 카카오톡 채널 (주소가 있을 때만 보임) ---------- */
  if (KAKAO_URL) $$('[data-kakao]').forEach(function (a) { a.href = KAKAO_URL; a.target = '_blank'; a.rel = 'noopener'; a.hidden = false; });

  /* ---------- 히어로: 영상 + 전원 스위치 ---------- */
  var hero = $('#hero');
  if (hero) {
    var video = $('#heroVideo'), power = $('#power'), pwState = $('#pwState');
    function setLit(on) {
      hero.classList.toggle('lit', on);
      if (power) { power.setAttribute('aria-pressed', on ? 'true' : 'false'); power.setAttribute('aria-label', on ? '행사 스위치 끄기' : '행사 스위치 켜기'); }
      if (pwState) pwState.textContent = on ? 'ON' : 'OFF';
    }
    if (video) {
      if (reduce) { video.removeAttribute('autoplay'); video.preload = 'none'; }
      else {
        var w = window.innerWidth * Math.min(window.devicePixelRatio || 1, 2);
        var mp4 = video.canPlayType('video/mp4; codecs="avc1.42E01E"');
        // H.264 를 못 트는 브라우저(일부 리눅스 · 오픈소스 크로미움)는 webm 으로
        video.src = !mp4 ? video.getAttribute('data-src-webm') : (w < 1100 ? video.getAttribute('data-src-sm') : video.getAttribute('data-src'));
        video.muted = true;
        var tryPlay = function () { var p = video.play(); if (p && p.catch) p.catch(function () {}); };
        tryPlay(); video.addEventListener('canplay', tryPlay, { once: true });
        document.addEventListener('visibilitychange', function () { if (!document.hidden) tryPlay(); });
        document.addEventListener('pointerdown', function () { if (video.paused) tryPlay(); }, { once: true });
      }
    }
    if (reduce) setLit(true); else setTimeout(function () { setLit(true); }, 900);
    if (power) power.addEventListener('click', function () { setLit(!hero.classList.contains('lit')); });
  }

  /* ---------- 등장 · 숫자 · 전선 ---------- */
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: .12, rootMargin: '0px 0px -40px 0px' }) : null;
  $$('.rv, .flow').forEach(function (el) { if (io && !reduce) io.observe(el); else el.classList.add('in'); });
  // 카드에 차례로 불이 들어오게 (하는 일 8칸)
  $$('.svc8 a').forEach(function (a, i) { a.style.transitionDelay = (i % 4) * 70 + 'ms'; });
  // 하는 일 카드가 화면에 들어오면 스위치가 하나씩 켜진다
  var s8 = $('.svc8');
  if (s8) {
    var turnOn = function () { $$('a', s8).forEach(function (a, i) { setTimeout(function () { a.classList.add('is-on'); }, reduce ? 0 : 250 + i * 180); }); };
    if (io && !reduce) { var s8io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { s8io.disconnect(); turnOn(); } }, { threshold: .25 }); s8io.observe(s8); } else turnOn();
  }
  var counters = $$('[data-count]');
  if (counters.length && io && !reduce) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; cio.unobserve(e.target);
        var el = e.target, to = +el.getAttribute('data-count'), t0 = null, dur = 1400;
        (function step(ts) { if (!t0) t0 = ts; var k = Math.min(1, (ts - t0) / dur); k = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(to * k); if (k < 1) requestAnimationFrame(step); })(performance.now());
      });
    }, { threshold: .6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- 갤러리 (대문 8장 · 행사 사진 전체) + 라이트박스 ---------- */
  function workCard(w, k) {
    return '<figure tabindex="0" data-k="' + k + '" data-c="' + w.c + '"><img src="' + T + w.f + '.webp" alt="' + esc(w.t) + '" loading="lazy" width="800" height="600">' +
      '<figcaption><em>' + esc(w.o) + '</em>' + esc(w.t) + '</figcaption></figure>';
  }
  var gal = $('#gal'), pf = $('#pfGrid'), list = [];
  if (gal) { list = WORKS.slice(0, 8); gal.innerHTML = list.map(workCard).join(''); }
  if (pf) { list = WORKS; pf.innerHTML = list.map(workCard).join(''); }
  var grid = gal || pf, lb = $('#lb');
  if (grid && lb) {
    var figs = $$('figure', grid), lbImg = $('#lbImg'), lbT = $('#lbTitle'), lbM = $('#lbMeta'), lbK = 0, lastFocus = null;
    var visible = function () { return figs.filter(function (f) { return !f.classList.contains('hide'); }).map(function (f) { return +f.getAttribute('data-k'); }); };
    var openLb = function (k) {
      var w = list[k]; lbK = k; lbImg.src = P + w.f + '.webp'; lbImg.alt = w.t; lbT.textContent = w.t;
      lbM.innerHTML = esc(w.o) + (w.u ? ' · <a href="' + w.u + '" target="_blank" rel="noopener" style="color:#19D27A">블로그 글 보기</a>' : '');
      if (!lb.classList.contains('on')) lastFocus = document.activeElement;
      lb.classList.add('on'); document.body.style.overflow = 'hidden'; $('#lbX').focus();
    };
    var closeLb = function () { lb.classList.remove('on'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); };
    var stepLb = function (d) { var v = visible(), i = v.indexOf(lbK); openLb(v[(i + d + v.length) % v.length]); };
    grid.addEventListener('click', function (e) { var f = e.target.closest('figure'); if (f) openLb(+f.getAttribute('data-k')); });
    grid.addEventListener('keydown', function (e) { if (e.key !== 'Enter' && e.key !== ' ') return; var f = e.target.closest('figure'); if (f) { e.preventDefault(); openLb(+f.getAttribute('data-k')); } });
    $('#lbX').addEventListener('click', closeLb);
    $('#lbPrev').addEventListener('click', function () { stepLb(-1); });
    $('#lbNext').addEventListener('click', function () { stepLb(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', function (e) { if (!lb.classList.contains('on')) return; if (e.key === 'Escape') closeLb(); if (e.key === 'ArrowLeft') stepLb(-1); if (e.key === 'ArrowRight') stepLb(1); });
    var sx = 0;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) stepLb(dx < 0 ? 1 : -1); }, { passive: true });
    var filters = $('#filters');
    if (filters) {
      filters.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        $$('button', filters).forEach(function (x) { x.classList.remove('act'); x.setAttribute('aria-pressed', 'false'); });
        b.classList.add('act'); b.setAttribute('aria-pressed', 'true');
        var f = b.getAttribute('data-f');
        figs.forEach(function (fg) { fg.classList.toggle('hide', f !== 'all' && fg.getAttribute('data-c').split(' ').indexOf(f) < 0); });
      });
      // 필터별 사진 수
      $$('button', filters).forEach(function (b) {
        var f = b.getAttribute('data-f'), n = f === 'all' ? WORKS.length : WORKS.filter(function (w) { return w.c.split(' ').indexOf(f) >= 0; }).length;
        b.insertAdjacentHTML('beforeend', ' <small style="opacity:.6">' + n + '</small>');
      });
    }
  }

  /* ---------- 블로그 현장 이야기 카드 ---------- */
  var sc = $('#storyCards');
  if (sc) sc.innerHTML = STORIES.map(function (s) {
    return '<a class="rv in" href="' + s.u + '" target="_blank" rel="noopener"><div class="img" style="background-image:url(' + T + s.f + '.webp)"></div><div class="body"><small>' + esc(s.d) + '</small><b>' + esc(s.t) + '</b><p>' + esc(s.p) + '</p></div><span class="go">블로그에서 읽기 ↗</span></a>';
  }).join('');

  /* ---------- 블로그 글 목록 ---------- */
  $$('.blist[data-limit]').forEach(function (bl) {
    var LIMIT = +bl.getAttribute('data-limit') || 10, shown = LIMIT;
    bl.innerHTML = BLOG.map(function (b, k) { return '<a href="' + b.u + '" target="_blank" rel="noopener"' + (k >= shown ? ' class="hide"' : '') + '><small>' + b.d + '</small><b>' + esc(b.t) + '</b>' + ARR + '</a>'; }).join('');
    var more = bl.parentNode.querySelector('.blogMore');
    if (more) {
      if (BLOG.length <= LIMIT) more.hidden = true;
      more.addEventListener('click', function () { shown += LIMIT; $$('a', bl).forEach(function (a, k) { a.classList.toggle('hide', k >= shown); }); if (shown >= BLOG.length) more.hidden = true; });
    }
  });
  var bc = $('#blogCount'); if (bc) bc.textContent = BLOG.length;

  /* ---------- 공지 (대문 요약) ---------- */
  var nl = $('#noticeList');
  if (nl) nl.innerHTML = NOTICES.slice(0, 4).map(function (n) { return '<li><a href="notice.html#n' + NOTICES.indexOf(n) + '"><b>' + esc(n.t) + (n.n ? '<span class="new">NEW</span>' : '') + '</b></a><small>' + n.d + '</small></li>'; }).join('');

  /* ---------- 공지 · 블로그 · 자료실 (notice.html) ---------- */
  var board = $('#board');
  if (board) {
    var order = NOTICES.map(function (n, i) { return { n: n, i: i }; }).sort(function (a, b) { return (b.n.pin ? 1 : 0) - (a.n.pin ? 1 : 0); });
    var num = NOTICES.length;
    board.innerHTML = order.map(function (o) {
      var n = o.n, no = n.pin ? '<span class="no pin">공지</span>' : '<span class="no">' + (num - o.i) + '</span>';
      return '<details id="n' + o.i + '"><summary>' + no + '<b>' + esc(n.t) + (n.n ? '<span class="new">NEW</span>' : '') + '</b><small>' + n.d + '</small></summary><div class="txt">' + esc(n.b || '') + '</div></details>';
    }).join('');
  }
  var fl = $('#fileList');
  if (fl) fl.innerHTML = FILES.map(function (f) {
    var href = f.href || ('contact.html#q=' + encodeURIComponent('[자료 요청] ' + f.t + ' 를 받고 싶습니다.\n받으실 곳(이메일 · 휴대폰): '));
    return '<li><span class="ic">' + f.k + '</span><span><b>' + esc(f.t) + '</b><small>' + esc(f.s) + '</small></span><a class="btn btn-line btn-sm" href="' + href + '">' + f.btn + '</a></li>';
  }).join('');
  var tabs = $('#tabs');
  if (tabs) {
    var tbs = $$('button', tabs);
    var showTab = function (key, push) {
      tbs.forEach(function (b) { var on = b.getAttribute('data-t') === key; b.classList.toggle('on', on); b.setAttribute('aria-selected', on ? 'true' : 'false'); });
      $$('.pane').forEach(function (p) { p.classList.toggle('on', p.id === 'pane-' + key); });
      if (push) history.replaceState(null, '', '#' + key);
    };
    tbs.forEach(function (b) { b.addEventListener('click', function () { showTab(b.getAttribute('data-t'), true); }); });
    var h = location.hash.slice(1);
    if (/^n\d+$/.test(h)) { showTab('notice'); var d = document.getElementById(h); if (d) { d.open = true; setTimeout(function () { d.scrollIntoView({ block: 'center' }); }, 100); } }
    else if (h === 'blog' || h === 'files') showTab(h); else showTab('notice');
  }

  /* ---------- 문의 보내기 (폼 · 가격표 요청서 공용) ---------- */
  function isMobile() { return /iPhone|iPad|Android/i.test(navigator.userAgent); }
  function send(text, data, done, service) {
    if (FORM_ENDPOINT) {
      data.at = new Date().toISOString(); data.page = location.href; data.service = service; data.message = text;
      fetch(FORM_ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain' }, body: JSON.stringify(data) }).catch(function () {}).then(function () { done(true); });
      return;
    }
    if (isMobile()) { var ios = /iPhone|iPad/i.test(navigator.userAgent); location.href = 'sms:' + SMS_TO + (ios ? '&' : '?') + 'body=' + encodeURIComponent(text); done(true, 'sms'); return; }
    try { if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {}); } catch (e) {}
    done(false);
  }

  var form = $('#quoteForm');
  if (form) {
    var fdone = $('#formDone');
    var qm = location.hash.match(/^#q=(.+)$/);
    if (qm && form.elements.msg) { try { form.elements.msg.value = decodeURIComponent(qm[1]); } catch (e) {} }
    var aptSel = function () { if (location.hash === '#apt' && form.elements.type) { form.elements.type.value = '아파트 행사 (플리마켓 · 입주민축제 · 물놀이)'; form.scrollIntoView({ block: 'start' }); } };
    aptSel(); window.addEventListener('hashchange', aptSel);
    if (qm || location.hash === '#apt') setTimeout(function () { form.scrollIntoView({ block: 'start' }); }, 200);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.elements.website && form.elements.website.value) return; // 스팸 봇 함정
      var d = {};
      ['name', 'tel', 'org', 'type', 'date', 'place', 'people', 'msg'].forEach(function (k) { d[k] = form.elements[k] ? form.elements[k].value.trim() : ''; });
      if (!d.name || !d.tel) { alert('이름과 연락처는 꼭 적어 주세요.'); (d.name ? form.elements.tel : form.elements.name).focus(); return; }
      if (!$('#fAgree').checked) { alert('개인정보 수집 · 이용에 동의해 주세요.'); return; }
      var text = '[' + COMPANY + ' 견적 · 예약 문의]\n이름: ' + d.name + '\n연락처: ' + d.tel + '\n기관 · 단지: ' + (d.org || '-') + '\n행사 종류: ' + d.type + '\n날짜: ' + (d.date || '-') + '\n장소: ' + (d.place || '-') + '\n인원: ' + (d.people || '-') + '\n내용: ' + (d.msg || '-');
      d.phone = d.tel;
      send(text, d, function (sent, how) {
        fdone.classList.add('on');
        var p = $('p', fdone);
        if (how === 'sms') p.innerHTML = '문자 앱에 문의 내용을 담아 두었습니다.<br><b>보내기</b>를 누르시면 담당자 휴대폰(' + SMS_TO + ')으로 바로 갑니다.';
        else if (!sent) p.innerHTML = '문의 내용을 복사해 두었습니다.<br>문자 <b>' + SMS_TO + '</b> 에 붙여넣어 보내 주시거나,<br>대표전화 <b>' + TEL + '</b> (24시)로 전화 주세요.';
      }, '행사 견적 · 예약 문의');
    });
    var again = $('#formAgain'); if (again) again.addEventListener('click', function () { fdone.classList.remove('on'); });
  }

  /* ---------- 가격표: 품목 고르기 → 견적 요청서 ---------- */
  var ptab = $('#priceTables');
  if (ptab) {
    var picks = $$('input[type=checkbox][data-item]', ptab), cartN = $('#cartN'), cartL = $('#cartList'), cartGo = $('#cartGo'), cartCopy = $('#cartCopy');
    var chosen = function () { return picks.filter(function (c) { return c.checked; }).map(function (c) { return c.getAttribute('data-item'); }); };
    var req = function () {
      var c = chosen();
      return '[' + COMPANY + ' 견적 요청 — 가격표에서 고른 품목]\n' + (c.length ? c.map(function (x) { return '- ' + x; }).join('\n') : '- (품목 미정 · 상담 요청)') + '\n\n행사 날짜: \n장소: \n예상 인원: \n요청 사항: ';
    };
    var upd = function () {
      var c = chosen(); cartN.textContent = c.length; cartL.textContent = c.length ? c.join(' · ') : '표 오른쪽 스위치를 켜서 필요한 품목을 담아 보세요.';
      picks.forEach(function (x) { x.closest('tr').classList.toggle('on', x.checked); });
    };
    ptab.addEventListener('change', upd); upd();
    cartGo.addEventListener('click', function () { location.href = 'contact.html#q=' + encodeURIComponent(req()); });
    if (cartCopy) cartCopy.addEventListener('click', function () {
      var t = req();
      try { navigator.clipboard.writeText(t).then(function () { cartCopy.textContent = '복사됨 ✓'; setTimeout(function () { cartCopy.textContent = '목록 복사'; }, 1800); }); } catch (e) {}
    });
  }
})();

# -*- coding: utf-8 -*-
"""
큰길이벤트기획의 서류 3종(견적서 · 전자계약서 · 거래명세서)을 바로기획용으로 옮긴다.

  python tools/port_docs.py [큰길이벤트 레포 경로]      (기본 ~/Documents/클로드코드)

원본을 고친 뒤 다시 돌리면 같은 규칙으로 다시 옮긴다(바로기획 쪽 손수정은 여기 규칙으로 넣을 것).
하는 일: 회사 정보 · 문구 · 예시 · 품목표 교체, 주황 → 금색 · 남색, 머리글 로고 · 메뉴를 바로기획 것으로.
"""
import os, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Documents/클로드코드')
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 바로기획 계약 서버(앱스 스크립트) — 배포하면 여기에 주소를 넣고 다시 돌린다. 비어 있으면 서버 없이 동작.
BARO_CONTRACT = ''

LOGO = '<img src="assets/img/logo-mark.svg" alt="" style="width:2.3rem;height:2.3rem;border-radius:.6rem;display:block">'
LOGO_S = '<img src="assets/img/logo-mark.svg" alt="" style="width:2.1rem;height:2.1rem;border-radius:.55rem;display:block">'
MAIL_LOGO = '<img src="https://brizymedia.github.io/baro-event/assets/img/logo-h-white.png" height="32" alt="바로기획" style="vertical-align:middle;">'

COMMON = [
    # ── 회사 정보 ──
    ('큰길이벤트기획 (주식회사 브리지미디어)', '바로기획'),
    (' <span style="color:#9ca3af;">(주식회사 브리지미디어)</span>', ''),
    ('주식회사 브리지미디어 대표 직인', '바로기획 대표 직인'),
    ('(예금주: 주식회사 브리지미디어)', ''),
    ('주식회사 브리지미디어', '바로기획'),
    ('큰길이벤트기획', '바로기획'),
    ('[큰길이벤트]', '[바로기획]'),
    ('큰길이벤트.com/quote.html', 'brizymedia.github.io/baro-event/quote.html'),
    ('큰길이벤트.com', 'brizymedia.github.io/baro-event'),
    ('김동길', '김선호'),
    ('813-81-02252', '174-22-00074'),
    ("corp:'204611-0065269'", "corp:''"),
    ('전남광주통합특별시 광양시 광양읍 강변동길 1, 2층', '경기도 안산시 상록구 장화1길 56, 103호 (사동)'),
    ('전남광주통합특별시 광양시 광양읍 강변동길 1', '경기도 안산시 상록구 장화1길 56, 103호'),
    ('1533-7295', '010-2758-0655'),
    ('gilcaro@naver.com', 'mot2256@naver.com'),
    ("'KB국민은행 788101-01-397776 '", "''"),
    ("bank:'KB국민은행 788101-01-397776 '", "bank:''"),
    ("'KG-'", "'BR-'"),
    ('data-site="keungil"', 'data-site="baro"'),
    ('keungil-quote-box', 'baro-quote-box'),
    ('keungil-contract', 'baro-contract'),
    ('keungil-statement', 'baro-statement'),
    ('우리(큰길)', '우리(바로기획)'),
    # ── 예시 문구 ──
    ('예) 광양시청 / ○○총동문회', '예) 안산시 ○○동 주민자치회 / ○○교회'),
    ('예) 광양시 광양읍 일원', '예) 안산 와~스타디움 보조경기장'),
    ('예) 제25회 광양 매화축제', '예) 2026 ○○ 한마음 체육대회'),
    ('예) 고흥군청 문화관광과', '예) 화성시 새솔동 주민자치회'),
    ('고흥군 녹동항 일원', '화성 새솔동 수노을중앙공원'),
    ('2026 녹동바다불꽃축제 무대음향 운영', '2026 수노을 물놀이축제 운영'),
    ('음향 · 조명 · LED · 무대', '체육대회 · 축제 · 음향 · 무대'),
    ("spec:'전남 외 지역'", "spec:'경기 외 지역'"),
    # ── 아이콘 · 파비콘 ──
    ('<link rel="icon" href="/favicon.ico" sizes="32x32">\n', ''),
    ('href="/favicon.svg"', 'href="assets/img/favicon.svg"'),
    ('<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n', ''),
    ('  <link rel="alternate" type="application/rss+xml" title="바로기획 소식" href="/rss.xml">\n', ''),
    ('src="logo-kgm-transparent.png"', 'src="assets/img/logo-mark.svg"'),
    # ── 색: 주황 → 금색 · 남색 ──
    ('#F59E0B', '#C9A24B'), ('#FBBF24', '#E3C57E'), ('#D97706', '#B08A36'), ('#B45309', '#8F6E22'),
    ('#FCD34D', '#EBD39A'), ('#a05c00', '#8F6E22'), ('#09090b', '#081427'), ('#0B0A10', '#081427'),
    ('#16141C', '#0E1F3F'), ('#131317', '#0E1F3F'),
    ('rgba(245,158,11', 'rgba(201,162,75'), ('rgba(251,191,36', 'rgba(227,197,126'),
    ('rgba(9,9,11', 'rgba(8,20,39'), ('rgba(11,10,16', 'rgba(8,20,39'),
]

NAV = [
    ('href="index.html#services"', 'href="service.html"'),
    ('href="index.html#portfolio"', 'href="portfolio.html"'),
    ('href="index.html#gallery"', 'href="portfolio.html"'),
    ('href="index.html#contact"', 'href="contact.html"'),
    ('href="/blog/"', 'href="notice.html"'),
    ('href="/stories/"', 'href="stories/"'),
    ('>행사이력</a>', '>현장사진</a>'),
    ('href="/quote.html', 'href="quote.html'), ('href="/contract.html', 'href="contract.html'), ('href="/"', 'href="index.html"'),
    ('>블로그</a>', '>공지 · 블로그</a>'),
    ('TOTAL EVENT AGENCY', 'BARO PLANNING'),
]

CATALOG = """const CATALOG = [
  { group:'행사 진행', items:[
    { id:'p1', name:'체육대회 · 명랑운동회',  spec:'종목 구성 · 진행 · 본부석 운영',        unit:'식', price:null },
    { id:'p2', name:'지역축제 · 주민행사',    spec:'프로그램 · 무대 · 체험 부스',           unit:'식', price:null },
    { id:'p3', name:'커팅식 · 오픈 이벤트',   spec:'개업 · 이전 · 개원 · 준공',             unit:'식', price:null },
    { id:'p4', name:'송년회 · 레크리에이션',  spec:'기업 · 단체 · 모임',                    unit:'식', price:null },
    { id:'p5', name:'물놀이 축제',            spec:'풀장 · 워터슬라이드 · 영유아존',        unit:'식', price:null },
    { id:'p6', name:'점등식 · 기념식',        spec:'점등 연출 · 식순 · 의전',               unit:'식', price:null },
    { id:'p7', name:'캠프 · 야간 레크리에이션', spec:'캠프파이어 · 레크 · 공연',            unit:'식', price:null },
  ]},
  { group:'음향', items:[
    { id:'a1', name:'음향 (소형)',       spec:'100명 내외 · 실내 · 마이크 2ch',      unit:'식', price:null },
    { id:'a2', name:'음향 (중형)',       spec:'300명 내외 · 스피커 4통 · 믹서',      unit:'식', price:null },
    { id:'a3', name:'음향 (대형)',       spec:'500명 이상 · 야외 운동장 · 축제',     unit:'식', price:null },
    { id:'a4', name:'무선 마이크 추가',  spec:'핸드 / 핀 마이크',                    unit:'개', price:null, qty:true },
  ]},
  { group:'무대 · 조명', items:[
    { id:'b1', name:'조립식 무대',       spec:'크기 · 높이 협의',                    unit:'식', price:null },
    { id:'b2', name:'무대 조명',         spec:'개회식 · 시상식 · 공연용',            unit:'식', price:null },
    { id:'b3', name:'LED 전광판 · 스크린', spec:'실내외 · 크기 협의',                unit:'식', price:null },
    { id:'b4', name:'백드롭 · 현수막',   spec:'행사명 현수막 · 배너 출력',           unit:'식', price:null },
    { id:'b5', name:'포토존',            spec:'구조물 + 출력물',                     unit:'식', price:null },
  ]},
  { group:'천막 · 테이블', items:[
    { id:'d3',  name:'자바라 텐트 3m×3m', spec:'원터치 · 설치 · 철수',              unit:'동', price:null, qty:true },
    { id:'d10', name:'자바라 텐트 3m×6m', spec:'본부석 · 응원석',                   unit:'동', price:null, qty:true },
    { id:'d11', name:'몽골텐트',          spec:'대형 텐트',                          unit:'동', price:null, qty:true },
    { id:'d9',  name:'의자',              spec:'행사용 의자',                        unit:'개', price:null, qty:true },
    { id:'d12', name:'테이블',            spec:'직사각 · 원형',                      unit:'개', price:null, qty:true },
    { id:'d13', name:'테이블보',          spec:'테이블 크기에 맞춰',                 unit:'장', price:null, qty:true },
    { id:'d14', name:'파라솔 · 그늘막',   spec:'야외 쉼터',                          unit:'개', price:null, qty:true },
  ]},
  { group:'공연 · MC 섭외', items:[
    { id:'f1', name:'전문 MC · 사회자',     spec:'행사 성격에 맞춘 진행자',          unit:'명', price:null },
    { id:'f6', name:'레크리에이션 강사',    spec:'체육대회 · 송년회 · 캠프',          unit:'명', price:null },
    { id:'f2', name:'가수 섭외',            spec:'행사 성격에 맞는 라인업',           unit:'팀', price:null },
    { id:'f4', name:'댄스 · 공연팀',        spec:'오프닝 · 축하공연 · 벨리댄스',      unit:'팀', price:null },
    { id:'f7', name:'버블쇼 · 어린이 공연', spec:'축제 · 어린이 행사',                unit:'팀', price:null },
    { id:'f5', name:'행사 스탭',            spec:'현장 진행 인력',                    unit:'명', price:null, qty:true },
  ]},
  { group:'게임도구 · 행사용품', items:[
    { id:'h3', name:'체육대회 게임도구',   spec:'대형 공굴리기 · 단체 줄넘기 · 계주',  unit:'식', price:null },
    { id:'h4', name:'체육용품',            spec:'줄다리기 · 박 터뜨리기 · 조끼',       unit:'식', price:null },
    { id:'h1', name:'에어바운스',          spec:'공기주입식 놀이기구 · 송풍기 포함',   unit:'동', price:null, qty:true },
    { id:'h2', name:'대형 풀장 · 워터슬라이드', spec:'급배수 · 안전요원 협의',        unit:'동', price:null, qty:true },
    { id:'h5', name:'풍선장식 · 풍선 아치', spec:'오픈 · 커팅식 · 포토존',            unit:'식', price:null },
    { id:'h6', name:'커팅식 세트',         spec:'레드카펫 · 오색띠 · 금장가위 · 흰장갑', unit:'식', price:null },
    { id:'e5', name:'에어샷 · 축포',       spec:'컨페티 · 은박 테이프 발사',           unit:'대', price:null, qty:true },
    { id:'h7', name:'경품 · 시상 진행',    spec:'경품 추첨 · 시상식 운영',             unit:'식', price:null },
  ]},
  { group:'기타', items:[
    { id:'g1', name:'발전기',            spec:'전원 미확보 현장',                  unit:'대', price:null },
    { id:'g2', name:'운반 · 설치 인건비', spec:'상하차 · 설치 · 철수',             unit:'식', price:null },
    { id:'g3', name:'출장비',            spec:'경기 외 지역',                      unit:'식', price:null },
  ]},
];"""


def dedupe_nav(s):
    # 큰길이벤트는 「행사이력」「갤러리」가 따로지만 바로기획은 둘 다 현장사진 페이지 — 갤러리 줄은 뺀다
    s = re.sub(r'\s*<a href="portfolio\.html"[^>]*>갤러리</a>', '', s)
    return s


def rep_all(s, pairs, name):
    for a, b in pairs:
        s = s.replace(a, b)
    return s


def logo_fix(s):
    # 「KG」 네모 → 바로기획 마크
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.3rem;height:2\.3rem;[^"]*">KG</span>', LOGO, s)
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.1rem;height:2\.1rem;[^"]*">KG</span>', LOGO_S, s)
    s = re.sub(r'<span style="display:inline-block;width:32px;height:32px;line-height:32px;text-align:center;\s*background:#C9A24B;[^"]*">KG</span>\s*<span style="[^"]*">바로기획</span>', MAIL_LOGO, s)
    s = s.replace('<a class="brand" href="/"><i>KG</i> 바로기획</a>', '<a class="brand" href="index.html"><img src="assets/img/logo-mark.svg" alt="" style="width:26px;height:26px;border-radius:6px;vertical-align:-7px;margin-right:6px">바로기획</a>')
    return s


def no_stamp(s):
    # 바로기획은 직인 파일이 없다 → 직인 칸을 비운다(대표님 인감 이미지를 받으면 assets/img/stamp-baro.png 로 넣고 여기 규칙을 바꾼다)
    s = s.replace('<img class="stamp" src="stamp-keungil.png" alt="바로기획 대표 직인" onerror="this.style.display=\'none\'">', '')
    s = s.replace("'stamp-keungil.png'", "'assets/img/stamp-baro.png'")
    s = s.replace("'https://xn--wk0bn7yi8h24iszc.com/stamp-keungil.png'", "'https://brizymedia.github.io/baro-event/assets/img/stamp-baro.png'")
    s = s.replace('src="stamp-keungil\\.png', 'src="assets\\/img\\/stamp-baro\\.png')
    return s


def servers(s):
    s = re.sub(r"'https://script\.google\.com/macros/s/AKfycbwgO5Ry[A-Za-z0-9_-]+/exec'", repr(BARO_CONTRACT) if BARO_CONTRACT else "''", s)
    return s


def port(name, extra=None):
    s = open(os.path.join(SRC, name), encoding='utf-8').read()
    s = rep_all(s, COMMON, name)
    s = rep_all(s, NAV, name)
    s = dedupe_nav(s)
    s = logo_fix(s)
    s = no_stamp(s)
    s = servers(s)
    if extra: s = extra(s)
    left = [w for w in ('큰길', '김동길', '광양', '브리지미디어', '788101', 'xn--wk0', 'keungil', 'KG<', '>KG') if w in s]
    open(os.path.join(SITE, name), 'w', encoding='utf-8', newline='\n').write(s)
    print(name, '남은 큰길 흔적:', left or '없음')


def quote_extra(s):
    # 직인 안내문 · 메일 속 직인 칸 빼기
    s = re.sub(r'\s*<p class="no-print" id="stamp-note".*?</p>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<td valign="middle" align="right" width="66" style="padding-left:6px;">\s*<img src="\$\{직인\}".*?</td>', '', s, count=1, flags=re.S)
    a = s.index('const CATALOG = ['); b = s.index('];', a) + 2
    s = s[:a] + CATALOG + s[b:]
    s = s.replace('<title>행사 자동 견적서 — 무대·음향·LED·조명·MC 섭외 비용 즉시 계산 | 바로기획</title>',
                  '<title>자동 견적서 — 체육대회 · 축제 · 커팅식 · 음향 · 천막 | 바로기획</title>')
    s = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="안산 · 화성 · 경기 행사 견적을 항목만 골라 바로 문의하세요. 체육대회 · 지역축제 · 커팅식 · 송년회 · 물놀이 축제, 음향 · 무대 · 천막 · MC 섭외까지. 바로기획 010-2758-0655">\n  <meta name="robots" content="noindex,nofollow">', s, count=1)
    return s


def contract_extra(s):
    # 큰길 로고(투명 PNG)를 하얗게 칠하던 필터 — 바로기획 마크는 제 색 그대로
    s = s.replace('.brand img{ height:1.8rem;filter:brightness(0) invert(1) drop-shadow(0 0 6px rgba(201,162,75,.5)); }', '.brand img{ height:1.8rem;border-radius:.4rem; }')
    # 인감 파일이 없으면 가짜 도장을 그리지 않고 「(인)」 자리만 둔다
    s = re.sub(r"const STAMP_SRC = 'assets/img/stamp-baro\.png';[^\n]*", "const STAMP_SRC = 'assets/img/stamp-baro.png';  // 대표님 인감(투명 PNG)을 이 이름으로 넣으면 찍힌다. 없으면 「(인)」", s)
    s = s.replace('return `<div class="seal-css">${esc(C.co.brand||C.co.name)}<br>대표<br>인</div>`;', 'return `<div class="seal-none">(인)</div>`;')
    s = s.replace('<span class="stamp-flag ok">날인 완료</span>', "${stampOK?'<span class=\"stamp-flag ok\">날인 완료</span>':''}")
    s = s.replace('  #paper .stamp-flag.ok{', '  #paper .party .sig-slot .box .seal-none{ position:absolute;right:6mm;top:50%;transform:translateY(-50%);color:#9CA3AF;font-size:10pt; }\n  #paper .stamp-flag.ok{', 1)
    s = s.replace('<title>전자계약서 — 바로기획</title>', '<title>전자계약서 — 바로기획</title>\n<meta name="robots" content="noindex,nofollow">')
    return s


def statement_extra(s):
    # 상호와 브랜드가 같아 「바로기획 (바로기획)」으로 두 번 나오는 것 막기
    s = s.replace("우리.name + ' (' + 우리.brand + ')'", "우리.name")
    s = s.replace("esc(우리.name) + ' (' + esc(우리.brand) + ')'", "esc(우리.name)")
    s = s.replace('alt="바로기획 대표 직인">', 'alt="바로기획 대표 직인" onerror="this.remove()">')
    s = s.replace('공급자 칸에 대표 직인이 찍혀 나갑니다. 인쇄 · PDF · 메일 발송본에도 그대로 들어갑니다.', '인쇄하거나 PDF 로 저장해 보내시면 됩니다.')
    return s


UPLOAD_CATS = """const 갤러리항목 = [
  { slug: 'sports',   name: '체육대회 · 명랑운동회',
    desc: '기업 · 교회 · 학교 · 동문회 체육대회 현장입니다. 종목 구성과 게임도구, 음향과 전문 MC까지 바로기획이 준비했습니다.' },
  { slug: 'festival', name: '지역축제 · 주민행사',
    desc: '주민자치회 · 마을 축제 현장입니다. 무대와 음향, 체험 부스와 공연을 함께 준비했습니다.' },
  { slug: 'show',     name: '공연 · 점등식 · 캠프',
    desc: '점등식과 거리 공연, 캠프파이어와 야간 레크리에이션 현장입니다.' },
  { slug: 'water',    name: '물놀이 축제',
    desc: '대형 풀장 · 워터슬라이드 · 영유아존을 갖춘 물놀이 축제와 학교 물놀이 행사 현장입니다.' },
  { slug: 'ceremony', name: '커팅식 · 오픈 이벤트',
    desc: '개업 · 이전 · 개원 · 준공 커팅식과 오픈 이벤트 현장입니다. 레드카펫 · 오색띠 · 풍선장식까지 준비했습니다.' },
  { slug: 'gear',     name: '음향 · 장비 · 장식',
    desc: '음향 · 무대 · 천막 · 게임도구 · 풍선장식 등 장비와 행사용품 현장입니다.' },
];"""

UPLOAD_REGIONS = """const 지역표 = [
  ['안산', ['안산', '상록', '단원', '대부도', '와스타디움', '와~스타디움']], ['화성', ['화성', '새솔', '남양', '봉담', '향남', '송산']], ['동탄', ['동탄']],
  ['시흥', ['시흥', '배곧', '정왕', '물왕']], ['수원', ['수원', '광교', '영통', '팔달']], ['용인', ['용인', '수지', '기흥', '처인']],
  ['안양', ['안양', '평촌']], ['광명', ['광명']], ['평택', ['평택', '송탄']], ['군포', ['군포', '산본']], ['의왕', ['의왕']], ['오산', ['오산']],
  ['부천', ['부천']], ['인천', ['인천', '송도']], ['서울', ['서울']],
];"""


def upload_extra(s):
    a = s.index('const 갤러리항목 = ['); b = s.index('];', a) + 2
    s = s[:a] + UPLOAD_CATS + s[b:]
    a = s.index('const 지역표 = ['); b = s.index('];', a) + 2
    s = s[:a] + UPLOAD_REGIONS + s[b:]
    pairs = [
        ("'https://raw.githubusercontent.com/brizymedia/keungil-event/photos/photos/photos.json'", "'https://raw.githubusercontent.com/brizymedia/baro-event/photos/photos/photos.json'"),
        ("'https://cdn.jsdelivr.net/gh/brizymedia/keungil-event@photos/'", "'https://cdn.jsdelivr.net/gh/brizymedia/baro-event@photos/'"),
        ("const 홈주소 = 'https://brizymedia.github.io/baro-event';", "const 홈주소 = 'https://brizymedia.github.io/baro-event';"),
        ("'https://큰길이벤트.com'", "'https://brizymedia.github.io/baro-event'"),
        ("홈주소 + '/gallery.html#' + 갤러리슬러그(이름)", "홈주소 + '/portfolio.html'"),
        ("['순천', '여수', '광양', '고흥', '하동', '남원', '광주', '진주', '통영']", "['안산', '화성', '시흥', '수원', '용인', '안양', '광명', '평택']"),
        ("['무대', '음향', '조명', 'LED']", "['음향', '천막', '게임도구', 'MC']"),
        ("  ['천막',   ['천막', '몽골텐트', '부스']],\n];", "  ['천막',   ['천막', '몽골텐트', '부스', '텐트', '파라솔']],\n  ['게임도구', ['게임', '공굴리기', '줄다리기', '체육용품', '명랑운동회']],\n  ['물놀이', ['물놀이', '풀장', '워터슬라이드', '물대포', '워터밤']],\n  ['풍선장식', ['풍선', '아치', '포토존']],\n  ['레크', ['레크', '레크리에이션', '캠프파이어']],\n];"),
        ("'바로기획 · 전남광주통합특별시 광양'", "'바로기획 · 경기도 안산시 상록구 (2005년부터)'"),
        ("'행사기획 · 무대 · 음향 · LED · 조명 · MC/가수 섭외 · 드론쇼 — 광주·전남·경남 전역'", "'체육대회 · 지역축제 · 커팅식 · 송년회 · 물놀이 축제 · 음향 · 천막 · MC 섭외 — 경기 전역'"),
        ("' 등 광주·전남·경남 어디든 광양에서 출발해 당일 세팅합니다. '", "' 등 경기 어디든 안산에서 출발해 당일 세팅합니다. '"),
        ("(지역 ? 지역 : '전남') + ' 일원에서", "(지역 ? 지역 : '경기') + ' 일원에서"),
        ("'행사기획', '행사대행', '이벤트회사추천', '전남이벤트', '경남이벤트', '광양이벤트', '바로기획'", "'행사기획', '행사대행', '이벤트회사추천', '안산이벤트', '화성이벤트', '경기이벤트', '바로기획'"),
        ('예) 제25회 광양 매화축제', '예) 2026 ○○교회 연합 체육대회'),
        ('예) 광양시 광양읍 일원', '예) 수원 ○○대학교 대운동장'),
        ("'kg_", "'baro_"),
        # 바로기획에는 사진으로 행사 이야기 글을 자동으로 만드는 작업이 없다 — 안내를 사실대로
        ('여기 쓰신 글이 <b style="color:#E3C57E;">홈페이지의 「행사 이야기」 글로 그대로 올라갑니다.</b>\n      고객이 읽고, 네이버·구글·AI 검색에도 잡힙니다. 아래 블로그·인스타 글을 만들 때도 쓰입니다.',
         '여기 쓰신 글은 <b style="color:#E3C57E;">현장사진 페이지의 사진 설명</b>으로 저장되고, 아래 <b style="color:#E3C57E;">블로그 · 인스타 글</b>을 만들 때 쓰입니다.'),
        ('\n      <b>비워두면 글 페이지가 만들어지지 않습니다.</b>', ''),
        ('<b style="color:#a1a1aa;">행사 이야기 글의 대표 이미지</b>와\n        갤러리 칸 표지로 쓰입니다.', '<b style="color:#a1a1aa;">블로그 대표 이미지</b>로 쓰기 좋게 만들어 드립니다.'),
        ("    '천막':   '천막·부스 설치',\n  };", "    '천막':   '본부석 · 응원석 천막과 테이블 · 의자 설치',\n    '게임도구': '참가 인원 · 연령대에 맞춘 종목과 게임도구 준비',\n    '물놀이': '대형 풀장 · 워터슬라이드 · 영유아존 설치와 안전요원 배치',\n    '풍선장식': '풍선 아치 · 포토존 장식',\n    '레크':   '레크리에이션 강사와 함께하는 단체 프로그램',\n  };"),
        ("'천막': ['천막대여'] };", "'천막': ['천막대여'], '게임도구': ['체육대회게임', '명랑운동회'], '물놀이': ['물놀이축제', '워터슬라이드'], '풍선장식': ['풍선장식', '풍선아치'], '레크': ['레크리에이션', '레크강사'] };"),
        ("(무대·음향·LED·조명·MC·가수)", "(음향·천막·게임도구·MC·물놀이·풍선장식)"),
        ("(무대·음향·LED·조명·MC·가수·드론쇼)", "(음향·천막·게임도구·MC·물놀이·풍선장식)"),
    ]
    for x, y in pairs: s = s.replace(x, y)
    s = re.sub(r'placeholder="예\) 순천만 일원에서[^"]*"', 'placeholder="예) 6개 교회 600여 명이 모인 연합 체육대회. 입장 아치와 본부석 천막, 음향과 게임도구, 전문 MC가 하루를 진행했습니다."', s)
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.2rem;height:2\.2rem;[^"]*">KG</span>', LOGO_S, s)
    s = s.replace('<title>행사 사진 올리기 — 바로기획</title>', '<title>행사 사진 올리기 — 바로기획</title>\n  <meta name="robots" content="noindex,nofollow">')
    return s


if __name__ == '__main__':
    port('upload.html', upload_extra)
    port('quote.html', quote_extra)
    port('contract.html', contract_extra)
    port('statement.html', statement_extra)

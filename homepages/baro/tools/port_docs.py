# -*- coding: utf-8 -*-
"""
큰길이벤트기획의 업무 도구를 이 회사용으로 옮긴다.

  python tools/port_docs.py [큰길이벤트 레포 경로]      (기본 ~/Documents/클로드코드)

옮기는 것: 견적서(quote.html + quote-catalog.js) · 전자계약서 · 거래명세서 · 사진 올리기 ·
          행사 일정(schedule.html) · 서버 코드 2개(apps-script/contract · gallery) · 대표 전용 업무 문서함(office.html)
원본을 고친 뒤 다시 돌리면 같은 규칙으로 다시 옮긴다. 결과 HTML 은 손으로 고치지 말고 여기 규칙으로 넣을 것.

▶ 다른 회사에 쓰려면 「회사 설정」 칸만 바꾸면 된다(아래 「공통 규칙」은 그대로).
"""
import os, re, sys

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/Documents/클로드코드')
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ════════════════════════════ 회사 설정 ════════════════════════════
ID       = 'baro'                                   # 기기 저장 이름 · 유입 표시(data-site) 앞글자
NAME     = '바로기획'
NAME_EN  = 'BARO PLANNING'
CEO      = '김선호'
BIZNO    = '174-22-00074'
ADDR     = '경기도 안산시 상록구 장화1길 56, 103호 (사동)'
ADDR_S   = '경기도 안산시 상록구 장화1길 56, 103호'
TEL      = '010-2758-0655'
EMAIL    = 'mot2256@naver.com'
REPO     = 'brizymedia/baro-event'
HOME     = 'https://brizymedia.github.io/baro-event'
CODE_PRE = 'BR-'                                    # 계약 번호 앞글자
BLOG     = 'https://blog.naver.com/mot2256789'

# 서버(앱스 스크립트) — 배포하면 주소를 넣고 다시 돌린다. 비어 있으면 서버 없이 동작(저장함은 이 기기만, 계약은 긴 링크).
CONTRACT_URL = 'https://script.google.com/macros/s/AKfycby2Eo9fIIHFNkwLs89IrsIAojhlDHlPuU151K9ohcHrAzAhmyGM57gnD94_Z-jWDy-8/exec'   # 2026-10-01 어대리 배포 (gilauto325)
GALLERY_URL  = 'https://script.google.com/macros/s/AKfycbzYVe-C3O0Nu_3WysH4A7qmK7jp6fNQpzJoPmcGiHgPrJoIQ2wbd5L91VumgVG2OOS08A/exec'   # 비밀번호는 서버 속성에만

LOGO_FILE = 'assets/img/logo-mark.svg'              # 머리글에 쓰는 네모 마크
MAIL_LOGO = 'https://brizymedia.github.io/baro-event/assets/img/logo-h-white.png'   # 메일 머리(어두운 바탕용 가로 로고)
STAMP     = 'assets/img/stamp-baro.png'             # 대표 인감(투명 PNG). 파일이 없으면 「(인)」 자리만

# 색: 큰길이벤트 주황 → 이 회사 색 (앞 = 큰길 원래 색, 뒤 = 이 회사 색)
COLORS = [
    ('#F59E0B', '#C9A24B'), ('#FBBF24', '#E3C57E'), ('#D97706', '#B08A36'), ('#B45309', '#8F6E22'),
    ('#FCD34D', '#EBD39A'), ('#a05c00', '#8F6E22'), ('#09090b', '#081427'), ('#0B0A10', '#081427'),
    ('#16141C', '#0E1F3F'), ('#131317', '#0E1F3F'),
    ('rgba(245,158,11', 'rgba(201,162,75'), ('rgba(251,191,36', 'rgba(227,197,126'),
    ('rgba(9,9,11', 'rgba(8,20,39'), ('rgba(11,10,16', 'rgba(8,20,39'),
]
# 업무 문서함(office.html) 색
OFFICE = dict(bg='#081427', card='#0E1F3F', line='rgba(227,197,126,.16)', accent='#C9A24B', accent2='#E3C57E', ink='#081427')

# 예시 문구(견적서 · 계약서 입력칸 회색 글씨)
EXAMPLES = [
    ('예) 광양시청 / ○○총동문회', '예) 안산시 ○○동 주민자치회 / ○○교회'),
    ('예) 광양시 광양읍 일원', '예) 안산 와~스타디움 보조경기장'),
    ('예) 제25회 광양 매화축제', '예) 2026 ○○ 한마음 체육대회'),
    ('예) 고흥군청 문화관광과', '예) 화성시 새솔동 주민자치회'),
    ('고흥군 녹동항 일원', '화성 새솔동 수노을중앙공원'),
    ('2026 녹동바다불꽃축제 무대·음향 운영', '2026 수노을 물놀이축제 운영'),
    ('2026 녹동바다불꽃축제 무대음향 운영', '2026 수노을 물놀이축제 운영'),
    ('음향 · 조명 · LED · 무대', '체육대회 · 축제 · 음향 · 무대'),
    ("spec:'전남 외 지역'", "spec:'경기 외 지역'"),
    ('예: 2026 진향제', '예: 2026 ○○교회 연합 체육대회'),          # 행사 일정
    ('예: 광양읍 공설운동장', '예: 안산 와~스타디움'),
    ('예: 한국항만물류고등학교', '예: ○○동 주민자치회'),
]

QUOTE_TITLE = '자동 견적서 — 체육대회 · 축제 · 커팅식 · 음향 · 천막 | 바로기획'
QUOTE_DESC  = '안산 · 화성 · 경기 행사 견적을 항목만 골라 바로 문의하세요. 체육대회 · 지역축제 · 커팅식 · 송년회 · 물놀이 축제, 음향 · 무대 · 천막 · MC 섭외까지. 바로기획 010-2758-0655'

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

# 사진 올리기 — 사진 칸(현장사진 페이지 분류)
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

# 사진 올리기 — 행사명 · 장소 글자에서 지역 찾기
UPLOAD_REGIONS = """const 지역표 = [
  ['안산', ['안산', '상록', '단원', '대부도', '와스타디움', '와~스타디움']], ['화성', ['화성', '새솔', '남양', '봉담', '향남', '송산']], ['동탄', ['동탄']],
  ['시흥', ['시흥', '배곧', '정왕', '물왕']], ['수원', ['수원', '광교', '영통', '팔달']], ['용인', ['용인', '수지', '기흥', '처인']],
  ['안양', ['안양', '평촌']], ['광명', ['광명']], ['평택', ['평택', '송탄']], ['군포', ['군포', '산본']], ['의왕', ['의왕']], ['오산', ['오산']],
  ['부천', ['부천']], ['인천', ['인천', '송도']], ['서울', ['서울']],
];"""

# 사진 올리기 — 블로그 · 인스타 글을 만들 때 쓰는 이 회사 말
UPLOAD_PAIRS = [
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
    ("    '천막':   '천막·부스 설치',\n  };", "    '천막':   '본부석 · 응원석 천막과 테이블 · 의자 설치',\n    '게임도구': '참가 인원 · 연령대에 맞춘 종목과 게임도구 준비',\n    '물놀이': '대형 풀장 · 워터슬라이드 · 영유아존 설치와 안전요원 배치',\n    '풍선장식': '풍선 아치 · 포토존 장식',\n    '레크':   '레크리에이션 강사와 함께하는 단체 프로그램',\n  };"),
    ("'천막': ['천막대여'] };", "'천막': ['천막대여'], '게임도구': ['체육대회게임', '명랑운동회'], '물놀이': ['물놀이축제', '워터슬라이드'], '풍선장식': ['풍선장식', '풍선아치'], '레크': ['레크리에이션', '레크강사'] };"),
    ("(무대·음향·LED·조명·MC·가수)", "(음향·천막·게임도구·MC·물놀이·풍선장식)"),
    ("(무대·음향·LED·조명·MC·가수·드론쇼)", "(음향·천막·게임도구·MC·물놀이·풍선장식)"),
]
UPLOAD_PLACEHOLDER = '예) 6개 교회 600여 명이 모인 연합 체육대회. 입장 아치와 본부석 천막, 음향과 게임도구, 전문 MC가 하루를 진행했습니다.'

# 머리글 메뉴: 큰길이벤트 주소 → 이 회사 페이지
NAV_SITE = [
    ('href="index.html#services"', 'href="service.html"'),
    ('href="index.html#portfolio"', 'href="portfolio.html"'),
    ('href="index.html#gallery"', 'href="portfolio.html"'),
    ('href="index.html#contact"', 'href="contact.html"'),
    ('href="/blog/"', 'href="notice.html"'),
    ('>행사이력</a>', '>현장사진</a>'),
    ('>블로그</a>', '>공지 · 블로그</a>'),
]
GALLERY_PAGE = 'portfolio.html'                     # 사진이 모이는 페이지
# ════════════════════════════ 회사 설정 끝 ════════════════════════════


def common():
    return [
        ('큰길이벤트기획 (주식회사 브리지미디어)', NAME),
        (' <span style="color:#9ca3af;">(주식회사 브리지미디어)</span>', ''),
        ('주식회사 브리지미디어 대표 직인', NAME + ' 대표 직인'),
        ('(예금주: 주식회사 브리지미디어)', ''),
        ('주식회사 브리지미디어', NAME),
        ('큰길이벤트기획', NAME),
        ('[큰길이벤트]', '[' + NAME + ']'),
        ('큰길이벤트.com/quote.html', HOME.replace('https://', '') + '/quote.html'),
        ('큰길이벤트.com', HOME.replace('https://', '')),
        ('김동길', CEO),
        ('813-81-02252', BIZNO),
        ("corp:'204611-0065269'", "corp:''"),
        ('전남광주통합특별시 광양시 광양읍 강변동길 1, 2층', ADDR),
        ('전남광주통합특별시 광양시 광양읍 강변동길 1', ADDR_S),
        ('1533-7295', TEL),
        ('gilcaro@naver.com', EMAIL),
        ("'KB국민은행 788101-01-397776 '", "''"),
        ("bank:'KB국민은행 788101-01-397776 '", "bank:''"),
        ("'KG-'", "'" + CODE_PRE + "'"),
        ('data-site="keungil"', 'data-site="' + ID + '"'),
        ('keungil-quote-box', ID + '-quote-box'),
        ('keungil-contract', ID + '-contract'),
        ('keungil-statement', ID + '-statement'),
        ('keungil-sched', ID + '-sched'),
        ('우리(큰길)', '우리(' + NAME + ')'),
    ] + EXAMPLES + [
        # 아이콘 · 파비콘
        ('<link rel="icon" href="/favicon.ico" sizes="32x32">\n', ''),
        ('href="/favicon.svg"', 'href="assets/img/favicon.svg"'),
        ('<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n', ''),
        ('  <link rel="alternate" type="application/rss+xml" title="' + NAME + ' 소식" href="/rss.xml">\n', ''),
        ('src="logo-kgm-transparent.png"', 'src="' + LOGO_FILE + '"'),
        ('src="/quote-catalog.js"', 'src="quote-catalog.js"'),
    ] + COLORS


def nav():
    return NAV_SITE + [
        ('href="/stories/"', 'href="stories/"'),
        ('href="/quote.html', 'href="quote.html'), ('href="/contract.html', 'href="contract.html'),
        ('href="/statement.html', 'href="statement.html'), ('href="/schedule.html', 'href="schedule.html'),
        ('href="/"', 'href="index.html"'),
        ('TOTAL EVENT AGENCY', NAME_EN),
    ]


def img(size, radius):
    return '<img src="' + LOGO_FILE + '" alt="" style="width:' + size + ';height:' + size + ';border-radius:' + radius + ';display:block">'


def logo_fix(s):
    # 「KG」 네모 → 이 회사 마크
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.3rem;height:2\.3rem;[^"]*">KG</span>', img('2.3rem', '.6rem'), s)
    s = re.sub(r'<span style="display:grid;place-items:center;width:2\.(1|2)rem;height:2\.(1|2)rem;[^"]*">KG</span>', img('2.1rem', '.55rem'), s)
    s = re.sub(r'<span style="display:inline-block;width:32px;height:32px;line-height:32px;text-align:center;\s*background:[^;]+;[^"]*">KG</span>\s*<span style="[^"]*">' + re.escape(NAME) + '</span>',
               '<img src="' + MAIL_LOGO + '" height="32" alt="' + NAME + '" style="vertical-align:middle;">', s)
    mark = '<img src="' + LOGO_FILE + '" alt="" style="width:26px;height:26px;border-radius:6px;vertical-align:-7px;margin-right:6px">'
    s = re.sub(r'<a class="brand" href="(?:/|index\.html)"><i>KG</i> ([^<]*)</a>', lambda m: '<a class="brand" href="index.html">' + mark + m.group(1) + '</a>', s)
    return s


def no_stamp(s):
    s = s.replace('<img class="stamp" src="stamp-keungil.png" alt="' + NAME + ' 대표 직인" onerror="this.style.display=\'none\'">', '')
    s = s.replace("'stamp-keungil.png'", "'" + STAMP + "'")
    s = s.replace("'https://xn--wk0bn7yi8h24iszc.com/stamp-keungil.png'", "'" + HOME + '/' + STAMP + "'")
    s = s.replace('src="stamp-keungil\\.png', 'src="' + STAMP.replace('/', '\\/').replace('.png', '\\.png'))
    return s


def servers(s):
    s = re.sub(r"'https://script\.google\.com/macros/s/AKfycbwgO5Ry[A-Za-z0-9_-]+/exec'", "'" + CONTRACT_URL + "'", s)
    s = s.replace("const 서버주소_기본 = '';", "const 서버주소_기본 = '" + GALLERY_URL + "';")
    return s


def rep(s, pairs):
    for a, b in pairs:
        s = s.replace(a, b)
    return s


TRACES = ('큰길', '김동길', '광양', '브리지미디어', '788101', 'xn--wk0', 'keungil', 'KG<', '>KG', '녹동', '고흥', '전남')


def write(name, s):
    left = [w for w in TRACES if w in s]
    p = os.path.join(SITE, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)
    print(name, '남은 큰길 흔적:', left or '없음')


def port(name, extra=None, out=None):
    s = open(os.path.join(SRC, name), encoding='utf-8').read()
    s = rep(s, common())
    # 큰길이벤트 사이트의 검색엔진 소유확인 태그는 옮기지 않는다(이 사이트 것이 아님)
    s = re.sub(r'\s*<!-- 네이버 서치어드바이저 소유확인 -->', '', s)
    s = re.sub(r'\s*<meta name="(?:naver|google)-site-verification"[^>]*>', '', s)
    s = rep(s, nav())
    s = re.sub(r'\s*<a href="' + re.escape(GALLERY_PAGE) + r'"[^>]*>갤러리</a>', '', s) if GALLERY_PAGE != 'gallery.html' else s
    s = logo_fix(s)
    s = no_stamp(s)
    s = servers(s)
    if extra: s = extra(s)
    write(out or name, s)


def noindex(s, title_tag):
    if 'name="robots"' in s: return s
    return s.replace(title_tag, title_tag + '\n<meta name="robots" content="noindex,nofollow">', 1)


def catalog_extra(s):
    a = s.index('const CATALOG = ['); b = s.index('];', a) + 2
    return s[:a] + CATALOG + s[b:]


def quote_extra(s):
    s = re.sub(r'\s*<p class="no-print" id="stamp-note".*?</p>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<td valign="middle" align="right" width="66" style="padding-left:6px;">\s*<img src="\$\{직인\}".*?</td>', '', s, count=1, flags=re.S)
    s = re.sub(r'<title>[^<]*</title>', '<title>' + QUOTE_TITLE + '</title>', s, count=1)
    s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + QUOTE_DESC + '">', s, count=1)
    # 손님용 견적서는 검색에 나와도 되지만, 관리자 화면 주소가 같아 큰길이벤트처럼 noindex 를 두지 않는다
    return s


def contract_extra(s):
    s = re.sub(r'\.brand img\{ height:1\.8rem;filter:brightness\(0\) invert\(1\)[^}]*\}', '.brand img{ height:1.8rem;border-radius:.4rem; }', s)
    s = re.sub(r"const STAMP_SRC = '" + re.escape(STAMP) + r"';[^\n]*", "const STAMP_SRC = '" + STAMP + "';  // 대표님 인감(투명 PNG)을 이 이름으로 넣으면 찍힌다. 없으면 「(인)」", s)
    s = s.replace('return `<div class="seal-css">${esc(C.co.brand||C.co.name)}<br>대표<br>인</div>`;', 'return `<div class="seal-none">(인)</div>`;')
    s = s.replace('<span class="stamp-flag ok">날인 완료</span>', "${stampOK?'<span class=\"stamp-flag ok\">날인 완료</span>':''}")
    s = s.replace('  #paper .stamp-flag.ok{', '  #paper .party .sig-slot .box .seal-none{ position:absolute;right:6mm;top:50%;transform:translateY(-50%);color:#9CA3AF;font-size:10pt; }\n  #paper .stamp-flag.ok{', 1)
    return noindex(s, '<title>전자계약서 — ' + NAME + '</title>')


def statement_extra(s):
    s = s.replace("우리.name + ' (' + 우리.brand + ')'", "우리.name")
    s = s.replace("esc(우리.name) + ' (' + esc(우리.brand) + ')'", "esc(우리.name)")
    s = s.replace('alt="' + NAME + ' 대표 직인">', 'alt="' + NAME + ' 대표 직인" onerror="this.remove()">')
    s = s.replace('공급자 칸에 대표 직인이 찍혀 나갑니다. 인쇄 · PDF · 메일 발송본에도 그대로 들어갑니다.', '인쇄하거나 PDF 로 저장해 보내시면 됩니다.')
    return s


def schedule_extra(s):
    return s


def upload_extra(s):
    a = s.index('const 갤러리항목 = ['); b = s.index('];', a) + 2
    s = s[:a] + UPLOAD_CATS + s[b:]
    a = s.index('const 지역표 = ['); b = s.index('];', a) + 2
    s = s[:a] + UPLOAD_REGIONS + s[b:]
    pairs = [
        ("'https://raw.githubusercontent.com/brizymedia/keungil-event/photos/photos/photos.json'", "'https://raw.githubusercontent.com/" + REPO + "/photos/photos/photos.json'"),
        ("'https://cdn.jsdelivr.net/gh/brizymedia/keungil-event@photos/'", "'https://cdn.jsdelivr.net/gh/" + REPO + "@photos/'"),
        ("'https://큰길이벤트.com'", "'" + HOME + "'"),
        ("홈주소 + '/gallery.html#' + 갤러리슬러그(이름)", "홈주소 + '/" + GALLERY_PAGE + "'"),
        ("'kg_", "'" + ID + "_"),
        # 이 회사에는 사진으로 행사 이야기 글을 자동으로 만드는 작업이 없다 — 안내를 사실대로
        ('여기 쓰신 글이 <b style="color:' + OFFICE['accent2'] + ';">홈페이지의 「행사 이야기」 글로 그대로 올라갑니다.</b>\n      고객이 읽고, 네이버·구글·AI 검색에도 잡힙니다. 아래 블로그·인스타 글을 만들 때도 쓰입니다.',
         '여기 쓰신 글은 <b style="color:' + OFFICE['accent2'] + ';">현장사진 페이지의 사진 설명</b>으로 저장되고, 아래 <b style="color:' + OFFICE['accent2'] + ';">블로그 · 인스타 글</b>을 만들 때 쓰입니다.'),
        ('\n      <b>비워두면 글 페이지가 만들어지지 않습니다.</b>', ''),
        ('<b style="color:#a1a1aa;">행사 이야기 글의 대표 이미지</b>와\n        갤러리 칸 표지로 쓰입니다.', '<b style="color:#a1a1aa;">블로그 대표 이미지</b>로 쓰기 좋게 만들어 드립니다.'),
    ] + UPLOAD_PAIRS
    s = rep(s, pairs)
    s = re.sub(r'placeholder="예\) 순천만 일원에서[^"]*"', 'placeholder="' + UPLOAD_PLACEHOLDER + '"', s)
    return noindex(s, '<title>행사 사진 올리기 — ' + NAME + '</title>')


# ── 서버 코드(앱스 스크립트) — 형님 구글 계정으로 배포한다 ──
def port_servers():
    c = open(os.path.join(SRC, 'apps-script/contract/Code.gs'), encoding='utf-8').read()
    c = rep(c, [
        (' * 큰길이벤트기획 — 전자계약 서버 (Google Apps Script)', ' * ' + NAME + ' — 전자계약 서버 (큰길이벤트기획 계약 서버를 옮긴 것) (Google Apps Script)'),
        ("const COMPANY_EMAIL    = 'gilauto325@gmail.com';    //", "const COMPANY_EMAIL    = '" + EMAIL + "';    //"),
        ("const ROOT_FOLDER_NAME = '큰길이벤트기획 계약서';", "const ROOT_FOLDER_NAME = '" + NAME + " 계약서';"),
        ("const COMPANY_NAME     = '큰길이벤트기획';", "const COMPANY_NAME     = '" + NAME + "';"),
        ("service: 'keungil-contract'", "service: '" + ID + "-contract'"),
        ('const recipients = uniq_([COMPANY_EMAIL, to.company', 'const recipients = uniq_([COMPANY_EMAIL, MANAGER_EMAIL, to.company'),
    ])
    c = c.replace("    // 서명본 사본을 항상 받을 주소 (계약서의 co.email 과 별개로 무조건 수신)\n",
                  "    // 서명본 사본을 항상 받을 주소 (계약서의 co.email 과 별개로 무조건 수신)\nconst MANAGER_EMAIL    = 'gilauto325@gmail.com'; // 관리하는 큰길브리지도 사본을 받는다 (빼려면 '' )\n", 1)
    c = c.replace('형님과 직원이', '대표님과 직원이').replace('형님 암호(BOX_PW)', '대표님 암호(BOX_PW)')
    assert 'MANAGER_EMAIL    =' in c, '계약 서버: MANAGER_EMAIL 넣을 자리를 못 찾음'
    write('apps-script/contract/Code.gs', c)
    g = open(os.path.join(SRC, 'apps-script/gallery/Code.gs'), encoding='utf-8').read()
    g = rep(g, [
        (' * 큰길이벤트기획 · 행사 사진 업로드 서버', ' * ' + NAME + ' · 행사 사진 업로드 서버 (큰길이벤트기획 것을 옮긴 것)'),
        ('GITHUB_REPO    brizymedia/keungil-event', 'GITHUB_REPO    ' + REPO),
        ("'큰길이벤트기획 사진 업로드 서버'", "'" + NAME + " 사진 업로드 서버'"),
        ("'keungil-photo-uploader'", "'" + ID + "-photo-uploader'"),
    ])
    write('apps-script/gallery/Code.gs', g)


# ── 대표 전용 업무 문서함 ──
def office():
    O = OFFICE
    tools = [
        ('견적 · 계약', [
            ('quote.html?admin=1', '견적서 발행', '항목을 골라 견적서를 만들고 메일 · 인쇄 · PDF 로 보냅니다. 「견적서 저장함」 단추로 저장 · 찾기 · 불러오기.'),
            ('quote.html', '손님용 자동 견적서', '고객이 항목을 골라 문의하는 화면입니다. 고객에게는 이 주소를 보내세요(금액 · 직인은 안 보입니다).'),
            ('contract.html?admin=1', '전자계약서', '견적서에서 넘어오거나 직접 써서 서명 링크를 만듭니다. 고객은 폰으로 서명하고, PDF 가 메일로 옵니다.'),
            ('statement.html?admin=1', '거래명세서', '행사가 끝난 뒤 견적서에서 「이 견적으로 거래명세서 작성」을 누르면 내용이 그대로 넘어옵니다.'),
        ]),
        ('행사 준비', [
            ('schedule.html', '행사 일정 · 체크리스트', '월간 일정표와 행사별 챙길 품목. 직원과 같은 목록을 봅니다(직원 암호로는 일정만 열림).'),
            ('upload.html', '사진 올리기 + 블로그 · 인스타 글', '현장 사진을 올리면 ' + GALLERY_PAGE.replace('.html', '') + ' 페이지에 붙고, 블로그 · 인스타 글을 같이 만들어 줍니다.'),
        ]),
        ('홈페이지 · 검색', [
            ('stories/', '행사 이야기', '행사 한 편씩 준비 과정과 사진을 기록한 글입니다. 검색 · AI 검색에 잡히는 글입니다.'),
            ('areas/', '지역 페이지', '지역별 이동 시간과 그 지역에서 한 행사. 「○○ 행사대행」 검색을 노립니다.'),
            ('llms.txt', 'AI 검색 안내문 (llms.txt)', '챗GPT · 퍼플렉시티 같은 AI 가 회사 정보를 정확히 읽도록 정리한 글입니다.'),
            ('sitemap.xml', '사이트맵', '검색엔진에 알려 주는 페이지 목록입니다.'),
            ('https://www.ai-make.co.kr/stats/', '유입 현황', '어디서 몇 명이 들어왔는지(네이버 · 구글 · AI 검색 · 카톡) 큰길브리지가 함께 봅니다.'),
        ]),
    ]
    cards = ''
    for title, items in tools:
        cards += '<section class="grp"><h2>' + title + '</h2><div class="cards">'
        for href, name, desc in items:
            ext = href.startswith('http')
            cards += ('<a class="card" href="' + href + '"' + (' target="_blank" rel="noopener"' if ext else '') + '><b>' + name +
                      ('<i>↗</i>' if ext else '<i>→</i>') + '</b><span>' + desc + '</span><code>' + href.replace('https://', '') + '</code></a>')
        cards += '</div></section>'
    flow = ['문의가 오면 메일로 알림', '견적서 발행 · 저장', '전자계약 서명', '행사 일정 · 체크리스트', '행사 진행', '사진 올리기 · 블로그 글', '거래명세서']
    flow_html = ''.join('<li><em>' + str(i + 1) + '</em>' + f + '</li>' for i, f in enumerate(flow))
    html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex,nofollow">
<title>업무 문서함 — {NAME} 대표 전용</title>
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.min.css">
<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="{ID}"></script>
<style>
*,*::before,*::after{{box-sizing:border-box}}[hidden]{{display:none!important}}
body,h1,h2,p,ol{{margin:0}}
body{{background:{O['bg']};color:#fff;font-family:'Pretendard',system-ui,'Malgun Gothic',sans-serif;word-break:keep-all;-webkit-font-smoothing:antialiased;line-height:1.65}}
a{{color:inherit;text-decoration:none}}
.top{{position:sticky;top:0;z-index:5;background:{O['bg']}ee;backdrop-filter:blur(12px);border-bottom:1px solid {O['line']}}}
.top div{{max-width:64rem;margin:0 auto;padding:.85rem 1.25rem;display:flex;align-items:center;gap:.6rem;font-weight:800}}
.top img{{width:28px;height:28px;border-radius:7px}}
.top small{{margin-left:auto;font-weight:600;color:#9aa3b5;font-size:.78rem}}
.wrap{{max-width:64rem;margin:0 auto;padding:2rem 1.25rem 4rem}}
h1{{font-size:clamp(1.6rem,4.5vw,2.3rem);font-weight:900;letter-spacing:-.02em}}
h1 em{{font-style:normal;color:{O['accent2']}}}
.lead{{color:#aab2c3;margin-top:.6rem;font-size:.95rem}}
.flow{{list-style:none;padding:0;margin:1.6rem 0 0;display:flex;flex-wrap:wrap;gap:.45rem}}
.flow li{{background:{O['card']};border:1px solid {O['line']};border-radius:999px;padding:.38rem .85rem .38rem .4rem;font-size:.82rem;display:flex;align-items:center;gap:.45rem}}
.flow em{{font-style:normal;display:grid;place-items:center;width:1.45rem;height:1.45rem;border-radius:50%;background:{O['accent']};color:{O['ink']};font-weight:800;font-size:.75rem}}
.grp{{margin-top:2.2rem}}
.grp h2{{font-size:1rem;color:{O['accent2']};font-weight:800;margin-bottom:.8rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:.8rem}}
.card{{display:flex;flex-direction:column;gap:.4rem;background:{O['card']};border:1px solid {O['line']};border-radius:14px;padding:1.05rem 1.1rem;transition:.2s}}
.card:hover{{border-color:{O['accent']};transform:translateY(-2px)}}
.card b{{font-size:1.02rem;display:flex;justify-content:space-between;gap:.5rem}}
.card b i{{font-style:normal;color:{O['accent']}}}
.card span{{font-size:.85rem;color:#b9c0cf}}
.card code{{margin-top:auto;font-size:.72rem;color:#7d879b;font-family:ui-monospace,Consolas,monospace;word-break:break-all}}
.box{{margin-top:2.2rem;background:{O['card']};border:1px solid {O['line']};border-radius:14px;padding:1.1rem 1.2rem}}
.box h2{{font-size:1rem;font-weight:800;margin-bottom:.6rem}}
.box p,.box li{{font-size:.88rem;color:#c3c9d6}}
.box ul{{margin:.3rem 0 0;padding-left:1.1rem}}
.st{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.6rem;margin-top:.4rem}}
.st div{{border:1px solid {O['line']};border-radius:10px;padding:.65rem .8rem;font-size:.84rem}}
.st b{{display:block;margin-bottom:.15rem}}
.ok{{color:#5BE39B}}.no{{color:#FFB54A}}.wait{{color:#9aa3b5}}
.foot{{margin-top:2.5rem;font-size:.8rem;color:#7d879b;text-align:center}}
</style>
</head>
<body>
<header class="top"><div><img src="{LOGO_FILE}" alt="">{NAME} 업무 문서함<small>대표 전용 · 검색에 나오지 않는 페이지</small></div></header>
<main class="wrap">
  <h1>{NAME} <em>업무 문서함</em></h1>
  <p class="lead">견적부터 계약 · 일정 · 사진 · 명세서까지, 대표님이 쓰시는 화면을 한곳에 모았습니다. 이 주소는 즐겨찾기 해 두세요. 손님에게는 보내지 마세요.</p>
  <ol class="flow">{flow_html}</ol>
  {cards}
  <section class="box"><h2>서버 연결 상태</h2>
    <p>저장함 · 계약 · 일정 · 사진 올리기는 구글 서버를 씁니다. 빨간 표시가 있으면 큰길브리지에 알려 주세요.</p>
    <div class="st">
      <div><b>계약 · 저장함 · 일정 서버</b><span id="s-contract" class="wait">확인 중…</span></div>
      <div><b>사진 올리기 서버</b><span id="s-gallery" class="wait">확인 중…</span></div>
      <div><b>문의 알림</b><span class="ok">홈페이지 문의 · 견적 문의가 {EMAIL} 로 갑니다</span></div>
    </div>
  </section>
  <section class="box"><h2>암호 안내</h2>
    <ul>
      <li><b>보관함 암호</b> — 견적서 저장함 · 행사 일정을 엽니다. 대표님만 아시면 됩니다.</li>
      <li><b>직원 암호</b> — 행사 일정 · 체크리스트만 열립니다(견적 · 계약은 안 열림). 직원에게는 이것만 알려 주세요.</li>
      <li><b>사진 올리기 암호</b> — 사진 올리기 화면에서 씁니다.</li>
      <li>암호는 이 페이지 · 홈페이지 어디에도 적혀 있지 않습니다. 잊으셨으면 큰길브리지(1533-7295)로 연락 주세요. 카톡 · 메일로 암호를 주고받지 마세요.</li>
    </ul>
  </section>
  <section class="box"><h2>홈페이지 글 · 사진 고치기</h2>
    <p>홈페이지 주소 뒤에 <code>?edit=열쇠</code> 를 붙여 들어가면 글을 직접 고칠 수 있습니다(열쇠는 큰길브리지가 문자로 드린 것). 고친 뒤 「저장 파일 받기」로 보내 주시면 반영해 드립니다.</p>
  </section>
  <p class="foot">홈페이지 관리 · 큰길브리지 1533-7295 · www.ai-make.co.kr</p>
</main>
<script>
(function(){{
  var C = '{CONTRACT_URL}', G = '{GALLERY_URL}';
  function show(id, ok, msg){{ var el = document.getElementById(id); el.className = ok ? 'ok' : 'no'; el.textContent = msg; }}
  function ping(url, id, read){{
    if(!url){{ show(id, false, '아직 연결 전 — 서버 배포 대기'); return; }}
    var t = setTimeout(function(){{ show(id, false, '응답이 늦습니다 — 잠시 뒤 새로고침'); }}, 12000);
    fetch(url).then(function(r){{ return r.json(); }}).then(function(j){{ clearTimeout(t); read(j); }})
      .catch(function(){{ clearTimeout(t); show(id, false, '연결 안 됨 — 큰길브리지에 알려 주세요'); }});
  }}
  ping(C, 's-contract', function(j){{
    if(!j || !j.ok){{ show('s-contract', false, '응답 이상'); return; }}
    var m = ['연결됨'];
    m.push(j.box === 'ready' ? '저장함 암호 ✓' : '저장함 암호 미설정');
    if('sched' in j) m.push(j.sched === 'ready' ? '직원 암호 ✓' : '직원 암호 미설정');
    else m.push('일정 기능은 서버 새 버전 필요');
    show('s-contract', j.box === 'ready' && j.sched === 'ready', m.join(' · '));
  }});
  ping(G, 's-gallery', function(j){{ show('s-gallery', !!(j && j.ok), j && j.ok ? ('연결됨' + (j['설정완료'] === false ? ' · 설정 미완료' : '')) : '응답 이상'); }});
}})();
</script>
</body>
</html>
'''
    write('office.html', html)


if __name__ == '__main__':
    port('upload.html', upload_extra)
    port('quote.html', quote_extra)
    port('quote-catalog.js', catalog_extra)
    port('contract.html', contract_extra)
    port('statement.html', statement_extra)
    port('schedule.html', schedule_extra)
    port_servers()
    office()
    import admin_gate                      # 관리자 모드 잠금 화면 (대표 암호 = 계약 서버 BOX_PW)
    admin_gate.apply(os.path.join(SITE, 'office.html'), ID, NAME, CONTRACT_URL, OFFICE)

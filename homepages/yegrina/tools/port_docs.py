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
ID       = 'yegrina'                                # 기기 저장 이름 · 유입 표시(data-site) 앞글자
NAME     = '한국체대 예그리나'
NAME_EN  = 'KNSU YEGRINA'
CEO      = '문춘래'
BIZNO    = '212-91-97106'
ADDR     = '경기도 남양주시 별내면 청학리 346-1, 301호'
ADDR_S   = '경기도 남양주시 별내면 청학리 346-1, 301호'
TEL      = '02-482-1934'
EMAIL    = 'knsuyegrina@naver.com'
REPO     = 'brizymedia/yegrina'
HOME     = 'https://brizymedia.github.io/yegrina'
CODE_PRE = 'YG-'                                    # 계약 번호 앞글자
BLOG     = 'https://blog.naver.com/yegrinai'

# 서버(앱스 스크립트) — 배포하면 주소를 넣고 다시 돌린다. 비어 있으면 서버 없이 동작(저장함은 이 기기만, 계약은 긴 링크).
CONTRACT_URL = ''   # 아직 배포 전 — 형님 구글 계정으로 배포한 뒤 넣는다
GALLERY_URL  = ''   # 〃 (비밀번호는 서버 속성에만)

LOGO_FILE = 'assets/img/favicon.svg'                # 머리글에 쓰는 마크(초록 동그라미)
MAIL_LOGO = 'https://brizymedia.github.io/yegrina/assets/img/logo-mail.png'   # 메일 머리(어두운 바탕용 가로 로고, PNG)
STAMP     = 'assets/img/stamp-yegrina.png'          # 대표 인감(투명 PNG). 파일이 없으면 「(인)」 자리만

# 색: 큰길이벤트 주황 → 이 회사 색 (앞 = 큰길 원래 색, 뒤 = 이 회사 색). 문서 화면 바탕 = 가장 어두운 숲색 #0B3322
COLORS = [
    ('#F59E0B', '#22C55E'), ('#FBBF24', '#4ADE80'), ('#D97706', '#16A34A'), ('#B45309', '#15803D'),
    ('#FCD34D', '#86EFAC'), ('#a05c00', '#15803D'), ('#09090b', '#0B3322'), ('#0B0A10', '#0B3322'),
    ('#16141C', '#12402B'), ('#131317', '#12402B'),
    ('rgba(245,158,11', 'rgba(34,197,94'), ('rgba(251,191,36', 'rgba(74,222,128'),
    ('rgba(9,9,11', 'rgba(11,51,34'), ('rgba(11,10,16', 'rgba(11,51,34'),
]
# 업무 문서함(office.html) 색 — accent2 는 위 COLORS 에서 #FBBF24 가 바뀐 색과 같아야 한다(upload 안내 문구 치환에 쓰임)
OFFICE = dict(bg='#0B3322', card='#12402B', line='rgba(134,239,172,.16)', accent='#22C55E', accent2='#4ADE80', ink='#0B3322')

# 예시 문구(견적서 · 계약서 입력칸 회색 글씨)
EXAMPLES = [
    ('예) 광양시청 / ○○총동문회', '예) ○○어린이집 / ○○교회'),
    ('예) 광양시 광양읍 일원', '예) 남양주 ○○초등학교 운동장'),
    ('예) 제25회 광양 매화축제', '예) 2027 ○○유치원 가족한마음 체육대회'),
    ('예) 고흥군청 문화관광과', '예) ○○유치원 행정실'),
    ('고흥군 녹동항 일원', '남양주 ○○초등학교 운동장'),
    ('2026 녹동바다불꽃축제 무대·음향 운영', '2027 ○○초등학교 운동회 진행'),
    ('2026 녹동바다불꽃축제 무대음향 운영', '2027 ○○초등학교 운동회 진행'),
    ('음향 · 조명 · LED · 무대', '운동회 · 물놀이 · 놀이기구 렌탈'),
    ("spec:'전남 외 지역'", "spec:'서울 · 경기 외 지역'"),
    ('예: 2026 진향제', '예: 2027 ○○교회 전교인 체육대회'),          # 행사 일정
    ('예: 광양읍 공설운동장', '예: ○○초등학교 운동장'),
    ('예: 한국항만물류고등학교', '예: ○○어린이집'),
]

QUOTE_TITLE = '자동 견적서 — 운동회 · 체육대회 · 물놀이 · 놀이기구 렌탈 · 유아체육 | 한국체대 예그리나'
QUOTE_DESC  = '남양주 · 서울 · 경기 어린이 행사 견적을 항목만 골라 바로 문의하세요. 어린이집 · 유치원 · 초등학교 운동회, 교회 전교인 체육대회, 발표회 사회, 여름 물놀이, 에어바운스 · 실내놀이터 렌탈, 유아체육 수업. 한국체대 예그리나 02-482-1934'

CATALOG = """const CATALOG = [
  { group:'행사 진행', items:[
    { id:'p1', name:'어린이집 · 유치원 운동회',   spec:'가족한마음 체육대회 · 실내 체육관 운동회',          unit:'식', price:null },
    { id:'p2', name:'초등학교 운동회',            spec:'준비운동 · 학년별 프로그램 · 단체게임 · 부모님 경기', unit:'식', price:null },
    { id:'p3', name:'교회 전교인 체육대회',       spec:'부서별 · 교구별 게임 · 전교인 단체 경기',           unit:'식', price:null },
    { id:'p4', name:'발표회 · 재롱잔치 사회',     spec:'어린이집 · 유치원 · 놀이학교 발표회 진행',          unit:'식', price:null },
    { id:'p5', name:'여름성경학교 · 물놀이 행사', spec:'에어 워터슬라이드 · 유아용 수영장 · 환영 아치',      unit:'식', price:null },
  ]},
  { group:'유아 예체능 수업', items:[
    { id:'c1', name:'동화체육',             spec:'자사 캐릭터 「예그와 리나」 창작동화 + 신체활동', unit:'회', price:null, qty:true },
    { id:'c2', name:'파라슈트 · 뉴스포츠',  spec:'파도 만들기 · 팝콘 튀기기 등 함께하는 놀이',       unit:'회', price:null, qty:true },
    { id:'c3', name:'유아골프',             spec:'퍼팅 자세부터 차근차근',                          unit:'회', price:null, qty:true },
    { id:'c4', name:'유아 댄스 · 발레',     spec:'유아특기교육',                                    unit:'회', price:null, qty:true },
  ]},
  { group:'놀이기구 · 물놀이 렌탈', items:[
    { id:'h1', name:'에어바운스',            spec:'공기주입식 놀이기구 · 송풍기 포함',                 unit:'동', price:null, qty:true },
    { id:'h2', name:'실내놀이터 구성',       spec:'바운스 · 바이킹 · 자이언트 빅블럭 · 너프건 사격장', unit:'식', price:null },
    { id:'h3', name:'에어 워터슬라이드',     spec:'수영장 기구 일체 · 물 받기 포함',                   unit:'동', price:null, qty:true },
    { id:'h4', name:'유아용 낮은 수영장',    spec:'4 · 5세 어린 친구들용',                              unit:'개', price:null, qty:true },
    { id:'h5', name:'에어아바타',            spec:'꿀벌 등 공기주입 캐릭터',                            unit:'개', price:null, qty:true },
    { id:'h6', name:'민속놀이 기구',         spec:'운동회 · 명절 행사',                                  unit:'식', price:null },
    { id:'h7', name:'환영 아치 · 포토존',    spec:'행사장 입구 · 기념사진',                              unit:'식', price:null },
  ]},
  { group:'운동회 게임도구 · 체육용품', items:[
    { id:'h8', name:'운동회 게임도구',       spec:'대형 공 굴리기 · 깃발 뒤집기 · 풍선 이어달리기 등', unit:'식', price:null },
    { id:'h9', name:'체육용품 · 만국기',     spec:'만국기 · 대형 공 · 점수판',                          unit:'식', price:null },
  ]},
  { group:'천막 · 편의시설', items:[
    { id:'d1', name:'천막',                  spec:'운동회 · 야외 행사 그늘 · 본부석',                   unit:'동', price:null, qty:true },
    { id:'d2', name:'의자',                  spec:'행사용 의자',                                        unit:'개', price:null, qty:true },
  ]},
  { group:'진행 인력', items:[
    { id:'f1', name:'진행 사회자',           spec:'운동회 · 체육대회 · 발표회 진행',                     unit:'명', price:null },
    { id:'f2', name:'진행 선생님 · 스태프',  spec:'게임 진행 · 안전 관리',                              unit:'명', price:null, qty:true },
  ]},
  { group:'기타', items:[
    { id:'g1', name:'운반 · 설치 · 철수',    spec:'행사 당일 설치 · 정리',                              unit:'식', price:null },
    { id:'g2', name:'출장비',                spec:'서울 · 경기 외 지역',                                 unit:'식', price:null },
  ]},
];"""

# 사진 올리기 — 사진 칸(현장사진 페이지 분류). slug = portfolio.html 분류 단추(data-f)와 같게
UPLOAD_CATS = """const 갤러리항목 = [
  { slug: 'event',  name: '운동회 · 체육대회',
    desc: '어린이집 · 유치원 · 초등학교 운동회와 가족한마음 체육대회 현장입니다.' },
  { slug: 'church', name: '교회 행사',
    desc: '교회 전교인 체육대회 · 여름성경학교 현장입니다.' },
  { slug: 'water',  name: '물놀이',
    desc: '에어 워터슬라이드 · 유아용 수영장 · 환영 아치를 갖춘 물놀이 행사 현장입니다.' },
  { slug: 'rental', name: '놀이기구 · 렌탈',
    desc: '에어바운스 · 실내놀이터 · 천막 · 의자 렌탈 현장입니다.' },
  { slug: 'class',  name: '예체능 수업',
    desc: '동화체육 · 파라슈트 · 유아골프 수업 현장입니다.' },
  { slug: 'stage',  name: '발표회 · 무대',
    desc: '어린이집 · 유치원 발표회 사회와 무대 진행 현장입니다.' },
];"""

# 사진 올리기 — 행사명 · 장소 글자에서 지역 찾기
UPLOAD_REGIONS = """const 지역표 = [
  ['남양주', ['남양주', '별내', '다산', '진접', '오남', '호평', '평내', '화도', '와부', '퇴계원']], ['구리', ['구리', '갈매', '인창']], ['의정부', ['의정부', '민락']],
  ['양주', ['양주', '옥정', '덕정']], ['포천', ['포천', '송우']], ['하남', ['하남', '미사', '위례']], ['가평', ['가평', '청평']],
  ['노원', ['노원', '상계', '중계', '하계', '공릉']], ['중랑', ['중랑', '면목', '상봉', '망우', '신내']], ['강동', ['강동', '천호', '명일', '고덕', '길동', '암사']],
  ['도봉', ['도봉', '창동', '방학']], ['광진', ['광진', '구의', '자양']], ['송파', ['송파', '잠실']], ['서울', ['서울']],
];"""

# 사진 올리기 — 블로그 · 인스타 글을 만들 때 쓰는 이 회사 말 (앞 = 원본 글자. common() 치환 뒤 기준이라 회사 이름은 NAME)
UPLOAD_PAIRS = [
    ("['순천', '여수', '광양', '고흥', '하동', '남원', '광주', '진주', '통영']", "['남양주', '구리', '의정부', '양주', '노원', '중랑', '하남', '강동']"),
    ("['무대', '음향', '조명', 'LED']", "['게임도구', 'MC', '놀이기구']"),
    ("  ['천막',   ['천막', '몽골텐트', '부스']],\n];", "  ['천막',   ['천막', '몽골텐트', '부스', '텐트', '의자']],\n  ['게임도구', ['게임', '공굴리기', '줄다리기', '파라슈트', '이어달리기', '체육용품', '만국기']],\n  ['놀이기구', ['에어바운스', '바운스', '놀이기구', '실내놀이터', '빅블럭', '바이킹', '너프건', '에어아바타']],\n  ['물놀이', ['물놀이', '수영장', '풀장', '워터슬라이드', '슬라이드']],\n  ['아치',   ['환영아치', '환영 아치', '아치', '포토존']],\n];"),
    ("  ['워크숍', ['워크숍', '워크샵', '연수']],\n];", "  ['워크숍', ['워크숍', '워크샵', '연수']],\n  ['물놀이 행사', ['물놀이', '성경학교', '수영장']], ['발표회', ['발표회', '재롱잔치']], ['수업', ['수업', '동화체육', '유아체육']],\n];"),
    ("'" + NAME + " · 전남광주통합특별시 광양'", "'" + NAME + " · 경기도 남양주시 별내면 (2014년부터)'"),
    ("'행사기획 · 무대 · 음향 · LED · 조명 · MC/가수 섭외 · 드론쇼 — 광주·전남·경남 전역'", "'유아체육 · 운동회 · 전교인 체육대회 · 발표회 사회 · 물놀이 · 놀이기구 렌탈 — 서울 · 경기'"),
    ("' 등 광주·전남·경남 어디든 광양에서 출발해 당일 세팅합니다. '", "' 등 서울 · 경기 어디든 남양주에서 출발해 당일 아침 일찍 세팅합니다. '"),
    ("(지역 ? 지역 : '전남') + ' 일원에서 진행된 ' + 종류 + '입니다. 현장 여건에 맞춰 장비를 구성하고, 행사 시작 전 리허설로 소리와 조명을 먼저 잡았습니다.'",
     "(지역 ? 지역 : '서울 · 경기') + ' 일원에서 진행된 ' + 종류 + '입니다. 연령 · 인원 · 공간에 맞춰 프로그램을 짜고, 행사 전에 일찍 도착해 장비 자리를 잡고 세팅했습니다.'"),
    ("' 무대·음향·조명 준비, '", "' 프로그램 · 장비 준비, '"),
    ("'행사기획', '행사대행', '이벤트회사추천', '전남이벤트', '경남이벤트', '광양이벤트', '" + NAME + "'", "'어린이행사', '유아체육', '운동회업체', '남양주이벤트', '경기이벤트', '서울이벤트', '한국체대예그리나'"),
    ('예) 제25회 광양 매화축제', '예) 2026 ○○교회 전교인 체육대회'),
    ('예) 광양시 광양읍 일원', '예) 남양주 ○○초등학교 운동장'),
    ("    '천막':   '천막·부스 설치',\n  };", "    '천막':   '천막 · 의자 등 편의시설 설치',\n    '게임도구': '연령 · 인원에 맞춘 게임과 게임도구 준비',\n    '놀이기구': '에어바운스 · 실내놀이터 설치',\n    '물놀이': '에어 워터슬라이드 · 유아용 수영장 설치와 물 받기',\n    '아치':   '환영 아치 · 포토존 꾸미기',\n  };"),
    ("'천막': ['천막대여'] };", "'천막': ['천막대여'], '게임도구': ['운동회게임', '체육대회게임'], '놀이기구': ['에어바운스대여', '실내놀이터대여'], '물놀이': ['물놀이행사', '유아물놀이'], '아치': ['환영아치', '포토존'] };"),
    ("(무대·음향·LED·조명·MC·가수)", "(게임도구·놀이기구·물놀이·MC·천막·아치)"),
    ("(무대·음향·LED·조명·MC·가수·드론쇼)", "(게임도구·놀이기구·물놀이·MC·천막·아치)"),
]
UPLOAD_PLACEHOLDER = '예) 원아 120명과 가족이 함께한 가족한마음 체육대회. 환영 아치와 만국기를 걸고, 영아 동생 게임부터 조부모님 게임까지 진행했습니다.'

# 머리글 메뉴: 큰길이벤트 주소 → 이 회사 페이지
NAV_SITE = [
    ('href="index.html#services"', 'href="service.html"'),
    ('href="index.html#portfolio"', 'href="portfolio.html"'),
    ('href="index.html#gallery"', 'href="portfolio.html"'),
    ('href="index.html#contact"', 'href="contact.html"'),
    ('href="/blog/"', 'href="notice.html"'),
    ('>행사이력</a>', '>현장사진</a>'),
    ('>블로그</a>', '>소식</a>'),
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


TRACES = ('큰길', '김동길', '광양', '브리지미디어', '788101', 'xn--wk0', 'keungil', 'KG<', '>KG')


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

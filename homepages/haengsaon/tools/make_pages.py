# -*- coding: utf-8 -*-
"""
행사 이야기(stories/) · 운영 지역 페이지(areas/) 만들기 — 사이트 틀(머리글 · 바닥글)은 notice.html 에서 빌려 온다.
(바로기획 tools/make_pages.py 를 행사ON 마크업 · 색으로 옮긴 것)

  python tools/make_pages.py

내용은 아래 STORIES · AREAS 표만 고치면 된다. 사실만 적을 것(행사ON 네이버 블로그 글 · 사이트 글 · 대표님 확인분).
만든 뒤 sitemap.xml 도 같이 다시 쓴다.
"""
import os, re, html, datetime

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://brizymedia.github.io/haengsaon/'
BLOG = 'https://blog.naver.com/hoon0170800/'
NAME = '행사ON'
TEL = '1800-7947'
SMS = '010-9441-5542'
E = html.escape
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# ── 행사 이야기 ──────────────────────────────────────────────
# 모두 행사ON(구 스타컴퍼니) 네이버 블로그 글에 적힌 내용만 옮겼다. date = 블로그 글 올린 날.
# area 는 아래 AREAS 의 slug (운영 지역 9곳 밖의 현장이면 None)
STORIES = [
    dict(slug='asan-lh15-apartment', title='추석 맞이 아파트 주민행사 — 아산 배방 LH15단지', cat='아파트 행사', date='2026.09.18', place='아산 배방 LH15단지', area='asan',
         lead='단지 안 세교복지관이 추석을 맞아 준비한 주민행사. 어르신 댄스 · 장구 공연과 초청가수 무대를 위해 음향을 설치 · 운영하고, 무대 · 백드롭 · 트러스 · 천막으로 행사장을 꾸몄습니다.',
         facts=[('행사', '추석 맞이 주민행사'), ('장소', '아산 배방 LH15단지'), ('준비', '단지 내 세교복지관'), ('맡은 일', '음향 설치 · 운영 · 무대 공간 · 백드롭 · 트러스 · 천막')],
         body=['평소 복지관 프로그램에 참여하시는 어르신들의 댄스 · 장구 공연에 초청가수 공연, 여러 체험부스가 함께 운영된 행사였습니다. 공연이 끊기지 않도록 음향 시스템을 설치하고 현장에서 운영했습니다.',
               '단지 안 광장과 산책로에 무대를 만들고 천막을 세우니, 주민들이 매일 오가던 공간이 그대로 행사장이 되었습니다. 주민이 준비한 공연이 무대에 오르고 이웃들이 객석에 모여 박수를 치는 것만으로도 충분히 좋은 주민행사가 됩니다.',
               '행사ON은 음향 · 무대 · 트러스 · 천막 · 테이블 · 의자 · 에어바운스 · 물놀이 장비를 직접 가지고 있어, 아파트가 여러 업체를 따로 알아보지 않아도 됩니다. 봄에는 어린이날 가족축제와 에어바운스, 여름에는 물놀이장, 가을에는 야시장과 주민공연, 겨울에는 크리스마스 · 송년행사와 포토존처럼 계절마다 이어 가는 주민축제를 제안합니다.'],
         photos=['apt-lh-1', 'apt-lh-6', 'apt-lh-9'], blog='224416024254'),
    dict(slug='dangjin-dongkuk-sports', title='공장을 멈추지 않은 4일간의 기업 체육대회 — 당진 동국제강', cat='기업 체육대회', date='2026.09.10', place='충남 당진', area='dangjin',
         lead='1조부터 4조까지 하루에 한 조씩, 4일 동안 이어진 체육대회. 천막 · 음향 · 테이블 · 의자에 MC · 운영 스태프 · 게임장비와 프로그램 진행까지 함께 준비하고 운영했습니다.',
         facts=[('행사', '동국제강 기업 체육대회'), ('기간', '4일 (하루 한 조씩)'), ('장소', '충남 당진'), ('맡은 일', '천막 · 음향 · 테이블 · 의자 · MC · 운영 스태프 · 게임장비 · 프로그램 진행')],
         body=['공장을 멈추고 한꺼번에 여는 체육대회가 아니라, 1조부터 4조까지 하루에 한 조씩 나눠 진행한 행사였습니다. 회사 요청에 따라 4일 동안 날마다 다른 MC가 진행을 맡았고, 사원들은 출장뷔페 음식을 함께 나누며 체육대회를 즐겼습니다.',
               '여러 날 이어지는 체육대회는 같은 행사를 되풀이하는 것이 아닙니다. 매일 장비와 프로그램, 참가자 동선과 현장 상황을 다시 확인하며 다음 날 일정을 준비했습니다.',
               '음향업체 · 천막업체 · MC · 진행업체를 따로 섭외하지 않고, 사전 미팅부터 설치와 현장 운영까지 한 팀이 맡은 현장입니다.'],
         photos=['corp-dk-12', 'corp-dk-7'], blog='224407480300'),
    dict(slug='jungwon-univ-total-system', title='무대 · 트러스 · LED · 조명 · 음향을 하나의 시스템으로 — 중원대학교 박물관 행사', cat='토탈 시스템', date='2026.09.22', place='중원대학교 박물관', area=None,
         lead='무대 위로 외줄트러스를 길게 걸어 조명을 달고, 좌우에 음향을, 무대 뒤에 대형 LED를 세웠습니다. 장비를 따로 놓지 않고 출연자 동선까지 고려해 하나의 시스템으로 짠 현장입니다.',
         facts=[('행사', '중원대학교 박물관 행사'), ('맡은 일', '무대 · 외줄트러스 · LED · 조명 · 음향 전체 구성'), ('프로그램', '진행 · 보컬 공연 · 키보드 · 첼로 연주 · 퍼포먼스')],
         body=['무대 가운데 대형 LED는 행사 제목만 띄우지 않았습니다. 진행 순서에 맞춰 사진과 영상을 보여 주고, 공연 때는 음악에 맞는 영상을 띄워 무대 배경 자체를 연출로 썼습니다.',
               '외줄트러스에 단 조명은 프로그램마다 바꿨습니다. 보컬 공연에서는 출연자에게 시선이 모이게, 퍼포먼스에서는 빨강 · 파랑의 강한 색으로, 첼로 · 키보드 연주에서는 영상과 차분하게 어우러지도록 잡았습니다.',
               '무대 크기가 바뀌면 LED와 조명 자리가 달라지고, 공연이 바뀌면 음향과 조명도 달라집니다. 그래서 다섯 가지를 한 팀이 함께 짜는 것이 안전합니다. 무대가 이미 있는 곳이라면 음향 · 조명만, 영상이 중요한 행사라면 LED만 따로 맡기셔도 됩니다.'],
         photos=['stage-jw-0', 'stage-jw-6', 'stage-jw-18'], blog='224419910650'),
    dict(slug='asan-onyang-yonghwa-festival', title='학교 체육관이 공연장이 된 날 — 온양용화고 동아리 발표회', cat='학교축제', date='2026.09.21', place='아산 온양용화고등학교 체육관', area='asan',
         lead='밴드 공연과 보컬 무대가 이어진 동아리 발표회. YAMAHA DM3 디지털 믹서와 여러 채널의 무선마이크, 무대 모니터와 조명을 세팅하고 공연 내내 현장에서 직접 운영했습니다.',
         facts=[('행사', '동아리 발표회 (학교축제)'), ('장소', '온양용화고등학교 체육관'), ('장비', 'YAMAHA DM3 디지털 믹서 · 다채널 무선마이크 · 무대 모니터 · 무대 조명'), ('맡은 일', '설치 · 리허설 · 공연 오퍼레이팅')],
         body=['학교 체육관은 공연장과 구조가 달라 출력이 큰 스피커만 놓아서는 객석 끝까지 소리가 고르게 가지 않습니다. 도착하자마자 무대와 객석 위치, 공연 공간을 보고 시스템을 짰습니다.',
               '밴드 공연은 객석으로 나가는 소리만큼 무대 위 모니터가 중요합니다. 보컬과 연주자가 서로의 소리를 들을 수 있게 모니터를 두고, 공연 중에는 기타 · 베이스 · 드럼 · 키보드 사이에서 보컬이 묻히지 않도록 계속 밸런스를 맞췄습니다.',
               '무대 앞과 양쪽에 조명을 놓으니 평소 체육활동을 하던 공간이 축제 무대로 바뀌었습니다. 학생들이 직접 오르는 무대라 케이블 정리와 무대 동선까지 함께 확인했습니다.'],
         photos=['school-yh-2', 'school-yh-1'], blog='224418933345'),
    dict(slug='asan-urban-farming-festival', title='넓은 야외음악당 끝까지 고르게 — 제3회 아산시 도시농업축제', cat='지역축제', date='2026.09.08', place='아산 신정호 야외음악당', area='asan',
         lead='객석과 무대 사이가 넓은 야외 공연장. 무대 좌우 라인어레이와 전면 스피커, Yamaha DM3 디지털 콘솔로 어린이 공연 · 합창 · 진행 멘트를 객석 끝까지 전달했습니다.',
         facts=[('행사', '제3회 아산시 도시농업축제'), ('장소', '아산 신정호 야외음악당'), ('장비', '라인어레이 · 전면 스피커 · Yamaha DM3 디지털 콘솔 · 무선마이크'), ('프로그램', '어린이 공연 · 합창 · 진행')],
         body=['야외는 벽과 천장이 없어 소리가 되돌아오지 않고 관객도 넓게 흩어집니다. 출력만 올리지 않고, 행사장 구조에 맞춰 소리가 고르게 퍼지도록 무대 좌우에 라인어레이를 세우고 무대 앞에도 스피커를 따로 두었습니다.',
               '출연자가 계속 바뀌는 어린이 공연에서는 다음 순서의 마이크와 음원을 미리 챙겼고, 합창에서는 반주와 목소리의 균형을 잡아 야외 객석까지 자연스럽게 들리도록 현장에서 계속 조정했습니다.'],
         photos=['fest-agri-0', 'fest-agri-6'], blog='224405061050'),
]

# ── 운영 지역 ────────────────────────────────────────────────
# 분 · km: 본사(아산 탕정면로) → 각 시청 · 군청까지 OSRM(막히지 않을 때) 2026-10-03 조회, 5분 단위 반올림
# done: 행사ON 블로그 글 제목에 나온 그 지역 행사만. 기록이 없으면 비워 둔다.
AREAS = [
    dict(slug='asan', name='아산', hall='아산시청', min=10, km=10.5, hq=True,
         done=['배방 LH15단지 추석 주민행사 (2026)', '제3회 아산시 도시농업축제 음향 (신정호 야외음악당)', '온양용화고 동아리 발표회 음향 · 조명',
               '온양여고 2025 온화제 음향 · 조명', '배방초 발표회 핀마이크 12채널 운영', '염티초 학예발표회 음향 · 조명', '개소식 음향 · 레드카펫 · 테이프커팅식', '의정보고회 무대조명 · 핀마이크'],
         photos=['apt-lh-1', 'fest-agri-0', 'school-yh-2']),
    dict(slug='cheonan', name='천안', hall='천안시청', min=10, km=6.1,
         done=['천안여자상업고 축제 음향 · 조명', '천안중학교 체육대회 음향 · 천막 · MC · 게임도구 · 프로그램', '천안 행사 사진 전시벽 · 전시 구조물 제작'],
         photos=['school-bb-1', 'tent-incheon-1', 'truss-photo-1']),
    dict(slug='pyeongtaek', name='평택', hall='평택시청', min=30, km=24.3,
         done=['송탄 고등학교 체육대회 음향 · 천막 · 물놀이 · 게임장비'],
         photos=['tent-incheon-3', 'water-sch-2', 'corp-dk-7']),
    dict(slug='yesan', name='예산', hall='예산군청', min=35, km=33.4,
         done=['예산고등학교 체육대회 · 학교축제 3년 연속 진행 (음향 · 조명 · 천막 · 테이블 · 의자)'],
         photos=['tent-incheon-1', 'school-yh-1', 'corp-dk-12']),
    dict(slug='dangjin', name='당진', hall='당진시청', min=45, km=47.7,
         done=['동국제강 4일간 기업 체육대회 (2026)', '성당 · 교회 명랑운동회 MC · 음향 · 천막'],
         photos=['corp-dk-12', 'corp-dk-7', 'tent-incheon-3']),
    dict(slug='gongju', name='공주', hall='공주시청', min=50, km=52.2,
         done=['귀산초등학교 예술제 음향 · 조명'],
         photos=['school-bb-1', 'stage-jw-18', 'school-yh-1']),
    dict(slug='sejong', name='세종', hall='세종시청', min=55, km=58.3,
         done=['늘봄초등학교 축제 · 학예발표회 음향 · 조명'],
         photos=['school-yh-2', 'stage-jw-6', 'truss-photo-1']),
    dict(slug='seosan', name='서산', hall='서산시청', min=65, km=69.2, done=[],
         photos=['stage-jw-0', 'water-apt-5', 'yearend-3']),
    dict(slug='nonsan', name='논산', hall='논산시청', min=70, km=82.3,
         done=['채운초등학교 학예발표회 조명 · 옥타부스'],
         photos=['school-bb-1', 'stage-jw-18', 'water-sch-1']),
]

SERVICES = [('학교축제 · 학예발표회', '음향 · 조명 · 핀마이크 · 무대막 · 풍선장식'), ('체육대회', '학교 · 기업 · 기관 — 음향 · MC · 게임장비 · 천막'), ('토탈행사', '무대 · 트러스 · LED · 조명 · 음향을 하나로'),
            ('천막 · 테이블 · 의자 렌탈', '필요한 수량만큼 싣고 가서 설치'), ('에어바운스 · 물놀이', '놀이바운스 · 워터슬라이드 · 에어풀장'), ('아파트 행사', '플리마켓 · 입주민축제 · 아파트 물놀이')]


def shell():
    s = open(os.path.join(SITE, 'notice.html'), encoding='utf-8').read()
    head_end = s.index('<main id="top">')
    main_end = s.index('</main>') + len('</main>')
    return s[:head_end], s[main_end:]


def page(path, title, desc, main, img='assets/img/og.jpg', depth=1):
    top, bottom = shell()
    url = BASE + path
    top = re.sub(r'<title>.*?</title>', '<title>' + E(title) + '</title>', top, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        top = re.sub(r'(<meta ' + prop + r' content=")[^"]*', lambda m: m.group(1) + E(desc), top, count=1)
    top = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + E(title), top, count=1)
    top = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, top, count=1)
    top = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, top, count=1)
    top = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + BASE + img, top, count=1)
    top = re.sub(r'<meta property="og:image:(?:width|height)"[^>]*>\n?', '', top)
    top = re.sub(r'<meta name="hs-edit"[^>]*>\n?', '', top)               # 대표님 수정 모드는 기본 7쪽에만
    top = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "BreadcrumbList".*?</script>\n?', '', top)
    top = top.replace(' class="act"', '').replace('class="act" ', '')
    bottom = re.sub(r'<script src="assets/edit\.js[^"]*"></script>\n?', '', bottom)
    out = top + '<main id="top">\n' + main + '\n</main>' + bottom
    pre = '../' * depth
    out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|sms:|#|/|\.\./|data:)([^"]+)"', lambda m: m.group(1) + '="' + pre + m.group(2) + '"', out)
    out = re.sub(r"url\((?!https?:)(assets/[^)]+)\)", lambda m: 'url(' + pre + m.group(1) + ')', out)
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(out)
    return url


def pic(f, big=False):
    return 'assets/img/' + ('p/' if big else 't/') + f + '.webp'


def phead(bg, eyebrow, h1, lead, crumb):
    return ('<section class="ph"><div class="bg" style="background-image:url(' + pic(bg, True) + ')"></div><div class="wrap">'
            '<span class="eyebrow">' + eyebrow + '</span><h1>' + h1 + '</h1><p>' + lead + '</p><div class="crumb">' + crumb + '</div></div></section>')


def cta(title='행사 날짜가 정해지셨다면,<br>지금 <em>ON</em> 하세요.', sub='날짜 · 장소 · 인원만 알려 주시면 구성과 견적을 정리해 드립니다.'):
    return ('<section class="sec"><div class="wrap"><div class="callband rv"><div><h2>' + title + '</h2><p>' + sub + '</p>'
            '<a class="tel" href="tel:' + TEL + '">' + TEL + '<small>24시 상담</small></a></div>'
            '<div class="btns"><a class="btn btn-on" href="quote.html">자동 견적서로 문의' + ARROW + '</a><a class="btn btn-ghost" href="contact.html">예약 · 문의 폼</a>'
            '<a class="btn btn-ghost" href="sms:' + SMS + '">문자 보내기 ' + SMS + '</a></div></div></div></section>')


def story_pages():
    urls = []
    for st in STORIES:
        facts = ''.join('<dt>' + E(a) + '</dt><dd>' + E(b) + '</dd>' for a, b in st['facts'])
        body = ''.join('<p>' + E(p) + '</p>' for p in st['body'])
        photos = ''.join('<a href="' + pic(f, True) + '" target="_blank" rel="noopener"><img src="' + pic(f) + '" alt="' + E(st['title']) + ' 현장" loading="lazy" width="800" height="600"></a>' for f in st['photos'])
        area = next((a for a in AREAS if a['slug'] == st['area']), None)
        alink = ('<a class="alink" href="@@areas/' + area['slug'] + '.html">' + E(area['name']) + ' 행사 안내 →</a>') if area else '<a class="alink" href="@@areas/index.html">운영 지역 보기 →</a>'
        others = [o for o in STORIES if o['slug'] != st['slug']][:3]
        more = ''.join('<a class="scard" href="@@stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(o['cat'] + ' · ' + o['place']) + '</small>' + E(o['title']) + '</span></a>' for o in others)
        blog = ('<a class="btn btn-line" href="' + BLOG + st['blog'] + '" target="_blank" rel="noopener">블로그 원문 보기 ↗</a>') if st['blog'] else ''
        main = (phead(st['photos'][0], 'Event file · ' + E(st['cat']), E(st['title']), E(st['lead']),
                      '<a href="index.html">홈</a> · <a href="@@stories/index.html">행사 이야기</a> · ' + E(st['cat']))
                + '<section class="sec"><div class="wrap sstory">'
                '<aside class="rv"><span class="en">Event File</span><dl>' + facts + '<dt>블로그 기록</dt><dd>' + E(st['date']) + '</dd></dl>'
                '<a class="btn btn-on" href="quote.html">비슷한 행사 견적 받기</a>' + alink + '</aside>'
                '<div class="rv sbody">' + body + '<div class="sgrid">' + photos + '</div><div class="sbtns">' + blog + '<a class="btn btn-line" href="portfolio.html">행사 사진 더 보기</a></div></div>'
                '</div></section>'
                '<section class="sec soft"><div class="wrap"><div class="sh rv"><div><span class="eyebrow">More stories</span><h2>다른 <em>현장 이야기</em></h2></div><a class="more" href="@@stories/index.html">전체 보기' + ARROW + '</a></div><div class="scards">' + more + '</div></div></section>'
                + cta())
        urls.append(page('stories/' + st['slug'] + '.html', st['title'] + ' | ' + NAME + ' 행사 이야기', st['lead'][:120], main, img=pic(st['photos'][0], True)))
    cards = ''.join('<a class="scard rv" href="@@stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(o['cat'] + ' · ' + o['place']) + '</small>' + E(o['title']) + '<em>' + E(o['lead'][:60]) + '…</em></span></a>' for o in STORIES)
    main = (phead('stage-jw-6', 'Stories', '행사 이야기', '행사ON이 준비한 행사를 한 편씩 기록했습니다. 어디서, 무엇을, 어떻게 준비했는지 사진과 함께 보실 수 있습니다.', '<a href="index.html">홈</a> · 행사 이야기')
            + '<section class="sec"><div class="wrap"><div class="scards big">' + cards + '</div><p class="snote">더 많은 현장 기록은 <a href="' + BLOG + '" target="_blank" rel="noopener">행사ON 네이버 블로그</a>에 있습니다.</p></div></section>' + cta())
    urls.insert(0, page('stories/index.html', '행사 이야기 | 행사ON — 아파트 주민행사 · 기업 체육대회 · 학교축제 · 지역축제 현장 기록',
                        '행사ON이 준비한 행사를 한 편씩 기록했습니다. 배방 LH15단지 주민행사, 당진 동국제강 4일 체육대회, 온양용화고 발표회, 아산시 도시농업축제, 중원대학교 박물관 행사.', main, img=pic('stage-jw-6', True)))
    return urls


def area_pages():
    urls = []
    for a in AREAS:
        n = a['name']
        if a.get('hq'):
            how = '<b>행사ON 본사</b>가 있는 곳입니다. 충남 아산시 탕정면 탕정면로 141-13 — 아산시청까지 차로 약 <b>' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km</b>(막히지 않을 때 기준)입니다.'
        else:
            how = '아산 탕정 본사에서 ' + a['hall'] + '까지 차로 약 <b>' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km</b>(막히지 않을 때 기준)입니다. 설치 시간을 넉넉히 잡고 행사 시작 전에 세팅을 마칩니다.'
        if a['done']:
            done = '<ul class="alist">' + ''.join('<li>' + E(x) + '</li>' for x in a['done']) + '</ul><p class="muted" style="font-size:14px;margin-top:10px">행사ON 블로그에 올린 현장 기록 기준입니다.</p>'
        else:
            done = '<p class="muted">아직 이 페이지에 적을 만큼 정리된 기록이 없습니다. ' + n + ' 행사도 아산 탕정 본사에서 출발해 똑같이 준비합니다.</p>'
        stories = [s for s in STORIES if s['area'] == a['slug']]
        sl = ''.join('<a class="scard" href="@@stories/' + s['slug'] + '.html"><img src="' + pic(s['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(s['cat'] + ' · ' + s['date']) + '</small>' + E(s['title']) + '</span></a>' for s in stories)
        svc = ''.join('<li><b>' + E(x) + '</b><span>' + E(y) + '</span></li>' for x, y in SERVICES)
        photos = ''.join('<img src="' + pic(f) + '" alt="행사ON 행사 현장" loading="lazy" width="800" height="600">' for f in a['photos'])
        others = ' · '.join('<a href="@@areas/' + o['slug'] + '.html">' + o['name'] + '</a>' for o in AREAS if o['slug'] != a['slug'])
        title = n + ' 행사업체 · 학교축제 · 체육대회 · 음향 · 천막 렌탈 | 행사ON'
        desc = n + ' 학교축제 · 학예발표회 · 체육대회 · 아파트 행사, 음향 · 조명 · 무대 · 천막 · 에어바운스 렌탈까지. ' + ('아산 탕정 본사 — 2007년부터.' if a.get('hq') else '아산 탕정 본사에서 차로 약 ' + str(a['min']) + '분. 2007년부터 충남 행사를 준비해 온 행사ON.')
        main = (phead(a['photos'][0], 'Service area · ' + n, n + ' 행사, 행사ON이 켭니다', '학교축제 · 체육대회 · 아파트 행사 · 기업행사. 2007년부터 충남 행사를 준비해 온 행사ON이 ' + n + ' 현장도 설치부터 운영 · 철수까지 챙깁니다.',
                      '<a href="index.html">홈</a> · <a href="@@areas/index.html">운영 지역</a> · ' + n)
                + '<section class="sec"><div class="wrap area3"><div class="rv"><span class="eyebrow">How far</span><h2 class="h2s">' + n + (' — 본사' if a.get('hq') else '까지') + '</h2><p>' + how + '</p>'
                '<h3 class="h3s">' + n + '에서 한 행사</h3>' + done + ('<div class="scards sm">' + sl + '</div>' if sl else '') + '</div>'
                '<div class="rv"><div class="apics">' + photos + '</div></div></div></section>'
                '<section class="sec soft"><div class="wrap"><div class="sh rv"><div><span class="eyebrow">What we do</span><h2>' + n + '에서도 <em>이런 행사</em>를 맡습니다</h2></div><a class="more" href="price.html">품목 · 가격표' + ARROW + '</a></div><ul class="asvc">' + svc + '</ul>'
                '<p class="snote">다른 지역: ' + others + ' · <a href="@@areas/index.html">운영 지역 전체</a></p></div></section>'
                + cta(n + ' 행사 날짜가<br>정해지셨다면, 지금 <em>ON</em> 하세요.'))
        urls.append(page('areas/' + a['slug'] + '.html', title, desc, main, img=pic(a['photos'][0], True)))
    rows = ''.join('<a class="arow" href="@@areas/' + a['slug'] + '.html"><b>' + a['name'] + '</b><span>' + ('본사' if a.get('hq') else '차로 약 ' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km') + '</span><em>' + (E(a['done'][0]) if a['done'] else '출장 진행') + '</em></a>' for a in AREAS)
    main = (phead('tent-incheon-3', 'Service area', '운영 지역', '충남 아산 탕정에서 출발해 아산 · 천안을 중심으로 충남 전역, 일정에 따라 타 지역도 갑니다. 지역을 누르면 그 지역에서 한 행사와 이동 시간을 보실 수 있습니다.', '<a href="index.html">홈</a> · 운영 지역')
            + '<section class="sec region"><div class="wrap grid"><div class="base rv"><small>BASE · ASAN TANGJEONG</small><b>충남 아산 탕정에서 출발합니다.</b><p>충남 아산시 탕정면 탕정면로 141-13. 천안시청까지 약 10분, 평택 30분, 예산 35분, 당진 45분(막히지 않을 때).</p>'
            '<p style="margin-top:18px"><a class="btn btn-on btn-sm" href="tel:' + TEL + '">' + TEL + ' 24시 상담</a></p><span class="pin" aria-hidden="true"></span></div>'
            '<div class="rv"><div class="arows">' + rows + '</div><p class="note">이동 시간은 본사에서 각 시청 · 군청까지 차로 걸리는 시간(막히지 않을 때 기준)입니다. 표에 없는 지역도 전화 주시면 상담해 드립니다.</p></div></div></section>' + cta())
    urls.insert(0, page('areas/index.html', '운영 지역 | 행사ON — 아산 · 천안 · 평택 · 예산 · 당진 · 공주 · 세종 · 서산 · 논산 행사업체', '충남 아산 탕정 본사에서 아산 · 천안을 중심으로 충남 전역. 지역별 이동 시간과 그 지역에서 한 행사를 보실 수 있습니다.', main, img=pic('tent-incheon-3', True)))
    return urls


def fix_same_folder():
    """@@stories/x.html 같은 표시를 실제 상대 경로로(두 폴더 모두 한 단계 아래라 ../ 로 통일)."""
    for d in ('stories', 'areas'):
        for f in os.listdir(os.path.join(SITE, d)):
            p = os.path.join(SITE, d, f)
            s = open(p, encoding='utf-8').read()
            s = s.replace('../@@', '../').replace('@@', '../')
            open(p, 'w', encoding='utf-8', newline='\n').write(s)


def sitemap(extra):
    today = datetime.date.today().isoformat()
    pages = ['', 'about.html', 'service.html', 'price.html', 'portfolio.html', 'notice.html', 'contact.html', 'quote.html']
    urls = [BASE + p for p in pages] + extra
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + u + '</loc><lastmod>' + today + '</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)


if __name__ == '__main__':
    a = story_pages(); b = area_pages(); fix_same_folder(); sitemap(a + b)
    print('행사 이야기', len(a), '· 지역', len(b), '· sitemap.xml 갱신')

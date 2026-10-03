# -*- coding: utf-8 -*-
"""
행사 이야기(stories/) · 지역 페이지(areas/) 만들기 — 사이트 틀(머리글 · 푸터)은 notice.html 에서 빌려 온다.
(바로기획 tools/make_pages.py 를 힐링엔터테인먼트 틀 · 글로 옮긴 것)

  python tools/make_pages.py

내용은 아래 STORIES · AREAS 표만 고치면 된다. 사실만 적을 것(블로그 원문 · 대표 MC 프로필 · 대표님 확인분).
만든 뒤 sitemap.xml 도 같이 다시 쓴다.
"""
import os, re, html, datetime

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://brizymedia.github.io/healing-ent/'
BLOG = 'https://blog.naver.com/leehh2153/'
NAME = '힐링엔터테인먼트'
TEL = '010-5620-2153'
E = html.escape

# ── 행사 이야기 ──────────────────────────────────────────────
# 근거: 각 blog 번호의 네이버 블로그 원문(leehh2153). 숫자 · 고객 말은 원문에 있는 것만.
# area: AREAS 의 slug (원문에 지역이 없으면 None)
STORIES = [
    dict(slug='jeonnong-festival', title='전농동 상권 활성화 축제 — 추운 날씨에도 주민과 함께한 거리 축제', cat='지역축제', date='2024.12.07', place='서울 동대문구 전농동 사거리 일대', area='dongdaemun',
         lead='동대문구 전농동 사거리 일대에서 열린 상권 활성화 축제. 플리마켓 · 체험존 · 문화 공연과 MC 진행의 퀴즈 · 게임 이벤트로 추운 날씨에도 거리를 채웠습니다.',
         facts=[('행사', '전농동 상권 활성화 축제'), ('장소', '동대문구 전농동 사거리 일대'), ('프로그램', '플리마켓 · 체험존 · 문화 공연 · 퀴즈 · 게임 이벤트'), ('안전', '안전요원 배치 · 소화기 · 비상연락망 · 차량 통제')],
         body=['축제는 동대문 소상공인이 참여한 플리마켓과 체험존, 경기민요 · 북난타 · 전자 가야금 연주와 가수 공연으로 채워졌습니다. 무대에서는 MC 진행 속에 퀴즈와 게임 이벤트가 이어졌습니다.',
               '거리에서 여는 축제라 행사장과 주요 구역에 안전요원을 두고 소화기와 비상연락망을 준비했습니다. 차량을 통제해 방문객이 다닐 동선도 확보했습니다.',
               '축제에 앞서 11월 23일부터 12월 6일까지는 지역 음식점 · 카페 · 전통시장에서 쓸 수 있는 3,000원 할인 쿠폰 3,400매가 배포됐습니다.'],
         photos=['w3', 'w14', 'w8', 'w20', 'w17', 'w23'], blog='223702427949', quote=['p4', 'f1', 'a3', 'b1', 'f2']),
    dict(slug='childcare-conference', title='전국 국공립 어린이집 보육인대회 — 500여 명이 함께한 대동놀이', cat='대회 · 기념식', date='2024', place='서울 백범기념관', area=None,
         lead='전국 국공립 어린이집 보육인대회의 기획과 진행을 전해에 이어 2년째 맡았습니다. 500명이 넘는 참가자가 함께한 대회의 마지막은 시그니처 프로그램 「대동놀이」였습니다.',
         facts=[('행사', '제11회 전국 국공립 보육인대회'), ('규모', '500명 이상'), ('장소', '백범기념관'), ('맡은 일', '기획 · 진행 · 대동놀이')],
         body=['전국의 국공립 어린이집 원장님과 보육교사, 관계자가 한자리에 모이는 대회입니다. 오전부터 세미나와 특별 강연, 육아 전문가와 이야기 나누는 시간, 상담 부스가 이어졌습니다.',
               '500명이 넘는 인원이 움직이는 행사라 동선과 일정 조율이 가장 중요했습니다. 미리 상황을 하나씩 짚어 보며 동선과 공간 배치를 짰고, 행사장 곳곳에 안내 부스와 휴게 공간을 두었습니다.',
               '마지막 순서는 힐링엔터테인먼트의 시그니처 프로그램 「대동놀이」. 아이부터 어른까지 모두가 함께 참여하는 시간으로 대회를 마무리했습니다.'],
         photos=['b1', 'b2', 'b3', 'b4'], blog='223704847391', quote=['p5', 'f1', 'f8', 'a2']),
    dict(slug='union-workshop', title='16개 동 연합 워크숍 — 200명 넘는 인원을 3단계 게임으로', cat='연합 워크숍', date='2025.06', place='실내 체육관', area=None,
         lead='16개 동이 함께한 200명 이상의 연합 워크숍. 전체 게임 → 소그룹 교차전 → 동별 대항전의 3단계로 짜서 팀이 많아도 순서가 흐트러지지 않게 진행했습니다.',
         facts=[('행사', '16개 동 연합 워크숍'), ('규모', '200명 이상 · 16개 팀'), ('장소', '실내 체육관'), ('맡은 일', '프로그램 구성 · 진행 · 음향 · 내빈석 · 팀 자리 세팅')],
         body=['연령도 성별도, 동마다 분위기도 다른 200명 이상이 한 체육관에 모였습니다. 그래서 프로그램을 전체 게임 → 중간 그룹 교차전 → 동별 대항전의 3단계로 나눴습니다.',
               '전체 게임은 머리 위로 큰 공 넘기기 · 대형 주사위 옮기기 · 색지 뒤집기처럼 8개 동씩 편을 이루는 종목, 교차전은 에어사다리 릴레이 · 볼풀 공 넣기 · 달고나 게임으로 4개 동씩 겨뤘습니다.',
               '마지막 동별 대항전은 16개 팀이 에어바운스 공 튀기기 · 골프 퍼팅 · 신발 던지기 · 훌라후프 넘기기 · 고리 던지기 부스를 돌며 기록을 쌓는 방식이었습니다. 진행자 · 보조자 · 운영지원팀이 팀별 체크인부터 현장 운영까지 나눠 맡았습니다.'],
         photos=['w1', 'w4', 'w7', 'w10', 'w15', 'w21'], blog='223913412790', quote=['p1', 'p8', 'f1', 'f5', 'h3', 'h1', 'a2']),
    dict(slug='elementary-sportsday', title='초등학교 가을 운동회 — 전교생이 함께 뛴 운동장', cat='학교 운동회', date='2025.10', place='초등학교 운동장', area=None,
         lead='전교생이 운동장에 모인 초등학교 운동회. 준비 체조부터 큰 공을 함께 옮기는 단체 게임, 이어달리기, 단체 줄다리기까지 경기 사이의 이동과 교대를 챙겼습니다.',
         facts=[('행사', '초등학교 운동회'), ('장소', '야외 운동장'), ('프로그램', '준비 체조 · 대형 공 굴리기 · 이어달리기 · 단체 게임 · 줄다리기')],
         body=['학생 수와 학년 구성에 따라 경기 공간과 대기 공간을 먼저 나눴습니다. 학생들이 언제 출발하고 어디서 기다리는지, 다음 팀으로 어떻게 교대하는지가 운동회의 흐름을 좌우합니다.',
               '큰 공을 함께 옮기는 단체 게임과 학년별 이어달리기처럼 여러 팀이 함께 뛰는 종목은 시작 신호와 교대 순서를 맞추는 것이 중요합니다. 진행자가 설명하는 동안 경기용품을 준비하고 학생 이동을 안내하는 역할을 따로 두었습니다.',
               '본부석 음향과 캐릭터 풍선으로 운동장 분위기를 만들고, 만국기 아래 단체 경기까지 이어 갔습니다.'],
         photos=['w2', 'w5', 'w9', 'w16', 'w24', 'w26'], blog='224408721656', quote=['p2', 'f1', 'f5', 'h3', 'a3']),
    dict(slug='school-sports-daedong', title='학교 체육대회 — 어깨동무로 하나가 된 대동놀이', cat='학교 체육대회', date='2026.09.13', dlabel='기록일', place='학교 운동장', area=None,
         lead='학교 체육대회는 같은 프로그램이라도 학년 · 인원 · 운동장 조건에 따라 짜는 방식이 달라집니다. 팀 대항 게임부터 어깨동무로 함께 움직이는 대동놀이까지, 현장 모습을 사진으로 남겼습니다.',
         facts=[('행사', '학교 체육대회'), ('장소', '학교 운동장'), ('프로그램', '팀 대항 게임 · MC와 함께하는 운동장 게임 · 대동놀이'), ('영상', '현장 촬영 5개를 이은 52초 영상(블로그)')],
         body=['학교 체육대회는 같은 프로그램을 준비해도 학년과 인원, 운동장이나 체육관 조건에 따라 구성이 달라집니다. 그래서 상담할 때 참가 인원과 학년, MC 진행만 필요한지 프로그램과 운영 물품까지 필요한지를 먼저 여쭙니다.',
               '팀별로 모여 앉은 학생들, MC와 함께하는 운동장 게임, 어깨동무를 하고 원을 그리며 함께 움직이는 대동놀이까지 — 사진에 그날 운동장의 모습이 담겨 있습니다.',
               '현장 모습은 같은 행사를 찍은 영상 5개를 이어 52초로 편집해 블로그에 올려 두었습니다.'],
         photos=['w12', 'w6', 'w18', 'w25'], blog='224410240152', quote=['p2', 'f1', 'f8', 'a3']),
]

# ── 지역 ────────────────────────────────────────────────────
# 분 · km: 본사(노원구 덕릉로 595)에서 각 구청 · 시청까지 OSRM(막히지 않을 때) 2026-10-03 조회, 5분 단위 반올림
# done: 그 지역에서 한 행사 — 대표 MC 프로필 · 블로그에 기록된 것만
AREAS = [
    dict(slug='nowon', name='노원', min=0, km=0, hq=True,
         done=['상계1동 하나로 축제 총괄 감독 (2,000명)', '상계 중앙시장 구정맞이 축제'],
         photos=['w14', 'w11', 'w20']),
    dict(slug='dobong', name='도봉', min=5, km=4.1, done=[], photos=['w7', 'w5', 'w4']),
    dict(slug='gangbuk', name='강북', min=5, km=5.1, done=[], photos=['w18', 'w10', 'w13']),
    dict(slug='jungnang', name='중랑', min=10, km=6.4, done=[], photos=['w1', 'w16', 'w8']),
    dict(slug='seongbuk', name='성북', min=10, km=9.8, done=[], photos=['w12', 'w15', 'w22']),
    dict(slug='dongdaemun', name='동대문', min=15, km=11.0,
         done=['전농동 골목 상권 활성화 축제 (2024.12)', '청량리 종합시장 「달빛 나들이」 기획 · 무대 · 연출 총괄 감독 (2만 명)'],
         photos=['w3', 'w23', 'w17']),
    dict(slug='uijeongbu', name='의정부', min=15, km=12.7, city=True, done=[], photos=['w26', 'w21', 'w9']),
    dict(slug='eunpyeong', name='은평', min=20, km=17.6,
         done=['은평구청 어린이날 행사 (2023~26)', '은평구 주민자치회 연합 워크숍', '은평구 주민자치회 우리마을 워터파크'],
         photos=['w10', 'w27', 'w19']),
    dict(slug='namyangju', name='남양주', min=20, km=17.4, city=True, done=[], photos=['w6', 'w24', 'w25']),
]

SERVICES = [('기업 체육대회 · 워크숍', '팀빌딩 · 참여형 프로그램'), ('학교 운동회 · 체육대회', '대동놀이 · 수학여행 레크리에이션'), ('지역축제 · 관공서 행사', '기획 · 무대 진행 · 현장 운영'),
            ('전문 MC · 레크리에이션', '대표 MC 이현호 직접 진행'), ('음향 · 무대 · 조명 · DJ', '행사 규모에 맞춘 장비와 운영'), ('기념식 · 회원 대회', '기획 · 연출 · 진행')]

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'


def shell():
    s = open(os.path.join(SITE, 'notice.html'), encoding='utf-8').read()
    head_end = s.index('<main id="main">')
    main_end = s.index('</main>') + len('</main>')
    return s[:head_end], s[main_end:]


def page(path, title, desc, main, img='assets/img/og.jpg', depth=1):
    top, bottom = shell()
    url = BASE + path
    top = re.sub(r'<title>.*?</title>', '<title>' + E(title) + '</title>', top, count=1)
    for prop in ('name="description"', 'property="og:description"'):
        top = re.sub(r'(<meta ' + prop + r' content=")[^"]*', r'\g<1>' + E(desc).replace('\\', '\\\\'), top, count=1)
    top = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + E(title), top, count=1)
    top = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\g<1>' + url, top, count=1)
    top = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>' + url, top, count=1)
    top = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\g<1>' + BASE + img, top, count=1)
    top = re.sub(r'<meta property="og:image:(width|height)"[^>]*>\n?', '', top)    # 이야기 사진은 크기가 제각각
    top = re.sub(r'<meta name="es-edit"[^>]*>\n?', '', top)            # 대표님 수정 모드는 기본 쪽에만
    top = top.replace(' class="act"', '').replace('class="act" ', '')
    bottom = re.sub(r'<script src="assets/edit\.js[^"]*"></script>\n?', '', bottom)
    out = top + '<main id="main">\n' + main + '\n</main>' + bottom
    pre = '../' * depth
    out = re.sub(r'(href|src)="(?!https?:|mailto:|tel:|sms:|#|/|\.\./)([^"]+)"', lambda m: m.group(1) + '="' + pre + m.group(2) + '"', out)
    out = re.sub(r"url\((?!https?:)(assets/[^)]+)\)", lambda m: 'url(' + pre + m.group(1) + ')', out)
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8', newline='\n').write(out)
    return url


def pic(f, big=False):
    return 'assets/img/works/' + ('' if big else 'th/') + f + '.webp'


def head(eyebrow, h1, lead, crumbs, img):
    cr = '<a href="index.html">홈</a>' + ''.join('<span>›</span>' + c for c in crumbs)
    return ('<section class="ph-head"><div class="wrap"><div><p class="eyebrow">' + eyebrow + '</p><h1>' + h1 + '</h1><p>' + lead + '</p>'
            '<div class="crumb">' + cr + '</div></div><div class="pimg" style="background-image:url(' + img + ')" role="img" aria-label="' + E(re.sub('<[^>]+>', '', h1)) + ' 대표 사진"></div></div></section>')


def cta(title='행사 날짜가 정해졌다면,<br>지금 편하게 물어보세요.', sub='날짜 · 지역 · 인원 · 행사 종류만 알려 주시면 행사에 맞춰 상담 · 견적을 안내드립니다. 행사 중엔 통화가 어려우니 문자 · 카톡을 남겨 주세요.'):
    return ('<section class="band"><div class="wrap"><div class="in rv"><div><h2>' + title + '</h2><p>' + sub + '</p></div>'
            '<div class="acts"><a class="btn btn-white" href="tel:' + TEL + '">' + PHONE + TEL + '</a><a class="btn btn-white" href="quote.html">자동 견적서</a>'
            '<a class="btn btn-or" href="contact.html#form">빠른 견적 문의' + ARROW + '</a></div></div></div></section>')


def card(o, extra=''):
    return ('<a class="scard' + extra + '" href="@@stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' +
            E(o['cat'] + ' · ' + o['date']) + '</small>' + E(o['title']) + '</span></a>')


def story_pages():
    urls = []
    for st in STORIES:
        facts = ''.join('<dt>' + E(a) + '</dt><dd>' + E(b) + '</dd>' for a, b in st['facts'])
        body = ''.join('<p>' + E(p) + '</p>' for p in st['body'])
        photos = ''.join('<a href="' + pic(f, True) + '" target="_blank" rel="noopener"><img src="' + pic(f) + '" alt="' + E(st['title']) + ' 현장" loading="lazy" width="800" height="600"></a>' for f in st['photos'])
        area = next((a for a in AREAS if a['slug'] == st['area']), None)
        others = [o for o in STORIES if o['slug'] != st['slug']][:3]
        more = ''.join(card(o) for o in others)
        blog = ('<a class="btn btn-line" href="' + BLOG + st['blog'] + '" target="_blank" rel="noopener">블로그 원문 보기 ↗</a>') if st['blog'] else ''
        alink = ('<a class="alink" href="@@areas/' + area['slug'] + '.html">' + E(area['name']) + ' 행사 안내 →</a>') if area else '<a class="alink" href="@@areas/index.html">운영 지역 보기 →</a>'
        main = (head('Event story · ' + E(st['cat']), E(st['title']), E(st['lead']), ['<a href="@@stories/index.html">행사 이야기</a>', '<span>' + E(st['cat']) + '</span>'], pic(st['photos'][0], True)) +
                '<section class="sec"><div class="wrap sstory">'
                '<aside class="rv"><span class="en">Event File</span><dl>' + facts + '<dt>' + E(st.get('dlabel', '날짜')) + '</dt><dd>' + E(st['date']) + '</dd></dl>'
                '<a class="btn btn-or" href="quote.html">비슷한 행사 견적 받기</a>' + alink + '</aside>'
                '<div class="rv d1 sbody">' + body + '<div class="sgrid">' + photos + '</div><div class="sbtns">' + blog + '<a class="btn btn-line" href="portfolio.html">현장 갤러리 더 보기</a></div></div>'
                '</div></section>'
                '<section class="sec sky"><div class="wrap"><div class="sh rv"><div><p class="eyebrow">More stories</p><h2>다른 <em>현장 이야기</em></h2></div><a class="more" href="@@stories/index.html">전체 보기' + ARROW + '</a></div><div class="scards">' + more + '</div></div></section>'
                + cta())
        urls.append(page('stories/' + st['slug'] + '.html', st['title'] + ' | ' + NAME + ' 행사 이야기', st['lead'][:120], main, img=pic(st['photos'][0], True)))
    cards = ''.join('<a class="scard rv" href="@@stories/' + o['slug'] + '.html"><img src="' + pic(o['photos'][0]) + '" alt="" loading="lazy" width="800" height="600"><span><small>' + E(o['cat'] + ' · ' + o['date'] + ' · ' + o['place']) + '</small>' + E(o['title']) + '<em>' + E(o['lead'][:60]) + '…</em></span></a>' for o in STORIES)
    main = (head('Event stories', '행사 이야기', '힐링엔터테인먼트가 진행한 행사를 한 편씩 기록했습니다. 어떤 준비를 했는지, 현장에서 무엇을 했는지 사진과 함께 보실 수 있습니다.', ['<span>행사 이야기</span>'], pic('w7', True)) +
            '<section class="sec"><div class="wrap"><div class="scards big">' + cards + '</div><p class="snote">더 많은 현장 기록은 <a href="' + BLOG + '" target="_blank" rel="noopener">힐링엔터테인먼트 네이버 블로그</a>와 <a href="video.html">영상</a>에 있습니다.</p></div></section>' + cta())
    urls.insert(0, page('stories/index.html', '행사 이야기 | ' + NAME + ' — 지역축제 · 보육인대회 · 연합 워크숍 · 운동회 · 체육대회 현장 기록',
                        '힐링엔터테인먼트가 진행한 행사를 한 편씩 기록했습니다. 전농동 상권 활성화 축제, 국공립 어린이집 보육인대회, 16개 동 연합 워크숍, 초등학교 운동회, 학교 체육대회 현장.', main, img=pic('w7', True)))
    return urls


def where(a):
    return a['name'] + ('시청' if a.get('city') else '구청')


def area_pages():
    urls = []
    for a in AREAS:
        n = a['name']
        if a.get('hq'):
            how = '<b>' + NAME + ' 본사</b>가 있는 곳입니다. 서울특별시 노원구 덕릉로 595 — 노원 안의 학교 · 기관 · 행사장은 가까이서 바로 찾아갑니다.'
        else:
            how = '노원 본사에서 ' + where(a) + '까지 차로 약 <b>' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km</b>(막히지 않을 때 기준)입니다. 행사 시작 전에 미리 도착해 음향과 진행 준비를 마칩니다.'
        if a['done']:
            done = '<ul class="alist">' + ''.join('<li>' + E(x) + '</li>' for x in a['done']) + '</ul>'
        else:
            done = '<p class="muted">아직 이 페이지에 적을 만큼 정리된 기록이 없습니다. ' + n + ' 행사도 노원 본사에서 출발해 똑같이 준비합니다.</p>'
        stories = [s for s in STORIES if s['area'] == a['slug']]
        sl = ''.join(card(s) for s in stories)
        svc = ''.join('<li><b>' + E(x) + '</b><span>' + E(y) + '</span></li>' for x, y in SERVICES)
        photos = ''.join('<img src="' + pic(f) + '" alt="' + NAME + ' 행사 현장" loading="lazy" width="800" height="600">' for f in a['photos'])
        others = ' · '.join('<a href="@@areas/' + o['slug'] + '.html">' + o['name'] + '</a>' for o in AREAS if o['slug'] != a['slug'])
        title = n + ' 행사 MC · 체육대회 · 운동회 · 워크숍 | ' + NAME
        desc = n + ' 기업 체육대회 · 학교 운동회 · 워크숍 · 지역축제, 전문 MC · 레크리에이션 · 음향까지. ' + ('노원 본사 — 대표 MC 이현호, 20년 · 3,000회 이상의 현장 경험.' if a.get('hq') else '노원 본사에서 차로 약 ' + str(a['min']) + '분. 20년 · 3,000회 이상의 현장 경험, ' + NAME + '.')
        main = (head('Area · ' + n, n + ' 행사, ' + NAME + '가 갑니다', '기업 체육대회 · 학교 운동회 · 워크숍 · 지역축제. 대표 MC 이현호가 ' + n + ' 현장도 기획부터 진행까지 함께합니다.',
                     ['<a href="@@areas/index.html">운영 지역</a>', '<span>' + n + '</span>'], pic(a['photos'][0], True)) +
                '<section class="sec"><div class="wrap area3"><div class="rv"><span class="en">How far</span><h2 class="h2s">' + n + (' — 본사' if a.get('hq') else '까지') + '</h2><p>' + how + '</p>'
                '<h3 class="h3s">' + n + '에서 한 행사</h3>' + done + ('<div class="scards sm">' + sl + '</div>' if sl else '') + '</div>'
                '<div class="rv d1"><div class="apics">' + photos + '</div></div></div></section>'
                '<section class="sec sky"><div class="wrap"><div class="sh rv"><div><p class="eyebrow">What we do</p><h2>' + n + '에서도 <em>이런 행사</em>를 맡습니다</h2></div></div><ul class="asvc">' + svc + '</ul>'
                '<p class="snote">다른 지역: ' + others + ' · <a href="@@areas/index.html">운영 지역 전체</a></p></div></section>' + cta(n + ' 행사 날짜가 정해졌다면,<br>지금 편하게 물어보세요.'))
        urls.append(page('areas/' + a['slug'] + '.html', title, desc, main, img=pic(a['photos'][0], True)))
    rows = ''.join('<a class="arow" href="@@areas/' + a['slug'] + '.html"><b>' + a['name'] + '</b><span>' + ('본사' if a.get('hq') else '차로 약 ' + str(a['min']) + '분 · ' + ('%g' % a['km']) + 'km') + '</span><em>' + (E(a['done'][0]) if a['done'] else '출장 진행') + '</em></a>' for a in AREAS)
    main = (head('Areas', '운영 지역', '서울 노원 본사에서 출발해 서울 · 경기 어디든 찾아갑니다. 지역을 누르면 그 지역에서 한 행사와 이동 시간을 보실 수 있습니다.', ['<span>운영 지역</span>'], pic('w8', True)) +
            '<section class="sec"><div class="wrap"><div class="arows rv">' + rows + '</div><p class="snote">이동 시간은 본사(노원구 덕릉로 595)에서 각 구청 · 시청까지 차로 걸리는 시간(막히지 않을 때 기준)입니다. 출퇴근 시간에는 더 걸릴 수 있고, 표에 없는 지역 · 해외 행사도 전화 주시면 상담해 드립니다.</p></div></section>' + cta())
    urls.insert(0, page('areas/index.html', '운영 지역 | ' + NAME + ' — 노원 · 도봉 · 강북 · 중랑 · 성북 · 동대문 · 의정부 · 은평 · 남양주 행사',
                        '서울 노원 본사에서 서울 · 경기 어디든. 지역별 이동 시간과 그 지역에서 한 행사를 보실 수 있습니다.', main, img=pic('w8', True)))
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
    pages = ['', 'about.html', 'service.html', 'portfolio.html', 'video.html', 'notice.html', 'contact.html', 'quote.html']
    urls = [BASE + p for p in pages] + extra
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('  <url><loc>' + u + '</loc><lastmod>' + today + '</lastmod></url>\n' for u in urls) + '</urlset>\n'
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(xml)


if __name__ == '__main__':
    a = story_pages(); b = area_pages(); fix_same_folder(); sitemap(a + b)
    print('행사 이야기', len(a), '· 지역', len(b), '· sitemap.xml 갱신')

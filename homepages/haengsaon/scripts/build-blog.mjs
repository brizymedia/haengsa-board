/**
 * 행사ON 블로그 — _blog/posts/*.json 을 홈페이지 글로 만든다
 * ──────────────────────────────────────────────────────
 *   blog/               글 목록 (최신순, 24개씩 → blog/page/2/)
 *   blog/<지역>/        지역별 모음 (예: blog/asan/)
 *   blog/<글주소>/      글 하나
 *   rss.xml             블로그 RSS
 *   sitemap.xml · llms.txt 의 블로그 부분도 같이 갱신한다
 *
 * 사이트가 brizymedia.github.io/haengsaon/ 아래에 있어서, 글 JSON 의 주소는 사이트 루트 기준 /… 로 쓰고
 * 여기서 페이지 깊이에 맞는 ../ 상대 주소로 바꾼다(전용 도메인을 붙이면 SITE 한 줄만 고치면 된다).
 * 머리글 · 폰 메뉴 · 바닥글 · 빠른 연락 줄은 notice.html 에서 빌려 온다(tools/make_pages.py 와 같은 방식).
 * blog/ 는 매번 지우고 새로 만든다 — 결과 HTML 을 손으로 고치지 말고 원본 JSON 이나 이 템플릿을 고친다.
 * (HD기획 scripts/build-blog.mjs(큰길이벤트기획 원본)를 행사ON에 맞게 옮긴 것)
 *
 * 실행:  node scripts/build-blog.mjs      글 형식 · 규칙: _blog/GUIDE.md   ·   검사: node scripts/blog-check.mjs
 */
import { readFileSync, readdirSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

export const SITE = 'https://brizymedia.github.io/haengsaon';   // 끝에 / 없이
export const BRAND = '행사ON';
const TEL = '1800-7947';
const SMS = '010-9441-5542';
const 쪽당 = 24;

export const esc = (s) => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** 사이트 루트 기준 /주소 → 이 페이지에서 쓸 상대 주소. 앞 = '../' 를 깊이만큼 */
export const 상대 = (u, 앞) => (String(u).startsWith('/') ? (앞 + String(u).slice(1)) || './' : String(u));

/** 글 안에서는 **굵게** 와 [글자](주소) 만 쓴다. 주소는 / 로 시작하거나 https:// 여야 한다. */
export function 인라인(글, 앞 = '') {
  return esc(글)
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\[([^\]]+)\]\(((?:\/|https:\/\/)[^)\s]*)\)/g, (m, t, u) =>
      u.startsWith('/') ? `<a href="${상대(u, 앞)}">${t}</a>` : `<a href="${u}" target="_blank" rel="noopener">${t}</a>`);
}
export const 글자만 = (글) => String(글 ?? '').replace(/\*\*(.+?)\*\*/g, '$1').replace(/\[([^\]]+)\]\([^)]*\)/g, '$1');
export const 날짜글 = (d) => { const m = String(d || '').match(/^(\d{4})-(\d{2})-(\d{2})$/); return m ? `${m[1]}년 ${+m[2]}월 ${+m[3]}일` : String(d || ''); };
export const 글주소 = (slug) => `/blog/${encodeURIComponent(slug)}/`;

export function 지역표(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'regions.json'), 'utf8'));
  const 표 = new Map(j.지역.map((r) => [r.slug, r]));
  표.set('common', { slug: 'common', 이름: '행사 준비 공통', 서비스페이지: '', 이동: '', 비중: 0 });
  return 표;
}

/** photos.json 의 묶음을 사진 한 장씩 풀어 경로 → 정보 로 */
export function 사진목록(ROOT) {
  const j = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'photos.json'), 'utf8'));
  const 표 = new Map();
  j.묶음.forEach((g, i) => { (g.path || []).forEach((p) => 표.set(p, { ...g, path: p, 묶음번호: i })); });
  return 표;
}

export function 글읽기(ROOT) {
  const 폴더 = resolve(ROOT, '_blog', 'posts');
  if (!existsSync(폴더)) return [];
  return readdirSync(폴더).filter((f) => f.endsWith('.json')).map((f) => {
    const p = JSON.parse(readFileSync(resolve(폴더, f), 'utf8'));
    Object.defineProperty(p, '_파일', { value: f, enumerable: false });
    return p;
  }).sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : a.slug < b.slug ? -1 : 1));
}

/** 본문 글자 — 읽는 시간·검사·중복 비교에 쓴다 */
export function 본문글(p) {
  const 조각 = [p.lead, ...(p.points || [])];
  for (const s of p.sections || []) {
    조각.push(s.h2);
    for (const b of s.blocks || []) {
      if (b.p) 조각.push(b.p);
      if (b.tip) 조각.push(b.tip);
      if (b.ul) 조각.push(...b.ul);
      if (b.ol) 조각.push(...b.ol);
      if (b.table) 조각.push(...(b.table.head || []), ...(b.table.rows || []).flat());
    }
  }
  for (const f of p.faq || []) 조각.push(f.q, f.a);
  return 조각.map(글자만).join('\n');
}

export function 글이미지들(p) {
  const 목록 = p.cover ? [p.cover] : [];
  for (const s of p.sections || []) for (const b of s.blocks || []) if (b.img) 목록.push(b.img);
  return 목록;
}

/* 사이트 style.css 위에 블로그 본문만 얹는다(.bl 아래로 묶음). 색은 사이트 변수 그대로 */
const CSS = `
.bl-crumb{width:min(1200px,100% - 40px);margin:0 auto;padding:22px 0 0;font-size:13px;color:var(--mute)}
.bl-crumb.narrow{width:min(760px,100% - 40px)}.bl-crumb a:hover{color:var(--on-ink)}
.bl-art{width:min(760px,100% - 40px);margin:0 auto;padding:14px 0 56px}
.bl .eyebrow2{display:inline-flex;align-items:center;gap:8px;font-family:var(--en);font-size:12px;font-weight:700;letter-spacing:.16em;color:var(--on-ink);margin:0 0 12px;text-transform:uppercase}
.bl .eyebrow2::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--on);box-shadow:0 0 8px var(--glow)}
.bl h1{font-size:clamp(26px,4.2vw,40px);line-height:1.3;letter-spacing:-.03em;margin:0 0 16px;font-weight:700;color:var(--ink);text-wrap:balance}
.bl .meta{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 24px}
.bl .meta a,.bl .meta span{font-size:13px;font-weight:600;padding:5px 12px;border-radius:999px;background:var(--soft);color:var(--mute)}
.bl .meta a{background:rgba(25,210,122,.13);color:var(--on-ink)}.bl .meta a:hover{background:rgba(25,210,122,.22)}
.bl .lead{font-size:17px;line-height:1.85;color:var(--ink);margin:0 0 24px}.bl .lead a{color:var(--on-ink);font-weight:700;text-decoration:underline}
.bl figure{margin:0 0 28px}.bl figure img{width:100%;height:auto;aspect-ratio:4/3;object-fit:cover;border-radius:14px;background:var(--soft)}
.bl figure.cover img{aspect-ratio:16/9}
.bl figcaption{font-size:13.5px;color:var(--mute);margin-top:8px;line-height:1.6}
.bl .points{background:var(--soft);border-radius:14px;padding:18px 22px;margin:0 0 28px}
.bl .points b{display:block;font-family:var(--en);font-size:12px;letter-spacing:.18em;color:var(--on-ink);margin-bottom:8px}
.bl .points ul,.bl .body ul{list-style:disc;padding-left:20px}.bl .body ol{list-style:decimal;padding-left:20px}
.bl .points li{line-height:1.75;margin:4px 0;color:var(--ink)}
.bl .toc{border-left:3px solid var(--on);padding:2px 0 2px 16px;margin:0 0 36px}
.bl .toc b{font-size:13px;color:var(--mute)}.bl .toc ol{margin:6px 0 0}.bl .toc li{line-height:1.9}.bl .toc a:hover{color:var(--on-ink)}
.bl .body h2,.bl .faq h2{font-size:22px;line-height:1.4;letter-spacing:-.02em;margin:42px 0 14px;font-weight:700;color:var(--ink);scroll-margin-top:calc(var(--hd) + 16px);text-wrap:balance}
.bl .body p,.bl .faq p{font-size:16px;line-height:1.95;color:var(--ink2);margin:0 0 18px}
.bl .body ul,.bl .body ol{margin:0 0 20px;color:var(--ink2)}.bl .body li{line-height:1.85;margin:5px 0}
.bl .body b{color:var(--ink)}.bl .body a,.bl .faq a{color:var(--on-ink);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.bl .tbl{overflow-x:auto;margin:0 0 22px;border:1px solid var(--line);border-radius:12px;background:#fff}
.bl table{border-collapse:collapse;width:100%;font-size:14.5px;min-width:520px}
.bl th,.bl td{padding:10px 13px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line);line-height:1.6}
.bl th{background:var(--soft);font-weight:700;white-space:nowrap;color:var(--ink)}.bl tbody tr:last-child td{border-bottom:0}
.bl .tip{background:rgba(25,210,122,.1);border-radius:12px;padding:14px 18px;margin:0 0 22px;font-size:15.5px;line-height:1.8;color:var(--ink)}
.bl .tip::before{content:'현장 메모';display:block;font-size:12px;font-weight:700;letter-spacing:.08em;color:var(--on-ink);margin-bottom:3px}
.bl .faq details{background:#fff;border:1px solid var(--line);border-radius:12px;margin:0 0 8px;padding:0 16px}
.bl .faq summary{cursor:pointer;font-weight:700;padding:13px 0;line-height:1.6;color:var(--ink)}.bl .faq details p{margin:0 0 14px}
.bl .src{margin-top:32px;font-size:13.5px;color:var(--mute);line-height:1.7}.bl .src ul{list-style:disc;padding-left:18px;margin:6px 0 0}.bl .src a{text-decoration:underline}
.bl .bcta{background:var(--ink);color:#fff;border-radius:18px;padding:26px;margin-top:40px;display:flex;flex-wrap:wrap;gap:18px;align-items:center;justify-content:space-between}
.bl .bcta h3{margin:0 0 5px;font-size:20px;letter-spacing:-.02em}.bl .bcta p{margin:0;color:#C8D2DF;font-size:14.5px;line-height:1.7}
.bl .bcta .num{font-family:var(--en);font-weight:800;font-size:24px;color:#fff;display:block;margin-bottom:10px}.bl .bcta .num small{font:600 12px var(--kr);color:var(--on);margin-left:6px}
.bl .bcta .btns{display:flex;gap:8px;flex-wrap:wrap}
.bl .bcta .btn-ghost{color:#fff;border-color:rgba(255,255,255,.35)}
.bl-more{width:min(1200px,100% - 40px);margin:0 auto;padding:8px 0 64px}.bl-more h2{font-size:20px;margin:0 0 16px;color:var(--ink)}
.bl-wrap{width:min(1200px,100% - 40px);margin:0 auto;padding:18px 0 64px}
.bl .cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.bl .card{display:block;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:transform .35s,box-shadow .35s}
.bl .card:hover{transform:translateY(-4px);box-shadow:var(--sh)}
.bl .card img{width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;background:var(--soft)}
.bl .card .in{padding:14px 16px 17px}.bl .card .r{font-size:12px;font-weight:700;color:var(--on-ink);margin-bottom:6px}
.bl .card .t{font-size:16.5px;font-weight:700;line-height:1.45;letter-spacing:-.02em;color:var(--ink)}
.bl .card .s{font-size:13.5px;color:var(--mute);line-height:1.6;margin-top:6px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.bl .chips{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 28px}
.bl .chips a{font-size:14px;font-weight:600;padding:8px 14px;border-radius:999px;background:#fff;border:1px solid var(--line);color:var(--ink2)}
.bl .chips a[aria-current]{background:var(--ink);color:#fff;border-color:var(--ink)}.bl .chips small{font-weight:600;margin-left:4px;opacity:.6}
.bl .pager{display:flex;gap:7px;justify-content:center;margin-top:32px}
.bl .pager a,.bl .pager span{padding:8px 14px;border-radius:8px;border:1px solid var(--line);font-weight:700;font-size:14px;background:#fff}.bl .pager span{background:var(--ink);color:#fff}
.bl .empty{background:#fff;border:1px dashed var(--line);border-radius:14px;padding:22px;color:var(--mute);line-height:1.8;margin-bottom:24px}
.bl a:focus-visible,.bl summary:focus-visible{outline:2px solid var(--on);outline-offset:3px;border-radius:4px}
@media (max-width:640px){.bl .bcta{padding:22px 18px}.bl .lead{font-size:16px}}
@media (prefers-reduced-motion:reduce){.bl .card{transition:none}.bl .card:hover{transform:none}}
`.trim();

export function buildBlog(옵션 = {}) {
  const ROOT = 옵션.ROOT;
  const 절대 = (path) => SITE + String(path).split('/').map(encodeURIComponent).join('/');   // og · JSON-LD 용
  const 썸네일 = (path) => String(path).replace('/assets/img/p/', '/assets/img/t/');
  const 지역 = 지역표(ROOT);
  const posts = 글읽기(ROOT);
  const 제이슨 = (o) => `<script type="application/ld+json">${JSON.stringify(o).replace(/</g, '\\u003c')}</script>`;

  /* 사이트 틀 — notice.html 의 <main> 앞뒤 */
  const 원본 = readFileSync(resolve(ROOT, 'notice.html'), 'utf8').replace(/\r\n/g, '\n');
  const 틀위 = 원본.slice(0, 원본.indexOf('<main id="top">'));
  const 틀아래 = 원본.slice(원본.indexOf('</main>') + '</main>'.length);

  rmSync(resolve(ROOT, 'blog'), { recursive: true, force: true });
  const 쓰기 = (폴더, html) => {
    const d = resolve(ROOT, 폴더);
    mkdirSync(d, { recursive: true });
    writeFileSync(resolve(d, 'index.html'), html, 'utf8');
  };

  /** 틀에 제목 · 설명 · 주소를 끼우고, 상대 주소를 깊이에 맞춘다 */
  const 페이지 = ({ 제목, 설명, 경로, 이미지, 종류 = 'website', 더넣기 = '', 색인 = true, 본문 }) => {
    const 깊이 = 경로.split('/').filter(Boolean).length;   // /blog/ = 1, /blog/x/ = 2
    const 앞 = '../'.repeat(깊이);
    const url = SITE + 경로;
    const 바꿈 = (s, 식, 값) => s.replace(식, (m, a) => a + 값);
    let 위 = 틀위;
    위 = 위.replace(/<title>[^]*?<\/title>/, `<title>${esc(제목)}</title>`);
    위 = 바꿈(위, /(<meta name="description" content=")[^"]*/, esc(설명));
    위 = 바꿈(위, /(<meta property="og:description" content=")[^"]*/, esc(설명));
    위 = 바꿈(위, /(<meta property="og:title" content=")[^"]*/, esc(제목));
    위 = 바꿈(위, /(<link rel="canonical" href=")[^"]*/, url);
    위 = 바꿈(위, /(<meta property="og:url" content=")[^"]*/, url);
    위 = 바꿈(위, /(<meta property="og:image" content=")[^"]*/, esc(이미지));
    위 = 바꿈(위, /(<meta name="robots" content=")[^"]*/, 색인 ? 'index,follow,max-image-preview:large' : 'noindex,follow');
    위 = 바꿈(위, /(<meta property="og:type" content=")[^"]*/, 종류);
    위 = 위.replace(/<meta property="og:image:(?:width|height)"[^>]*>\n?/g, '')
      .replace(/<meta name="hs-edit"[^>]*>\n?/g, '')
      .replace(/<meta name="keywords"[^>]*>\n?/g, '')
      .replace(/<script type="application\/ld\+json">\{"@context": "https:\/\/schema.org", "@type": "BreadcrumbList"[^]*?<\/script>\n?/, '')
      .replace(/ class="act"/g, '').replace(/class="act" /g, '')
      .replace('</head>', `<link rel="alternate" type="application/rss+xml" title="${BRAND} 행사 준비 블로그" href="${SITE}/rss.xml">\n${더넣기}\n<style>${CSS}</style>\n</head>`)
      .replace(/(<nav class="menu"[^>]*>[^]*?)<a href="blog\/">/, '$1<a href="blog/" class="act" aria-current="page">');
    const 아래 = 틀아래.replace(/<script src="assets\/edit\.js[^"]*"><\/script>\n?/, '');
    let out = 위 + '<main id="top" class="bl">\n' + 본문 + '\n</main>' + 아래;
    out = out.replace(/(href|src)="(?!https?:|mailto:|tel:|sms:|#|\/|\.\.\/|\.\/|data:)([^"]+)"/g, (m, k, v) => `${k}="${앞}${v}"`);
    out = out.replace(/url\((?!https?:)(assets\/[^)]+)\)/g, (m, v) => `url(${앞}${v})`);
    return out;
  };

  const 상담 = (앞) => `<div class="bcta">
    <div><h3>행사 날짜가 정해지셨나요?</h3><p>날짜 · 장소 · 인원만 알려 주시면 구성과 견적을 정리해 드립니다. 상담은 24시간 받습니다.</p></div>
    <div><a class="num" href="tel:${TEL}">${TEL}<small>24시 상담</small></a><div class="btns"><a class="btn btn-on" href="${앞}quote.html">자동 견적서</a><a class="btn btn-ghost" href="${앞}contact.html">예약 · 문의 폼</a><a class="btn btn-ghost" href="sms:${SMS}">문자 ${SMS}</a></div></div>
  </div>`;

  const 카드 = (p, 앞) => {
    const r = 지역.get(p.region);
    return `<a class="card" href="${상대(글주소(p.slug), 앞)}">
      <img src="${esc(상대(썸네일(p.cover.path), 앞))}" alt="${esc(p.cover.alt)}" loading="lazy" decoding="async" width="800" height="500">
      <div class="in"><div class="r">${esc(r ? r.이름 : '')} · ${esc(날짜글(p.date))}</div><div class="t">${esc(p.title)}</div><div class="s">${esc(p.description)}</div></div>
    </a>`;
  };

  const 개수 = new Map();
  posts.forEach((p) => 개수.set(p.region, (개수.get(p.region) || 0) + 1));
  const 칩 = (현재, 앞) => `<nav class="chips" aria-label="지역별 글">
    <a href="${상대('/blog/', 앞)}"${현재 === '' ? ' aria-current="page"' : ''}>전체<small>${posts.length}</small></a>
    ${[...지역.values()].filter((r) => 개수.get(r.slug)).map((r) =>
      `<a href="${상대(`/blog/${r.slug}/`, 앞)}"${현재 === r.slug ? ' aria-current="page"' : ''}>${esc(r.이름)}<small>${개수.get(r.slug)}</small></a>`).join('\n    ')}
  </nav>`;

  /* ── 글 페이지 ── */
  for (const p of posts) {
    const r = 지역.get(p.region) || { 이름: '', 서비스페이지: '' };
    const 지역글 = p.region !== 'common';
    const 경로 = 글주소(p.slug);
    const 앞 = '../../';
    const 분 = Math.max(1, Math.round(본문글(p).length / 500));
    const 관련 = [...posts.filter((o) => o !== p && o.region === p.region),
                  ...posts.filter((o) => o !== p && o.region !== p.region && o.topic === p.topic),
                  ...posts.filter((o) => o !== p && o.region !== p.region && o.topic !== p.topic)].slice(0, 3);
    const 이미지html = (im, 표지) => `<figure${표지 ? ' class="cover"' : ''}>
    <img src="${esc(상대(im.path, 앞))}" alt="${esc(im.alt)}" ${표지 ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async" width="${표지 ? 1600 : 1200}" height="900">
    <figcaption>${인라인(im.caption, 앞)}</figcaption>
  </figure>`;
    const 블록 = (b) => {
      if (b.p) return `<p>${인라인(b.p, 앞)}</p>`;
      if (b.tip) return `<div class="tip">${인라인(b.tip, 앞)}</div>`;
      if (b.ul) return `<ul>${b.ul.map((x) => `<li>${인라인(x, 앞)}</li>`).join('')}</ul>`;
      if (b.ol) return `<ol>${b.ol.map((x) => `<li>${인라인(x, 앞)}</li>`).join('')}</ol>`;
      if (b.table) return `<div class="tbl"><table><thead><tr>${b.table.head.map((h) => `<th scope="col">${인라인(h, 앞)}</th>`).join('')}</tr></thead><tbody>${
        b.table.rows.map((row) => `<tr>${row.map((c) => `<td>${인라인(c, 앞)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
      if (b.img) return 이미지html(b.img, false);
      return '';
    };

    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        ...(지역글 ? [{ '@type': 'ListItem', position: 3, name: r.이름 + ' 행사 준비', item: `${SITE}/blog/${p.region}/` }] : []),
        { '@type': 'ListItem', position: 지역글 ? 4 : 3, name: p.title, item: SITE + 경로 } ] },
      { '@type': 'BlogPosting', '@id': SITE + 경로, headline: p.title, description: p.description,
        image: 글이미지들(p).map((im) => 절대(im.path)),
        datePublished: p.date, dateModified: p.updated || p.date, inLanguage: 'ko',
        keywords: [p.keyword.main, ...(p.keyword.sub || [])].join(', '),
        author: { '@type': 'Organization', name: BRAND, url: SITE + '/' },
        publisher: { '@id': SITE + '/#business' },
        mainEntityOfPage: { '@type': 'WebPage', '@id': SITE + 경로 },
        ...(지역글 ? { spatialCoverage: { '@type': 'Place', name: r.도 === r.시군 ? r.시군 : `${r.도} ${r.시군}` } } : {}) },
      ...((p.faq || []).length ? [{ '@type': 'FAQPage', '@id': SITE + 경로 + '#faq',
        mainEntity: p.faq.map((f) => ({ '@type': 'Question', name: f.q, acceptedAnswer: { '@type': 'Answer', text: 글자만(f.a) } })) }] : []),
    ] };

    const 본문 = `<div class="bl-crumb narrow"><a href="${앞}index.html">홈</a> › <a href="${앞}blog/">블로그</a>${지역글 ? ` › <a href="${앞}blog/${p.region}/">${esc(r.이름)}</a>` : ''}</div>
<article class="bl-art">
  <p class="eyebrow2">${esc(지역글 ? r.이름 + ' 행사 준비' : '행사 준비')} · ${esc(날짜글(p.date))}</p>
  <h1>${esc(p.title)}</h1>
  <div class="meta">
    ${지역글 ? `<a href="${앞}blog/${p.region}/">${esc(r.이름)} 글 모음</a>` : ''}
    ${r.서비스페이지 ? `<a href="${상대(r.서비스페이지, 앞)}">${esc(r.이름)} 행사 안내</a>` : ''}
    <span>읽는 시간 약 ${분}분</span>
  </div>
  <p class="lead">${인라인(p.lead, 앞)}</p>
  ${이미지html(p.cover, true)}
  <div class="points"><b>이 글의 요점</b><ul>${p.points.map((x) => `<li>${인라인(x, 앞)}</li>`).join('')}</ul></div>
  <nav class="toc" aria-label="목차"><b>목차</b><ol>${p.sections.map((s, i) => `<li><a href="#s${i + 1}">${esc(s.h2)}</a></li>`).join('')}</ol></nav>
  <div class="body">
${p.sections.map((s, i) => `<h2 id="s${i + 1}">${esc(s.h2)}</h2>\n${s.blocks.map(블록).join('\n')}`).join('\n')}
  </div>
  ${(p.faq || []).length ? `<section class="faq" id="faq"><h2>자주 묻는 질문</h2>${p.faq.map((f) => `<details><summary>${esc(f.q)}</summary><p>${인라인(f.a, 앞)}</p></details>`).join('')}</section>` : ''}
  ${(p.sources || []).length ? `<div class="src"><b>확인한 자료</b> (${esc(날짜글(p.updated || p.date))} 기준)<ul>${p.sources.map((s) => `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)}</a></li>`).join('')}</ul></div>` : ''}
  ${상담(앞)}
</article>
${관련.length ? `<section class="bl-more"><h2>같이 보면 좋은 글</h2><div class="cards">${관련.map((o) => 카드(o, 앞)).join('\n')}</div></section>` : ''}`;
    쓰기(`blog/${p.slug}`, 페이지({ 제목: `${p.title} | ${BRAND}`, 설명: p.description, 경로, 이미지: 절대(p.cover.path), 종류: 'article',
      더넣기: `<meta property="article:published_time" content="${p.date}">\n${제이슨(ld)}`, 본문 }));
  }

  /* ── 목록 (blog/, blog/page/N/) ── */
  const 대표이미지 = posts[0] ? 절대(posts[0].cover.path) : `${SITE}/assets/img/og.jpg`;
  const 쪽수 = Math.max(1, Math.ceil(posts.length / 쪽당));
  for (let n = 1; n <= 쪽수; n++) {
    const 조각 = posts.slice((n - 1) * 쪽당, n * 쪽당);
    const 경로 = n === 1 ? '/blog/' : `/blog/page/${n}/`;
    const 앞 = n === 1 ? '../' : '../../../';
    const 쪽나눔 = 쪽수 > 1 ? `<nav class="pager" aria-label="쪽 이동">${Array.from({ length: 쪽수 }, (_, i) => i + 1).map((k) =>
      k === n ? `<span aria-current="page">${k}</span>` : `<a href="${상대(k === 1 ? '/blog/' : `/blog/page/${k}/`, 앞)}">${k}</a>`).join('')}</nav>` : '';
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' } ] },
      { '@type': 'Blog', '@id': SITE + '/blog/', name: `${BRAND} 행사 준비 블로그`, inLanguage: 'ko', publisher: { '@id': SITE + '/#business' },
        blogPost: 조각.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug), datePublished: p.date, image: 절대(p.cover.path) })) } ] };
    const 본문 = `<div class="bl-crumb"><a href="${앞}index.html">홈</a> › 블로그${n > 1 ? ` › ${n}쪽` : ''}</div>
<div class="bl-wrap">
  <p class="eyebrow2">Blog · Event guide</p>
  <h1>행사 준비 블로그</h1>
  <p class="lead" style="max-width:760px">아파트 주민행사 · 학교축제 · 체육대회 · 기업행사를 맡은 담당자가 먼저 확인할 것들을 지역별로 정리합니다. 장비와 배치, 날씨와 안전, 견적 항목까지 현장 기준으로 씁니다.</p>
  ${칩('', 앞)}
  ${posts.length ? `<div class="cards">${조각.map((p) => 카드(p, 앞)).join('\n')}</div>` : '<div class="empty">첫 글을 준비하고 있습니다.</div>'}
  ${쪽나눔}
  ${상담(앞)}
</div>`;
    쓰기(n === 1 ? 'blog' : `blog/page/${n}`, 페이지({
      제목: n === 1 ? `행사 준비 블로그 — 아산 · 천안 · 충남 지역별 행사 준비 정보 | ${BRAND}` : `행사 준비 블로그 ${n}쪽 | ${BRAND}`,
      설명: '아산 · 천안 · 평택 · 예산 · 당진 · 공주 · 세종 · 서산 · 논산에서 행사를 준비하는 담당자를 위한 글. 아파트 주민행사 · 학교축제 · 체육대회 · 물놀이 · 무대 · 음향 · 천막까지 현장 기준으로 정리합니다.',
      경로, 이미지: 대표이미지, 더넣기: 제이슨(ld), 본문 }));
  }

  /* ── 지역 모음 (blog/<지역>/) ── */
  const 허브 = [];
  for (const r of 지역.values()) {
    const 목록 = posts.filter((p) => p.region === r.slug);
    if (r.slug === 'common' && !목록.length) continue;
    const 경로 = `/blog/${r.slug}/`;
    const 앞 = '../../';
    const 허브제목 = r.slug === 'common' ? '행사 준비 공통 정보' : `${r.이름} 행사 준비 정보`;
    const 소개 = r.slug === 'common'
      ? '지역과 상관없이 행사 준비에 두루 쓰이는 글입니다.'
      : `${esc(r.이름)}에서 행사를 준비하는 담당자를 위한 글입니다. ${esc(r.이동)}(막히지 않을 때).${r.서비스페이지 ? ` 서비스 안내는 <a href="${상대(r.서비스페이지, 앞)}" style="text-decoration:underline">${esc(r.이름)} 행사 안내 페이지</a>에 있습니다.` : ''}`;
    const ld = { '@context': 'https://schema.org', '@graph': [
      { '@type': 'BreadcrumbList', itemListElement: [
        { '@type': 'ListItem', position: 1, name: '홈', item: SITE + '/' },
        { '@type': 'ListItem', position: 2, name: '블로그', item: SITE + '/blog/' },
        { '@type': 'ListItem', position: 3, name: 허브제목, item: SITE + 경로 } ] },
      { '@type': 'CollectionPage', '@id': SITE + 경로, name: 허브제목, inLanguage: 'ko',
        hasPart: 목록.map((p) => ({ '@type': 'BlogPosting', headline: p.title, url: SITE + 글주소(p.slug) })) } ] };
    const 본문 = `<div class="bl-crumb"><a href="${앞}index.html">홈</a> › <a href="${앞}blog/">블로그</a> › ${esc(r.이름)}</div>
<div class="bl-wrap">
  <p class="eyebrow2">${r.slug === 'common' ? 'Guide' : esc(r.도 === r.시군 ? r.시군 : `${r.도} ${r.시군}`)}</p>
  <h1>${esc(허브제목)}</h1>
  <p class="lead" style="max-width:760px">${소개}</p>
  ${칩(r.slug, 앞)}
  ${목록.length ? `<div class="cards">${목록.map((p) => 카드(p, 앞)).join('\n')}</div>`
    : `<div class="empty">${esc(r.이름)} 글은 곧 올라옵니다. 그동안 다른 지역 글을 참고해 보세요.</div>${posts.length ? `<div class="cards">${posts.slice(0, 6).map((p) => 카드(p, 앞)).join('\n')}</div>` : ''}`}
  ${상담(앞)}
</div>`;
    쓰기(`blog/${r.slug}`, 페이지({
      제목: `${허브제목} — 주민행사 · 학교축제 · 체육대회 · 음향 · 천막 | ${BRAND}`,
      설명: r.slug === 'common' ? '지역과 상관없이 행사 준비에 두루 필요한 내용. 준비 순서 · 안전 · 견적 항목을 현장 기준으로 정리한 글 모음입니다.' : `${r.이름}에서 행사를 준비할 때 확인할 것들. 아파트 주민행사 · 학교축제 · 체육대회 같은 행사와 음향 · 조명 · 무대 · 천막, 날씨와 안전, 견적 항목까지 현장 기준으로 정리한 글 모음입니다.`,
      경로, 이미지: 목록[0] ? 절대(목록[0].cover.path) : 대표이미지, 색인: 목록.length > 0, 더넣기: 제이슨(ld), 본문 }));
    if (목록.length) 허브.push({ loc: 경로, lastmod: 목록[0].updated || 목록[0].date });
  }

  /* ── sitemap.xml — 기존 항목은 두고 /blog/ 부분만 바꾼다 ── */
  const 블로그주소 = posts.length ? [
    { loc: '/blog/', lastmod: posts[0].updated || posts[0].date },
    ...허브,
    ...posts.map((p) => ({ loc: 글주소(p.slug), lastmod: p.updated || p.date })),
  ] : [];
  const sm = resolve(ROOT, 'sitemap.xml');
  if (existsSync(sm)) {
    let xml = readFileSync(sm, 'utf8');
    xml = xml.replace(/[ \t]*<url><loc>[^<]*\/blog\/[^<]*<\/loc>[^]*?<\/url>\n?/g, '');
    const 추가 = 블로그주소.map((u) => `  <url><loc>${SITE}${u.loc}</loc><lastmod>${u.lastmod}</lastmod></url>\n`).join('');
    xml = xml.replace(/<\/urlset>\s*$/, 추가 + '</urlset>\n');
    writeFileSync(sm, xml, 'utf8');
  }

  /* ── llms.txt — 「## 블로그」 절을 다시 쓴다 ── */
  const ll = resolve(ROOT, 'llms.txt');
  if (existsSync(ll) && posts.length) {
    let t = readFileSync(ll, 'utf8').replace(/\r\n/g, '\n');
    const 절 = `## 블로그 (행사 준비 정보, 지역별)\n- [행사 준비 블로그](${SITE}/blog/): 아산 · 천안 · 충남 지역별 행사 준비 체크리스트\n` +
      posts.map((p) => `- [${p.title}](${SITE}${글주소(p.slug)}): ${p.description}`).join('\n') + '\n';
    t = /^## 블로그[^]*?(?=^## |(?![^]))/m.test(t) ? t.replace(/^## 블로그[^]*?(?=^## |(?![^]))/m, 절) : t.trimEnd() + '\n\n' + 절;
    writeFileSync(ll, t, 'utf8');
  }

  /* ── rss.xml ── */
  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>${esc(BRAND)} 행사 준비 블로그</title><link>${SITE}/blog/</link><description>아산 · 천안 · 충남에서 행사를 준비하는 담당자를 위한 글</description><language>ko</language>
${posts.slice(0, 50).map((p) => `<item><title>${esc(p.title)}</title><link>${SITE}${글주소(p.slug)}</link><guid>${SITE}${글주소(p.slug)}</guid><description>${esc(p.description)}</description><pubDate>${new Date(p.date + 'T09:00:00+09:00').toUTCString()}</pubDate></item>`).join('\n')}
</channel></rss>
`;
  writeFileSync(resolve(ROOT, 'rss.xml'), rss, 'utf8');

  return { posts, 블로그주소 };
}

/* 혼자 실행할 때 */
const 이파일 = fileURLToPath(import.meta.url);
if (process.argv[1] && resolve(process.argv[1]) === 이파일) {
  const ROOT = resolve(dirname(이파일), '..');
  const { posts, 블로그주소 } = buildBlog({ ROOT });
  console.log(`blog/: 글 ${posts.length}개 · sitemap 항목 ${블로그주소.length}개 · rss.xml · llms.txt 갱신`);
}

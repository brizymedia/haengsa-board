/* ─────────────────────────────────────────────
   행사 고시 알림판 — 공통 스크립트
   외부 라이브러리 없음. events.json 하나만 읽습니다.
   ───────────────────────────────────────────── */
const KIND_LABEL = { bid: "입찰", festival: "축제", notice: "고시" };
const SIDO_ORDER = ["서울","부산","대구","인천","광주","대전","울산","세종",
                    "경기","강원","충북","충남","전북","전남","경북","경남","제주"];

/* ── 도우미 ─────────────────────────────── */
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g,
  c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c]));

function won(v){
  const n = parseInt(v, 10);
  if (!n || isNaN(n)) return "";
  if (n >= 100000000){
    const e = n / 100000000;
    return (e % 1 ? e.toFixed(1) : e) + "억원";
  }
  return Math.round(n / 10000).toLocaleString() + "만원";
}

function ymd(s){
  const d = String(s || "").replace(/\D/g, "").slice(0, 8);
  return d.length === 8 ? d : null;
}

function daysLeft(s){
  const d = ymd(s);
  if (!d) return null;
  const t = new Date(+d.slice(0,4), +d.slice(4,6)-1, +d.slice(6,8));
  const now = new Date(); now.setHours(0,0,0,0);
  return Math.round((t - now) / 86400000);
}

function sealHTML(rec){
  const n = daysLeft(rec.deadline);
  if (n === null) return `<div class="seal none"><span class="n">상시</span></div>`;
  if (n < 0)      return `<div class="seal none"><span class="n">종료</span></div>`;
  const openNow = rec.kind === "festival" &&
                  ymd(rec.start_date) && ymd(rec.start_date) <= ymd(new Date().toISOString());
  if (openNow)    return `<div class="seal open"><span class="n">진행</span><span class="u">중</span></div>`;
  if (n === 0)    return `<div class="seal soon"><span class="n">오늘</span><span class="u">마감</span></div>`;
  return `<div class="seal${n <= 3 ? " soon" : ""}"><span class="n">${n}</span><span class="u">일 남음</span></div>`;
}

function highlight(text, q){
  const safe = esc(text);
  if (!q) return safe;
  const needle = esc(q).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return safe.replace(new RegExp(needle, "gi"), m => `<mark>${m}</mark>`);
}

/* ── 데이터 ─────────────────────────────── */
async function loadData(){
  // 단일 파일(미리보기.html)로 열었을 때는 문서에 심어둔 데이터를 쓴다.
  // file:// 에서는 브라우저가 보안 정책상 fetch로 로컬 파일을 읽지 못한다.
  if (window.__EVENTS__) return window.__EVENTS__;
  try {
    const r = await fetch("data/events.json", { cache: "no-store" });
    if (!r.ok) throw new Error(r.status);
    return await r.json();
  } catch (e) {
    console.warn("events.json을 읽지 못했습니다:", e);
    return { generated_at: "", count: 0, items: [], error: true, offline: true };
  }
}

function fillStats(data){
  const g = $("#genAt"), t = $("#total"), f = $("#mockflag");
  if (g) g.textContent = (data.generated_at || "—").replace("T", " ").slice(0, 16);
  if (t) t.textContent = (data.items || []).length;
  if (f && data.mock) f.hidden = false;
}

/* ── 알림판 (index) ─────────────────────── */
function initBoard(data){
  const all = data.items || [];
  const state = { kind: "all", region: "all", q: "", sort: "deadline", page: 1 };
  const PER = 20;

  // 지역 칩은 실제 데이터에 있는 시도만 만든다
  const present = new Set(all.map(r => r.region));
  const regionRow = $("#regionRow");
  ["all", ...SIDO_ORDER.filter(s => present.has(s))].forEach(r => {
    const b = document.createElement("button");
    b.className = "chip";
    b.dataset.region = r;
    b.textContent = r === "all" ? "전국" : r;
    b.setAttribute("aria-pressed", String(r === "all"));
    regionRow.appendChild(b);
  });

  function filtered(){
    const q = state.q.trim().toLowerCase();
    let rows = all.filter(r =>
      (state.kind === "all" || r.kind === state.kind) &&
      (state.region === "all" || r.region === state.region) &&
      (!q || (r.title + " " + (r.org || "")).toLowerCase().includes(q)));

    const key = {
      deadline: r => { const n = daysLeft(r.deadline); return n === null ? 9999 : (n < 0 ? 9998 : n); },
      recent:   r => -(+(ymd(r.posted_at) || ymd(r.start_date) || "0")),
      budget:   r => -(parseInt(r.budget, 10) || 0),
    }[state.sort];
    return rows.sort((a, b) => key(a) - key(b));
  }

  function render(){
    const rows = filtered();
    const pages = Math.max(1, Math.ceil(rows.length / PER));
    state.page = Math.min(state.page, pages);
    const slice = rows.slice((state.page - 1) * PER, state.page * PER);

    $("#resultCount").textContent = rows.length
      ? `${rows.length}건 중 ${(state.page-1)*PER+1}–${(state.page-1)*PER+slice.length}`
      : "";

    const list = $("#list");
    if (!rows.length){
      list.innerHTML = data.error
        ? `<div class="empty"><b>공고를 불러오지 못했습니다</b>
             data/events.json 파일이 있는지 확인한 뒤 새로고침하세요.</div>`
        : `<div class="empty"><b>해당 조건의 공고가 없습니다</b>
             구분이나 지역을 바꾸거나, 검색어를 지워보세요.</div>`;
      $("#pager").innerHTML = "";
      return;
    }

    list.innerHTML = slice.map(r => {
      const period = r.start_date
        ? `${r.start_date} ~ ${r.end_date || ""}`
        : (r.deadline ? `마감 ${r.deadline}`
                      : (r.posted_at ? `게시 ${r.posted_at}` : "상시"));
      const amt = r.budget ? ` · 추정가 <span class="amt">${won(r.budget)}</span>` : "";
      return `<a class="item" data-kind="${esc(r.kind)}"
                 href="${esc(r.url || '#')}" target="_blank" rel="noopener noreferrer">
        <div>
          <div class="meta">
            <span class="tag ${esc(r.kind)}">${KIND_LABEL[r.kind] || esc(r.kind)}</span>
            <span>${esc(r.region || "")}</span>
            <span>${esc(r.source || "")}</span>
          </div>
          <div class="title">${highlight(r.title, state.q.trim())}</div>
          <div class="sub">${esc(r.org || "")}${r.org ? " · " : ""}${esc(period)}${amt}</div>
        </div>
        ${sealHTML(r)}
      </a>`;
    }).join("");

    // 페이지 이동
    const btn = (label, page, cur, dis) =>
      `<button data-page="${page}"${cur ? ' aria-current="true"' : ""}${dis ? " disabled" : ""}>${label}</button>`;
    let html = btn("‹", state.page - 1, false, state.page === 1);
    const from = Math.max(1, state.page - 2), to = Math.min(pages, from + 4);
    for (let i = from; i <= to; i++) html += btn(i, i, i === state.page, false);
    html += btn("›", state.page + 1, false, state.page === pages);
    $("#pager").innerHTML = pages > 1 ? html : "";
  }

  document.addEventListener("click", e => {
    const chip = e.target.closest(".chip");
    if (chip){
      [...chip.parentElement.querySelectorAll(".chip")]
        .forEach(c => c.setAttribute("aria-pressed", "false"));
      chip.setAttribute("aria-pressed", "true");
      if (chip.dataset.kind)   state.kind = chip.dataset.kind;
      if (chip.dataset.region) state.region = chip.dataset.region;
      state.page = 1; render(); return;
    }
    const sort = e.target.closest(".sortbtns button");
    if (sort){
      [...sort.parentElement.children].forEach(b => b.setAttribute("aria-pressed", "false"));
      sort.setAttribute("aria-pressed", "true");
      state.sort = sort.dataset.sort; state.page = 1; render(); return;
    }
    const pg = e.target.closest("#pager button");
    if (pg && !pg.disabled){
      state.page = +pg.dataset.page;
      render();
      window.scrollTo({ top: 0 });
    }
  });

  let timer;
  $("#search").addEventListener("input", e => {
    clearTimeout(timer);
    timer = setTimeout(() => { state.q = e.target.value; state.page = 1; render(); }, 180);
  });

  render();
}

/* ── 달력 (calendar) ────────────────────── */
function initCalendar(data){
  const fests = (data.items || []).filter(r => r.kind === "festival" && ymd(r.start_date));
  let cur = new Date(); cur.setDate(1);

  function render(){
    const y = cur.getFullYear(), m = cur.getMonth();
    $("#calTitle").textContent = `${y}년 ${m + 1}월`;

    const first = new Date(y, m, 1), last = new Date(y, m + 1, 0);
    const startPad = first.getDay();
    const cells = [];
    for (let i = startPad; i > 0; i--)
      cells.push({ d: new Date(y, m, 1 - i), out: true });
    for (let d = 1; d <= last.getDate(); d++)
      cells.push({ d: new Date(y, m, d), out: false });
    while (cells.length % 7) {
      const n = cells.length - startPad - last.getDate() + 1;
      cells.push({ d: new Date(y, m + 1, n), out: true });
    }

    const todayKey = new Date().toISOString().slice(0, 10).replace(/-/g, "");
    const dows = ["일","월","화","수","목","금","토"];
    let html = dows.map(d => `<div class="dow">${d}</div>`).join("");
    let shown = 0;

    html += cells.map(c => {
      const key = c.d.getFullYear() * 10000 + (c.d.getMonth()+1) * 100 + c.d.getDate();
      const ks = String(key);
      const on = fests.filter(f => {
        const s = ymd(f.start_date), e = ymd(f.end_date) || s;
        return s <= ks && ks <= e;
      });
      shown += on.length ? 1 : 0;
      const evs = on.slice(0, 3).map(f =>
        `<a class="ev" href="${esc(f.url || '#')}" target="_blank" rel="noopener noreferrer"
            title="${esc(f.title)} — ${esc(f.org || '')}">${esc(f.title)}</a>`).join("");
      const more = on.length > 3 ? `<span class="ev more">외 ${on.length - 3}건</span>` : "";
      const cls = ["cell", c.out ? "out" : "", ks === todayKey ? "today" : ""].join(" ").trim();
      return `<div class="${cls}"><span class="dnum">${c.d.getDate()}</span>${evs}${more}</div>`;
    }).join("");

    $("#cal").innerHTML = html;
    $("#calNote").textContent = shown
      ? `이 달에 일정이 있는 날 ${shown}일 · 전체 축제 ${fests.length}건`
      : "이 달에는 등록된 축제가 없습니다. 다른 달을 확인해 보세요.";
  }

  $("#prevM").addEventListener("click", () => { cur.setMonth(cur.getMonth() - 1); render(); });
  $("#nextM").addEventListener("click", () => { cur.setMonth(cur.getMonth() + 1); render(); });
  render();
}

/* ── 시작 ───────────────────────────────── */
document.addEventListener("DOMContentLoaded", async () => {
  const page = document.body.dataset.page;
  if (!page) return;
  const data = await loadData();
  fillStats(data);

  // 파일 하나로 합친 미리보기 — 세 화면을 한 문서에 담고 전환한다
  if (page === "single"){
    initBoard(data);
    initCalendar(data);
    const show = name => {
      document.querySelectorAll("section[data-view]").forEach(s => {
        s.hidden = s.dataset.view !== name;
      });
      document.querySelectorAll(".nav a").forEach(a => {
        a.toggleAttribute("aria-current", a.dataset.go === name);
        if (a.dataset.go === name) a.setAttribute("aria-current", "page");
      });
      history.replaceState(null, "", "#" + name);
      window.scrollTo({ top: 0 });
    };
    document.querySelectorAll(".nav a").forEach(a => {
      a.addEventListener("click", e => { e.preventDefault(); show(a.dataset.go); });
    });
    show((location.hash || "#board").slice(1));
    return;
  }

  if (page === "board")    initBoard(data);
  if (page === "calendar") initCalendar(data);
});


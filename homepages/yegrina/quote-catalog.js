/*
 * 한국체대 예그리나 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
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
];
const BY_ID = {};
CATALOG.forEach(g => g.items.forEach(it => { BY_ID[it.id] = it; }));

const 견적정보칸 = ['org','name','tel','email','title','date','place','people','memo'];
const 견적정보짧게 = { org:'o', name:'n', tel:'t', email:'e', title:'m', date:'d', place:'p', people:'c', memo:'x' };

const 견적b64u   = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const 견적unb64u = (s) => {
  let t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (t.length % 4) t += '=';
  return decodeURIComponent(escape(atob(t)));
};

/**
 * 견적 코드를 사람이 읽을 수 있는 모양으로 푼다.
 *   { 정보:{org,name,tel,…}, 줄:[{id,name,spec,qty,unit,days,price}], 할인 }
 * 못 읽으면 null.
 */
function 견적풀기(코드) {
  try {
    const s = JSON.parse(견적unb64u(코드));
    const 정보 = {};
    견적정보칸.forEach((k, idx) => {
      const i = s.i;
      if (!i) { 정보[k] = ''; return; }
      const v = Array.isArray(i) ? i[idx]
              : (i[견적정보짧게[k]] != null ? i[견적정보짧게[k]] : i[k]);
      정보[k] = v == null ? '' : String(v);
    });

    const 책 = (id) => BY_ID[id] || { name: '', spec: '', unit: '식' };
    const 줄 = (s.r || []).map((a) => {
      if (typeof a === 'string') {
        const c = 책(a);
        return { id: a, name: c.name, spec: c.spec, qty: 1, unit: c.unit, days: 1, price: null };
      }
      if (a.length <= 4) {
        const c = 책(a[0]);
        return { id: a[0], name: c.name, spec: c.spec,
                 qty: a[1] != null ? a[1] : 1, unit: c.unit,
                 days: a[2] != null ? a[2] : 1,
                 price: a[3] != null ? a[3] : null };
      }
      return { id: a[0], name: a[1], spec: a[2], qty: a[3], unit: a[4], days: a[5], price: a[6] };
    });

    return { 정보: 정보, 줄: 줄, 할인: +s.d || 0 };
  } catch (e) { return null; }
}

/* 견적 한 줄을 「300명 내외 · 스피커 4통 · 2개 · 2일」 같은 한 줄 설명으로 */
function 견적줄설명(r) {
  return [r.spec, (+r.qty > 1 ? r.qty + (r.unit || '') : ''), (+r.days > 1 ? r.days + '일' : '')]
    .filter(Boolean).join(' · ');
}

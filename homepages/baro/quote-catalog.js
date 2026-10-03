/*
 * 바로기획 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
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

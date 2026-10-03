/*
 * 힐링엔터테인먼트 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
  { group:'행사 기획 · 진행', items:[
    { id:'p1', name:'기업 체육대회 · 워크숍',   spec:'기획 · 프로그램 구성 · 진행',          unit:'식', price:null },
    { id:'p2', name:'학교 운동회 · 체육대회',   spec:'초 · 중 · 고 · 어린이집 · 유치원',      unit:'식', price:null },
    { id:'p3', name:'수학여행 · 청소년 레크리에이션', spec:'떼창 · 랜덤플레이 댄스 · 음향 · 조명', unit:'식', price:null },
    { id:'p4', name:'지역축제 · 관공서 행사',   spec:'기획 · 무대 진행 · 현장 운영',          unit:'식', price:null },
    { id:'p5', name:'송년회 · 신년회 · 기념식', spec:'창립 기념식 · 회원 대회 · 이취임식',    unit:'식', price:null },
    { id:'p6', name:'국내 · 해외 워크숍 · 연수', spec:'초대 행사 · 연수 프로그램 진행',        unit:'식', price:null },
    { id:'p7', name:'골프대회 · 스포츠 대회',   spec:'대회 진행 · 시상식',                    unit:'식', price:null },
    { id:'p8', name:'팀빌딩 프로그램',          spec:'협업 · 소통 중심 단체 프로그램',        unit:'식', price:null },
  ]},
  { group:'MC · 레크리에이션', items:[
    { id:'f1', name:'대표 MC 이현호 진행',      spec:'행사 전체 진행',                        unit:'명', price:null },
    { id:'f6', name:'레크리에이션 강사',        spec:'체육대회 · 워크숍 · 캠프',              unit:'명', price:null },
    { id:'f8', name:'대동놀이 · 참여 프로그램', spec:'전원이 함께하는 마무리 프로그램',       unit:'식', price:null },
    { id:'f5', name:'진행 보조 · 운영 스탭',    spec:'경기 진행 · 이동 안내 · 용품 준비',     unit:'명', price:null, qty:true },
  ]},
  { group:'공연 섭외', items:[
    { id:'f2', name:'가수 섭외',                spec:'행사 성격에 맞는 라인업',               unit:'팀', price:null },
    { id:'f4', name:'댄스 · 공연팀',            spec:'오프닝 · 축하공연',                     unit:'팀', price:null },
    { id:'f7', name:'DJ',                       spec:'파티 · 레크리에이션 음악',              unit:'명', price:null },
  ]},
  { group:'음향', items:[
    { id:'a1', name:'음향 (소형)',       spec:'100명 내외 · 실내 · 마이크 2ch',      unit:'식', price:null },
    { id:'a2', name:'음향 (중형)',       spec:'300명 내외 · 체육관 · 강당',          unit:'식', price:null },
    { id:'a3', name:'음향 (대형)',       spec:'500명 이상 · 운동장 · 축제',          unit:'식', price:null },
    { id:'a4', name:'무선 마이크 추가',  spec:'핸드 / 핀 마이크',                    unit:'개', price:null, qty:true },
  ]},
  { group:'무대 · 조명', items:[
    { id:'b1', name:'무대',              spec:'크기 · 높이 협의',                    unit:'식', price:null },
    { id:'b2', name:'무대 조명',         spec:'공연 · 시상식 · 야간 행사',           unit:'식', price:null },
    { id:'b3', name:'LED · 스크린',      spec:'실내외 · 크기 협의',                  unit:'식', price:null },
    { id:'b4', name:'현수막 · 백드롭',   spec:'행사명 출력물',                       unit:'식', price:null },
  ]},
  { group:'게임도구 · 이벤트 존', items:[
    { id:'h3', name:'체육대회 게임도구',   spec:'대형 공 · 대형 주사위 · 에어사다리 등', unit:'식', price:null },
    { id:'h1', name:'에어바운스',          spec:'설치 · 운영',                           unit:'동', price:null, qty:true },
    { id:'h8', name:'스포츠 이벤트 존',    spec:'체험 부스 구성 · 운영',                 unit:'식', price:null },
    { id:'h2', name:'물놀이 시설',         spec:'렌탈 · 진행',                           unit:'식', price:null },
    { id:'h7', name:'경품 · 시상 진행',    spec:'경품 추첨 · 시상식 운영',               unit:'식', price:null },
  ]},
  { group:'천막 · 테이블', items:[
    { id:'d3',  name:'천막',              spec:'본부석 · 응원석',                    unit:'동', price:null, qty:true },
    { id:'d12', name:'테이블',            spec:'행사용',                             unit:'개', price:null, qty:true },
    { id:'d9',  name:'의자',              spec:'행사용',                             unit:'개', price:null, qty:true },
  ]},
  { group:'기타', items:[
    { id:'g4', name:'장소 섭외 · 대관',  spec:'워크숍 · 행사장',                    unit:'식', price:null },
    { id:'g1', name:'발전기',            spec:'전원 미확보 현장',                  unit:'대', price:null },
    { id:'g2', name:'운반 · 설치 인건비', spec:'상하차 · 설치 · 철수',             unit:'식', price:null },
    { id:'g3', name:'출장비',            spec:'서울 · 경기 외 지역',               unit:'식', price:null },
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

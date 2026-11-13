/* Scènes : accroche, titre, cabinet, audit. Données entièrement fictives. */
const ICONS = {
  check: '<path d="M5 13l4 4L19 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
  cross: '<path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>',
  warn: '<path d="M12 3L2 20h20L12 3z" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round"/><path d="M12 10v4.5M12 17.2v.3" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
  lock: '<rect x="5" y="11" width="14" height="10" rx="2" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M8 11V8a4 4 0 018 0v3" fill="none" stroke="currentColor" stroke-width="2.4"/>',
  user: '<circle cx="12" cy="8" r="4" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M4 21c1-4.5 4.5-6.5 8-6.5s7 2 8 6.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>',
  file: '<path d="M6 2h8l5 5v15H6z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M14 2v5h5" fill="none" stroke="currentColor" stroke-width="2.2"/>',
  mail: '<rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M3 7l9 6 9-6" fill="none" stroke="currentColor" stroke-width="2.2"/>',
  cal: '<rect x="3" y="5" width="18" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="2.2"/>',
  db: '<ellipse cx="12" cy="5.5" rx="8" ry="3" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M4 5.5v13c0 1.7 3.6 3 8 3s8-1.3 8-3v-13M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3" fill="none" stroke="currentColor" stroke-width="2.2"/>',
  folder: '<path d="M3 6h7l2 2h9v11H3z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>',
  tpl: '<rect x="4" y="3" width="16" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M8 8h8M8 12h8M8 16h5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
  task: '<rect x="3" y="4" width="18" height="17" rx="2" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M7 10l2 2 4-4M7 16h10" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
  search: '<circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M15.5 15.5L21 21" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/>',
  eye: '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="2.2"/>',
  send: '<path d="M3 11l18-8-8 18-2-8z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>',
  spark: '<path d="M12 2l2.2 6.8L21 11l-6.8 2.2L12 20l-2.2-6.8L3 11l6.8-2.2z" fill="currentColor"/>',
  shield: '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>',
  clock: '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M12 7v5l3 2" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>',
  arrow: '<path d="M3 12h16M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
  phone: '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 005 5L15 12l5 2v4a2 2 0 01-2 2A16 16 0 013 5a2 2 0 012-2z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>',
  chat: '<path d="M4 4h16v12H9l-5 4z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>',
};
function ic(name, color, size) {
  return `<svg class="icon" viewBox="0 0 24 24" style="color:${color || 'currentColor'};${size ? `width:${size}px;height:${size}px` : ''}">${ICONS[name]}</svg>`;
}
function av(letter, size) {
  const s = size || 64;
  return `<span class="avatar av-${letter}" style="width:${s}px;height:${s}px;font-size:${Math.round(s * 0.44)}px">${letter}</span>`;
}
const AGENT = (txt) => `<span class="chip agent">${ic('spark', 'var(--agent)', 18)} ${txt || 'Agent : prépare'}</span>`;
const HUMAN = (txt) => `<span class="chip human">${ic('user', 'var(--human)', 18)} ${txt}</span>`;
const stag = (n, start, step) => (start + n * step).toFixed(2);

/* ===================== ACCROCHE ===================== */
registerScene('hook', (root) => {
  const mails = [
    ['Famille M. (client)', 'Pièce manquante ?'],
    ['Formulaire du site', 'Demande de rendez-vous'],
    ['Partenaire assureur', 'Avenant à signer'],
    ['Mme D. (cliente)', 'Ce que nous avions convenu'],
    ['Étude notariale', 'Date de signature'],
    ['M. B. (client)', 'Question sur le compte rendu'],
  ];
  root.innerHTML = `
  <div class="phase" data-out="h_cond-0.2">
    <div class="abs" style="left:0;top:20px;width:1040px;height:760px">
      <div class="win abs" style="left:0;top:0;width:560px;height:440px" data-in="0.6" data-anim="pop">
        <div class="bar"><i></i><i></i><i></i><span class="ttl">Messagerie</span><span style="margin-left:auto" class="chip red" data-in="h_24+5">${'<span data-count="h_24+0.6:8:0:23:0">0</span>'} non lus</span></div>
        <div class="body col" style="gap:8px">
          ${mails.map((m, i) => `<div class="row" style="gap:12px;padding:8px 6px;border-bottom:1px solid #EEF1F5" data-in="h_24+${stag(i, 0.9, 1.3)}" data-anim="down" data-dur="0.4">
            ${ic('mail', '#8B98AB', 24)}<div style="font-size:19px;font-weight:700;width:220px;white-space:nowrap">${m[0]}</div><div style="font-size:19px;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;width:250px">${m[1]}</div></div>`).join('')}
        </div>
      </div>
      <div class="win abs" style="left:500px;top:70px;width:520px;height:330px" data-in="h_24+2.2" data-anim="pop">
        <div class="bar"><i></i><i></i><i></i><span class="ttl">Agenda : lundi</span></div>
        <div class="body col" style="gap:10px;font-size:20px">
          <div class="row"><b style="width:70px">09:30</b><span>Point équipe</span></div>
          <div class="row"><b style="width:70px">11:00</b><span>Premier rendez-vous prospect</span></div>
          <div class="row" style="background:var(--agent-soft);border-radius:8px;padding:6px"><b style="width:70px">14:00</b><span>Revue de dossier</span></div>
          <div class="row"><b style="width:70px">16:30</b><span>Rappel client à faire</span></div>
        </div>
      </div>
      <div class="win abs" style="left:110px;top:330px;width:540px;height:340px" data-in="h_24+4.2" data-anim="pop">
        <div class="bar"><i></i><i></i><i></i><span class="ttl">CRM : fiche foyer</span><span class="chip fict" style="margin-left:auto">fictif</span></div>
        <div class="body col" style="gap:12px;font-size:20px">
          <div class="row"><span style="color:var(--muted);width:200px">Foyer</span><b>Famille M.</b></div>
          <div class="row"><span style="color:var(--muted);width:200px">Dernier échange</span><b>?</b></div>
          <div class="row"><span style="color:var(--muted);width:200px">Action promise</span><b>à retrouver</b></div>
          <div class="row"><span style="color:var(--muted);width:200px">Pièces</span><b>dossier partagé</b></div>
        </div>
      </div>
      <div class="win abs" style="left:600px;top:390px;width:430px;height:300px" data-in="h_24+6.2" data-anim="pop">
        <div class="bar"><i></i><i></i><i></i><span class="ttl">Documents</span></div>
        <div class="body col" style="gap:10px;font-size:19px">
          ${['2023_situation.pdf', 'scan_0412.pdf', 'CR_mars_v2.docx', 'piece_id_recto.jpg', 'a_classer (14)'].map(f => `<div class="row" style="gap:10px">${ic('file', '#8B98AB', 22)}<span>${f}</span></div>`).join('')}
        </div>
      </div>
      <div class="abs" style="left:380px;top:250px;width:250px;height:190px;background:#FFF4B8;border-radius:6px;box-shadow:0 10px 24px rgba(0,0,0,.14);padding:18px;font-size:21px;font-weight:600;line-height:1.35;transform:rotate(-3deg);color:#5C4B00" data-in="h_24+8" data-anim="pop">
        Rappeler Mme D. ?<br>Pièce Famille M. ?<br>CR de jeudi à finir
      </div>
      <div class="win abs" style="left:40px;top:600px;width:420px;height:170px" data-in="h_24+9.4" data-anim="pop">
        <div class="bar"><i></i><i></i><i></i><span class="ttl">Tâches</span></div>
        <div class="body col" style="gap:8px;font-size:19px"><div class="row">${ic('task', '#8B98AB', 22)} 12 tâches sans échéance</div><div class="row">${ic('task', '#8B98AB', 22)} 5 relances en attente</div></div>
      </div>
    </div>
    <div class="abs" style="left:1110px;top:10px;width:630px">
      <div class="kicker" data-in="h_24@1">Temps de travail répétitif</div>
      <div class="row" style="align-items:baseline;gap:18px;margin-top:6px" data-in="h_24@1+0.2">
        <span class="big"><span data-count="h_24@1+0.3:2.2:0:24:0">0</span> h</span><span class="h3" style="color:var(--muted)">/ semaine</span><span class="chip amber" style="align-self:center">simulation</span>
      </div>
      <div class="t" style="margin-top:6px;color:var(--muted)" data-in="h_24@1+2">recherches, préparation, vérifications, suivis</div>
      <div class="row" style="gap:5px;margin-top:26px" data-in="h_10" data-anim="fade">
        ${Array.from({ length: 24 }, (_, i) => `<div style="width:21px;height:42px;border-radius:5px;background:#C9D2DE" ${i >= 14 ? `data-cls="h_10+${stag(i - 14, 1.0, 0.18)}:hl10"` : ''}></div>`).join('')}
      </div>
      <div class="row" style="align-items:baseline;gap:14px;margin-top:14px" data-in="h_10+0.8">
        <span style="font-size:86px;font-weight:800;color:var(--agent);letter-spacing:-.03em">10 h</span>
        <span class="t" style="font-weight:700">à récupérer ?</span>
        <span class="chip amber">hypothèse à tester</span>
      </div>
      <div class="card" style="margin-top:22px;padding:20px 26px" data-in="h_460">
        <div style="font-size:40px;font-weight:800;color:var(--navy)">10 h <span style="color:var(--muted);font-weight:600">×</span> 46 semaines <span style="color:var(--muted);font-weight:600">=</span> <span data-count="h_460+1.2:1.6:0:460:0">0</span> h</div>
        <div class="small" style="margin-top:4px">de capacité potentielle sur une année</div>
      </div>
      <div class="row" style="margin-top:20px;gap:12px;flex-wrap:wrap">
        <span class="chip red strike" data-in="h_notca" data-var="h_notca+1.2:0.6:p:0:1">chiffre d'affaires promis</span>
        <span class="chip human" data-in="h_notca@1">du temps pour les clients et les dossiers</span>
        <span class="chip amber" data-in="h_notca@1+3.5">si les mesures du pilote le confirment</span>
      </div>
    </div>
  </div>

  <div class="phase" data-in="h_cond" data-out="h_mission-0.2" data-anim="fade">
    <div class="h2" style="text-align:center;margin-top:30px" data-in="h_cond">Une condition</div>
    <div class="row" style="justify-content:center;gap:40px;margin-top:60px">
      ${[['Situations patrimoniales', 'h_cond@1+0.9'], ["Documents d'identité", 'h_cond@1+2.4'], ['Échanges privés', 'h_cond@1+3.6']].map(([l, t]) => `
        <div class="card col" style="width:440px;align-items:center;text-align:center;padding:40px" data-in="${t}" data-anim="pop">
          <div style="width:96px;height:96px;border-radius:50%;background:var(--amber-soft);display:flex;align-items:center;justify-content:center">${ic('lock', 'var(--amber)', 54)}</div>
          <div class="h3" style="margin-top:10px">${l}</div><div class="small">données sensibles</div>
        </div>`).join('')}
    </div>
    <div class="row" style="justify-content:center;margin-top:70px" data-in="h_cond@1+5">
      <div class="card row" style="gap:22px;padding:24px 36px;border:2px solid var(--red)">
        ${ic('chat', 'var(--red)', 44)}
        <span class="h3 strike" data-var="h_cond@1+6.3:0.7:p:0:1">Un chatbot branché sur tous les fichiers du cabinet</span>
        <span class="x-mark" style="font-size:44px" data-in="h_cond@1+6.8" data-anim="pop">✕</span>
      </div>
    </div>
  </div>

  <div class="phase" data-in="h_mission" data-anim="fade">
    <div class="kicker" style="text-align:center;margin-top:40px" data-in="h_mission">La mission que nous allons suivre</div>
    <div class="row" style="justify-content:center;gap:0;margin-top:70px">
      ${[['search', 'Diagnostic', 'les personnes et les outils', 'h_mission+0.8'], ['task', 'Note sur 100', 'du fonctionnement initial', 'h_plan+0.3'], ['spark', '3 agents en situation', 'sur une semaine type', 'h_plan+4.6'], ['user', 'Décision', 'déployer, ajuster ou arrêter', 'h_mission+4.2']].map(([i, a, b, t], k) => `
        ${k ? `<div style="width:70px;color:#AFBACB" data-in="${t}" data-anim="fade">${ic('arrow', '#AFBACB', 60)}</div>` : ''}
        <div class="card col" style="width:330px;align-items:center;text-align:center;padding:34px 24px" data-in="${t}" data-anim="pop">
          <div style="width:84px;height:84px;border-radius:22px;background:${k === 2 ? 'var(--agent-soft)' : k === 3 ? 'var(--human-soft)' : '#E9EEF5'};display:flex;align-items:center;justify-content:center">${ic(i, k === 2 ? 'var(--agent)' : k === 3 ? 'var(--human)' : 'var(--navy)', 46)}</div>
          <div class="h3" style="margin-top:12px">${a}</div><div class="small">${b}</div>
        </div>`).join('')}
    </div>
    <div class="row" style="justify-content:center;margin-top:70px" data-in="h_plan+7.2" data-anim="pop">
      <span class="chip human" style="font-size:28px;padding:14px 28px">${ic('user', 'var(--human)', 30)} Le CGP garde la main à chaque étape</span>
    </div>
  </div>`;
  const st = document.createElement('style');
  st.textContent = '.hl10{background:var(--agent)!important}';
  root.appendChild(st);
  return {};
});

/* ===================== TITRE ===================== */
registerScene('title', (root) => {
  root.classList.add('dark');
  root.innerHTML = `
  <div class="abs" style="left:160px;top:250px;width:1600px">
    <div style="font-size:30px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)" data-in="scene:title+0.2">Agentic Wealth</div>
    <div class="h1" style="font-size:92px;margin-top:22px;color:#fff" data-in="scene:title+0.5">On audite un cabinet<br>de gestion de patrimoine</div>
    <div style="font-size:34px;color:#B9C6D8;margin-top:26px;font-weight:500" data-in="scene:title+0.9">Une mission, du premier diagnostic à la décision</div>
    <div class="sim-banner" style="margin-top:60px;font-size:28px" data-in="t_disc+0.3">${ic('warn', '#8A5A08', 32)} Simulation pédagogique : cabinet, personnes, dossiers et chiffres fictifs</div>
  </div>
  <div class="abs col" style="left:1430px;top:250px;width:380px;gap:18px">
    ${[['spark', "L'agent prépare", 'var(--agent)', 1.2], ['check', 'Le CGP valide', '#8FD6B8', 1.6], ['user', 'Le CGP décide', '#8FD6B8', 2.0]].map(([i, l, c, d]) => `<div class="row" style="gap:18px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:22px 26px" data-in="scene:title+${d}" data-anim="left">${ic(i, c, 40)}<span style="font-size:30px;font-weight:700;color:#fff">${l}</span></div>`).join('')}
  </div>`;
  return { chrome: false };
});

/* ===================== CABINET ===================== */
registerScene('cabinet', (root) => {
  const people = [
    ['S', 'Sophie', 'Dirigeante, CGP', ['Conduit les rendez-vous patrimoniaux', 'Prend les décisions de conseil', 'Valide les communications importantes'], 'c_sophie'],
    ['K', 'Karim', 'Conseiller', ['Prépare les dossiers', 'Suit une partie des clients', 'Réalise des rendez-vous'], 'c_karim'],
    ['L', 'Léa', 'Coordinatrice, 4 jours / semaine', ['Accueil et agenda', 'Demandes de pièces', 'Suivi administratif'], 'c_lea'],
  ];
  const tools = [['db', 'CRM'], ['mail', 'Messagerie'], ['cal', 'Agenda'], ['folder', 'Espace documentaire'], ['tpl', 'Modèles de documents']];
  root.innerHTML = `
  <div class="phase" data-out="c_tools-0.2">
    <div class="card abs" style="left:0;top:20px;width:560px;padding:34px" data-in="c_name">
      <div class="row" style="justify-content:space-between"><div class="kicker">Cabinet</div><span class="chip fict">fictif</span></div>
      <div class="h2" style="margin-top:10px">Horizon Patrimoine</div>
      <div class="col" style="margin-top:22px;gap:16px;font-size:24px">
        <div class="row">${ic('cal', 'var(--muted)', 28)} Aix-en-Provence</div>
        <div class="row">${ic('user', 'var(--muted)', 28)} 3 personnes</div>
        <div class="row" data-in="c_180">${ic('folder', 'var(--muted)', 28)} ~180 foyers clients <span class="chip amber" style="font-size:15px">simulation</span></div>
        <div class="row" data-in="c_180+3.6">${ic('search', 'var(--muted)', 28)} De nouveaux prospects</div>
      </div>
      <div class="divider" style="margin:26px 0 18px"></div>
      <div class="row" data-in="c_statut" style="align-items:flex-start;gap:12px">${ic('shield', 'var(--amber)', 30)}<div class="t" style="font-size:21px"><b>Statuts réglementaires :</b> non supposés ici. À vérifier lors d'une vraie mission, avec les prestations et procédures.</div></div>
    </div>
    <div class="abs col" style="left:620px;top:20px;width:1120px;gap:22px">
      ${people.map(([l, n, r, items, b]) => `
      <div class="card row" style="gap:26px;padding:26px 30px" data-in="${b}" data-anim="left">
        ${av(l, 92)}
        <div style="width:330px"><div class="h3">${n}</div><div class="small" style="font-size:20px;margin-top:4px">${r}</div></div>
        <div class="col" style="gap:8px;font-size:21px">${items.map((it, i) => `<div class="row" style="gap:10px" data-in="${b}+${stag(i, 1.2, 1.4)}" data-anim="fade">${ic('check', 'var(--human)', 22)} ${it}</div>`).join('')}</div>
      </div>`).join('')}
    </div>
  </div>

  <div class="phase" data-in="c_tools" data-anim="fade">
    <div class="h2" style="text-align:center" data-in="c_tools">Les outils existent. Les passages, moins.</div>
    <svg class="abs" style="left:0;top:0;width:1740px;height:800px;overflow:visible" viewBox="0 0 1740 800">
      <path d="M174 335 C 280 480, 420 480, 522 335 C 700 160, 1040 160, 1218 335 C 1000 570, 400 570, 174 345" pathLength="1" fill="none" stroke="var(--navy2)" stroke-width="5" stroke-dasharray="1" style="stroke-dashoffset:calc(1 - var(--p))" data-var="c_before:9:p:0:1:lin" stroke-linecap="round"/>
      <path d="M1218 345 C 1330 480, 1460 480, 1566 335 C 1400 610, 1000 610, 870 345 C 700 610, 300 610, 174 350" pathLength="1" fill="none" stroke="var(--amber)" stroke-width="5" stroke-dasharray="1" style="stroke-dashoffset:calc(1 - var(--p))" data-var="c_after:5:p:0:1:lin" stroke-linecap="round"/>
    </svg>
    <div class="abs row" style="left:0;top:250px;width:1740px;justify-content:space-around">
      ${tools.map(([i, l], k) => `<div class="node col tool-${k}" style="width:250px;align-items:center;gap:10px" data-in="c_tools+${stag(k, 0.5, 0.9)}" data-anim="pop" data-cls="c_relay+${stag(k, 0.4, 0.25)}:relay">
        <div style="width:72px;height:72px;border-radius:18px;background:#E9EEF5;display:flex;align-items:center;justify-content:center">${ic(i, 'var(--navy)', 40)}</div>${l}</div>`).join('')}
    </div>
    <div class="abs col" style="left:120px;top:560px;width:1500px;gap:12px">
      <div class="row" style="gap:14px;flex-wrap:wrap" data-in="c_before">${av('S', 46)}
        ${[['Note dans le CRM', 0.8], ['Dernier échange', 3.6], ['Pièces du dossier', 6.4], ['Action promise faite ?', 9.2]].map(([l, d], k) => `<span class="chip slate" data-in="c_before+${d}" data-anim="pop">${k + 1}. ${l}</span>`).join('')}
      </div>
      <div class="row" style="gap:14px;flex-wrap:wrap" data-in="c_after">${'<span style="width:46px"></span>'}
        ${[['Compte rendu', 1.2], ['Suite à organiser', 3.4]].map(([l, d], k) => `<span class="chip amber" data-in="c_after+${d}" data-anim="pop">${k + 5}. ${l}</span>`).join('')}
      </div>
    </div>
    <div class="abs" style="left:0;width:1740px;top:740px;text-align:center" data-in="c_relay" data-anim="pop">
      <span class="chip navy" style="font-size:26px;padding:12px 26px">Périmètre de l'audit : les passages de relais</span>
    </div>
  </div>`;
  const st = document.createElement('style');
  st.textContent = '.relay{border-color:var(--amber)!important;box-shadow:0 0 0 8px rgba(185,122,18,.18)!important}';
  root.appendChild(st);
  return {};
});

/* ===================== AUDIT ===================== */
registerScene('audit', (root) => {
  const qs = ['Comment arrive une demande ?', 'Quelles sources sont consultées ?', 'Qui repère une pièce manquante ?', 'Qui valide le compte rendu ?', 'Où voit-on la prochaine action ?'];
  const scores = [
    ['Processus', 13, 'étapes connues, peu documentées', 'a_s1'],
    ['Interconnexion des outils', 6, 'recherches et ressaisies', 'a_s2'],
    ['Maîtrise des accès et des données', 7, "règles d'usage de l'IA à préciser", 'a_s3'],
    ["Appropriation par l'équipe", 9, 'intérêt, aucun workflow testé', 'a_s4'],
    ['Validations et traçabilité', 10, 'historique difficile à retrouver', 'a_s5'],
  ];
  const domains = [
    ['Acquisition et conversion', ['Prospects', 'Premiers rendez-vous', 'Relances'], 'a_d1', 'Agent 3'],
    ['Conseil et préparation', ['Briefs', 'Comptes rendus', 'Questions à poser'], 'a_d2', 'Agent 1'],
    ['Conformité et traçabilité', ['Pièces', 'Listes de contrôle', 'Journaux de validation'], 'a_d3', 'Agent 2'],
    ['Service et relation client', ['Demandes entrantes', 'Engagements', 'Réponses'], 'a_d4', 'Agent 3'],
    ['Pilotage du cabinet', ['Priorités', 'Échéances', 'Dossiers sans action récente'], 'a_d5', 'Agent 3'],
  ];
  root.innerHTML = `
  <div class="phase" data-out="a_split-0.2">
    <div class="row" style="gap:20px" data-in="a_people">
      ${['S', 'K', 'L'].map((l, i) => `<div data-in="a_people+${stag(i, 0.3, 0.4)}" data-anim="pop">${av(l, 80)}</div>`).join('')}
      <div class="h2" style="margin-left:16px">D'abord les personnes, pas la démonstration</div>
    </div>
    <div class="row" style="gap:30px;margin-top:40px;align-items:flex-start">
      <div class="card" style="width:820px" data-in="a_show">
        <div class="kicker">Un dossier de bout en bout</div>
        <div class="col" style="margin-top:18px;gap:14px">
          ${qs.map((q, i) => `<div class="row t" style="gap:14px;font-weight:600" data-in="a_q@${i}" data-anim="left">${ic('search', 'var(--navy)', 26)} ${q}</div>`).join('')}
        </div>
      </div>
      <div class="col" style="width:880px;gap:16px">
        ${[['Déclaré', "ce que l'équipe dit faire", 'slate'], ['Observé', 'les traces dans les outils', 'agent'], ['À mesurer', 'pendant le pilote', 'amber']].map(([a, b, c], i) => `
        <div class="card row" style="padding:22px 28px;gap:20px" data-in="a_cols+${stag(i, 0.3, 1.5)}" data-anim="left">
          <span class="chip ${c}" style="font-size:24px;width:190px;justify-content:center">${a}</span><span class="t">${b}</span>
        </div>`).join('')}
      </div>
    </div>
  </div>

  <div class="phase" data-in="a_split" data-out="a_grid-0.2" data-anim="fade">
    <div class="row" style="justify-content:space-between"><div class="h2">24 heures de travail répétitif, en 3 blocs</div><span class="chip amber" style="font-size:22px">hypothèses de départ</span></div>
    <div class="row" style="gap:6px;margin-top:60px;height:120px">
      ${[[8, 'var(--agent)', 'a_8', 'Préparer les rendez-vous et remettre les notes en forme'], [9, '#2B5D8C', 'a_9', 'Rechercher les pièces, vérifier les listes, préparer les revues'], [7, 'var(--human)', 'a_7', 'Retrouver les engagements, brouillons de suivi, priorités']].map(([h, c, b]) => `
        <div style="flex:${h};height:100%;background:${c};border-radius:14px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:56px;font-weight:800" data-in="${b}" data-anim="pop">${h} h</div>`).join('')}
    </div>
    <div class="row" style="gap:6px;margin-top:20px;align-items:flex-start">
      ${[[8, 'a_8', 'Préparer les rendez-vous, rassembler le contexte, remettre les notes en forme'], [9, 'a_9', 'Rechercher les pièces, vérifier les listes de contrôle, préparer les revues'], [7, 'a_7', 'Retrouver les engagements, brouillons de suivi, priorités de la semaine']].map(([h, b, l]) => `
        <div class="t" style="flex:${h};padding:0 14px;font-size:22px" data-in="${b}+0.3">${l}</div>`).join('')}
    </div>
    <div class="row" style="justify-content:center;margin-top:70px" data-in="a_sum">
      <div class="eq">8 <span class="op">+</span> 9 <span class="op">+</span> 7 <span class="op">=</span> 24 h</div>
    </div>
    <div class="row" style="justify-content:center;margin-top:24px;gap:16px" data-in="a_sum@2">
      <span class="chip slate" style="font-size:22px">${ic('clock', 'var(--slate)', 22)} À chronométrer sur un échantillon réel</span>
      <span class="chip slate" style="font-size:22px">Sans double compte</span>
    </div>
  </div>

  <div class="phase" data-in="a_grid" data-out="a_map-0.2" data-anim="fade">
    <div class="row" style="justify-content:space-between"><div class="h2">Note du fonctionnement initial</div><span class="chip amber" style="font-size:22px">grille illustrative</span></div>
    <div class="row" style="align-items:flex-start;gap:50px;margin-top:40px">
      <div class="card col" style="width:1180px;gap:40px;padding:44px">
        ${scores.map(([l, v, c, b]) => `
        <div class="row" style="gap:24px" data-in="${b}" data-anim="left">
          <div style="width:450px"><div style="font-size:29px;font-weight:700">${l}</div><div class="small">${c}</div></div>
          <div class="bar-bg grow" style="height:30px"><div class="bar-fg" style="background:${v >= 10 ? 'var(--navy2)' : 'var(--amber)'}" data-var="${b}+0.3:1.1:p:0:${v / 20}"></div></div>
          <div style="width:110px;text-align:right;font-size:34px;font-weight:800"><span data-count="${b}+0.3:1.1:0:${v}:0">0</span><span style="font-size:22px;color:var(--muted)">/20</span></div>
        </div>`).join('')}
      </div>
      <div class="col" style="width:500px;align-items:center;gap:6px">
        <div class="card col" style="width:500px;align-items:center;padding:40px" data-in="a_45" data-anim="pop">
          <div class="kicker">Total</div>
          <div style="font-size:150px;font-weight:800;color:var(--navy);letter-spacing:-.04em;line-height:1"><span data-count="a_45+0.2:1.4:0:45:0">0</span><span style="font-size:56px;color:var(--muted)">/100</span></div>
          <span class="chip amber" style="margin-top:10px">note illustrative</span>
        </div>
        <div class="card" style="width:500px;margin-top:22px;padding:24px 28px" data-in="a_not">
          <div class="row" style="gap:10px;font-size:22px;font-weight:700">${ic('cross', 'var(--red)', 24)} Pas une note des conseillers</div>
          <div class="row" style="gap:10px;font-size:22px;font-weight:700;margin-top:10px" data-in="a_not+3.6">${ic("check", "var(--human)", 24)} Photo fictive d'un système de travail</div>
          <div class="row" style="gap:10px;font-size:22px;font-weight:700;margin-top:10px" data-in="a_not@1">${ic('check', 'var(--human)', 24)} Chaque critère à rendre vérifiable</div>
        </div>
      </div>
    </div>
  </div>

  <div class="phase" data-in="a_map" data-anim="fade">
    <div class="row" style="justify-content:space-between"><div class="h2">Cartographie Agentic Wealth : 5 domaines métier</div></div>
    <div class="row" style="gap:20px;margin-top:46px;align-items:stretch">
      ${domains.map(([n, items, b, ag], i) => `
      <div class="card col" style="width:332px;min-height:500px;padding:28px;gap:18px;border-top:8px solid ${['#2B5D8C', 'var(--agent)', '#8C4F2B', 'var(--human)', 'var(--navy)'][i]}" data-in="${b}" data-anim="up">
        <div class="h3" style="font-size:30px;min-height:76px">${n}</div>
        ${items.map((it, k) => `<div class="row" style="gap:10px;font-size:24px" data-in="${b}+${stag(k, 0.8, 0.7)}" data-anim="fade">${ic('check', '#8B98AB', 20)} ${it}</div>`).join('')}
        <div style="margin-top:auto" data-in="a_rule@1">${AGENT(ag)}</div>
      </div>`).join('')}
    </div>
    <div class="row" style="justify-content:center;gap:24px;margin-top:50px;zoom:1.3" data-in="a_rule" data-anim="pop">
      ${AGENT("L'agent prépare")}<span class="h3" style="color:var(--muted)">·</span>${HUMAN('Le conseiller décide')}
    </div>
  </div>`;
  return {};
});

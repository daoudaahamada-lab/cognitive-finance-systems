/* Agent 1 : préparer le rendez-vous et sa suite. Données entièrement fictives. */
registerScene('agent1', (root) => {
  const steps = [
    ['Rendez-vous sélectionné', 'humanact', 'p_1'], ['Sources autorisées', 'humanact', 'p_2'], ['Collecte', 'agent', 'p_3'],
    ['Rapprochement', 'agent', 'p_4'], ['Manques signalés', 'agent', 'p_5'], ['Brief sourcé', 'agent', 'p_6'],
    ['Correction et validation CGP', 'validate', 'p_7'], ['Rendez-vous', 'humanact', 'p_8'], ['Brouillon de compte rendu', 'agent', 'p_9'],
    ['Validation du compte rendu', 'validate', 'p_10'], ['Tâches et suivi validés', 'validate', 'p_11'],
  ];
  const nextOf = i => (i + 1 < steps.length ? steps[i + 1][2] : 'p_gain');
  const sources = [
    ['db', 'Fiche CRM : Camille R.', 'fiche du foyer', true],
    ['file', 'Comptes rendus validés', '2 documents', true],
    ['mail', 'Échanges professionnels pertinents', '3 messages sélectionnés', true],
    ['folder', 'Documents du dossier', 'accès autorisé à Sophie', true],
    ['folder', 'Archive ancienne (dossier 2019)', 'hors périmètre', false],
    ['mail', 'Messagerie complète', 'hors périmètre', false],
  ];
  const srcT = ['p_2+3.2', 'p_2+4.6', 'p_2+6.0', 'p_2+7.8'];
  root.innerHTML = `
  <style>
    .scene-agent1 .ph { position:absolute; left:90px; top:238px; width:1740px; height:650px; }
    .tog { width:58px; height:32px; border-radius:16px; background:#CFD6E0; position:relative; flex:none; }
    .tog::after { content:''; position:absolute; left:4px; top:4px; width:24px; height:24px; border-radius:50%; background:#fff; box-shadow:0 1px 3px rgba(0,0,0,.2); }
    .tog.on { background:var(--human); } .tog.on::after { left:30px; }
    .srow { display:flex; align-items:center; gap:18px; padding:14px 18px; border-radius:12px; border:1.5px solid #E3E8EF; font-size:22px; }
    .srow.off { background:#F4F6F9; color:#9AA6B6; }
    .srow .d { margin-left:auto; font-size:18px; color:var(--muted); }
    .logl { font-family:'DejaVu Sans Mono',monospace; font-size:20px; padding:6px 0; color:#2B3A52; }
    .bitem { font-size:23px; line-height:1.42; margin-bottom:7px; display:flex; gap:10px; align-items:baseline; }
    .bsec { font-size:18px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; margin:10px 0 6px; }
    .crc { background:#fff; border-radius:14px; border:1px solid #E3E8EF; padding:22px; font-size:24px; line-height:1.38; box-shadow:0 6px 16px rgba(15,30,51,.07); }
    .crc h4 { font-size:18px; text-transform:uppercase; letter-spacing:.07em; color:var(--muted); margin-bottom:10px; }
    .field { display:flex; align-items:center; white-space:nowrap; gap:10px; font-size:21px; color:var(--muted); }
    .field b { color:var(--ink); }
  </style>
  <div class="stepper" data-in="p_path" data-anim="down" data-out="p_gain-0.2">
    ${steps.map(([l, c, b], i) => `<div class="step ${c}" data-cls="${b}:on; ${nextOf(i)}:-on; ${nextOf(i)}:done" data-in="p_path+${stag(i, 0.1, 0.22)}" data-anim="pop" data-dur="0.4"><div class="dot">${i + 1}</div><div class="lbl">${l}</div></div>`).join('')}
  </div>
  <div class="clock" id="a1clock" data-in="p_intro@1" data-out="p_gain-0.3"><span>●</span><b id="a1clocktxt">Mardi 08:35</b></div>

  <!-- P0 agenda + sans agent -->
  <div class="phase" data-out="p_path-0.2">
    <div class="win abs" style="left:0;top:20px;width:820px;height:740px" data-in="p_intro">
      <div class="bar"><i></i><i></i><i></i><span class="ttl">Agenda de Sophie : mardi</span><span class="chip fict" style="margin-left:auto">données fictives</span></div>
      <div class="body" style="position:relative;height:690px">
        ${['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'].map((h, i) => `<div class="abs row" style="left:24px;top:${16 + i * 64}px;width:760px;gap:16px"><span style="width:70px;font-size:19px;color:var(--muted);font-weight:600">${h}</span><div style="flex:1;height:1px;background:#E6EAF0"></div></div>`).join('')}
        <div class="abs" style="left:110px;top:${16 + 0.58 * 64 + 12}px;width:680px;height:3px;background:var(--red)" data-in="p_intro@1" data-anim="fade"><span class="abs" style="left:-14px;top:-7px;width:16px;height:16px;border-radius:50%;background:var(--red)"></span></div>
        <div class="abs" style="left:120px;top:${16 + 1.5 * 64 + 12}px;width:400px;height:56px;border-radius:10px;background:#EEF1F5;padding:14px 16px;font-size:19px;font-weight:600">09:30 Point équipe</div>
        <div class="abs" style="left:120px;top:${16 + 3 * 64 + 12}px;width:400px;height:56px;border-radius:10px;background:#EEF1F5;padding:14px 16px;font-size:19px;font-weight:600">11:00 Appel partenaire</div>
        <div class="abs" style="left:120px;top:${16 + 6 * 64 + 12}px;width:660px;height:${1.17 * 64}px;border-radius:12px;background:var(--agent-soft);border:2px solid var(--agent);padding:12px 18px" data-in="p_intro@2" data-anim="pop">
          <div style="font-size:21px;font-weight:800;color:var(--navy)">14:00 à 15:10 · Rendez-vous de suivi</div>
          <div class="row" style="gap:10px;font-size:19px;margin-top:2px">Camille R. <span class="chip fict">cliente fictive</span></div>
        </div>
        <div class="abs" style="left:120px;top:${16 + 8.5 * 64 + 12}px;width:400px;height:56px;border-radius:10px;background:#EEF1F5;padding:14px 16px;font-size:19px;font-weight:600">16:30 Préparer une revue</div>
      </div>
    </div>
    <div class="card abs" style="left:880px;top:20px;width:860px;padding:30px 34px" data-in="p_today">
      <div class="row" style="justify-content:space-between"><div class="h3">Aujourd'hui, sans agent</div><span class="chip slate">manuel</span></div>
      <div class="col" style="gap:13px;margin-top:20px">
        ${[['db', 'Ouvrir le CRM', 0.8], ['search', 'Chercher le dernier compte rendu', 1.9], ['mail', 'Relire trois échanges', 3.3], ['folder', 'Vérifier les documents', 4.6], ['tpl', 'Noter ses questions', 6.0]].map(([i, l, d]) => `<div class="row t" style="gap:14px" data-in="p_today+${d}" data-anim="left">${ic(i, 'var(--slate)', 26)} ${l}</div>`).join('')}
        <div class="small" style="margin-top:6px;font-weight:700;letter-spacing:.06em;text-transform:uppercase" data-in="p_today@1">Après le rendez-vous</div>
        ${[['file', 'Rédiger le compte rendu', 0.6], ['task', 'Retrouver les engagements, créer les actions', 1.6]].map(([i, l, d]) => `<div class="row t" style="gap:14px" data-in="p_today@1+${d}" data-anim="left">${ic(i, 'var(--amber)', 26)} ${l}</div>`).join('')}
      </div>
      <div class="divider"></div>
      <div class="row" style="gap:14px" data-in="p_today2"><span class="chip amber" style="font-size:22px">Bloc 1 : 8 h / semaine</span><span class="small">hypothèse de départ</span></div>
    </div>
  </div>

  <!-- P1 légende du parcours -->
  <div class="ph" data-in="p_path+0.4" data-out="p_1-0.2" data-anim="fade">
    <div class="col" style="align-items:center;margin-top:120px;gap:34px">
      <div class="h2">11 étapes, dont 3 validations humaines</div>
      <div class="legend" style="font-size:24px;gap:40px">
        <span><i style="background:var(--agent)"></i>L'agent prépare</span>
        <span><i style="background:#fff;border:3px solid var(--human)"></i>Sophie agit</span>
        <span><i style="background:var(--human)"></i>Validation humaine</span>
      </div>
    </div>
  </div>

  <!-- P2 sélection du rendez-vous -->
  <div class="ph" data-in="p_1" data-out="p_2-0.2" data-anim="fade">
    <div class="win abs" style="left:260px;top:60px;width:1220px">
      <div class="bar"><i></i><i></i><i></i><span class="ttl">Agenda : mardi 14:00</span></div>
      <div class="body row" style="gap:26px;padding:34px">
        ${av('C', 76)}
        <div class="grow"><div class="h3">Rendez-vous de suivi : Camille R.</div><div class="small" style="margin-top:4px">14:00 à 15:10 · cliente fictive · dossier de démonstration</div></div>
        <div class="btn agent" id="a1prep" data-cls="p_1+1.6:pressed">${ic('spark', '#fff', 22)} Préparer</div>
      </div>
    </div>
    <div class="row abs" style="left:260px;top:320px;gap:20px" data-in="p_1+1.8">
      ${HUMAN('Choix de Sophie')}<span class="t">L'agent ne choisit pas seul les dossiers à ouvrir.</span>
    </div>
  </div>

  <!-- P3 sources autorisées -->
  <div class="ph" data-in="p_2" data-out="p_3-0.2" data-anim="fade">
    <div class="card abs" style="left:0;top:0;width:1100px;padding:26px 30px">
      <div class="row" style="justify-content:space-between"><div class="h3">Sources pour ce rendez-vous</div>${HUMAN('Autorisation : Sophie')}</div>
      <div class="col" style="gap:10px;margin-top:18px">
        ${sources.map(([i, l, d, ok], k) => `<div class="srow ${ok ? '' : 'off'}" ${ok ? '' : `data-in="p_2b" data-anim="fade"`} id="src${k}">
          <div class="tog" ${ok ? `data-cls="${srcT[k]}:on"` : ''}></div>${ic(ok ? i : 'lock', ok ? 'var(--navy)' : '#A9B3C2', 26)}<span style="font-weight:600">${l}</span><span class="d">${d}</span></div>`).join('')}
      </div>
      <div class="row" style="margin-top:18px;justify-content:flex-end"><div class="btn human" id="srcok" data-cls="p_2b+3.4:pressed">${ic('check', '#fff', 22)} Autoriser ces 4 sources</div></div>
    </div>
    <div class="col abs" style="left:1150px;top:0;width:590px;gap:20px">
      <div class="card" data-in="p_2+1.5"><div class="kicker">Périmètre</div><div class="h3" style="margin-top:8px">Ce dossier. Ces sources. Rien d'autre.</div></div>
      <div class="card row" style="gap:16px" data-in="p_2b+0.6">${ic('lock', 'var(--amber)', 40)}<div class="t">Archive ancienne et messagerie complète : <b>grisées, hors périmètre</b></div></div>
    </div>
  </div>

  <!-- P4 collecte -->
  <div class="ph" data-in="p_3" data-out="p_4-0.2" data-anim="fade">
    <div class="col abs" style="left:0;top:0;width:620px;gap:14px">
      ${[['S1', 'Fiche CRM'], ['S2', 'Compte rendu validé du 14/03'], ['S3', 'Échanges pertinents (3)'], ['S4', 'Documents du dossier (6)']].map(([s, l], k) => `<div class="card row" style="padding:20px 24px;gap:16px" data-in="p_3+${stag(k, 0.3, 0.3)}" data-anim="left"><span class="src" style="font-size:20px;margin:0">${s}</span><span class="t" style="font-weight:600">${l}</span></div>`).join('')}
    </div>
    <div class="win abs" style="left:680px;top:0;width:1060px;height:520px">
      <div class="bar"><i></i><i></i><i></i><span class="ttl">Agent de préparation : collecte</span><span style="margin-left:auto">${AGENT('lecture seule')}</span></div>
      <div class="body">
        ${['Lecture S1 : fiche CRM ........................ ok', 'Lecture S2 : compte rendu du 14/03 ............. ok', 'Lecture S3 : 3 échanges ........................ ok', 'Lecture S4 : 6 documents ....................... ok', 'Chaque information garde sa source [S1 à S4]'].map((l, k) => `<div class="logl" data-type="p_3+${stag(k, 0.9, 0.9)}:70">${l}</div>`).join('')}
        <div class="bar-bg" style="margin-top:22px"><div class="bar-fg" style="background:var(--agent)" data-var="p_3+0.8:4.2:p:0:1:lin"></div></div>
      </div>
    </div>
  </div>

  <!-- P5 rapprochement -->
  <div class="ph" data-in="p_4" data-out="p_5-0.2" data-anim="fade">
    <div class="row" style="gap:40px;justify-content:center;margin-top:30px">
      <div class="card" style="width:560px" data-in="p_4@1" data-anim="left"><div class="row" style="justify-content:space-between"><div class="h3">Fiche CRM</div><span class="src">S1</span></div><div class="t" style="margin-top:16px">Dernière revue : <b class="amber-hl">12 mars</b></div></div>
      <div class="h1" style="color:var(--amber)" data-in="p_4@1+2.8" data-anim="pop">≠</div>
      <div class="card" style="width:560px" data-in="p_4@1+2.2" data-anim="right"><div class="row" style="justify-content:space-between"><div class="h3">Compte rendu validé</div><span class="src">S2</span></div><div class="t" style="margin-top:16px">Revue du <b class="amber-hl">14 mars</b></div></div>
    </div>
    <div class="row" style="justify-content:center;margin-top:60px" data-in="p_4@2" data-anim="pop">
      <div class="card row" style="gap:18px;border:2px solid var(--amber);padding:22px 30px">${ic('warn', 'var(--amber)', 40)}<div><div class="h3">Écart signalé, non tranché</div><div class="t">L'agent ne choisit pas : la date sera vérifiée par Sophie.</div></div></div>
    </div>
  </div>

  <!-- P6 manques -->
  <div class="ph" data-in="p_5" data-out="p_6-0.2" data-anim="fade">
    <div class="h2" style="margin-top:10px">Manques et points d'attention</div>
    <div class="col" style="gap:18px;margin-top:30px;width:1500px">
      ${[['red', 'Absent', 'Justificatif attendu : introuvable dans les sources autorisées', 'liste du cabinet', 'p_5@1'], ['amber', 'À vérifier', 'Échéance citée dans l’échange du 2 septembre, absente du suivi', 'S3', 'p_5@1+2.6'], ['amber', 'Ancien', 'Information de situation datée d’il y a deux ans', 'S1', 'p_5@1+5.2']].map(([c, s, l, src, t]) => `
      <div class="card row" style="gap:22px;padding:22px 28px" data-in="${t}" data-anim="left"><span class="chip ${c}" style="width:150px;justify-content:center">${s}</span><span class="t grow" style="font-weight:600">${l}</span><span class="src" style="font-size:18px">source : ${src}</span></div>`).join('')}
    </div>
  </div>

  <!-- P7 brief -->
  <div class="ph" data-in="p_6" data-out="p_8-0.2" data-anim="fade">
    <div class="card abs" style="left:0;top:0;width:1290px;height:640px;padding:24px 30px">
      <div class="row" style="justify-content:space-between">
        <div><div class="h3">Brief : rendez-vous de suivi</div><div class="small">Camille R. (fictive) · mardi 14:00</div></div>
        <span class="chip agent" data-out="p_7@2+4.8" data-outdur="0.2">${ic('spark', 'var(--agent)', 18)} Brouillon v1 préparé par l'agent</span>
      </div>
      <div class="row" style="gap:30px;align-items:flex-start;margin-top:8px">
        <div style="width:610px">
          <div class="bsec" style="color:var(--human)" data-in="p_6@1">Faits sourcés</div>
          ${[['Dernier échange : 2 septembre', 'S3'], ['Objectif exprimé : préparer les études des enfants', 'S2'], ['Action convenue : envoi d’un justificatif par la cliente', 'S2'], ['Documents disponibles : 6 sur 7 attendus', 'S4']].map(([l, s], k) => `<div class="bitem" data-in="p_6@1+${stag(k, 0.8, 1.5)}" data-anim="fade">${ic('check', 'var(--human)', 20)}<span>${l}<span class="src">${s}</span></span></div>`).join('')}
          <div class="bitem" data-in="p_6@1+6.5" data-anim="fade">${ic('warn', 'var(--amber)', 20)}<span>Dernière revue : <span style="display:inline-grid"><span style="grid-area:1/1" class="amber-hl" data-out="p_7@2+2.6" data-outdur="0.15">12/03 ou 14/03 ?</span><span style="grid-area:1/1" class="ok-hl" data-in="p_7@2+2.7" data-anim="fade">14/03, corrigé par Sophie</span></span><span class="src">S1 S2</span></span></div>
          <div class="bsec" style="color:var(--amber);margin-top:16px" data-in="p_6@2">Points à vérifier</div>
          ${['Justificatif attendu introuvable', 'Échéance du 2 septembre absente du suivi', 'Information de situation ancienne'].map((l, k) => `<div class="bitem" data-in="p_6@2+${stag(k, 0.2, 0.5)}" data-anim="fade">${ic('warn', 'var(--amber)', 20)}<span>${l}</span></div>`).join('')}
        </div>
        <div style="width:580px">
          <div class="bsec" style="color:var(--agent)" data-in="p_6q">Questions proposées</div>
          <div class="bitem" data-in="p_6q+1.6" data-anim="fade" style="background:var(--agent-soft);border-radius:10px;padding:8px 10px">${ic('chat', 'var(--agent)', 20)}<span>« L'objectif formulé au dernier rendez-vous est-il toujours d'actualité ? »</span></div>
          <div class="bitem" data-in="p_6q+4.5" data-anim="fade" style="padding:8px 10px">${ic('chat', 'var(--agent)', 20)}<span>« Votre situation a-t-elle changé depuis notre dernier échange ? »</span></div>
          <div class="bitem" data-in="p_6q+5.4" data-anim="fade" style="padding:8px 10px" data-cls="p_7@2+0.6:dim" id="q3">${ic('chat', 'var(--agent)', 20)}<span class="q3t">« Avez-vous lu notre dernière lettre d'information ? »</span></div>
          <div class="note" style="margin-top:14px" data-in="p_6q@1">Une aide à la conversation, pas une conclusion sur la situation de la cliente.</div>
        </div>
      </div>
      <div class="stamp" style="right:40px;bottom:30px" data-in="p_7@2+4.8" data-anim="pop">✓ Brief v2 validé par Sophie · 09:02</div>
    </div>
    <div class="col abs" style="left:1330px;top:0;width:410px;gap:18px">
      <div class="card" data-in="p_7" data-anim="left"><div class="kicker">Correction CGP</div>
        <div class="col" style="gap:10px;margin-top:12px;font-size:20px">
          <div class="row" style="gap:10px" data-in="p_7@1">${ic('eye', 'var(--human)', 22)} Voit chaque source</div>
          <div class="row" style="gap:10px" data-in="p_7@2+0.6">${ic('cross', 'var(--human)', 22)} Retire une question</div>
          <div class="row" style="gap:10px" data-in="p_7@2+2.7">${ic('check', 'var(--human)', 22)} Corrige une date</div>
        </div>
        <div class="btn human" style="margin-top:18px" id="briefok" data-cls="p_7@2+4.4:pressed">${ic('check', '#fff', 22)} Valider le brief</div>
      </div>
      <div class="card" style="border:2px solid var(--human)" data-in="p_7@3" data-anim="pop"><div class="t"><b>Sophie mène le rendez-vous</b> et interprète les réponses.</div></div>
    </div>
  </div>

  <!-- P8 rendez-vous -->
  <div class="ph" data-in="p_8" data-out="p_9-0.2" data-anim="fade">
    <div class="col" style="align-items:center;margin-top:30px">
      <div class="row" style="gap:120px;align-items:center">
        <div class="col" style="align-items:center;gap:10px" data-in="p_8+0.3" data-anim="right">${av('S', 150)}<div class="h3">Sophie</div><div class="small">CGP</div></div>
        <div style="width:300px;height:14px;border-radius:7px;background:#C9B79A"></div>
        <div class="col" style="align-items:center;gap:10px" data-in="p_8+0.3" data-anim="left">${av('C', 150)}<div class="h3">Camille R.</div><div class="small">cliente fictive</div></div>
      </div>
      <div class="row" style="gap:20px;margin-top:60px" data-in="p_8@1" data-anim="pop">
        <span class="chip slate" style="font-size:26px;padding:12px 24px">${ic('cross', 'var(--slate)', 26)} Pas d'écran d'IA pendant le rendez-vous</span>
      </div>
      <div class="t" style="margin-top:26px;font-size:28px;font-weight:600" data-in="p_8@1+1.2">La conversation appartient à la cliente et à sa conseillère.</div>
    </div>
  </div>

  <!-- P9 brouillon de compte rendu -->
  <div class="ph" data-in="p_9" data-out="p_11-0.2" data-anim="fade">
    <div class="row" style="justify-content:space-between">
      <div class="h3">Compte rendu : brouillon préparé par l'agent</div>
      <span class="chip slate" data-in="p_9@1">${ic('tpl', 'var(--slate)', 20)} Notes de Sophie · transcription seulement si autorisée et encadrée</span>
    </div>
    <div class="row" style="gap:18px;align-items:stretch;margin-top:26px;height:330px">
      ${[['Faits rapportés par la cliente', 'p_9b+2.0', ['Changement d’employeur prévu l’an prochain', 'Souhaite un point plus régulier']],
        ['Questions ouvertes', 'p_9b+3.6', ['Date d’envoi du justificatif ?', 'Prochaine revue : quand ?']],
        ['Décisions prises par Sophie', 'p_9b+5.2', ['Mettre à jour le dossier avant la prochaine revue']]].map(([h, t, items]) => `
        <div class="crc" style="flex:1" data-in="${t}"><h4>${h}</h4>${items.map(it => `<div class="row" style="gap:8px;align-items:baseline;margin-bottom:8px">• ${it}</div>`).join('')}</div>`).join('')}
      <div class="crc" style="flex:1.25" data-in="p_9b+6.6"><h4>Actions proposées</h4>
        <div style="margin-bottom:10px">• Relancer le justificatif manquant</div>
        <div style="position:relative;min-height:120px">
          <div class="abs" style="left:0;top:0;width:100%" data-out="p_10@1+0.4" data-outdur="0.2"><span data-cls="p_9c:amber-hl">• « revoir le dossier le mois prochain »</span>
            <div class="row" style="gap:8px;margin-top:10px;font-size:18px;color:var(--amber);font-weight:700" data-in="p_9c@1">${ic('warn', 'var(--amber)', 20)} Ambigu : quoi ? avec qui ? quand ?</div>
            <div style="font-size:17px;color:var(--muted);margin-top:4px" data-in="p_9c@2">Non complété par l'agent</div>
          </div>
          <div class="abs" style="left:0;top:0;width:100%" data-in="p_10@1+0.5" data-anim="fade"><span class="ok-hl">• Point téléphonique dans 4 semaines, mené par Sophie</span><div style="font-size:17px;color:var(--human);margin-top:8px;font-weight:700">précisé par Sophie</div></div>
        </div>
      </div>
    </div>
    <div class="row" style="justify-content:flex-end;margin-top:22px;gap:20px">
      <div class="btn human" id="crok" data-in="p_10" data-cls="p_10@2+0.4:pressed">${ic('check', '#fff', 22)} Valider le compte rendu</div>
    </div>
    <div class="stamp" style="left:560px;top:520px" data-in="p_10@2+0.6" data-anim="pop">✓ Compte rendu validé par Sophie · 15:31</div>
  </div>

  <!-- P10 tâches et message -->
  <div class="ph" data-in="p_11" data-out="p_gain-0.2" data-anim="fade">
    <div class="card abs" style="left:0;top:0;width:900px;padding:26px 30px">
      <div class="row" style="justify-content:space-between"><div class="h3">Tâches proposées</div>${AGENT('proposition')}</div>
      ${[['Point téléphonique avec Camille R.', 'Sophie', 'dans 4 semaines'], ['Relancer le justificatif manquant', 'Léa', 'vendredi']].map(([l, r, e], k) => `
      <div style="border:1.5px solid #E3E8EF;border-radius:14px;padding:16px 20px;margin-top:16px" data-in="p_11@1+${stag(k, 0.3, 1.2)}" data-anim="left">
        <div style="font-size:23px;font-weight:700">${l}</div>
        <div class="col" style="gap:6px;margin-top:8px">
          <div class="field">Responsable : <b>${r}</b> <span style="display:inline-grid"><span style="grid-area:1/1" class="chip amber" data-out="p_11@2+1.2" data-outdur="0.15">à confirmer</span><span style="grid-area:1/1" class="chip human" data-in="p_11@2+1.3" data-anim="fade">confirmé</span></span></div>
          <div class="field">Échéance : <b>${e}</b> <span style="display:inline-grid"><span style="grid-area:1/1" class="chip amber" data-out="p_11@2+1.2" data-outdur="0.15">à confirmer</span><span style="grid-area:1/1" class="chip human" data-in="p_11@2+1.3" data-anim="fade">confirmée</span></span></div>
        </div>
      </div>`).join('')}
      <div class="row" style="margin-top:18px;gap:18px">
        <div class="btn human" id="taskok" data-cls="p_11@2+1.0:pressed">${ic('check', '#fff', 22)} Valider les 2 tâches</div>
        <span class="chip human" data-in="p_11@2+2.0" data-anim="pop">${ic('task', 'var(--human)', 18)} Ajoutées à l'outil de suivi autorisé</span>
      </div>
    </div>
    <div class="win abs" style="left:950px;top:0;width:790px" data-in="p_11b">
      <div class="bar"><i></i><i></i><i></i><span class="ttl">Message à Camille R.</span><span class="chip amber" style="margin-left:auto">Brouillon · non envoyé</span></div>
      <div class="body">
        <div class="field">À : <b>Camille R. (fictive)</b></div>
        <div class="field" style="margin-top:6px">Objet : <b>Suite à notre rendez-vous</b></div>
        <div class="divider"></div>
        <div style="font-size:23px;line-height:1.5;color:#2B3A52">Bonjour,<br>Merci pour notre échange de ce jour. Comme convenu, je vous propose un point téléphonique dans quatre semaines. …</div>
        <div class="divider"></div>
        <div class="row" style="gap:16px">
          <div class="btn disabled">${ic('spark', '#A3AEBE', 20)} Agent : préparer</div>
          <div class="btn human" id="msgsend">${ic('send', '#fff', 20)} Vérifier et envoyer (Sophie)</div>
        </div>
      </div>
    </div>
    <div class="abs" style="left:950px;top:470px" data-in="p_11b@2" data-anim="pop"><span class="chip navy" style="font-size:24px;padding:12px 24px">Rien ne part sans le clic de Sophie</span></div>
  </div>

  <!-- P11 gains et jalon -->
  <div class="phase" data-in="p_gain" data-anim="fade">
    <div class="row" style="gap:30px;align-items:stretch;margin-top:90px;height:560px">
      <div class="card col" style="width:700px;gap:22px">
        <div class="kicker">Bloc 1 : préparation et suivi</div>
        <div class="row" style="gap:16px;align-items:flex-end;height:350px">
          <div class="col" style="align-items:center;gap:8px"><div style="width:130px;height:300px;background:#C9D2DE;border-radius:12px"></div><b style="font-size:27px;white-space:nowrap">8 h avant</b></div>
          <div class="col" style="align-items:center;gap:8px"><div style="width:130px;height:150px;background:var(--agent);border-radius:12px" data-in="p_gain+1.4" data-anim="up"></div><b style="font-size:27px;white-space:nowrap">4 h visées</b></div>
          <div class="col" style="gap:8px;margin-left:16px" data-in="p_gain+2.6"><div style="font-size:64px;font-weight:800;color:var(--agent)">4 h</div><div class="t" style="white-space:nowrap">gain cible / semaine</div></div>
        </div>
        <span class="chip amber" style="align-self:flex-start" data-in="p_gain@1">gain cible, pas un résultat</span>
      </div>
      <div class="card col" style="width:440px;gap:14px" data-in="p_measure">
        <div class="kicker">À mesurer</div>
        ${['Temps avant et après', 'Corrections demandées', 'Erreurs relevées', 'Utilité réelle des briefs'].map((m, k) => `<div class="row t" style="gap:12px" data-in="p_measure+${stag(k, 0.6, 1.0)}">${ic('clock', 'var(--navy)', 26)} ${m}</div>`).join('')}
      </div>
      <div class="card col" style="width:540px;gap:18px" data-in="p_jalon">
        <div class="kicker">Premier jalon</div>
        <div class="row" style="gap:14px"><span style="font-size:60px;font-weight:800;color:var(--navy)">3</span><span class="h3">briefs</span>${ic('arrow', 'var(--muted)', 36)}${HUMAN('Décision de Sophie')}</div>
        <div class="col" style="gap:10px;margin-top:6px">
          ${[['human', 'Continuer'], ['amber', 'Ajuster'], ['red', "Retirer l'accès"]].map(([c, l], k) => `<span class="chip ${c}" style="font-size:24px;align-self:flex-start" data-in="p_jalon@1+${stag(k, 0, 0.8)}" data-anim="pop">${l}</span>`).join('')}
        </div>
      </div>
    </div>
  </div>`;

  const st = document.createElement('style');
  st.textContent = '.dim{opacity:.5}.dim .q3t{text-decoration:line-through;text-decoration-color:var(--red);text-decoration-thickness:3px}';
  root.appendChild(st);
  const clock = root.querySelector('#a1clocktxt');
  const t8 = T('p_8'), t8e = T('p_8$'), t9 = T('p_9'), tv = T('p_7@2+4.8'), tcr = T('p_10@2+0.6');
  return {
    update(t) {
      let txt = 'Mardi 08:35';
      if (t >= tv) txt = 'Mardi 09:02';
      if (t >= t8) {
        const k = Math.min(1, Math.max(0, (t - t8 - 0.5) / Math.max(1, t8e - t8 - 1)));
        const m = Math.round(14 * 60 + k * 70);
        txt = `Mardi ${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`;
      }
      if (t >= t9) txt = 'Mardi 15:10';
      if (t >= tcr) txt = 'Mardi 15:31';
      clock.textContent = txt;
    },
    cursors: [
      [{ t: 'p_1+0.9', sel: '#a1prep', fx: 0.3 }, { t: 'p_1+1.6', sel: '#a1prep', click: true, hold: 1.5 }],
      [{ t: 'p_2+3.2', sel: '#src0 .tog', click: true, move: 0.6 }, { t: 'p_2+4.6', sel: '#src1 .tog', click: true }, { t: 'p_2+6.0', sel: '#src2 .tog', click: true }, { t: 'p_2+7.8', sel: '#src3 .tog', click: true }, { t: 'p_2b+3.4', sel: '#srcok', click: true, hold: 1.3 }],
      [{ t: 'p_7@1', sel: '#q3', fx: 0.8 }, { t: 'p_7@2+0.6', sel: '#q3', fx: 0.8, click: true }, { t: 'p_7@2+2.6', sel: '.ok-hl', fx: 0.3, click: true }, { t: 'p_7@2+4.4', sel: '#briefok', click: true, hold: 1.5 }],
      [{ t: 'p_10@1', sel: '.scene-agent1 [data-cls="p_9c:amber-hl"]', fx: 0.6 }, { t: 'p_10@1+0.4', sel: '.scene-agent1 [data-cls="p_9c:amber-hl"]', fx: 0.6, click: true }, { t: 'p_10@2+0.4', sel: '#crok', click: true, hold: 1.5 }],
      [{ t: 'p_11@2+0.3', sel: '#taskok', fx: 0.2 }, { t: 'p_11@2+1.0', sel: '#taskok', click: true }, { t: 'p_11b@1+0.8', sel: '#msgsend', hold: 2.5 }],
    ],
  };
});

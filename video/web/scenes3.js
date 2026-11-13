/* Agents 2 et 3. Données entièrement fictives ; listes de démonstration, non réglementaires. */
function clockEl(id, txt, tin, tout) {
  return `<div class="clock" id="${id}" data-in="${tin}" data-out="${tout}"><span>●</span><b>${txt}</b></div>`;
}
function gainsPanel(prefix, bloc, before, after, gain, metrics, tGain, tMeasure, extra) {
  return `
  <div class="phase" data-in="${tGain}" data-anim="fade">
    <div class="row" style="gap:30px;align-items:stretch;margin-top:90px;height:560px">
      <div class="card col" style="width:700px;gap:22px">
        <div class="kicker">${bloc}</div>
        <div class="row" style="gap:16px;align-items:flex-end;height:350px">
          <div class="col" style="align-items:center;gap:8px"><div style="width:130px;height:${before * 34}px;background:#C9D2DE;border-radius:12px"></div><b style="font-size:27px">${before} h avant</b></div>
          <div class="col" style="align-items:center;gap:8px"><div style="width:130px;height:${after * 34}px;background:var(--agent);border-radius:12px" data-in="${tGain}+1.4" data-anim="up"></div><b style="font-size:27px">${after} h visées</b></div>
          <div class="col" style="gap:8px;margin-left:16px" data-in="${tGain}+2.4"><div style="font-size:64px;font-weight:800;color:var(--agent)">${gain} h</div><div class="t">gain cible / semaine</div></div>
        </div>
        <span class="chip amber" style="align-self:flex-start" data-in="${tGain}+2.8">hypothèse, à mesurer pendant le pilote</span>
      </div>
      <div class="card col" style="width:1010px;gap:22px" data-in="${tMeasure}">
        <div class="kicker">Ce que le pilote suivra aussi</div>
        ${metrics.map(([m, d], k) => `<div class="row t" style="gap:14px" data-in="${tMeasure}+${d}">${ic('clock', 'var(--navy)', 28)} ${m}</div>`).join('')}
        ${extra || ''}
      </div>
    </div>
  </div>`;
}

/* ===================== AGENT 2 ===================== */
registerScene('agent2', (root) => {
  const cols = [
    ['Présent', 'var(--human)', 'human', [['Pièce d’identité', 0.4], ['Lettre de mission', 1.2], ['Dernier compte rendu signé', 2.0]]],
    ['Absent', 'var(--red)', 'red', [['Questionnaire client à jour', 3.0]]],
    ['Ambigu', 'var(--amber)', 'amber', [['Justificatif de domicile', 4.2]]],
    ['Non vérifié', 'var(--slate)', 'slate', [['Relevé de situation : lien inaccessible', 5.4]]],
  ];
  root.innerHTML = `
  ${clockEl('a2clock', 'Mercredi 10:20', 'd_intro@1', 'd_gain-0.3')}
  <div class="phase" data-out="d_limit-0.2">
    <div class="win abs" style="left:0;top:10px;width:860px;height:640px" data-in="d_intro">
      <div class="bar"><i></i><i></i><i></i><span class="ttl">Espace documentaire : dossiers à préparer</span></div>
      <div class="body col" style="gap:10px;font-size:22px">
        ${[['folder', 'Famille M. / Revue périodique', 0], ['folder', 'Camille R. / Suivi', 1], ['file', 'scan_0412.pdf', 2], ['file', 'justif_dom_2.jpg', 2], ['file', 'piece_id_recto.jpg', 2], ['file', 'CR_mars_v2.docx', 2], ['folder', 'M. B. / Suivi', 1], ['file', 'a_classer (14)', 2]].map(([i, l, lv], k) => `
          <div class="row" style="gap:12px;padding-left:${lv * 30}px" data-in="d_intro@2+${stag(k, 0.2, 0.35)}" data-anim="fade">${ic(i, '#8B98AB', 26)} ${l}</div>`).join('')}
        <div class="row" style="gap:12px;margin-top:20px" data-in="d_today+2.4">${ic('search', 'var(--amber)', 28)}<span class="t" style="color:var(--amber);font-weight:700">Date de la pièce ? Illisible…</span></div>
      </div>
    </div>
    <div class="col abs" style="left:920px;top:10px;width:820px;gap:22px">
      <div class="card" data-in="d_today" data-anim="left">
        <div class="row" style="justify-content:space-between"><div class="h3">Liste du cabinet</div>${av('L', 52)}</div>
        <div class="col" style="gap:10px;margin-top:14px">
          ${['Comparer les fichiers à la liste', 'Chercher les dates sur les pièces', 'Faire trancher les cas incertains'].map((l, k) => `<div class="row t" style="gap:12px" data-in="d_today+${stag(k, 0.6, 2.1)}">${ic('task', 'var(--slate)', 26)} ${l}</div>`).join('')}
        </div>
      </div>
      <div class="card row" style="gap:16px" data-in="d_today+5.6" data-anim="pop">${av('S', 52)}${av('K', 52)}<span class="t">« Celui-ci, on le garde ? »</span></div>
      <div class="row" style="gap:14px" data-in="d_9"><span class="chip amber" style="font-size:24px;padding:10px 20px">Bloc 2 : 9 h / semaine</span><span class="small">simulation</span></div>
    </div>
  </div>

  <div class="phase" data-in="d_limit" data-out="d_run-0.2" data-anim="fade">
    <div class="row" style="gap:40px;align-items:stretch;margin-top:30px">
      <div class="card col" style="width:820px;gap:20px">
        <div class="kicker">Règles de contrôle</div>
        <div class="h3">L'agent n'invente pas les règles</div>
        <div class="row t" style="gap:14px" data-in="d_limit@1">${ic('file', 'var(--navy)', 30)} Liste fournie par le cabinet</div>
        <div class="row t" style="gap:14px" data-in="d_limit@1+1.8">${HUMAN('Validée par la personne compétente')}</div>
        <div class="row" style="gap:14px;margin-top:10px" data-in="d_limit+1.0"><span class="chip agent strike" data-var="d_limit+1.8:0.5:p:0:1">${ic('spark', 'var(--agent)', 18)} Règles créées par l'agent</span></div>
      </div>
      <div class="card col" style="width:880px;gap:16px" data-in="d_frame">
        <div class="kicker">Cadre d'accès aux données</div>
        ${['Quelles sources', 'Quelles personnes habilitées', 'Quelle finalité', 'Quel sous-traitant éventuel', 'Quelle conservation'].map((l, k) => `<div class="row t" style="gap:14px;padding:8px 0;border-bottom:1px solid #EEF1F5" data-in="d_frame+${stag(k, 1.4, 1.35)}" data-anim="left">${ic('shield', 'var(--navy)', 28)} ${l}<span class="chip slate" style="margin-left:auto">à vérifier</span></div>`).join('')}
      </div>
    </div>
  </div>

  <div class="phase" data-in="d_run" data-out="d_review-0.2" data-anim="fade">
    <div class="row" style="justify-content:space-between"><div class="h3">Inventaire : Famille M. (fictive)</div><span class="chip slate">liste fictive de démonstration, non réglementaire</span></div>
    <div class="row" style="gap:18px;align-items:stretch;margin-top:20px;height:600px">
      ${cols.map(([n, c, cls, items], k) => `
      <div class="kcol" style="flex:1;border-top-color:${c}" data-in="d_run+${stag(k, 6.2, 0.7)}" data-anim="up">
        <div class="row" style="justify-content:space-between"><span class="chip ${cls}" style="font-size:22px">${n}</span></div>
        ${items.map(([l, d]) => `<div class="kcard" ${cls === 'amber' ? 'id="ambcard" data-cls="d_amb@2:sel"' : ''} data-in="d_run+${(6.6 + d).toFixed(2)}" data-anim="down">${l}</div>`).join('')}
      </div>`).join('')}
    </div>
    <div class="card abs" style="left:780px;top:150px;width:960px;padding:26px 30px;border:2px solid var(--amber)" data-in="d_amb@2" data-anim="pop">
      <div class="row" style="justify-content:space-between"><div class="h3">Justificatif de domicile</div><span class="chip amber">Ambigu</span></div>
      <div class="row" style="gap:26px;margin-top:16px;align-items:flex-start">
        <div style="width:300px;height:260px;border-radius:10px;background:#F4F1EA;border:1px solid #E2DCCF;padding:20px;font-size:17px;color:#6A6457;line-height:1.7">
          FACTURE<br>Mme M.<br>12, rue fictive<br><span style="filter:blur(5px)">Date : 14/02/2023</span><br>Montant : ███
        </div>
        <div class="col" style="gap:12px">
          <div class="row t" style="gap:10px">${ic('warn', 'var(--amber)', 26)} Date illisible</div>
          <div class="row t" style="gap:10px">${ic('cross', 'var(--muted)', 26)} Ni « valide »</div>
          <div class="row t" style="gap:10px">${ic('cross', 'var(--muted)', 26)} Ni « périmé »</div>
          <div class="small">Source : justif_dom_2.jpg</div>
        </div>
      </div>
      <div class="row" style="gap:14px;margin-top:18px" data-in="d_lea">
        <div class="btn human" id="a2better" data-cls="d_lea+1.6:pressed">${ic('search', '#fff', 20)} Demander une meilleure version</div>
        <div class="btn ghost">${ic('user', 'var(--ink)', 20)} Soumettre à Sophie</div>
      </div>
    </div>
  </div>

  <div class="phase" data-in="d_review" data-out="d_kyc-0.2" data-anim="fade">
    <div class="h3">Revue périodique : comparaison avec la dernière revue</div>
    <div class="row" style="gap:20px;margin-top:24px">
      ${[['Éléments nouveaux', 2, 'agent'], ['Inchangés', 5, 'slate'], ['Pièces à examiner', 2, 'amber'], ['Contrôles sans réponse', 1, 'red']].map(([l, n, c], k) => `
      <div class="card col" style="flex:1;gap:8px" data-in="d_review+${stag(k, 3.0, 1.0)}" data-anim="up"><span class="chip ${c}" style="align-self:flex-start">${l}</span><div style="font-size:70px;font-weight:800;color:var(--navy)">${n}</div></div>`).join('')}
    </div>
    <div class="row" style="gap:40px;margin-top:50px;justify-content:center">
      <div class="card row" style="gap:20px;border:3px solid var(--amber);padding:26px 36px" data-in="d_human+2.2" data-anim="pop">${ic('user', 'var(--amber)', 48)}<div><div class="h3" style="color:var(--amber)">Décision humaine requise</div><div class="t">une information essentielle manque</div></div></div>
      <div class="card row" style="gap:20px;padding:26px 36px;opacity:.9" data-in="d_human@1" data-anim="fade">
        <span class="chip human strike" style="font-size:26px;padding:10px 22px" data-var="d_human@1+1.0:0.5:p:0:1">${ic('check', 'var(--human)', 24)} Dossier conforme</span>
        <div class="t" style="width:260px">jamais attribué par l'agent seul</div>
      </div>
    </div>
  </div>

  <div class="phase" data-in="d_kyc" data-out="d_log-0.2" data-anim="fade">
    <div class="row" style="justify-content:space-between"><div class="h3">Connaissance client et vigilance : repères généraux</div><span class="chip slate">selon les activités du cabinet</span></div>
    <div class="col" style="gap:18px;margin-top:26px;width:1740px">
      <div class="card row" style="gap:20px" data-in="d_kyc@1" data-anim="left">${ic('shield', 'var(--navy)', 40)}<div class="t">Chaque professionnel applique les exigences propres aux activités qu'il exerce.</div></div>
      <div class="card row" style="gap:20px" data-in="d_amf" data-anim="left">${ic('file', 'var(--navy)', 40)}<div class="t"><b>Conseil en investissements financiers (repère AMF)</b> : informations à recueillir avant de conseiller, déclaration d'adéquation remise au client avant la réalisation de l'opération conseillée.</div></div>
      <div class="card row" style="gap:20px" data-in="d_amf@1" data-anim="left">${ic('search', 'var(--navy)', 40)}<div class="t"><b>Vigilance à l'égard des clients</b> (professionnels assujettis) : approche fondée sur les risques.</div></div>
      <div class="row" style="gap:20px;margin-top:10px">
        <div data-in="d_nostat">${AGENT("L'agent prépare et retrouve")}</div>
        <span class="chip red strike" data-in="d_nostat+2.0" data-var="d_nostat+2.6:0.5:p:0:1">L'agent statue sur la suffisance</span>
        <span class="chip slate" data-in="d_nostat@1">Pas un modèle universel de dossier réglementaire</span>
      </div>
    </div>
  </div>

  <div class="phase" data-in="d_log" data-out="d_gain-0.2" data-anim="fade">
    <div class="h3">Journal de la revue</div>
    <div class="card" style="margin-top:20px;padding:10px 26px">
      <table class="tbl"><tr><th>Horodatage</th><th>Événement</th><th>Acteur</th><th>Version et sources</th></tr>
        ${[['Mer. 10:24', 'Inventaire préparé', AGENT('Agent'), 'v1 · sources S1 à S7'], ['Mer. 10:41', 'Meilleure version retrouvée', HUMAN('Léa'), 'v2 · pièce remplacée'], ['Mer. 11:05', 'Revue arbitrée', HUMAN('Sophie'), 'v2 · points ouverts, suite décidée']].map((r, k) => `
        <tr data-in="d_log+${stag(k, 1.5, 2.6)}" data-anim="fade"><td class="mono" style="font-size:22px">${r[0]}</td><td style="font-weight:600">${r[1]}</td><td>${r[2]}</td><td style="color:var(--muted)">${r[3]}</td></tr>`).join('')}
      </table>
      <div class="small" style="padding:12px 16px" data-in="d_log+8.5">Conservation : selon les règles décidées par le cabinet</div>
    </div>
    <div class="card row" style="gap:20px;margin-top:30px;border:2px solid var(--amber)" data-in="d_lognot" data-anim="pop">${ic('warn', 'var(--amber)', 44)}<div class="t"><b>Un journal technique</b> n'est pas, à lui seul, la preuve que les obligations réglementaires sont remplies.</div></div>
  </div>
  ${gainsPanel('a2', 'Bloc 2 : contrôles et revues', 9, 6, 3, [['Faux positifs', 0.4], ['Vrais manques détectés', 1.6], ["Situations correctement laissées à l'équipe", 2.8]], 'd_gain', 'd_measure')}
  `;
  const st = document.createElement('style');
  st.textContent = '.sel{box-shadow:0 0 0 4px var(--amber)!important}';
  root.appendChild(st);
  return {
    cursors: [[{ t: 'd_amb@1', sel: '#ambcard', fx: 0.6 }, { t: 'd_amb@2-0.1', sel: '#ambcard', fx: 0.6, click: true }, { t: 'd_lea+1.6', sel: '#a2better', click: true, hold: 1.4 }]],
  };
});

/* ===================== AGENT 3 ===================== */
registerScene('agent3', (root) => {
  root.innerHTML = `
  ${clockEl('a3clock', 'Jeudi 16:40', 's_intro@1', 's_monday-0.2')}
  ${clockEl('a3clock2', 'Lundi 09:00', 's_monday', 's_gain-0.3')}
  <div class="phase" data-out="s_class-0.2">
    <div class="win abs" style="left:0;top:10px;width:980px" data-in="s_intro@1">
      <div class="bar"><i></i><i></i><i></i><span class="ttl">Messagerie du cabinet</span><span class="chip red" style="margin-left:auto">nouveau</span></div>
      <div class="body">
        <div class="row" style="gap:16px"><span class="avatar av-C" style="width:56px;height:56px;font-size:25px">D</span><div><div style="font-size:24px;font-weight:700">Mme D. <span class="chip fict">cliente fictive</span></div><div class="small">jeudi 16:40</div></div></div>
        <div style="font-size:30px;line-height:1.45;margin-top:22px;font-weight:500" data-type="s_intro@2+0.8:24">« Pouvez-vous me rappeler ce que nous avions convenu pour la suite ? »</div>
      </div>
    </div>
    <div class="row abs" style="left:0;top:380px;gap:16px" data-in="s_today">
      ${av('L', 56)}
      ${[['search', 'Dernier compte rendu', 0.6], ['task', 'Tâche correspondante', 2.0], ['user', 'Question à Karim : c’est fait ?', 3.4]].map(([i, l, d]) => `<span class="chip slate" style="font-size:22px;padding:10px 18px" data-in="s_today+${d}" data-anim="pop">${ic(i, 'var(--slate)', 22)} ${l}</span>`).join('')}
    </div>
    <div class="card col abs" style="left:1040px;top:10px;width:700px;gap:14px" data-in="s_today@1">
      <div class="kicker">En parallèle</div>
      <div class="row t" style="gap:12px" data-in="s_today@1+0.6">${ic('user', 'var(--amber)', 28)} Un prospect attend un retour</div>
      <div class="row t" style="gap:12px" data-in="s_today@1+1.8">${ic('cal', 'var(--amber)', 28)} Échéance : renouvellement d'un document</div>
      <div class="row t" style="gap:12px" data-in="s_today@1+2.4">${ic('cal', 'var(--amber)', 28)} Échéance : revue annuelle à planifier</div>
    </div>
  </div>

  <div class="phase" data-in="s_class" data-out="s_draft-0.2" data-anim="fade">
    <div class="row" style="gap:16px">${AGENT('Agent de service')}<span class="chip navy" data-in="s_class+1.6" data-anim="pop">Demande : rappel d'un engagement</span></div>
    <div class="row" style="gap:16px;margin-top:20px">
      ${[['mail', 'Message reçu', 3.0], ['file', 'Compte rendu validé du 3 octobre', 4.2], ['task', 'Tâche T-118 et son statut', 5.6]].map(([i, l, d]) => `<span class="chip slate" style="font-size:22px;padding:10px 18px" data-in="s_class+${d}" data-anim="pop">${ic(i, 'var(--slate)', 22)} ${l}</span>`).join('')}
      <span class="chip slate" style="font-size:20px" data-in="s_class+6.6">seuls éléments autorisés</span>
    </div>
    <div class="card" style="margin-top:28px;padding:10px 30px" data-in="s_card">
      <table class="tbl">
        ${[['Engagement retrouvé', 'Envoyer la synthèse des pièces à mettre à jour', 1], ['Source', '<span class="src" style="margin:0">CR validé du 3 octobre</span>', 2], ['État connu', '<span class="chip amber">statut non renseigné</span> tâche T-118 sans mise à jour', 3], ['Ce que nous ne savons pas encore', 'Si l’envoi a été fait par Karim', 4]].map(([a, b, n]) => `
        <tr data-in="s_card@${n}" data-anim="fade"><td style="width:430px;font-weight:700;color:var(--muted)">${a}</td><td style="font-weight:600">${b}</td></tr>`).join('')}
      </table>
    </div>
  </div>

  <div class="phase" data-in="s_draft" data-out="s_prosp-0.2" data-anim="fade">
    <div class="win abs" style="left:0;top:0;width:1100px">
      <div class="bar"><i></i><i></i><i></i><span class="ttl">Réponse à Mme D.</span><span class="chip amber" style="margin-left:auto">Brouillon</span></div>
      <div class="body" style="font-size:25px;line-height:1.55;color:#2B3A52">
        Bonjour Madame,<br>Lors de notre dernier rendez-vous, nous avions convenu de vous envoyer la synthèse des pièces à mettre à jour.
        <span style="display:inline-grid"><span style="grid-area:1/1" class="amber-hl" data-in="s_draft@1+1.0" data-anim="fade" data-out="s_karim+2.0" data-outdur="0.2">Je vérifie où en est cet envoi et je reviens vers vous.</span><span style="grid-area:1/1" class="ok-hl" data-in="s_karim+2.2" data-anim="fade">Après vérification, elle vous sera envoyée demain matin.</span></span>
<div class="row" style="gap:10px;margin-top:16px;font-size:19px;color:var(--amber);font-weight:700" data-in="s_draft@1+2.6">${ic('warn', 'var(--amber)', 22)} Statut non fiable : le brouillon n'affirme pas que c'est fait</div>
        <div class="row" style="gap:10px;margin-top:6px;font-size:19px;color:var(--human);font-weight:700" data-in="s_karim+2.2">${ic('user', 'var(--human)', 22)} Complété par Karim après vérification</div>
      </div>
    </div>
    <div class="col abs" style="left:1160px;top:0;width:580px;gap:22px">
      <div class="card" data-in="s_karim@1"><div class="kicker">Boutons de l'agent</div><div class="row" style="gap:12px;margin-top:14px"><div class="btn agent">${ic('spark', '#fff', 20)} Préparer</div><span class="small">et rien d'autre</span></div></div>
      <div class="card" data-in="s_karim@1+0.6"><div class="row" style="justify-content:space-between"><div class="kicker">Boutons de Karim</div>${av('K', 46)}</div><div class="btn human" id="a3send" style="margin-top:14px" data-cls="s_karim@2+0.9:pressed">${ic('send', '#fff', 20)} Vérifier et envoyer</div></div>
      <div data-in="s_karim@2+1.2" data-anim="pop">${HUMAN('Envoi décidé par Karim')}</div>
    </div>
  </div>

  <div class="phase" data-in="s_prosp" data-out="s_monday-0.2" data-anim="fade">
    <div class="row" style="gap:30px;align-items:stretch">
      <div class="card col" style="width:1000px;gap:14px">
        <div class="row" style="justify-content:space-between"><div class="h3">Fiche de qualification : prospect</div>${AGENT('proposition')}</div>
        <div class="small">À partir du formulaire du site et d'un échange autorisé · données fictives</div>
        ${[['Demande exprimée', 'Faire un point sur sa situation après un changement professionnel', 1.0], ['Disponibilités', 'Mardi ou jeudi, en fin de journée', 2.4], ['Questions pour un premier rendez-vous', 'Objectifs ? Horizon ? Documents déjà réunis ?', 4.0], ['Relance contextualisée', 'Brouillon prêt, non envoyé', 6.0]].map(([a, b, d]) => `
          <div style="border-top:1px solid #EEF1F5;padding-top:10px" data-in="s_prosp@1+${d}" data-anim="fade"><div style="font-size:18px;font-weight:800;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)">${a}</div><div class="t" style="font-weight:600">${b}</div></div>`).join('')}
      </div>
      <div class="col" style="width:710px;gap:20px">
        <div class="card col" style="gap:14px" data-in="s_noscore">
          <div class="row" style="justify-content:space-between"><div class="kicker">Le conseiller choisit</div>${av('K', 46)}</div>
          ${['Prendre contact ?', 'Accepter ou non le prospect', 'Envoyer chaque message'].map((l, k) => `<div class="row t" style="gap:12px" data-in="s_noscore+${stag(k, 0.6, 1.4)}">${ic('user', 'var(--human)', 26)} ${l}</div>`).join('')}
        </div>
        <div class="card row" style="gap:16px;border:2px solid var(--red)" data-in="s_noscore@1" data-anim="pop">
          <span class="chip red strike" style="font-size:24px" data-var="s_noscore@1+0.6:0.5:p:0:1">Score de « valeur » : 82/100</span><span class="t">aucun score automatique</span>
        </div>
      </div>
    </div>
  </div>

  <div class="phase" data-in="s_monday" data-out="s_gain-0.2" data-anim="fade">
    <div class="row" style="justify-content:space-between"><div class="h3">Pilotage de la semaine</div><span class="chip slate" data-in="s_lists+10.5">règle du cabinet : sans action depuis 90 jours (paramètre)</span></div>
    <div class="row" style="gap:16px;align-items:stretch;margin-top:18px;height:620px">
      ${[['Rendez-vous à préparer', 'var(--agent)', [['Foyer G. · mardi', 'brief à lancer'], ['Famille M. · jeudi', 'revue périodique']], 4.0],
        ['Engagements sans responsable confirmé', 'var(--amber)', [['M. B. · envoi d’une synthèse', 'responsable non renseigné']], 6.2],
        ['Échéances à vérifier', '#2B5D8C', [['Renouvellement d’un document', 'date dans 12 jours']], 8.6],
        ['Dossiers sans action récente', 'var(--slate)', [['Foyer H.', 'pas d’action depuis 96 jours', 'Attend volontairement une date', 'human'], ['Foyer P.', 'pas d’action depuis 104 jours', 'Mérite un appel', 'human'], ['Foyer T.', 'pas d’action depuis 131 jours', 'Donnée CRM incorrecte', 'amber']], 10.5]].map(([h, c, items, d], k) => `
      <div class="kcol" style="flex:1;border-top-color:${c}" data-in="s_lists+${d}" data-anim="up">
        <div style="font-size:22px;font-weight:800;color:var(--navy);min-height:58px">${h}</div>
        ${items.map((it, j) => `<div class="kcard" data-in="s_lists+${(d + 0.5 + j * 0.4).toFixed(2)}" data-anim="fade"><div>${it[0]}</div><div style="font-size:18px;color:var(--muted);font-weight:500;margin-top:4px" data-in="s_reason+0.3">Raison : ${it[1]}</div>${it[2] ? `<div style="margin-top:8px" data-in="s_arb+${(j * 2.2 + 0.4).toFixed(2)}" data-anim="pop"><span class="chip ${it[3]}" style="font-size:17px">${ic('user', `var(--${it[3]})`, 16)} Sophie : ${it[2]}</span></div>` : ''}</div>`).join('')}
        ${k === 3 ? `<div data-in="s_reason@1" style="margin-top:auto"><span class="chip red strike" style="font-size:19px" data-var="s_reason@1+1.0:0.5:p:0:1">« client négligé »</span></div>` : ''}
      </div>`).join('')}
    </div>
  </div>
  ${gainsPanel('a3', 'Bloc 3 : relation client et pilotage', 7, 4, 3, [['Alertes utiles ou écartées', 0.4], ['Brouillons corrigés', 2.0], ['Engagements réellement retrouvés', 3.4]], 's_gain', 's_measure',
    `<div class="divider"></div><div class="row t" style="gap:14px" data-in="s_measure@1">${ic('warn', 'var(--amber)', 28)} Du bruit ? On réduit le périmètre.</div><div class="row t" style="gap:14px" data-in="s_measure@1+3">${ic('cross', 'var(--red)', 28)} Un cockpit que personne n'ouvre n'est pas un gain.</div>`)}
  `;
  return {
    cursors: [[{ t: 's_karim@2', sel: '#a3send', fx: 0.3 }, { t: 's_karim@2+0.9', sel: '#a3send', click: true, hold: 1.4 }]],
  };
});

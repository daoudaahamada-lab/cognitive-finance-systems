/* Données et limites, bilan, déploiement, conclusion. */

/* ===================== DONNÉES ===================== */
registerScene('data', (root) => {
  const nodes = [['db', 'Source autorisée'], ['lock', 'Accès limité'], ['spark', 'Préparation'], ['user', 'Validation humaine'], ['send', 'Destination autorisée']];
  root.innerHTML = `
  <div class="phase" data-out="x_flow-0.2">
    <div class="row" style="gap:30px;margin-top:80px;align-items:flex-start;justify-content:center">
      <div data-in="x_q" data-anim="pop">${av('S', 120)}</div>
      <div class="card" style="width:1100px;padding:34px 40px;border-radius:24px 24px 24px 4px" data-in="x_q+0.4" data-anim="left">
        <div class="h3" style="font-size:38px;line-height:1.3">« Pour préparer tout ça, l'agent doit-il lire tous mes mails et tous mes dossiers ? »</div>
      </div>
    </div>
    <div class="row" style="justify-content:center;margin-top:70px;gap:30px" data-in="x_no" data-anim="pop">
      <span style="font-size:110px;font-weight:800;color:var(--human)">Non.</span>
      <span class="t" style="width:520px">Un objectif défini, des sources approuvées, des droits limités, des personnes habilitées.</span>
    </div>
  </div>

  <div class="phase" data-in="x_flow" data-out="x_host-0.2" data-anim="fade">
    <div class="h3">Le chemin autorisé des données</div>
    <div class="row" style="gap:0;margin-top:40px;justify-content:space-between">
      ${nodes.map(([i, l], k) => `${k ? `<div data-in="x_flow@1+${stag(k, 0, 1.15)}" data-anim="fade">${ic('arrow', 'var(--navy2)', 46)}</div>` : ''}
        <div class="node col" style="width:270px;align-items:center;gap:10px;border-color:${k === 3 ? 'var(--human)' : k === 2 ? 'var(--agent)' : 'var(--line)'}" data-in="x_flow@1+${stag(k, 0, 1.15)}" data-anim="pop">${ic(i, k === 3 ? 'var(--human)' : k === 2 ? 'var(--agent)' : 'var(--navy)', 44)}${l}</div>`).join('')}
    </div>
    <div class="row" style="gap:20px;margin-top:26px;justify-content:center" data-in="x_flow@1+5.4">
      ${['Toute la messagerie', 'Envoi direct au client', 'Outil non approuvé'].map(l => `<span class="chip red" style="font-size:22px">${ic('cross', 'var(--red)', 20)} ${l}</span>`).join('')}
    </div>
    <div class="card" style="margin-top:36px" data-in="x_check">
      <div class="kicker">Avant toute donnée client, le cabinet examine</div>
      <div class="row" style="gap:16px;margin-top:16px;flex-wrap:wrap">
        ${['Ses responsabilités', 'Contrats prestataires', 'Sécurité', 'Conservation', 'Transferts éventuels'].map((l, k) => `<span class="chip slate" style="font-size:24px;padding:10px 20px" data-in="x_check+${stag(k, 1.6, 1.5)}" data-anim="pop">${ic('check', 'var(--slate)', 22)} ${l}</span>`).join('')}
      </div>
    </div>
  </div>

  <div class="phase" data-in="x_host" data-out="x_stop-0.2" data-anim="fade">
    <div class="row" style="gap:30px;margin-top:40px;justify-content:center;align-items:center" data-in="x_host">
      <div class="card col" style="width:560px;align-items:center;gap:12px">${ic('db', 'var(--navy)', 60)}<div class="h3" style="text-align:center">Modèle auto-hébergé<br>ou open source</div></div>
      <div style="font-size:120px;font-weight:800;color:var(--red)">≠</div>
      <div class="card col" style="width:560px;align-items:center;gap:12px">${ic('shield', 'var(--human)', 60)}<div class="h3" style="text-align:center">Traitement<br>conforme</div></div>
    </div>
    <div class="card" style="margin:50px auto 0;width:1500px" data-in="x_host@1">
      <div class="kicker">Points d'attention rappelés par la CNIL</div>
      <div class="row" style="gap:18px;margin-top:16px">
        ${['Encadrer la sous-traitance', 'Protéger les données', 'Garder une intervention humaine adaptée'].map((l, k) => `<span class="chip navy" style="font-size:24px;padding:12px 22px" data-in="x_host@1+${stag(k, 1.4, 1.4)}" data-anim="pop">${l}</span>`).join('')}
      </div>
    </div>
  </div>

  <div class="phase" data-in="x_stop" data-out="x_never-0.2" data-anim="fade">
    <div class="h2">L'agent sait s'arrêter</div>
    <div class="col" style="gap:24px;margin-top:40px">
      ${[['search', 'Source d’un fait introuvable', '« Information non vérifiée »', 'x_s1', 'amber'], ['file', 'Pièce illisible', 'Demande de vérification', 'x_s2', 'amber'], ['user', 'Interprétation patrimoniale ou décision de conseil', 'Transmis au CGP', 'x_s3', 'human']].map(([i, a, b, t, c]) => `
      <div class="card row" style="gap:26px;padding:26px 34px" data-in="${t}" data-anim="left">
        ${ic(i, 'var(--navy)', 44)}<div class="t grow" style="font-weight:700">${a}</div>${ic('arrow', 'var(--muted)', 40)}<span class="chip ${c}" style="font-size:26px;padding:12px 24px;min-width:420px;justify-content:center">${b}</span>
      </div>`).join('')}
    </div>
  </div>

  <div class="phase" data-in="x_never" data-out="x_demo-0.2" data-anim="fade">
    <div class="h2">Ce que l'agent ne fait jamais</div>
    <div class="col" style="gap:18px;margin-top:36px">
      ${['Recommander un produit', 'Déterminer seul un profil de risque', 'Déclarer un dossier conforme', 'Contacter quelqu’un automatiquement', 'Modifier un engagement client sans validation'].map((l, k) => `
      <div class="card row" style="gap:22px;padding:20px 30px" data-in="x_never@${k}" data-anim="left"><span class="x-mark" style="font-size:40px">✕</span><span class="t" style="font-weight:700;font-size:30px">${l}</span></div>`).join('')}
    </div>
  </div>

  <div class="phase" data-in="x_demo" data-anim="fade">
    <div class="h2">Un déploiement progressif</div>
    <div class="row" style="gap:0;margin-top:80px;justify-content:space-between">
      ${[['Données de démonstration', 'slate', 'x_demo+1.5'], ['Accès limité', 'slate', 'x_demo+3.0'], ['Revue du cadre et autorisation du cabinet', 'human', 'x_demo@1+1.5'], ['Données réelles', 'navy', 'x_demo@1+0.3']].map(([l, c, t], k) => `${k ? `<div data-in="${t}" data-anim="fade">${ic('arrow', 'var(--navy2)', 50)}</div>` : ''}
        <div class="node" style="width:360px;font-size:26px;padding:34px 24px;border-color:${c === 'human' ? 'var(--human)' : c === 'navy' ? 'var(--navy)' : 'var(--line)'}" data-in="${t}" data-anim="pop">${l}</div>`).join('')}
    </div>
  </div>`;
  return {};
});

/* ===================== BILAN ===================== */
registerScene('bilan', (root) => {
  root.innerHTML = `
  <div class="phase" data-out="b_460-0.2">
    <div class="row" style="justify-content:space-between"><div class="h2">Bilan : avant et après visé</div><span class="chip amber" style="font-size:22px">simulation · gains cibles</span></div>
    <div class="card" style="margin-top:24px;padding:12px 30px">
      <table class="tbl" style="font-size:28px">
        <tr><th>Bloc</th><th>Avant</th><th>Après visé</th><th>Gain cible</th></tr>
        ${[['Préparation des rendez-vous et suivi', 8, 4, 'b_1'], ['Contrôles et revues', 9, 6, 'b_2'], ['Relation client et pilotage', 7, 4, 'b_3']].map(([l, a, b, t]) => `
        <tr data-in="${t}" data-anim="fade"><td style="font-weight:700">${l}</td><td>${a} h</td><td data-in="${t}+1.6" data-anim="fade" style="color:var(--agent);font-weight:800">${b} h</td><td data-in="${t}@1" data-anim="pop"><span class="chip amber" style="font-size:22px">${a - b} h à confirmer</span></td></tr>`).join('')}
        <tr data-in="b_sum" data-anim="fade" style="background:#F6F8FB"><td style="font-weight:800">Total hebdomadaire</td><td style="font-weight:800">8 + 9 + 7 = 24 h</td><td data-in="b_sum@1" style="font-weight:800;color:var(--agent)">4 + 6 + 4 = 14 h</td><td data-in="b_sum@2" data-anim="pop"><span style="font-size:34px;font-weight:800;color:var(--navy)">10 h</span></td></tr>
      </table>
    </div>
    <div class="row" style="justify-content:center;margin-top:34px" data-in="b_cap" data-anim="pop">
      <div class="sim-banner" style="font-size:30px;padding:18px 32px">24 h → 14 h / semaine · Gain cible : 10 h · Mesure réelle : à établir</div>
    </div>
  </div>

  <div class="phase" data-in="b_460" data-anim="fade">
    <div class="col" style="gap:22px;margin-top:10px">
      <div class="card row" style="gap:30px;padding:24px 36px" data-in="b_460">
        <div class="eq" style="font-size:54px">10 h <span class="op">×</span> 46 semaines <span class="op">=</span> 460 h</div><span class="t" style="color:var(--muted)">de capacité potentielle par an</span>
      </div>
      <div class="card row" style="gap:30px;padding:24px 36px" data-in="b_euro">
        <div class="eq" style="font-size:54px">460 h <span class="op">×</span> 60 € <span class="op">=</span> <span data-count="b_euro+3.5:1.5:0:27600:0"></span> €</div>
        <div class="col" style="gap:6px"><span class="chip amber">valorisation interne illustrative</span><span class="chip amber">capacité théorique annuelle</span></div>
      </div>
    </div>
    <div class="row" style="gap:20px;margin-top:30px;align-items:stretch" data-in="b_not">
      ${[['Capacité théorique', 'ce calcul', 'navy'], ['Économies encaissées', 'non acquises', 'red'], ["Chiffre d'affaires additionnel", 'non promis', 'red']].map(([a, b, c], k) => `
      ${k ? `<div style="font-size:70px;font-weight:800;color:var(--muted);align-self:center" data-in="b_not@1+${stag(k, 0.6, 1.2)}">≠</div>` : ''}
      <div class="card col" style="flex:1;gap:10px;align-items:center;text-align:center" data-in="b_not@1+${stag(k, 0, 1.2)}" data-anim="pop"><div class="h3">${a}</div><span class="chip ${c}">${b}</span></div>`).join('')}
    </div>
    <div class="row" style="gap:16px;margin-top:30px;flex-wrap:wrap" data-in="b_minus">
      <span class="t" style="font-weight:800">À déduire :</span>
      ${['temps de contrôle humain', 'coût des outils', 'maintenance', 'erreurs à corriger'].map((l, k) => `<span class="chip slate" style="font-size:23px;padding:9px 18px" data-in="b_minus+${stag(k, 1.4, 1.0)}" data-anim="pop">${l}</span>`).join('')}
    </div>
  </div>`;
  return {};
});

/* ===================== DÉPLOIEMENT ET CONCLUSION ===================== */
registerScene('deploy', (root) => {
  root.innerHTML = `
  <div class="phase" data-out="y_plan-0.2">
    <div class="h2">Quel agent en premier ?</div>
    <div class="row" style="gap:0;margin-top:50px;justify-content:space-between;align-items:stretch">
      ${[['1', 'Préparation d’un rendez-vous', 'sur 3 briefs', 'y_first@1', 'agent'], ['2', 'Compte rendu et tâches', 'si briefs utiles et accès maîtrisés', 'y_order+1.8', 'slate'], ['3', 'Contrôles documentaires', 'ensuite seulement', 'y_order+5.4', 'slate'], ['4', 'Relation client et cockpit', 'en dernier', 'y_order+7.2', 'slate']].map(([n, a, b, t, c], k) => `${k ? `<div style="align-self:center" data-in="${t}" data-anim="fade">${ic('arrow', 'var(--navy2)', 44)}</div>` : ''}
        <div class="card col" style="width:370px;gap:10px;${k === 0 ? 'border:3px solid var(--agent)' : ''}" data-in="${t}" data-anim="pop">
          <div style="font-size:56px;font-weight:800;color:${k === 0 ? 'var(--agent)' : 'var(--muted)'}">${n}</div><div class="h3">${a}</div><span class="chip ${c}" style="align-self:flex-start;white-space:normal">${b}</span></div>`).join('')}
    </div>
    <div class="row" style="gap:16px;margin-top:40px" data-in="y_first@1+4.2">
      ${['Périmètre étroit', 'Compréhensible par Sophie', 'Mesurable'].map(l => `<span class="chip human" style="font-size:24px;padding:10px 20px">${ic('check', 'var(--human)', 22)} ${l}</span>`).join('')}
    </div>
  </div>

  <div class="phase" data-in="y_plan" data-out="y_goal-0.2" data-anim="fade">
    <div class="row" style="justify-content:space-between"><div class="h2">Planning de mission</div><span class="chip amber" style="font-size:24px">planning proposé</span></div>
    <div class="row" style="gap:18px;margin-top:40px;align-items:stretch">
      ${[['Semaines 1 et 2', ['Diagnostic réel', 'Chronométrage', 'Cartographie des données', 'Choix d’un seul cas d’usage'], 'y_w12', 2],
        ['Semaines 3 à 5', ['Premier workflow construit', 'Test sur données fictives', 'Puis périmètre autorisé', '3 briefs relus par Sophie'], 'y_w35', 3],
        ['Semaines 6 à 8', ['Étendre, ajuster ou arrêter', 'Autres agents : seulement si résultats vérifiables', 'et accès approuvés'], 'y_w68', 3]].map(([h, items, t, f]) => `
      <div class="card col" style="flex:${f};gap:12px" data-in="${t}" data-anim="up">
        <div class="h3">${h}</div><div style="height:8px;border-radius:4px;background:var(--navy2)"></div>
        ${items.map((it, k) => `<div class="row t" style="gap:12px" data-in="${t}+${stag(k, 1.0, 1.3)}">${ic('check', 'var(--human)', 24)} ${it}</div>`).join('')}
      </div>`).join('')}
    </div>
    <div class="row" style="justify-content:center;margin-top:34px" data-in="y_not3" data-anim="pop">
      <span class="chip red" style="font-size:26px;padding:12px 26px">8 semaines ≠ 3 agents achevés dans tous les cabinets</span>
    </div>
  </div>

  <div class="phase" data-in="y_goal" data-out="y_cta-0.2" data-anim="fade">
    ${[['CRM', 60, 60], ['Messagerie', 420, 30], ['Documents', 140, 300], ['Notes', 520, 330], ['Tâches', 260, 520]].map(([l, x, y], k) => `
      <div class="win abs" style="left:${x}px;top:${y}px;width:380px;height:220px" data-out="y_goal+${stag(k, 0.8, 0.35)}" data-outdur="0.3"><div class="bar"><i></i><i></i><i></i><span class="ttl">${l}</span></div></div>`).join('')}
    <div class="card abs" style="left:420px;top:40px;width:900px;padding:30px 36px" data-in="y_goal+3.0" data-anim="pop">
      <div class="row" style="justify-content:space-between"><div class="h3">Brief : rendez-vous de suivi</div><span class="chip human">validé par Sophie</span></div>
      <div class="col" style="gap:10px;margin-top:16px">
        ${[['Contexte retrouvé', 'S1 S2 S3'], ['Manques visibles', 'S4'], ['Questions relues par le CGP', 'brief v2']].map(([a, b]) => `<div class="row t" style="gap:12px">${ic('check', 'var(--human)', 24)} ${a}<span class="src">${b}</span></div>`).join('')}
      </div>
    </div>
    <div class="row abs" style="left:0;width:1740px;top:430px;justify-content:center;gap:30px" data-in="y_goal@1">
      ${[['Retrouve le contexte', 'search'], ['Voit les manques', 'eye'], ['Décide', 'user']].map(([l, i], k) => `<div class="card row" style="gap:16px;padding:22px 30px" data-in="y_goal@1+${stag(k, 1.2, 1.6)}" data-anim="up">${ic(i, 'var(--human)', 36)}<span class="h3">${l}</span></div>`).join('')}
    </div>
    <div class="abs" style="left:0;width:1740px;top:600px;text-align:center" data-in="y_goal+0.6"><span class="chip slate strike" style="font-size:24px;padding:10px 22px" data-var="y_goal+1.8:0.5:p:0:1">L'IA parle à la place du conseiller</span></div>
  </div>

  <div class="phase" data-in="y_cta" data-out="y_end-0.3" data-anim="fade">
    <div class="col" style="align-items:center;margin-top:50px;gap:30px">
      <div class="kicker">Vous dirigez un cabinet de gestion de patrimoine ?</div>
      <div class="h1" style="text-align:center" data-in="y_cta+2.5">Montrez-nous un dossier<br>et une semaine réelle.</div>
      <div class="row" style="gap:24px;margin-top:30px">
        ${['Ce qui mérite d’être préparé', 'Ce qui doit rester humain', 'Ce qu’un pilote peut mesurer'].map((l, k) => `<div class="card" style="width:460px;text-align:center" data-in="y_cta2+${stag(k, 0.6, 1.6)}" data-anim="up"><div class="h3">${l}</div></div>`).join('')}
      </div>
    </div>
  </div>

  <div class="abs" style="inset:0;background:var(--navy);z-index:30" data-in="y_end-0.2" data-anim="fade" data-dur="0.6">
    <div class="abs" style="left:160px;top:300px;width:1600px">
      <div style="font-size:40px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--gold)" data-in="y_end">Agentic Wealth</div>
      <div style="font-size:80px;font-weight:800;color:#fff;margin-top:26px;letter-spacing:-.02em;line-height:1.1" data-in="y_end@1">L'agent prépare.<br><span data-in="y_end@2" style="color:#8FD6B8">Le CGP valide et décide.</span></div>
      <div style="font-size:22px;color:#93A3B8;margin-top:60px;line-height:1.6" data-in="y_end@2+0.8">Simulation pédagogique : cabinet, personnes, dossiers et chiffres fictifs. Gains présentés comme hypothèses.<br>Voix de synthèse locale : Piper, voix « siwis » (jeu de données SIWIS, licence CC BY 4.0).</div>
    </div>
  </div>`;
  return { chromeUntil: 'y_end' };
});

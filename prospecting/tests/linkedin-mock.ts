import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import type { AddressInfo } from "node:net";

/**
 * A small stand-in for linkedin.com, close enough to its markup and accessible labels
 * (French UI) to exercise the browser provider end to end. Not a copy of LinkedIn:
 * just the structures the provider relies on, plus the traps it must avoid.
 */
export type ProfileState = "connectable" | "connect-in-more" | "pending" | "connected" | "no-connect" | "limit" | "email";

export type MockProfile = { slug: string; name: string; headline: string; location: string; state: ProfileState };

export type MockState = {
  cookie: string;
  own: MockProfile;
  profiles: Map<string, MockProfile>;
  invitations: { slug: string; note: string | null }[];
  messages: { slug: string; text: string }[];
  connections: string[];
  threads: Map<string, { participant: string; events: { from: string; text: string }[] }>;
  searches: string[];
  visitors: string[];
  reactions: string[];
};

const esc = (s: string) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]!);

function page(title: string, main: string, extra = "") {
  return `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>${esc(title)}</title></head>
<body><header><nav><a href="/feed/">Accueil</a><a href="/messaging/">Messagerie</a></nav></header>
<main>${main}</main><aside><h2>Autres profils consultés</h2><ul><li><a href="/in/aside-person/">Aside Person</a><button aria-label="Invitez Aside Person à rejoindre votre réseau">Se connecter</button></li></ul></aside>${extra}</body></html>`;
}

function profileActions(p: MockProfile): string {
  const first = p.name.split(" ")[0];
  const invite = `aria-label="Invitez ${esc(p.name)} à rejoindre votre réseau"`;
  const more = (items: string) => `<button aria-label="Plus d’actions" onclick="document.getElementById('more-menu').hidden=false">Plus</button>
    <div id="more-menu" hidden>${items}<div role="button" tabindex="0">Enregistrer en PDF</div></div>`;
  switch (p.state) {
    case "pending":
      return `<button aria-label="En attente, cliquez pour retirer l’invitation envoyée à ${esc(p.name)}">En attente</button>${more("")}`;
    case "connected":
      return `<span>· 1er</span><button aria-label="Envoyer un message à ${esc(p.name)}" onclick="openComposer()">Message</button>${more("")}`;
    case "connect-in-more":
      return `<button>Suivre</button>${more(`<div role="button" tabindex="0" ${invite} onclick="openInvite()">Se connecter</div>`)}`;
    case "no-connect":
      return `<button>Suivre</button>${more("")}`;
    default:
      return `<button ${invite} onclick="openInvite()">Se connecter</button>
        <button aria-label="Envoyer un message à ${esc(first ?? "")}" onclick="openComposer()">Message</button>${more("")}`;
  }
}

const SCRIPT = (p: MockProfile) => `<script>
const slug = ${JSON.stringify(p.slug)};
const state = ${JSON.stringify(p.state)};
function closeDialog(){ document.querySelectorAll('[role=dialog]').forEach(d => d.remove()); }
function dialog(html){ closeDialog(); const d=document.createElement('div'); d.setAttribute('role','dialog'); d.setAttribute('aria-modal','true'); d.innerHTML=html; document.body.appendChild(d); return d; }
document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeDialog(); const m=document.getElementById('more-menu'); if (m) m.hidden = true; } });
async function invite(note){
  const r = await fetch('/__mock/invite', { method:'POST', body: JSON.stringify({ slug, note }) });
  closeDialog();
  if (r.status === 429) { dialog('<p>Vous avez atteint la limite hebdomadaire d’invitations.</p><button onclick="closeDialog()">OK</button>'); return; }
  document.querySelector('main section button, main section [role=button]').outerHTML = '<button aria-label="En attente, cliquez pour retirer l’invitation">En attente</button>';
}
function openInvite(){
  document.getElementById('more-menu').hidden = true;
  if (state === 'limit') { dialog('<h2>Vous avez atteint la limite hebdomadaire d’invitations</h2><button onclick="closeDialog()">Compris</button>'); return; }
  if (state === 'email') { dialog('<p>Pour vérifier que vous connaissez ce membre, saisissez son adresse e-mail pour vous connecter.</p><input type="email"><button>Envoyer</button>'); return; }
  const d = dialog('<h2>Ajouter une note à votre invitation ?</h2><button id="add">Ajouter une note</button><button id="plain">Envoyer sans note</button>');
  d.querySelector('#plain').onclick = () => invite(null);
  d.querySelector('#add').onclick = () => {
    d.innerHTML = '<label for="custom-message">Note</label><textarea id="custom-message" name="message"></textarea><button id="send" aria-label="Envoyer l’invitation" disabled>Envoyer</button>';
    const t = d.querySelector('textarea'), s = d.querySelector('#send');
    t.oninput = () => { s.disabled = !t.value.trim(); };
    s.onclick = () => invite(t.value);
  };
}
function openComposer(){
  const o = document.createElement('div');
  o.className = 'msg-overlay';
  o.innerHTML = '<form><div role="textbox" contenteditable="true" aria-label="Rédiger un message"></div><button type="submit">Envoyer</button></form><button type="button" aria-label="Fermer votre conversation">×</button>';
  o.querySelector('form').onsubmit = async (e) => {
    e.preventDefault();
    const box = o.querySelector('[role=textbox]');
    await fetch('/__mock/message', { method:'POST', body: JSON.stringify({ slug, text: box.innerText }) });
    box.innerHTML = '';
  };
  o.querySelector('[aria-label="Fermer votre conversation"]').onclick = () => o.remove();
  document.body.appendChild(o);
}
</script>`;

function personItem(p: MockProfile, mutual?: MockProfile): string {
  return `<li class="result"><div><a href="/in/${encodeURIComponent(p.slug)}/?miniProfileUrn=x"><span aria-hidden="true">${esc(p.name)}</span><span class="visually-hidden">Voir le profil de ${esc(p.name)}</span></a>
    <span>• 2e</span></div><div>${esc(p.headline)}</div><div>${esc(p.location)}</div>
    ${mutual ? `<p><a href="/in/${encodeURIComponent(mutual.slug)}/">${esc(mutual.name)}</a> est une relation en commun</p>` : ""}
    <button aria-label="Invitez ${esc(p.name)} à rejoindre votre réseau">Se connecter</button></li>`;
}

export async function startMockLinkedIn() {
  const own: MockProfile = { slug: "alex-martin", name: "Alex Martin", headline: "Fondateur chez Clarity", location: "Paris", state: "connected" };
  const state: MockState = {
    cookie: "valid-session-cookie-0123456789",
    own,
    profiles: new Map(),
    invitations: [],
    messages: [],
    connections: [],
    threads: new Map(),
    searches: [],
    visitors: [],
    reactions: [],
  };
  const add = (p: MockProfile) => state.profiles.set(p.slug, p);
  add(own);
  for (let i = 1; i <= 23; i++) add({ slug: `prospect-${i}`, name: `Camille Durand${i}`, headline: `CFO chez Nova ${i} | SaaS`, location: "Paris", state: "connectable" });
  add({ slug: "in-more", name: "Paul Roux", headline: "DAF chez Atlas", location: "Lyon", state: "connect-in-more" });
  add({ slug: "already-pending", name: "Inès Blanc", headline: "CFO chez Orion", location: "Lille", state: "pending" });
  add({ slug: "already-friend", name: "Hugo Morel", headline: "CEO chez Helio", location: "Nantes", state: "connected" });
  add({ slug: "follow-only", name: "Léa Faure", headline: "Influenceuse", location: "Paris", state: "no-connect" });
  add({ slug: "limit-person", name: "Nora Haddad", headline: "CFO chez Kairos", location: "Paris", state: "limit" });
  add({ slug: "email-person", name: "Victor Girard", headline: "CFO chez Pragma", location: "Paris", state: "email" });
  add({ slug: "mutual-friend", name: "Mutual Friend", headline: "Ami", location: "Paris", state: "connected" });
  state.visitors = ["prospect-21", "prospect-22"];
  state.reactions = ["prospect-23", "in-more"];

  const results = () => [...state.profiles.values()].filter((p) => p.slug.startsWith("prospect-"));

  const server = createServer(async (req: IncomingMessage, res: ServerResponse) => {
    const url = new URL(req.url ?? "/", "http://mock");
    const send = (status: number, html: string, headers: Record<string, string> = {}) => {
      res.writeHead(status, { "content-type": "text/html; charset=utf-8", ...headers });
      res.end(html);
    };
    const authed = (req.headers.cookie ?? "").split(/;\s*/).includes(`li_at=${state.cookie}`);
    if (url.pathname.startsWith("/__mock/")) {
      let body = "";
      for await (const chunk of req) body += chunk;
      const data = JSON.parse(body || "{}") as { slug: string; note?: string | null; text?: string };
      if (url.pathname === "/__mock/invite") {
        if (state.invitations.length >= 1000) return send(429, "");
        state.invitations.push({ slug: data.slug, note: data.note ?? null });
        state.profiles.get(data.slug)!.state = "pending";
      } else if (url.pathname === "/__mock/accept") {
        // Test control: the prospect accepts.
        state.connections.unshift(data.slug);
        state.profiles.get(data.slug)!.state = "connected";
      } else if (url.pathname === "/__mock/reply") {
        // Test control: the prospect writes.
        const id = `thread-${data.slug}`;
        const thread = state.threads.get(id) ?? { participant: data.slug, events: [] };
        thread.events.push({ from: data.slug, text: data.text ?? "" });
        state.threads.set(id, thread);
      } else if (url.pathname === "/__mock/state") {
        res.writeHead(200, { "content-type": "application/json" });
        return res.end(JSON.stringify({ invitations: state.invitations, messages: state.messages }));
      } else if (url.pathname === "/__mock/message") {
        state.messages.push({ slug: data.slug, text: data.text ?? "" });
        const id = `thread-${data.slug}`;
        const thread = state.threads.get(id) ?? { participant: data.slug, events: [] };
        thread.events.push({ from: own.slug, text: data.text ?? "" });
        state.threads.set(id, thread);
      }
      return send(200, "ok");
    }
    if (url.pathname === "/login" || url.pathname.startsWith("/uas/")) return send(200, page("Connexion", "<h1>S’identifier</h1>"));
    if (!authed) return send(302, "", { location: `/login?session_redirect=${encodeURIComponent(url.pathname)}` });

    if (url.pathname === "/feed/") return send(200, page("Fil", "<h2>Fil d’actualité</h2>"));
    if (url.pathname === "/in/me/") return send(302, "", { location: `/in/${own.slug}/` });
    const profileMatch = /^\/in\/([^/]+)\/?$/.exec(url.pathname);
    if (profileMatch) {
      const p = state.profiles.get(decodeURIComponent(profileMatch[1]!));
      if (!p) return send(404, page("Introuvable", "<h2>Cette page n’existe pas</h2>"));
      const others = `<section><h2>Personnes que vous pourriez connaître</h2><ul><li><a href="/in/someone-else/">Someone Else</a><button aria-label="Invitez Someone Else à rejoindre votre réseau">Se connecter</button></li></ul></section>`;
      return send(200, page(p.name, `<section class="top-card"><h1>${esc(p.name)}</h1><div class="text-body-medium">${esc(p.headline)}</div><span class="text-body-small inline">${esc(p.location)}</span><div>${p.slug === own.slug ? "" : profileActions(p)}</div></section>${others}`, SCRIPT(p)));
    }
    if (url.pathname === "/search/results/people/") {
      state.searches.push(url.search);
      const pageNumber = Number(url.searchParams.get("page") ?? "1");
      const slice = results().slice((pageNumber - 1) * 10, pageNumber * 10);
      const mutual = state.profiles.get("mutual-friend");
      const list = slice.length ? `<ul>${slice.map((p, i) => personItem(p, i === 0 ? mutual : undefined)).join("")}</ul>` : "<h2>Aucun résultat</h2>";
      return send(200, page("Recherche", list));
    }
    if (url.pathname === "/mynetwork/invite-connect/connections/") {
      const items = state.connections.map((s) => state.profiles.get(s)!).map((p) => `<li><a href="/in/${p.slug}/">${esc(p.name)}</a><p>${esc(p.headline)}</p><button aria-label="Envoyer un message à ${esc(p.name)}">Message</button></li>`);
      return send(200, page("Relations", `<h1>${items.length} relations</h1><ul>${items.join("")}</ul>`));
    }
    if (url.pathname === "/me/profile-views/") {
      return send(200, page("Vues", `<ul>${state.visitors.map((s) => personItem(state.profiles.get(s)!)).join("")}</ul>`));
    }
    if (url.pathname.startsWith("/feed/update/")) {
      const people = state.reactions.map((s) => state.profiles.get(s)!);
      return send(200, page("Post", `<article><p>Un post</p><button onclick="document.getElementById('reactions').hidden=false">${people.length} réactions</button></article>`,
        `<div id="reactions" role="dialog" hidden><ul>${people.map((p) => personItem(p)).join("")}</ul></div>`));
    }
    if (url.pathname === "/messaging/") {
      const items = [...state.threads.entries()].map(([id, t]) => {
        const p = state.profiles.get(t.participant)!;
        const last = t.events.at(-1);
        return `<li><a href="/messaging/thread/${id}/">${esc(p.name)}</a><p>${last?.from === own.slug ? "Vous : " : ""}${esc(last?.text ?? "")}</p></li>`;
      });
      return send(200, page("Messagerie", `<ul>${items.join("")}</ul>`));
    }
    const threadMatch = /^\/messaging\/thread\/([^/]+)\/?$/.exec(url.pathname);
    if (threadMatch) {
      const t = state.threads.get(threadMatch[1]!);
      if (!t) return send(404, page("Introuvable", "<h2>Cette page n’existe pas</h2>"));
      const p = state.profiles.get(t.participant)!;
      let previous = "";
      const events = t.events.map((e) => {
        const author = state.profiles.get(e.from)!;
        const header = e.from !== previous ? `<a href="/in/${author.slug}/" class="msg-s-message-group__profile-link">${esc(author.name)}</a>` : "";
        previous = e.from;
        return `<li class="msg-s-message-list__event">${header}<p class="msg-s-event-listitem__body">${esc(e.text)}</p></li>`;
      });
      return send(200, page("Conversation", `<div class="msg-thread"><h2><a href="/in/${p.slug}/">${esc(p.name)}</a></h2><ul>${events.join("")}</ul></div>`));
    }
    send(404, page("Introuvable", "<h2>Cette page n’existe pas</h2>"));
  });

  await new Promise<void>((resolve) => server.listen(0, "127.0.0.1", resolve));
  const { port } = server.address() as AddressInfo;
  return {
    url: `http://127.0.0.1:${port}`,
    state,
    /** The prospect accepts the invitation. */
    accept(slug: string) {
      state.connections.unshift(slug);
      state.profiles.get(slug)!.state = "connected";
    },
    /** The prospect writes in the thread. */
    reply(slug: string, text: string) {
      const id = `thread-${slug}`;
      const thread = state.threads.get(id) ?? { participant: slug, events: [] };
      thread.events.push({ from: slug, text });
      state.threads.set(id, thread);
    },
    close: () => new Promise<void>((resolve) => server.close(() => resolve())),
  };
}

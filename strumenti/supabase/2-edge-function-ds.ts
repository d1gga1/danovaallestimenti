// DANOVA — Edge Function "ds" su Supabase (stessa struttura della funzione "pd" di Pan.door.a).
// Un solo database e una sola dashboard per più siti: Danova Stand, Danova Costruzioni, Danova Tech.
// Ogni sito manda il suo nome ("si") con ogni segnale; la dashboard sceglie il sito con ?sito=.
//   /functions/v1/ds/s         → statistiche visite (riceve i segnali di /assets/js/ds-live.js)
//   /functions/v1/ds/richiesta → copia nel database delle richieste inviate dai moduli del sito
//                                (l'email a info@danova-tech.com continua ad arrivare da FormSubmit come prima)
//   /functions/v1/ds/admin     → dashboard danovastand.com/private_area/: live, storico, persone, richieste
//
// Segreti da impostare in Supabase (Edge Functions → Secrets):
//   ADMIN_PASSWORD  password per entrare in danovastand.com/private_area/
//   DS_SEGRETO      una frase lunga a caso (non cambiarla dopo l'avvio)
//   IPINFO_TOKEN    facoltativo: posizione dei visitatori più precisa (ipinfo.io, piano gratuito)
// SUPABASE_DB_URL è già fornito da Supabase.

import postgres from "npm:postgres@3.4.4";

/* ======================= impostazioni ======================= */
/* i siti collegati: nome breve → dominio */
const SITI: Record<string, string> = { stand: "danovastand.com", costruzioni: "danovacostruzioni.it", tech: "danova-tech.com" };
function sitoDi(x: unknown, req?: Request) {
  const s = String(x ?? "");
  if (SITI[s]) return s;
  try { // ripiego: dal dominio della pagina che manda il segnale
    const h = new URL(req?.headers.get("origin") || req?.headers.get("referer") || "").hostname.replace(/^www\./, "");
    for (const [k, d] of Object.entries(SITI)) if (h === d) return k;
  } catch { /* */ }
  return "stand";
}
const CFG = {
  origini: (Deno.env.get("DS_ORIGINI") || "https://danovastand.com,https://www.danovastand.com,https://danovacostruzioni.it,https://www.danovacostruzioni.it,https://danova-tech.com,https://www.danova-tech.com").split(",").map((s) => s.trim()),
  contatto: "info@danova-tech.com",
  segreto: Deno.env.get("DS_SEGRETO") || "",
  admin_password: Deno.env.get("ADMIN_PASSWORD") || "",
  admin_ore: 12,
  live_secondi: 45,
  conserva_mesi: 25,
};

/* ======================= database ======================= */
const sql = postgres(Deno.env.get("SUPABASE_DB_URL")!, {
  prepare: false,
  max: 3,
  idle_timeout: 20,
  types: {
    int8: { to: 20, from: [20], serialize: (x: unknown) => String(x), parse: (x: string) => Number(x) },
    num: { to: 1700, from: [1700], serialize: (x: unknown) => String(x), parse: (x: string) => Number(x) },
  },
});
// le query sono scritte con "?" come nei PHP originali: le convertiamo in $1, $2…
function pg(q: string) { let i = 0; return q.replace(/\?/g, () => "$" + (++i)); }
// deno-lint-ignore no-explicit-any
type Row = Record<string, any>;
async function righe(q: string, p: unknown[] = []): Promise<Row[]> { return await sql.unsafe(pg(q), p as never[]) as unknown as Row[]; }
async function riga(q: string, p: unknown[] = []): Promise<Row | null> { const r = await righe(q, p); return r[0] || null; }
async function val(q: string, p: unknown[] = []) { const r = await righe(q, p); if (!r[0]) return null; return Object.values(r[0])[0]; }
async function esegui(q: string, p: unknown[] = []) { const r = await sql.unsafe(pg(q), p as never[]); return r.count; }

/* ======================= utilità ======================= */
class Risposta { constructor(public dati: unknown, public codice = 200, public extra: Record<string, string> = {}) {} }
const json = (d: unknown, c = 200): never => { throw new Risposta(d, c); };
const errore = (msg: string, c = 400, campo = ""): never => json({ ok: false, errore: msg, campo }, c);
const ora = () => Math.floor(Date.now() / 1000);
function t(s: unknown, max = 200) {
  const x = String(s ?? "").replace(/[\x00-\x1F\x7F]+/g, " ").trim();
  return Array.from(x).slice(0, max).join("");
}
function h(s: unknown) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));
}
const email_ok = (e: string) => e.length <= 190 && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(e);
const pw_ok = (p: unknown) => typeof p === "string" && p.length >= 8 && p.length <= 200;
const isNum = (x: unknown) => x !== null && x !== "" && !isNaN(Number(x));
const num = (x: unknown) => isNum(x) ? Math.round(Number(x) * 100) / 100 : 0;
const hex = (b: ArrayBuffer) => Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
async function sha256(s: string) { return hex(await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s))); }
async function hmac(chiave: string, s: string) {
  const k = await crypto.subtle.importKey("raw", new TextEncoder().encode(chiave), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", k, new TextEncoder().encode(s)));
}
function token_nuovo() { const a = new Uint8Array(32); crypto.getRandomValues(a); return hex(a.buffer); }
function uguali(a: string, b: string) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }

/* date nel fuso di Roma */
function roma(ts: number) {
  const f = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Rome", year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit", weekday: "short", hourCycle: "h23" });
  const p: Record<string, string> = {};
  for (const x of f.formatToParts(new Date(ts * 1000))) p[x.type] = x.value;
  return p;
}
const giornoDi = (ts: number) => { const p = roma(ts); return `${p.year}-${p.month}-${p.day}`; };
const oraDi = (ts: number) => Number(roma(ts).hour);
const dowDi = (ts: number) => ({ Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 } as Record<string, number>)[roma(ts).weekday];
const dataOra = (ts: number) => { const p = roma(ts); return `${p.day}/${p.month}/${p.year} ${p.hour}:${p.minute}`; };
const hhmm = (ts: number) => { const p = roma(ts); return `${p.hour}:${p.minute}`; };
const hhmmss = (ts: number) => { const p = roma(ts); return `${p.hour}:${p.minute}:${p.second}`; };
/* mezzanotte di Roma di un giorno "AAAA-MM-GG", in secondi */
function mezzanotte(g: string) {
  const [y, m, d] = g.split("-").map(Number);
  const u = Date.UTC(y, m - 1, d) / 1000;
  const p = roma(u);
  const off = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second) / 1000 - u;
  return u - off;
}
function piuGiorni(g: string, n: number) {
  const [y, m, d] = g.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d + n)).toISOString().slice(0, 10);
}
const diffGiorni = (a: string, b: string) => Math.round((Date.parse(b + "T00:00:00Z") - Date.parse(a + "T00:00:00Z")) / 86400000);

function ipDi(req: Request) {
  const x = req.headers.get("x-forwarded-for") || req.headers.get("x-real-ip") || "";
  return x.split(",")[0].trim();
}

/* massimo `max` azioni dello stesso tipo in `sec` secondi */
async function limite(tipo: string, chiave: string | number, max: number, sec: number) {
  const k = await sha256(tipo + "|" + chiave);
  if (Math.random() < 0.02) await esegui("DELETE FROM limiti_c WHERE ts < ?", [ora() - 86400]);
  const n = Number(await val("SELECT COUNT(*) FROM limiti_c WHERE k = ? AND ts > ?", [k, ora() - sec]));
  if (n >= max) return false;
  await esegui("INSERT INTO limiti_c (k, ts) VALUES (?, ?)", [k, ora()]);
  return true;
}

/* come limite(), ma conta senza registrare: il tentativo si registra con limite_segna() solo quando va a buon fine,
   così chi sbaglia qualche campo non resta bloccato */
async function limite_ok(tipo: string, chiave: string | number, max: number, sec: number) {
  if (String(chiave) === "") return true;
  const k = await sha256(tipo + "|" + chiave);
  return Number(await val("SELECT COUNT(*) FROM limiti_c WHERE k = ? AND ts > ?", [k, ora() - sec])) < max;
}
async function limite_segna(tipo: string, chiave: string | number) {
  if (String(chiave) === "") return;
  await esegui("INSERT INTO limiti_c (k, ts) VALUES (?, ?)", [await sha256(tipo + "|" + chiave), ora()]);
}
/* lavoro lento (email) dopo aver già risposto al cliente */
function in_background(p: Promise<unknown>) {
  const q = p.catch((e) => console.error("background: " + ((e as Error)?.message || e)));
  const er = (globalThis as unknown as { EdgeRuntime?: { waitUntil?: (x: Promise<unknown>) => void } }).EdgeRuntime;
  if (er && typeof er.waitUntil === "function") { er.waitUntil(q); return Promise.resolve(); }
  return q;
}
/* il CAP è obbligatorio per l'Italia; per i Paesi senza codice postale (es. Emirati) è facoltativo */
async function identifica(pdv: unknown, d: { email?: string; nome?: string; telefono?: string; cliente_id?: number | null; fonte: string }) {
  try {
    if (!/^[a-z0-9]{12,40}$/.test(String(pdv ?? "")) || (!d.email && !d.telefono)) return;
    const vid = await anonimo("v" + pdv), adesso = ora();
    await esegui(`INSERT INTO visitatori (id, primo, ultimo, sessioni, email, nome, telefono, cliente_id, fonte, identificato) VALUES (?,?,?,0,?,?,?,?,?,?)
      ON CONFLICT (id) DO UPDATE SET email = COALESCE(NULLIF(EXCLUDED.email, ''), visitatori.email), nome = COALESCE(NULLIF(EXCLUDED.nome, ''), visitatori.nome),
        telefono = COALESCE(NULLIF(EXCLUDED.telefono, ''), visitatori.telefono), cliente_id = COALESCE(EXCLUDED.cliente_id, visitatori.cliente_id),
        fonte = COALESCE(visitatori.fonte, EXCLUDED.fonte), identificato = COALESCE(visitatori.identificato, EXCLUDED.identificato)`,
      [vid, adesso, adesso, t(d.email, 190).toLowerCase() || null, t(d.nome, 160), t(d.telefono, 40), d.cliente_id ?? null, d.fonte, adesso]);
    await esegui("UPDATE sessioni SET visitatore_noto = 1 WHERE visitatore = ?", [vid]);
  } catch (e) { console.error("identifica: " + (e as Error).message); }
}

const rif_ok = (x: unknown) => { const r = String(x ?? "").toUpperCase().replace(/[^A-Z0-9]/g, ""); return /^[A-Z0-9]{4,8}$/.test(r) ? r : ""; };

function e_robot(ua: string) {
  return ua === "" || /bot|crawl|spider|slurp|headless|lighthouse|pagespeed|preview|phantom|selenium|puppeteer|playwright|python|curl|wget|httpclient|monitor|uptime|facebookexternalhit|bingpreview|gtmetrix/i.test(ua);
}
function dispositivo(ua: string, w: number): [string, string, string] {
  let d: string, b: string, o: string;
  if (/iPad|Tablet|PlayBook|Silk|(Android(?!.*Mobile))/i.test(ua)) d = "Tablet";
  else if (/Mobi|iPhone|iPod|Android.*Mobile|Windows Phone|Opera Mini/i.test(ua)) d = "Mobile";
  else d = (w > 0 && w < 768) ? "Mobile" : "Desktop";
  if (/Edg\//.test(ua)) b = "Edge"; else if (/OPR\/|Opera/.test(ua)) b = "Opera"; else if (/SamsungBrowser/.test(ua)) b = "Samsung Internet";
  else if (/Firefox|FxiOS/.test(ua)) b = "Firefox"; else if (/Chrome|CriOS/.test(ua)) b = "Chrome"; else if (/Safari/.test(ua)) b = "Safari"; else b = "Altro";
  if (/iPhone|iPad|iPod/.test(ua)) o = "iOS"; else if (/Android/.test(ua)) o = "Android"; else if (/Windows/.test(ua)) o = "Windows";
  else if (/Mac OS X|Macintosh/.test(ua)) o = "macOS"; else if (/CrOS/.test(ua)) o = "ChromeOS"; else if (/Linux/.test(ua)) o = "Linux"; else o = "Altro";
  return [d, b, o];
}
const ucfirst = (s: string) => s.charAt(0).toUpperCase() + s.slice(1);
function provenienza(ref: string, utm: Row): [string, string, string] {
  let host = "";
  try { host = ref ? new URL(ref).hostname.toLowerCase() : ""; } catch { host = ""; }
  host = host.replace(/^(www\.|m\.|l\.|lm\.)/, "");
  const src = String(utm.s || "").toLowerCase(), med = String(utm.m || "").toLowerCase();
  if (utm.g) return ["Pubblicità", "Google Ads", host];
  if (utm.f) return ["Social", "Facebook / Instagram", host];
  if (med && /cpc|ppc|paid|ads/.test(med)) return ["Pubblicità", src ? ucfirst(src) : "Annunci", host];
  if (med === "email" || src === "newsletter") return ["Email", src ? ucfirst(src) : "Email", host];
  const mappa: Record<string, Record<string, string>> = {
    Ricerca: { "google.": "Google", "bing.": "Bing", "duckduckgo.": "DuckDuckGo", "yahoo.": "Yahoo", "ecosia.": "Ecosia", "yandex.": "Yandex", "baidu.": "Baidu",
      "qwant.": "Qwant", "seznam.": "Seznam", "naver.": "Naver", "brave.": "Brave Search", "startpage.": "Startpage" },
    AI: { "chatgpt.": "ChatGPT", "openai.": "ChatGPT", "perplexity.": "Perplexity", "claude.ai": "Claude", "gemini.google": "Gemini", "copilot.": "Copilot",
      "you.com": "You.com", "deepseek.": "DeepSeek", "mistral.ai": "Mistral", "grok.": "Grok", "meta.ai": "Meta AI" },
    Social: { "facebook.": "Facebook", "fb.": "Facebook", "instagram.": "Instagram", "linkedin.": "LinkedIn", "lnkd.in": "LinkedIn", "t.co": "X / Twitter",
      "twitter.": "X / Twitter", "x.com": "X / Twitter", "youtube.": "YouTube", "tiktok.": "TikTok", "pinterest.": "Pinterest", "reddit.": "Reddit",
      "whatsapp.": "WhatsApp", "telegram.": "Telegram", "threads.": "Threads" },
  };
  const rt = (k: string) => k.replace(/\.$/, "");
  if (src) for (const [c, m] of Object.entries(mappa)) for (const [k, n] of Object.entries(m)) if (src.includes(rt(k))) return [c, n, host];
  if (host === "") return src ? ["Campagne", ucfirst(src), ""] : ["Diretto", "Diretto", ""];
  for (const [c, m] of Object.entries(mappa)) for (const [k, n] of Object.entries(m)) {
    if (host.startsWith(k) || host.includes("." + k) || host === rt(k)) return [c, n, host];
  }
  if (/mail\.|outlook\.|webmail/.test(host)) return ["Email", host, host];
  return ["Altri siti", host, host];
}
const anonimo = (id: string) => hmac(CFG.segreto || "ds", id).then((x) => x.slice(0, 32));
const NOMI_PAESI = new Intl.DisplayNames(["it"], { type: "region" });

/* posizione approssimata dall'IP: più servizi in cascata, si tiene il risultato più preciso (città + CAP).
   L'IP non viene salvato: solo città, CAP, regione, paese, coordinate e provider. */
const geoCache = new Map<string, { t: number; g: Row }>();
const GEO_VUOTO: Row = { cc: "", paese: "", regione: "", citta: "", cap: "", lat: null, lon: null, isp: "", fonte: "" };
const numGeo = (x: unknown) => { const n = parseFloat(String(x ?? "")); return isFinite(n) && n !== 0 ? Math.round(n * 10000) / 10000 : null; };
type FonteGeo = { nome: string; url: (ip: string) => string; leggi: (d: any) => Row | null };
const IPINFO_TOKEN = Deno.env.get("IPINFO_TOKEN") || "";
const FONTI_GEO: FonteGeo[] = [
  ...(IPINFO_TOKEN ? [{ nome: "ipinfo", url: (ip: string) => `https://ipinfo.io/${ip}/json?token=${IPINFO_TOKEN}`,
    leggi: (d: any) => { if (!d || d.bogon || !d.country) return null; const [la, lo] = String(d.loc || "").split(",");
      return { cc: d.country, regione: d.region, citta: d.city, cap: d.postal, lat: numGeo(la), lon: numGeo(lo), isp: String(d.org || "").replace(/^AS\d+\s+/, "") }; } }] : []),
  { nome: "geojs", url: (ip) => `https://get.geojs.io/v1/ip/geo/${ip}.json`,
    leggi: (d) => d && d.country_code ? { cc: d.country_code, regione: d.region, citta: d.city, cap: "", lat: numGeo(d.latitude), lon: numGeo(d.longitude), isp: d.organization_name || d.organization } : null },
  { nome: "ipwho", url: (ip) => `https://ipwho.is/${ip}?lang=it`,
    leggi: (d) => d && d.success !== false && d.country_code ? { cc: d.country_code, regione: d.region, citta: d.city, cap: d.postal, lat: numGeo(d.latitude), lon: numGeo(d.longitude), isp: d.connection?.isp || d.connection?.org } : null },
  { nome: "freeipapi", url: (ip) => `https://freeipapi.com/api/json/${ip}`,
    leggi: (d) => d && d.countryCode && d.countryCode !== "-" ? { cc: d.countryCode, regione: d.regionName, citta: d.cityName, cap: d.zipCode, lat: numGeo(d.latitude), lon: numGeo(d.longitude), isp: d.asnOrganization || "" } : null },
  { nome: "ipapi", url: (ip) => `https://ipapi.co/${ip}/json/`,
    leggi: (d) => d && !d.error && d.country_code ? { cc: d.country_code, regione: d.region, citta: d.city, cap: d.postal, lat: numGeo(d.latitude), lon: numGeo(d.longitude), isp: d.org } : null },
];
const pulisciGeo = (x: unknown, n: number) => { const s = t(x, n); return s === "-" || /^(unknown|null|undefined)$/i.test(s) ? "" : s; };
async function chiediGeo(f: FonteGeo, ip: string): Promise<Row | null> {
  try {
    const r = await fetch(f.url(encodeURIComponent(ip)), { signal: AbortSignal.timeout(1800), headers: { accept: "application/json" } });
    if (!r.ok) return null;
    const g = f.leggi(await r.json()); if (!g) return null;
    return { cc: String(g.cc || "").toUpperCase().slice(0, 2), regione: pulisciGeo(g.regione, 80), citta: pulisciGeo(g.citta, 80),
      cap: pulisciGeo(g.cap, 12), lat: g.lat ?? null, lon: g.lon ?? null, isp: pulisciGeo(g.isp, 120), fonte: f.nome };
  } catch { return null; }
}
const puntiGeo = (g: Row | null) => !g ? -1 : (g.citta ? 4 : 0) + (g.cap ? 2 : 0) + (g.regione ? 1 : 0) + (g.lat != null ? 1 : 0);
async function geo(ip: string, req: Request): Promise<Row> {
  if (!ip || /^(10\.|127\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.|::1|fc|fd)/i.test(ip)) return { ...GEO_VUOTO };
  const c = geoCache.get(ip);
  if (c && Date.now() - c.t < 6 * 3600e3) return c.g;
  // primo giro: la fonte principale; se manca la città (tipico degli IP mobili) chiediamo in parallelo alle altre
  let migliore: Row | null = await chiediGeo(FONTI_GEO[0], ip);
  if (!migliore || !migliore.citta || !migliore.cap) {
    const altri = await Promise.all(FONTI_GEO.slice(1).map((f) => chiediGeo(f, ip)));
    const tutti = [migliore, ...altri].filter((x): x is Row => !!x);
    // se più servizi concordano sulla stessa città, quella vince
    const voti = new Map<string, number>(); for (const x of tutti) if (x.citta) voti.set(x.citta.toLowerCase(), (voti.get(x.citta.toLowerCase()) || 0) + 1);
    tutti.sort((a, b) => (puntiGeo(b) + (voti.get(String(b.citta).toLowerCase()) || 0) * 3) - (puntiGeo(a) + (voti.get(String(a.citta).toLowerCase()) || 0) * 3));
    migliore = tutti[0] || null;
    if (migliore) { // completa i campi mancanti con quelli degli altri servizi che danno la stessa città/paese
      for (const x of tutti) {
        if (x === migliore || x.cc !== migliore.cc) continue;
        const stessa = !migliore.citta || !x.citta || x.citta.toLowerCase() === String(migliore.citta).toLowerCase();
        if (!stessa) continue;
        for (const k of ["citta", "cap", "regione", "isp"]) if (!migliore[k] && x[k]) migliore[k] = x[k];
        if (migliore.lat == null && x.lat != null) { migliore.lat = x.lat; migliore.lon = x.lon; }
      }
    }
  }
  const g: Row = { ...GEO_VUOTO, ...(migliore || {}) };
  if (!g.cc) g.cc = (req.headers.get("cf-ipcountry") || req.headers.get("x-country-code") || "").toUpperCase().replace(/[^A-Z]/g, "").slice(0, 2);
  if (g.cc) { try { g.paese = NOMI_PAESI.of(g.cc) || g.cc; } catch { g.paese = g.cc; } }
  if (geoCache.size > 2000) geoCache.clear();
  geoCache.set(ip, { t: Date.now(), g });
  return g;
}
/* colonne nuove (CAP e fonte della posizione): aggiunte da sole al primo avvio */
let colonneGeoOk = false;
async function colonneGeo() {
  if (colonneGeoOk) return;
  try { await esegui(`ALTER TABLE sessioni ADD COLUMN IF NOT EXISTS cap text, ADD COLUMN IF NOT EXISTS geo_fonte text,
      ADD COLUMN IF NOT EXISTS gps_lat double precision, ADD COLUMN IF NOT EXISTS gps_lon double precision, ADD COLUMN IF NOT EXISTS gps_acc int,
      ADD COLUMN IF NOT EXISTS gps_indirizzo text, ADD COLUMN IF NOT EXISTS gps_citta text, ADD COLUMN IF NOT EXISTS gps_cap text, ADD COLUMN IF NOT EXISTS gps_ts bigint, ADD COLUMN IF NOT EXISTS consenso int, ADD COLUMN IF NOT EXISTS sito text`);
    await esegui("ALTER TABLE eventi ADD COLUMN IF NOT EXISTS sito text");
    await esegui("UPDATE sessioni SET sito = 'stand' WHERE sito IS NULL");
    await esegui("UPDATE eventi SET sito = 'stand' WHERE sito IS NULL");
    await esegui("CREATE INDEX IF NOT EXISTS i_s_sito ON sessioni (sito, giorno)");
    await esegui("CREATE INDEX IF NOT EXISTS i_e_sito ON eventi (sito, giorno)");
    colonneGeoOk = true; } catch (e) { console.error("colonne geo", e); }
}
/* da coordinate GPS a indirizzo (OpenStreetMap / Nominatim) */
async function indirizzoDa(lat: number, lon: number): Promise<Row> {
  try {
    const r = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&addressdetails=1&zoom=18&lat=${lat}&lon=${lon}&accept-language=it`,
      { signal: AbortSignal.timeout(3000), headers: { "User-Agent": "DanovaStandStatistiche/1.0 (info@danova-tech.com)", accept: "application/json" } });
    if (!r.ok) return {};
    const a = ((await r.json()) || {}).address || {};
    const citta = a.city || a.town || a.village || a.municipality || a.suburb || "";
    const prov = String(a["ISO3166-2-lvl6"] || "").split("-").pop() || "";
    const via = [a.road || a.pedestrian || a.hamlet || "", a.house_number || ""].filter(Boolean).join(" ");
    const zona = [a.postcode || "", citta].filter(Boolean).join(" ") + (prov && prov.length <= 3 ? ` (${prov})` : "");
    return { indirizzo: t([via, zona, a.country_code && a.country_code !== "it" ? String(a.country || "") : ""].filter(Boolean).join(", "), 200),
      citta: t(citta, 80), cap: t(a.postcode, 12), regione: t(a.state, 80), cc: String(a.country_code || "").toUpperCase().slice(0, 2) };
  } catch { return {}; }
}
/* statistiche dettagliate: arrivano solo da chi ha accettato il banner cookie (ds-live.js manda c: 1) */
const TIPI_DETTAGLIO = ["clic", "scelta", "sezione", "modulo", "carrello_tolto"];
const FUORI_ELENCHI = "('clic','scelta','sezione')"; // troppo numerosi per gli elenchi "ultime azioni": si vedono nella scheda persona
const TIPI_EVENTO = ["richiesta", "render", "whatsapp", "telefono", "email", "carrello", "checkout", "ordine", "registrazione", "iscrizione", "preventivo", "download", "esterno", "ricerca", "copia", "preferito", "aiuto", "consenso"];
const intOk = (x: unknown, max: number) => { const n = parseInt(String(x)); return isFinite(n) && n >= 0 ? Math.min(n, max) : null; };

async function statistiche(req: Request) {
  if (req.method !== "POST") return new Risposta(null, 405);
  const ua = req.headers.get("user-agent") || "";
  if (e_robot(ua)) return new Risposta(null, 204);
  let inp: Row;
  try { inp = JSON.parse((await req.text()).slice(0, 8192)); } catch { return new Risposta(null, 204); }
  if (!inp || typeof inp !== "object") return new Risposta(null, 204);
  const e = inp.e;
  if (!["pv", "hb", "bye", "ev", "pos"].includes(e)) return new Risposta(null, 204);
  if (!/^[a-z0-9]{12,40}$/.test(String(inp.v ?? "")) || !/^[a-z0-9]{12,40}$/.test(String(inp.s ?? ""))) return new Risposta(null, 204);
  const sid = await anonimo("s" + inp.s), vid = await anonimo("v" + inp.v);
  const adesso = ora();
  let percorso = t(inp.p ?? "/", 250); if (percorso === "" || percorso[0] !== "/") percorso = "/";
  const titolo = t(inp.t, 200);
  const sito = sitoDi(inp.si, req);
  await colonneGeo();
  try {
    if (e === "pos") { // posizione GPS concessa dal visitatore
      const la = parseFloat(inp.la), lo = parseFloat(inp.lo), ac = parseFloat(inp.ac);
      if (!isFinite(la) || !isFinite(lo) || Math.abs(la) > 90 || Math.abs(lo) > 180 || (la === 0 && lo === 0)) return new Risposta(null, 204);
      await colonneGeo();
      if (Math.random() < 0.02) await esegui("UPDATE sessioni SET gps_lat = NULL, gps_lon = NULL, gps_acc = NULL, gps_indirizzo = NULL WHERE gps_ts < ?", [adesso - 730 * 86400]); // si conservano 24 mesi
      const prima = await riga("SELECT gps_lat FROM sessioni WHERE id = ?", [sid]);
      if (!prima) return new Risposta(null, 204);
      const ind = await indirizzoDa(la, lo);
      const acc = isFinite(ac) ? Math.min(Math.round(ac), 100000) : null;
      await esegui("UPDATE sessioni SET gps_lat = ?, gps_lon = ?, gps_acc = ?, gps_indirizzo = ?, gps_citta = ?, gps_cap = ?, gps_ts = ? WHERE id = ?",
        [Math.round(la * 1e5) / 1e5, Math.round(lo * 1e5) / 1e5, acc, ind.indirizzo || null, ind.citta || null, ind.cap || null, adesso, sid]);
      if (prima.gps_lat == null) {
        const modo = inp.m === "modulo" ? "dal modulo indirizzo" : inp.m === "auto" ? "già autorizzata" : "dall'avviso";
        await esegui("INSERT INTO eventi (sessione, visitatore, ts, giorno, ora, tipo, dettaglio, percorso, titolo, sito) VALUES (?,?,?,?,?,?,?,?,?,?)",
          [sid, vid, adesso, giornoDi(adesso), oraDi(adesso), "posizione", t((ind.indirizzo || `${la}, ${lo}`) + (acc != null ? ` (± ${acc} m, ${modo})` : ""), 200), percorso, titolo, sito]);
        await esegui("UPDATE sessioni SET azioni = COALESCE(azioni,0) + 1 WHERE id = ?", [sid]);
      }
      return new Risposta(null, 204);
    }
    if (e === "ev") { // azione: clic WhatsApp, telefono, email, carrello…
      const tipo = String(inp.k || "");
      const dettagliato = TIPI_DETTAGLIO.includes(tipo);
      if (!TIPI_EVENTO.includes(tipo) && !dettagliato) return new Risposta(null, 204);
      if (dettagliato && inp.c !== 1) return new Risposta(null, 204); // senza consenso non si salva
      if (dettagliato && !await val("SELECT id FROM sessioni WHERE id = ?", [sid])) return new Risposta(null, 204);
      await esegui("INSERT INTO eventi (sessione, visitatore, ts, giorno, ora, tipo, dettaglio, percorso, titolo, sito) VALUES (?,?,?,?,?,?,?,?,?,?)",
        [sid, vid, adesso, giornoDi(adesso), oraDi(adesso), tipo, t(inp.x, 200), percorso, titolo, sito]);
      if (dettagliato) { await colonneGeo(); await esegui("UPDATE sessioni SET ultimo = ?, consenso = 1 WHERE id = ?", [adesso, sid]); }
      else await esegui("UPDATE sessioni SET azioni = COALESCE(azioni,0) + 1, ultimo = ? WHERE id = ?", [adesso, sid]);
      return new Risposta(null, 204);
    }
    if (e === "hb" || e === "bye") {
      if (e === "hb") await esegui("UPDATE sessioni SET ultimo = ?, pagina = ?, titolo = ?, chiuso = 0 WHERE id = ?", [adesso, percorso, titolo, sid]);
      else await esegui("UPDATE sessioni SET ultimo = ?, chiuso = 1 WHERE id = ? AND pagina = ?", [adesso, sid, percorso]);
      const sc = intOk(inp.sc, 100);
      await esegui(`UPDATE visualizzazioni SET scroll = GREATEST(COALESCE(scroll,0), ?), tempo = GREATEST(COALESCE(tempo,0), ? - ts)
        WHERE id = (SELECT MAX(id) FROM visualizzazioni WHERE sessione = ? AND percorso = ?)`, [sc ?? 0, adesso, sid, percorso]);
      return new Risposta(null, 204);
    }
    if (!await val("SELECT id FROM sessioni WHERE id = ?", [sid])) {
      const v = await riga("SELECT primo, sessioni FROM visitatori WHERE id = ?", [vid]);
      let n: number, ritorno: number;
      if (v) { n = Number(v.sessioni) + 1; await esegui("UPDATE visitatori SET ultimo = ?, sessioni = ? WHERE id = ?", [adesso, n, vid]); ritorno = 1; }
      else { n = Math.max(1, Math.min(9999, parseInt(inp.k) || 1)); await esegui("INSERT INTO visitatori (id, primo, ultimo, sessioni) VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING", [vid, adesso, adesso, n]); ritorno = n > 1 ? 1 : 0; }
      const g = await geo(ipDi(req), req);
      await colonneGeo();
      const utm: Row = {}; if (inp.u && typeof inp.u === "object") for (const [k, x] of Object.entries(inp.u)) utm[k] = typeof x === "string" ? t(x, 80) : x;
      const rif = t(inp.r, 400);
      const [canale, sorgente, host] = provenienza(rif, utm);
      const [disp, browser, so] = dispositivo(ua, parseInt(inp.w) || 0);
      const lingua = String(inp.l ?? "").replace(/[^a-zA-Z-]/g, "").slice(0, 2).toLowerCase();
      const dim = (x: unknown) => /^\d{2,5}x\d{2,5}$/.test(String(x ?? "")) ? String(x) : "";
      const dpr = parseFloat(inp.dpr), mem = parseFloat(inp.mem);
      await esegui(`INSERT INTO sessioni (id, visitatore, inizio, ultimo, giorno, ora, dow, ritorno, n_visita, cc, paese, regione, citta, lat, lon,
        canale, sorgente, ref_host, campagna, ingresso, pagina, titolo, dispositivo, browser, so, lingua, pagine, chiuso,
        isp, fuso, schermo, finestra, dpr, touch, connessione, memoria, cpu, tema, lingue, riferimento, utm_sorgente, utm_mezzo, utm_termine, ua, azioni, modello, so_versione, visitatore_noto, cap, geo_fonte, sito)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0,0,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,0,?,?,
          CASE WHEN EXISTS (SELECT 1 FROM visitatori WHERE id = ? AND identificato IS NOT NULL) THEN 1 ELSE 0 END, ?, ?, ?) ON CONFLICT (id) DO NOTHING`,
        [sid, vid, adesso, adesso, giornoDi(adesso), oraDi(adesso), dowDi(adesso), ritorno, n, g.cc, g.paese, g.regione, g.citta, g.lat, g.lon,
          canale, sorgente, host, t(utm.c, 120), percorso, percorso, titolo, disp, browser, so, lingua,
          g.isp, t(inp.tz, 60), dim(inp.sch), dim(inp.fin), isFinite(dpr) ? Math.min(dpr, 10) : null, inp.tc ? 1 : 0, t(inp.cn, 20),
          isFinite(mem) ? Math.min(mem, 64) : null, intOk(inp.cpu, 256), inp.dk ? "scuro" : "chiaro", t(inp.ls, 60), rif,
          t(utm.s, 80), t(utm.m, 80), t(utm.t, 120), t(ua, 300), t(inp.mo, 60), t(inp.ov, 30), vid, g.cap || null, g.fonte || null, sito]);
    }
    await esegui("INSERT INTO visualizzazioni (sessione, ts, giorno, ora, percorso, titolo, scroll, tempo) VALUES (?,?,?,?,?,?,0,0)", [sid, adesso, giornoDi(adesso), oraDi(adesso), percorso, titolo]);
    await esegui("UPDATE sessioni SET ultimo = ?, pagina = ?, titolo = ?, pagine = pagine + 1, chiuso = 0 WHERE id = ?", [adesso, percorso, titolo, sid]);
    if (CFG.conserva_mesi > 0 && Math.random() < 1 / 400) {
      const lim = piuGiorni(giornoDi(adesso), -Math.round(CFG.conserva_mesi * 30.44));
      await esegui("DELETE FROM visualizzazioni WHERE giorno < ?", [lim]);
      await esegui("DELETE FROM eventi WHERE giorno < ?", [lim]);
      await esegui("DELETE FROM sessioni WHERE giorno < ?", [lim]);
      await esegui("DELETE FROM visitatori WHERE ultimo < ?", [mezzanotte(lim)]);
    }
  } catch (x) { console.error("live: " + (x as Error).message); }
  return new Risposta(null, 204);
}

/* ======================= /admin : dashboard ======================= */
async function firma(scad: number) { return scad + "." + await hmac(CFG.segreto || "ds", "area|" + scad); }
async function autorizzato(req: Request) {
  const tk = req.headers.get("x-area-token") || new URL(req.url).searchParams.get("t") || "";
  const m = /^(\d+)\.([a-f0-9]{64})$/.exec(tk.trim());
  if (!m || Number(m[1]) < ora() || !CFG.segreto) return false;
  return uguali(await firma(Number(m[1])), tk.trim());
}
function csv(nome: string, intest: string[], dati: unknown[][]) {
  const cella = (v: unknown) => { const s = String(v ?? ""); return /[";\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  const corpo = "﻿" + [intest, ...dati].map((r) => r.map(cella).join(";")).join("\r\n") + "\r\n";
  return new Risposta(corpo, 200, { "Content-Type": "text/csv; charset=utf-8", "Content-Disposition": `attachment; filename="${nome}"` });
}
const vir = (x: unknown) => (Number(x) || 0).toFixed(2).replace(".", ",");

async function admin(req: Request) {
  const url = new URL(req.url);
  const G = url.searchParams;
  const a = G.get("a") || "live";
  let inp: Row = {};
  if (req.method === "POST") { try { inp = JSON.parse(await req.text()) || {}; } catch { inp = {}; } }
  const ip = ipDi(req);

  if (a === "login") {
    if (!CFG.admin_password || !CFG.segreto) errore("Impostate prima i segreti ADMIN_PASSWORD e DS_SEGRETO in Supabase.", 500);
    if (!await limite("area_login", ip, 8, 900)) errore("Troppi tentativi. Riprovate tra 15 minuti.", 429);
    if (!uguali(String(inp.password ?? ""), CFG.admin_password)) { await new Promise((r) => setTimeout(r, 500)); errore("Password non corretta.", 401); }
    const scad = ora() + 3600 * CFG.admin_ore;
    return json({ ok: true, token: await firma(scad), scade: scad, siti: SITI });
  }
  if (!await autorizzato(req)) return json({ ok: false, errore: "accesso" }, 401);
  await colonneGeo();
  await tabellaRichieste();

  const g = (k: string, max = 190) => t(G.get(k) ?? inp[k] ?? "", max);
  const adesso = ora();
  const SITO = SITI[G.get("sito") || ""] ? String(G.get("sito")) : "";   // vuoto = tutti i siti
  const soloSito = (p: unknown[], alias = "s") => { if (!SITO) return ""; p.push(SITO); return ` AND ${alias}.sito = ?`; };

  /* ---------- filtri delle statistiche ---------- */
  const filtri = (p: unknown[], alias = "s") => {
    const w: string[] = [];
    if (SITO) { w.push(`${alias}.sito = ?`); p.push(SITO); }
    const mappa: Record<string, string> = { paese: "cc", canale: "canale", sorgente: "sorgente", dispositivo: "dispositivo", citta: "citta", browser: "browser", so: "so", lingua: "lingua" };
    for (const [k, col] of Object.entries(mappa)) { const v = G.get(k); if (v !== null && v !== "") { w.push(`${alias}.${col} = ?`); p.push(v); } }
    if (G.get("tipo") === "nuovi") w.push(`${alias}.ritorno = 0`);
    if (G.get("tipo") === "ritorno") w.push(`${alias}.ritorno = 1`);
    const ing = G.get("ingresso"); if (ing) { w.push(`${alias}.ingresso = ?`); p.push(ing); }
    const pag = G.get("pagina"); if (pag) { w.push(`${alias}.id IN (SELECT sessione FROM visualizzazioni WHERE percorso = ?)`); p.push(pag); }
    const reg = G.get("regione"); if (reg) { w.push(`${alias}.regione = ?`); p.push(reg); }
    const isp = G.get("isp"); if (isp) { w.push(`${alias}.isp = ?`); p.push(isp); }
    const az = G.get("azione"); if (az) { w.push(`${alias}.id IN (SELECT sessione FROM eventi WHERE tipo = ?)`); p.push(az); }
    if (G.get("noti") === "1") w.push(`${alias}.visitatore IN (SELECT id FROM visitatori WHERE identificato IS NOT NULL)`);
    if (G.get("noti") === "0") w.push(`${alias}.visitatore NOT IN (SELECT id FROM visitatori WHERE identificato IS NOT NULL)`);
    const pers = String(G.get("persona") || "").replace(/[^a-f0-9]/g, ""); if (pers.length >= 12) { w.push(`${alias}.visitatore LIKE ?`); p.push(pers + "%"); }
    return w.length ? " AND " + w.join(" AND ") : "";
  };
  const kpi = async (da: string, a_: string, senzaFiltri = false) => {
    const p: unknown[] = [da, a_]; const w = senzaFiltri ? soloSito(p) : filtri(p);
    const r = (await riga(`SELECT COUNT(*) sessioni, COUNT(DISTINCT s.visitatore) visitatori, COALESCE(SUM(s.ritorno),0) sess_ritorno,
      COUNT(DISTINCT CASE WHEN s.ritorno = 1 THEN s.visitatore END) vis_ritorno,
      COALESCE(SUM(CASE WHEN s.pagine <= 1 THEN 1 ELSE 0 END),0) rimbalzi, AVG(s.ultimo - s.inizio) durata, COALESCE(SUM(s.pagine),0) pagine
      FROM sessioni s WHERE s.giorno BETWEEN ? AND ?${w}`, p))!;
    const n = Number(r.sessioni);
    return { visitatori: Number(r.visitatori), sessioni: n, pagine: Number(r.pagine), nuovi: Number(r.visitatori) - Number(r.vis_ritorno), ritorno: Number(r.vis_ritorno),
      pagine_sessione: n ? Math.round(100 * Number(r.pagine) / n) / 100 : 0, durata: n ? Math.round(Number(r.durata)) : 0,
      rimbalzo: n ? Math.round(1000 * Number(r.rimbalzi) / n) / 10 : 0 };
  };
  const giorno_ok = (x: string | null, def: string) => /^\d{4}-\d{2}-\d{2}$/.test(String(x ?? "")) ? String(x) : def;

  if (a === "live") {
    const live = await righe(`SELECT s.id, s.ritorno, s.n_visita, s.cc, s.paese, s.regione, s.citta, s.cap, s.gps_lat, s.gps_lon, s.gps_acc, s.gps_indirizzo, s.gps_citta, s.gps_cap, s.lat, s.lon, s.canale, s.sorgente, s.ingresso, s.pagina, s.titolo,
      s.dispositivo, s.browser, s.so, s.lingua, s.pagine, s.inizio, s.ultimo, s.modello, s.azioni, SUBSTR(s.visitatore, 1, 16) pid, v.nome, v.email, v.telefono
      FROM sessioni s LEFT JOIN visitatori v ON v.id = s.visitatore AND v.identificato IS NOT NULL WHERE s.ultimo >= ? AND s.chiuso = 0${SITO ? " AND s.sito = ?" : ""} ORDER BY s.inizio DESC LIMIT 500`, SITO ? [adesso - CFG.live_secondi, SITO] : [adesso - CFG.live_secondi]);
    for (const x of live) { x.id = String(x.id).slice(0, 12); x.durata = adesso - Number(x.inizio); }
    const rec = await righe(`SELECT inizio, ultimo FROM sessioni WHERE ultimo >= ?${SITO ? " AND sito = ?" : ""}`, SITO ? [adesso - 1900, SITO] : [adesso - 1900]);
    const serie = [];
    for (let i = 29; i >= 0; i--) {
      const fine = adesso - i * 60, ini = fine - 60; let n = 0;
      for (const r of rec) if (Number(r.inizio) <= fine && Number(r.ultimo) >= ini - 20) n++;
      serie.push({ t: hhmm(fine), n });
    }
    const oggi = giornoDi(adesso), ieri = giornoDi(adesso - 86400);
    const contaAzioni = async (g2: string) => { const m: Row = {}; for (const r of await righe(`SELECT tipo, COUNT(*) n FROM eventi WHERE giorno = ?${SITO ? " AND sito = ?" : ""} GROUP BY tipo`, SITO ? [g2, SITO] : [g2])) m[r.tipo] = Number(r.n); return m; };
    const ultimeAzioni = await righe(`SELECT e.ts, e.tipo, e.dettaglio, e.percorso, e.titolo, s.citta, s.paese, s.cc, s.dispositivo, SUBSTR(e.sessione, 1, 12) sid, v.nome
      FROM eventi e LEFT JOIN sessioni s ON s.id = e.sessione LEFT JOIN visitatori v ON v.id = e.visitatore AND v.identificato IS NOT NULL WHERE e.ts >= ? AND e.tipo NOT IN ${FUORI_ELENCHI}${SITO ? " AND e.sito = ?" : ""} ORDER BY e.ts DESC LIMIT 30`, SITO ? [adesso - 86400, SITO] : [adesso - 86400]);
    return json({ ok: true, ora: adesso, live, serie, oggi: await kpi(oggi, oggi, true), ieri: await kpi(ieri, ieri, true), tuo_ip: ip, geo: true,
      azioni_oggi: await contaAzioni(oggi), azioni_ieri: await contaAzioni(ieri), ultime_azioni: ultimeAzioni });
  }

  if (a === "storico" || a === "csv") {
    let a_ = giorno_ok(G.get("a_"), giornoDi(adesso));
    let da = giorno_ok(G.get("da"), piuGiorni(giornoDi(adesso), -29));
    if (da > a_) [da, a_] = [a_, da];
    if (a === "csv") {
      const p: unknown[] = [da, a_]; const w = filtri(p);
      const rs = await righe(`SELECT giorno, inizio, ultimo, ritorno, n_visita, paese, regione, citta, canale, sorgente, ref_host, campagna, ingresso, pagine,
        dispositivo, browser, so, lingua, isp, schermo, fuso, connessione, tema, azioni FROM sessioni s WHERE s.giorno BETWEEN ? AND ?${w} ORDER BY inizio`, p);
      return csv(`visite_${da}_${a_}.csv`, ["Giorno", "Ora inizio", "Durata (s)", "Tipo", "N. visita", "Paese", "Regione", "Città", "Canale", "Sorgente", "Sito di provenienza", "Campagna", "Pagina di ingresso", "Pagine viste", "Dispositivo", "Browser", "Sistema", "Lingua", "Provider", "Schermo", "Fuso orario", "Connessione", "Tema", "Azioni"],
        rs.map((r) => [r.giorno, hhmmss(Number(r.inizio)), Number(r.ultimo) - Number(r.inizio), r.ritorno ? "Di ritorno" : "Nuovo", r.n_visita, r.paese, r.regione, r.citta,
          r.canale, r.sorgente, r.ref_host, r.campagna, r.ingresso, r.pagine, r.dispositivo, r.browser, r.so, r.lingua, r.isp, r.schermo, r.fuso, r.connessione, r.tema, r.azioni]));
    }
    const giorni = diffGiorni(da, a_) + 1;
    const pda = piuGiorni(da, -giorni), pa = piuGiorni(da, -1);
    const out: Row = { ok: true, da, a: a_, giorni, kpi: await kpi(da, a_), prec: await kpi(pda, pa), prec_da: pda, prec_a: pa };
    const unita = giorni === 1 ? "ora" : (giorni > 92 ? "mese" : "giorno");
    const chiaveS = unita === "ora" ? "s.ora::text" : (unita === "mese" ? "SUBSTR(s.giorno, 1, 7)" : "s.giorno");
    const chiaveV = unita === "ora" ? "v.ora::text" : (unita === "mese" ? "SUBSTR(v.giorno, 1, 7)" : "v.giorno");
    let p: unknown[] = [da, a_]; let w = filtri(p);
    const S = await righe(`SELECT ${chiaveS} k, COUNT(*) sessioni, COUNT(DISTINCT s.visitatore) visitatori,
      COUNT(DISTINCT CASE WHEN s.ritorno = 0 THEN s.visitatore END) nuovi FROM sessioni s WHERE s.giorno BETWEEN ? AND ?${w} GROUP BY 1`, p);
    p = [da, a_]; w = filtri(p);
    const V = await righe(`SELECT ${chiaveV} k, COUNT(*) n FROM visualizzazioni v JOIN sessioni s ON s.id = v.sessione WHERE v.giorno BETWEEN ? AND ?${w} GROUP BY 1`, p);
    const idx: string[] = [];
    if (unita === "ora") for (let i = 0; i < 24; i++) idx.push(String(i));
    else if (unita === "mese") {
      let [y, m] = da.slice(0, 7).split("-").map(Number); const [ya, ma] = a_.slice(0, 7).split("-").map(Number);
      while (y < ya || (y === ya && m <= ma)) { idx.push(`${y}-${String(m).padStart(2, "0")}`); m++; if (m > 12) { m = 1; y++; } }
    } else for (let g2 = da; g2 <= a_; g2 = piuGiorni(g2, 1)) idx.push(g2);
    const mm: Record<string, Row> = {};
    for (const k of idx) mm[k] = { k, visitatori: 0, nuovi: 0, sessioni: 0, pagine: 0 };
    for (const r of S) { const k = String(r.k); if (mm[k]) { mm[k].visitatori = Number(r.visitatori); mm[k].nuovi = Number(r.nuovi); mm[k].sessioni = Number(r.sessioni); } }
    for (const r of V) { const k = String(r.k); if (mm[k]) mm[k].pagine = Number(r.n); }
    out.unita = unita; out.serie = Object.values(mm);
    const top = async (col: string, lim = 12, extra = "") => {
      const p2: unknown[] = [da, a_]; const w2 = filtri(p2);
      const extraCol = extra ? ", " + extra.replace(/^,\s*/, "") : "";
      return await righe(`SELECT ${col} k${extraCol}, COUNT(*) n, COUNT(DISTINCT s.visitatore) u FROM sessioni s WHERE s.giorno BETWEEN ? AND ?${w2} GROUP BY ${col}${extraCol} ORDER BY n DESC LIMIT ${lim}`, p2);
    };
    out.paesi = await top("s.cc", 50, ", s.paese");
    out.citta = await top("s.citta", 15, ", s.paese");
    out.canali = await top("s.canale", 10);
    out.sorgenti = await top("s.sorgente", 15, ", s.canale");
    out.dispositivi = await top("s.dispositivo", 5);
    out.browser = await top("s.browser", 8);
    out.so = await top("s.so", 8);
    out.lingue = await top("s.lingua", 10);
    out.ingressi = await top("s.ingresso", 15);
    p = [da, a_]; w = filtri(p);
    out.pagine = await righe(`SELECT v.percorso k, MAX(v.titolo) titolo, COUNT(*) n, COUNT(DISTINCT v.sessione) u FROM visualizzazioni v JOIN sessioni s ON s.id = v.sessione
      WHERE v.giorno BETWEEN ? AND ?${w} GROUP BY v.percorso ORDER BY n DESC LIMIT 25`, p);
    p = [da, a_]; w = filtri(p);
    out.mappa = await righe(`SELECT s.citta, s.paese, s.cc, ROUND(AVG(s.lat)::numeric, 2) lat, ROUND(AVG(s.lon)::numeric, 2) lon, COUNT(*) n, COUNT(DISTINCT s.visitatore) u
      FROM sessioni s WHERE s.giorno BETWEEN ? AND ? AND s.lat IS NOT NULL${w} GROUP BY s.citta, s.paese, s.cc ORDER BY n DESC LIMIT 600`, p);
    p = [da, a_]; w = filtri(p);
    out.orari = await righe(`SELECT s.dow d, s.ora h, COUNT(*) n FROM sessioni s WHERE s.giorno BETWEEN ? AND ?${w} GROUP BY s.dow, s.ora`, p);
    p = [da, a_]; w = filtri(p);
    const ult = await righe(`SELECT s.id, s.inizio, s.ultimo, s.ritorno, s.n_visita, s.cc, s.paese, s.regione, s.citta, s.cap, s.gps_lat, s.gps_lon, s.gps_acc, s.gps_indirizzo, s.gps_citta, s.gps_cap, s.canale, s.sorgente, s.ingresso, s.pagina, s.pagine, s.dispositivo, s.browser, s.so,
      s.modello, s.azioni, SUBSTR(s.visitatore, 1, 16) pid, v.nome, v.email
      FROM sessioni s LEFT JOIN visitatori v ON v.id = s.visitatore AND v.identificato IS NOT NULL WHERE s.giorno BETWEEN ? AND ?${w} ORDER BY s.inizio DESC LIMIT 300`, p);
    for (const x of ult) x.id = String(x.id).slice(0, 12);
    out.ultime = ult;
    // azioni (clic WhatsApp, telefono, email, carrello, ordini…) delle visite filtrate
    p = [da, a_]; w = filtri(p);
    out.azioni = await righe(`SELECT e.tipo k, COUNT(*) n, COUNT(DISTINCT e.sessione) u FROM eventi e JOIN sessioni s ON s.id = e.sessione
      WHERE e.giorno BETWEEN ? AND ?${w} GROUP BY e.tipo ORDER BY n DESC`, p);
    p = [pda, pa]; w = filtri(p);
    out.azioni_prec = await righe(`SELECT e.tipo k, COUNT(*) n FROM eventi e JOIN sessioni s ON s.id = e.sessione WHERE e.giorno BETWEEN ? AND ?${w} GROUP BY e.tipo`, p);
    p = [da, a_]; w = filtri(p);
    out.whatsapp_pagine = await righe(`SELECT e.percorso k, MAX(e.titolo) titolo, COUNT(*) n, COUNT(DISTINCT e.sessione) u FROM eventi e JOIN sessioni s ON s.id = e.sessione
      WHERE e.tipo = 'whatsapp' AND e.giorno BETWEEN ? AND ?${w} GROUP BY e.percorso ORDER BY n DESC LIMIT 20`, p);
    p = [da, a_]; w = filtri(p);
    out.azioni_ultime = await righe(`SELECT e.ts, e.tipo, e.dettaglio, e.percorso, e.titolo, s.citta, s.regione, s.paese, s.cc, s.dispositivo, s.sorgente, SUBSTR(e.sessione, 1, 12) sid,
      SUBSTR(e.visitatore, 1, 16) pid, v.nome FROM eventi e JOIN sessioni s ON s.id = e.sessione LEFT JOIN visitatori v ON v.id = e.visitatore AND v.identificato IS NOT NULL
      WHERE e.giorno BETWEEN ? AND ? AND e.tipo NOT IN ${FUORI_ELENCHI}${w} ORDER BY e.ts DESC LIMIT 300`, p);
    // comportamento dettagliato (solo visitatori con consenso): clic, scelte, sezioni lette, moduli
    const topDett = async (tipo: string, chiave: string, lim: number) => { const q: unknown[] = [tipo, da, a_]; const w2 = filtri(q);
      return await righe(`SELECT ${chiave} k, COUNT(*) n, COUNT(DISTINCT e.visitatore) u FROM eventi e JOIN sessioni s ON s.id = e.sessione
        WHERE e.tipo = ? AND e.giorno BETWEEN ? AND ?${w2} GROUP BY 1 ORDER BY n DESC LIMIT ${lim}`, q); };
    out.clic_top = await topDett("clic", "e.dettaglio", 30);
    out.scelte_top = await topDett("scelta", "e.dettaglio", 30);
    out.sezioni_top = await topDett("sezione", "e.dettaglio", 30);
    out.moduli = await topDett("modulo", "SPLIT_PART(e.dettaglio, ' · ', 1)", 40);
    out.tolti = await topDett("carrello_tolto", "e.dettaglio", 20);
    p = [da, a_]; w = filtri(p);
    out.ricerche = await righe(`SELECT LOWER(e.dettaglio) k, COUNT(*) n, COUNT(DISTINCT e.visitatore) u FROM eventi e JOIN sessioni s ON s.id = e.sessione
      WHERE e.tipo = 'ricerca' AND e.giorno BETWEEN ? AND ?${w} GROUP BY LOWER(e.dettaglio) ORDER BY n DESC LIMIT 20`, p);
    p = [da, a_]; w = filtri(p);
    out.prodotti = await righe(`SELECT x.percorso k, MAX(x.titolo) titolo, COUNT(*) n, COUNT(DISTINCT s.visitatore) u, ROUND(AVG(NULLIF(x.tempo,0))) tempo
      FROM visualizzazioni x JOIN sessioni s ON s.id = x.sessione WHERE x.giorno BETWEEN ? AND ?${w}
        AND (x.percorso ~ '(^|/)stand-[^/]+/{0,1}$' OR x.percorso ~ '/[^/]+-stand/{0,1}$' OR x.percorso LIKE '/render/%') GROUP BY x.percorso ORDER BY n DESC LIMIT 25`, p);
    p = [da, a_]; w = filtri(p);
    out.modelli = await righe(`SELECT COALESCE(NULLIF(s.modello, ''), s.so) k, COUNT(*) n, COUNT(DISTINCT s.visitatore) u FROM sessioni s WHERE s.giorno BETWEEN ? AND ?${w}
      GROUP BY 1 ORDER BY n DESC LIMIT 12`, p);
    p = [da, a_]; w = filtri(p);
    out.noti = (await riga(`SELECT COUNT(DISTINCT s.visitatore) FILTER (WHERE s.visitatore_noto = 1 OR s.visitatore IN (SELECT id FROM visitatori WHERE identificato IS NOT NULL)) noti,
      COUNT(DISTINCT s.visitatore) tutti FROM sessioni s WHERE s.giorno BETWEEN ? AND ?${w}`, p)) || {};
    out.regioni = await top("s.regione", 20, ", s.cc");
    out.schermi = await top("s.schermo", 12);
    out.isp = await top("s.isp", 15);
    out.fusi = await top("s.fuso", 10);
    out.connessioni = await top("s.connessione", 6);
    p = [da, a_]; w = filtri(p);
    out.scroll = (await riga(`SELECT ROUND(AVG(v.scroll)) scroll, ROUND(AVG(NULLIF(v.tempo,0))) tempo FROM visualizzazioni v JOIN sessioni s ON s.id = v.sessione
      WHERE v.giorno BETWEEN ? AND ?${w}`, p)) || {};
    return json(out);
  }

  /* ---------- persone: ogni visitatore con le sue visite (nome, telefono, email se ce li ha lasciati) ---------- */
  if (a === "persone") {
    let a_ = giorno_ok(G.get("a_"), giornoDi(adesso));
    let da = giorno_ok(G.get("da"), piuGiorni(giornoDi(adesso), -29));
    if (da > a_) [da, a_] = [a_, da];
    const p: unknown[] = [da, a_]; const w = filtri(p);
    const hv: string[] = [];
    const q = t(G.get("q") ?? "", 80);
    if (q) { hv.push(`(v.email ILIKE ? OR v.nome ILIKE ? OR v.telefono ILIKE ? OR STRING_AGG(DISTINCT s.citta, ' ') ILIKE ? OR STRING_AGG(DISTINCT s.isp, ' ') ILIKE ?
      OR EXISTS (SELECT 1 FROM eventi e WHERE e.visitatore = v.id AND e.dettaglio ILIKE ?))`); for (let i = 0; i < 6; i++) p.push("%" + q + "%"); }
    const minv = parseInt(G.get("min_visite") || "0"); if (minv > 1) { hv.push("COUNT(s.id) >= ?"); p.push(minv); }
    const ord: Record<string, string> = { recenti: "MAX(s.ultimo) DESC", visite: "COUNT(s.id) DESC", pagine: "SUM(s.pagine) DESC", tempo: "SUM(s.ultimo - s.inizio) DESC", azioni: "SUM(COALESCE(s.azioni,0)) DESC" };
    const r = await righe(`SELECT SUBSTR(v.id, 1, 16) pid, v.email, v.nome, v.telefono, v.fonte, v.identificato, v.primo, v.sessioni visite_totali,
        COUNT(s.id) visite, COALESCE(SUM(s.pagine),0) pagine, COALESCE(SUM(s.ultimo - s.inizio),0) tempo, MAX(s.ultimo) ultimo, MIN(s.inizio) inizio,
        COALESCE(SUM(s.azioni),0) azioni,
        (ARRAY_AGG(s.citta ORDER BY s.inizio DESC))[1] citta, (ARRAY_AGG(s.regione ORDER BY s.inizio DESC))[1] regione,
        (ARRAY_AGG(s.cc ORDER BY s.inizio DESC))[1] cc, (ARRAY_AGG(s.paese ORDER BY s.inizio DESC))[1] paese,
        (ARRAY_AGG(s.dispositivo ORDER BY s.inizio DESC))[1] dispositivo, (ARRAY_AGG(s.modello ORDER BY s.inizio DESC))[1] modello,
        (ARRAY_AGG(s.so ORDER BY s.inizio DESC))[1] so, (ARRAY_AGG(s.isp ORDER BY s.inizio DESC))[1] isp,
        (ARRAY_AGG(s.sorgente ORDER BY s.inizio ASC))[1] prima_sorgente, (ARRAY_AGG(s.canale ORDER BY s.inizio ASC))[1] primo_canale,
        (SELECT COUNT(*) FROM eventi e WHERE e.visitatore = v.id AND e.tipo = 'whatsapp') wa,
        (SELECT COUNT(*) FROM eventi e WHERE e.visitatore = v.id AND e.tipo = 'telefono') tel,
        (SELECT COUNT(*) FROM richieste r WHERE r.visitatore = v.id) richieste
      FROM visitatori v JOIN sessioni s ON s.visitatore = v.id
      WHERE s.giorno BETWEEN ? AND ?${w}
      GROUP BY v.id${hv.length ? " HAVING " + hv.join(" AND ") : ""}
      ORDER BY ${ord[G.get("ordina") || "recenti"] || ord.recenti} LIMIT 500`, p);
    const p2: unknown[] = [da, a_]; const w2 = filtri(p2);
    const tot = await riga(`SELECT COUNT(DISTINCT s.visitatore) tutti, COUNT(DISTINCT s.visitatore) FILTER (WHERE v.identificato IS NOT NULL) noti,
      COUNT(DISTINCT s.visitatore) FILTER (WHERE s.ritorno = 1) ritorno FROM sessioni s LEFT JOIN visitatori v ON v.id = s.visitatore WHERE s.giorno BETWEEN ? AND ?${w2}`, p2);
    return json({ ok: true, da, a: a_, persone: r, totali: tot });
  }

  if (a === "persona") {
    const pid = String(G.get("id") || "").replace(/[^a-f0-9]/g, "");
    if (pid.length < 12) return json({ ok: false }, 400);
    const v = await riga("SELECT * FROM visitatori WHERE id LIKE ? LIMIT 1", [pid + "%"]);
    if (!v) return json({ ok: false }, 404);
    const sess = await righe(`SELECT SUBSTR(id, 1, 12) id, inizio, ultimo, giorno, ritorno, n_visita, cc, paese, regione, citta, cap, lat, lon, gps_lat, gps_lon, gps_acc, gps_indirizzo, gps_citta, gps_cap, isp, canale, sorgente, ref_host, riferimento,
      campagna, utm_sorgente, utm_mezzo, utm_termine, ingresso, pagina, pagine, dispositivo, modello, browser, so, so_versione, schermo, finestra, dpr, touch, connessione,
      memoria, cpu, tema, lingua, lingue, fuso, azioni FROM sessioni WHERE visitatore = ? ORDER BY inizio DESC LIMIT 200`, [v.id]);
    const pagine = await righe(`SELECT SUBSTR(x.sessione, 1, 12) sid, x.ts, x.percorso, x.titolo, x.scroll, x.tempo FROM visualizzazioni x
      WHERE x.sessione IN (SELECT id FROM sessioni WHERE visitatore = ?) ORDER BY x.ts DESC LIMIT 1500`, [v.id]);
    const azioni = await righe("SELECT SUBSTR(sessione, 1, 12) sid, ts, tipo, dettaglio, percorso, titolo FROM eventi WHERE visitatore = ? ORDER BY ts DESC LIMIT 5000", [v.id]);
    const prodotti = await righe(`SELECT x.percorso k, MAX(x.titolo) titolo, COUNT(*) n, COALESCE(SUM(x.tempo),0) tempo, MAX(x.ts) ultimo FROM visualizzazioni x
      WHERE x.sessione IN (SELECT id FROM sessioni WHERE visitatore = ?) AND (x.percorso ~ '(^|/)stand-[^/]+/{0,1}$' OR x.percorso ~ '/[^/]+-stand/{0,1}$' OR x.percorso LIKE '/render/%')
      GROUP BY x.percorso ORDER BY n DESC, tempo DESC LIMIT 40`, [v.id]);
    const richieste = await righe(`SELECT id, creato, stato, oggetto, fiera, azienda, messaggio, valore FROM richieste
      WHERE visitatore = ?${v.email ? " OR LOWER(email) = ?" : ""} ORDER BY creato DESC LIMIT 50`, v.email ? [v.id, String(v.email).toLowerCase()] : [v.id]);
    const out: Row = { ...v, pid: String(v.id).slice(0, 16) }; delete out.id;
    return json({ ok: true, persona: out, sessioni: sess, pagine, azioni, prodotti, richieste, stati_nomi: STATI_R });
  }

  if (a === "csv_azioni") {
    let a_ = giorno_ok(G.get("a_"), giornoDi(adesso));
    let da = giorno_ok(G.get("da"), piuGiorni(giornoDi(adesso), -29));
    if (da > a_) [da, a_] = [a_, da];
    const p: unknown[] = [da, a_]; const w = filtri(p);
    const rs = await righe(`SELECT e.ts, e.tipo, e.dettaglio, e.percorso, e.titolo, s.citta, s.regione, s.paese, s.dispositivo, s.sorgente FROM eventi e
      JOIN sessioni s ON s.id = e.sessione WHERE e.giorno BETWEEN ? AND ?${w} ORDER BY e.ts`, p);
    return csv(`azioni_${da}_${a_}.csv`, ["Data e ora", "Azione", "Dettaglio", "Pagina", "Titolo pagina", "Città", "Regione", "Paese", "Dispositivo", "Arrivato da"],
      rs.map((r) => [dataOra(Number(r.ts)), r.tipo, r.dettaglio, r.percorso, r.titolo, r.citta, r.regione, r.paese, r.dispositivo, r.sorgente]));
  }

  if (a === "percorso") {
    const id = String(G.get("id") ?? "").replace(/[^a-f0-9]/g, "");
    if (id.length < 12) return json({ ok: false }, 400);
    const s = await riga("SELECT id, visitatore FROM sessioni WHERE id LIKE ? LIMIT 1", [id + "%"]);
    if (!s) return json({ ok: false }, 404);
    return json({ ok: true,
      persona: await riga("SELECT SUBSTR(id, 1, 16) pid, nome, email, telefono, fonte, identificato, primo, sessioni FROM visitatori WHERE id = ?", [s.visitatore]),
      sessione: await riga(`SELECT cc, ritorno, modello, so_versione, paese, regione, citta, cap, geo_fonte, lat, lon, gps_lat, gps_lon, gps_acc, gps_indirizzo, gps_citta, gps_ts, isp, fuso, schermo, finestra, dpr, touch, connessione, memoria, cpu, tema, lingue, lingua,
        riferimento, utm_sorgente, utm_mezzo, utm_termine, campagna, canale, sorgente, dispositivo, browser, so, ua, n_visita, inizio, ultimo FROM sessioni WHERE id = ?`, [s.id]),
      azioni: await righe("SELECT ts, tipo, dettaglio, percorso, titolo FROM eventi WHERE sessione = ? ORDER BY ts", [s.id]),
      pagine: await righe("SELECT ts, percorso, titolo, scroll, tempo FROM visualizzazioni WHERE sessione = ? ORDER BY ts", [s.id]),
      visite_precedenti: await righe("SELECT giorno, inizio, pagine, sorgente, ingresso FROM sessioni WHERE visitatore = ? AND id <> ? ORDER BY inizio DESC LIMIT 20", [s.visitatore, s.id]) });
  }

  /* ---------- richieste arrivate dai moduli del sito ---------- */
  const like = (q: string) => "%" + q + "%";
  switch (a) {
    case "richieste": {
      const st = g("stato") || "aperte";
      const w: string[] = []; let p: unknown[] = [];
      if (SITO) { w.push("sito = ?"); p.push(SITO); }
      if (st === "aperte") w.push("stato IN ('nuova','contattato','preventivo')"); else if (STATI_R[st]) { w.push("stato = ?"); p.push(st); }
      const q = g("q", 80);
      if (q !== "") { w.push("(nome ILIKE ? OR email ILIKE ? OR telefono ILIKE ? OR azienda ILIKE ? OR fiera ILIKE ? OR messaggio ILIKE ? OR oggetto ILIKE ? OR rif ILIKE ?)"); p = p.concat(Array(8).fill(like(q))); }
      const r = await righe(`SELECT r.*, SUBSTR(r.visitatore, 1, 16) pid,
          (SELECT COUNT(*) FROM sessioni s WHERE s.visitatore = r.visitatore) visite,
          (SELECT COALESCE(SUM(s.pagine),0) FROM sessioni s WHERE s.visitatore = r.visitatore) pagine_viste
        FROM richieste r${w.length ? " WHERE " + w.join(" AND ") : ""} ORDER BY r.creato DESC LIMIT 500`, p);
      for (const x of r) { delete x.visitatore; delete x.sessione; try { x.campi = JSON.parse(x.campi || "[]"); } catch { x.campi = []; } }
      const conta: Row = {};
      for (const x of await righe(`SELECT stato, COUNT(*) n FROM richieste${SITO ? " WHERE sito = ?" : ""} GROUP BY stato`, SITO ? [SITO] : [])) conta[x.stato] = Number(x.n);
      const oggi = giornoDi(adesso);
      const per = await riga(`SELECT COUNT(*) FILTER (WHERE creato >= ?) oggi, COUNT(*) FILTER (WHERE creato >= ?) d7, COUNT(*) FILTER (WHERE creato >= ?) d30,
        COALESCE(SUM(valore) FILTER (WHERE stato = 'acquisita'), 0) valore_acquisito FROM richieste${SITO ? " WHERE sito = ?" : ""}`,
        [mezzanotte(oggi), mezzanotte(piuGiorni(oggi, -6)), mezzanotte(piuGiorni(oggi, -29)), ...(SITO ? [SITO] : [])]);
      return json({ ok: true, richieste: r, conta, periodo: per, stati: STATI_R });
    }
    case "richiesta_salva": {
      const id = parseInt(g("id")) || 0;
      const st = STATI_R[inp.stato] ? inp.stato : "nuova";
      const valore = isNum(inp.valore) ? num(inp.valore) : null;
      await esegui(`UPDATE richieste SET stato = ?, note_admin = ?, valore = ?, aggiornato = ?,
        contattato = CASE WHEN ? <> 'nuova' THEN COALESCE(contattato, ?) ELSE contattato END WHERE id = ?`,
        [st, t(inp.note_admin, 4000), valore, adesso, st, adesso, id]);
      return json({ ok: true });
    }
    case "rif": { // codice "Rif." arrivato su WhatsApp: a chi corrisponde
      const r = rif_ok(g("rif"));
      if (!r) return json({ ok: false, errore: "Codice non valido" }, 400);
      const ev = await riga("SELECT SUBSTR(visitatore, 1, 16) pid, ts, percorso, titolo FROM eventi WHERE dettaglio ILIKE ? ORDER BY ts DESC LIMIT 1", ["%Rif. " + r + "%"]);
      const rq = await righe("SELECT id, nome, email, telefono, azienda, fiera, stato, creato, SUBSTR(visitatore, 1, 16) pid FROM richieste WHERE rif = ? ORDER BY creato DESC LIMIT 5", [r]);
      const pid = ev ? ev.pid : (rq.find((x) => x.pid)?.pid || null);
      const chi = pid ? await riga("SELECT nome, email, telefono FROM visitatori WHERE id LIKE ? LIMIT 1", [pid + "%"]) : null;
      return json({ ok: true, rif: r, pid, chi, evento: ev, richieste: rq });
    }
    case "csv_richieste": {
      const rr = await righe(`SELECT * FROM richieste${SITO ? " WHERE sito = ?" : ""} ORDER BY creato`, SITO ? [SITO] : []);
      return csv(`richieste_${SITO || "tutti"}_${giornoDi(adesso)}.csv`, ["Data", "Sito", "Stato", "Nome", "Azienda", "Email", "Telefono", "Fiera", "Quando vuole partire", "Messaggio", "Oggetto", "Altri campi", "Pagina", "Lingua", "Città", "Regione", "Paese", "Arrivato da", "Rif. WhatsApp", "Valore (€)", "Note interne"],
        rr.map((x) => {
          let altri = ""; try { altri = (JSON.parse(x.campi || "[]") as string[][]).map((c) => c[0] + ": " + c[1]).join(" | "); } catch { /* */ }
          return [dataOra(Number(x.creato)), SITI[x.sito] || x.sito || "", STATI_R[x.stato] || x.stato, x.nome, x.azienda, x.email, x.telefono, x.fiera, x.urgenza, x.messaggio, x.oggetto, altri,
            x.pagina, x.lingua, x.citta, x.regione, x.paese, x.sorgente, x.rif, x.valore != null ? vir(x.valore) : "", x.note_admin];
        }));
    }
  }
  return json({ ok: false, errore: "azione" }, 404);
}

/* ======================= /richiesta : copia delle richieste dei moduli ======================= */
const STATI_R: Record<string, string> = { nuova: "Nuova", contattato: "Contattato", preventivo: "Preventivo inviato", acquisita: "Acquisita", persa: "Persa" };
let tabellaRichiesteOk = false;
async function tabellaRichieste() {
  if (tabellaRichiesteOk) return;
  await esegui(`CREATE TABLE IF NOT EXISTS richieste (
    id bigint generated by default as identity primary key, creato bigint, aggiornato bigint, stato text default 'nuova',
    nome text, email text, telefono text, azienda text, fiera text, urgenza text, messaggio text, oggetto text, campi text,
    pagina text, titolo text, lingua text, rif text, visitatore text, sessione text,
    citta text, regione text, paese text, cc text, canale text, sorgente text,
    valore numeric(12,2), note_admin text, contattato bigint)`);
  await esegui("ALTER TABLE richieste ENABLE ROW LEVEL SECURITY");
  await esegui("ALTER TABLE richieste ADD COLUMN IF NOT EXISTS sito text");
  await esegui("UPDATE richieste SET sito = 'stand' WHERE sito IS NULL");
  tabellaRichiesteOk = true;
}
// etichette dei campi dei moduli (contatto.js, fiere-richiesta.js) → colonne
const CAMPI: [string, RegExp][] = [
  ["nome", /^(nome|name|姓名|name \/ 姓名|nom|nombre)\b/i], ["email", /^(e-?mail)\b/i], ["telefono", /^(telefono|phone|tel|telefon|téléphone|teléfono)|电话|電話/i],
  ["azienda", /^(azienda|company|firma|société|empresa)|公司/i], ["fiera", /^(fiera|fair|messe|salon|feria)|展会|展會/i],
  ["urgenza", /^quando vuole partire/i], ["messaggio", /^(messaggio|message|nachricht|mensaje|note|notes|notizen)|备注|備註/i],
];
async function richiesta(req: Request) {
  if (req.method !== "POST") return new Risposta({ ok: false }, 405);
  let inp: Row;
  try { inp = JSON.parse((await req.text()).slice(0, 20000)); } catch { return new Risposta({ ok: false }, 400); }
  if (!inp || typeof inp !== "object" || !Array.isArray(inp.campi)) return new Risposta({ ok: false }, 400);
  if (!await limite("richiesta", ipDi(req), 15, 3600)) return new Risposta({ ok: false, errore: "troppe" }, 429);
  await tabellaRichieste();
  const adesso = ora();
  const campi: string[][] = [];
  const col: Row = {};
  for (const c of inp.campi.slice(0, 40)) {
    if (!Array.isArray(c)) continue;
    const k = t(c[0], 60), v = t(c[1], 3000);
    if (!k || !v || /^_/.test(k)) continue;
    if (/^(pagina|page)$/i.test(k)) continue;
    let usato = false;
    for (const [nome, re] of CAMPI) if (!col[nome] && re.test(k)) { col[nome] = v; usato = true; break; }
    if (!usato) campi.push([k, v]);
  }
  if (!col.email && email_ok(t(inp.email, 190))) col.email = t(inp.email, 190);
  if (col.email && !email_ok(col.email)) col.email = "";
  if (!col.nome && !col.email && !col.telefono) return new Risposta({ ok: false }, 422);
  const v = /^[a-z0-9]{12,40}$/.test(String(inp.v ?? "")) ? String(inp.v) : "";
  const s = /^[a-z0-9]{12,40}$/.test(String(inp.s ?? "")) ? String(inp.s) : "";
  const vid = v ? await anonimo("v" + v) : null, sid = s ? await anonimo("s" + s) : null;
  const ses = sid ? await riga("SELECT citta, regione, paese, cc, canale, sorgente FROM sessioni WHERE id = ?", [sid]) : null;
  let percorso = t(inp.p ?? "/", 250); if (percorso[0] !== "/") percorso = "/";
  const rif = v ? v.slice(0, 6).toUpperCase() : "";
  const sito = sitoDi(inp.si, req);
  await colonneGeo();
  const id = await val(`INSERT INTO richieste (creato, aggiornato, stato, nome, email, telefono, azienda, fiera, urgenza, messaggio, oggetto, campi, pagina, titolo, lingua, rif,
      visitatore, sessione, citta, regione, paese, cc, canale, sorgente, sito) VALUES (?,?,'nuova',?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) RETURNING id`,
    [adesso, adesso, t(col.nome, 160), t(col.email, 190).toLowerCase(), t(col.telefono, 40), t(col.azienda, 160), t(col.fiera, 160), t(col.urgenza, 60),
      t(col.messaggio, 3000), t(inp.oggetto, 200), JSON.stringify(campi), percorso, t(inp.t, 200), t(inp.l, 10), rif, vid, sid,
      ses?.citta || null, ses?.regione || null, ses?.paese || null, ses?.cc || null, ses?.canale || null, ses?.sorgente || null, sito]);
  if (v) await identifica(v, { email: col.email, nome: col.nome, telefono: col.telefono, fonte: "richiesta" });
  if (sid && vid) {
    await esegui("INSERT INTO eventi (sessione, visitatore, ts, giorno, ora, tipo, dettaglio, percorso, titolo, sito) VALUES (?,?,?,?,?,?,?,?,?,?)",
      [sid, vid, adesso, giornoDi(adesso), oraDi(adesso), "richiesta", t((col.fiera ? col.fiera + " · " : "") + (col.azienda || col.nome || ""), 200), percorso, t(inp.t, 200), sito]);
    await esegui("UPDATE sessioni SET azioni = COALESCE(azioni,0) + 1, ultimo = ? WHERE id = ?", [adesso, sid]);
  }
  return new Risposta({ ok: true, id });
}


/* ======================= ingresso ======================= */
Deno.serve(async (req) => {
  const origine = req.headers.get("origin") || "";
  const permesso = CFG.origini.includes(origine) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origine);
  const cors: Record<string, string> = permesso ? {
    "Access-Control-Allow-Origin": origine, "Vary": "Origin",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-Area-Token",
    "Access-Control-Max-Age": "86400",
  } : {};
  if (req.method === "OPTIONS") return new Response(null, { status: permesso ? 204 : 403, headers: cors });

  const percorso = new URL(req.url).pathname.replace(/\/+$/, "");
  const sezione = percorso.split("/").pop();
  // dal browser accettiamo solo il vostro sito (i link CSV della dashboard non hanno "Origin")
  if (origine && !permesso) return new Response(JSON.stringify({ ok: false, errore: "origine" }), { status: 403, headers: { "Content-Type": "application/json" } });

  let r: Risposta;
  try {
    if (sezione === "richiesta") r = await richiesta(req);
    else if (sezione === "s") r = await statistiche(req);
    else if (sezione === "admin") r = await admin(req) as unknown as Risposta;
    else r = new Risposta({ ok: true, servizio: "ds", sezioni: ["s", "richiesta", "admin"] });
  } catch (e) {
    if (e instanceof Risposta) r = e;
    else {
      console.error("ds " + sezione + ": " + ((e as Error)?.stack || e));
      r = new Risposta({ ok: false, errore: "Si è verificato un problema. Riprovate tra poco o scriveteci a " + CFG.contatto + "." }, 500);
    }
  }
  const head: Record<string, string> = { ...cors, "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow", ...r.extra };
  if (r.dati === null) return new Response(null, { status: r.codice, headers: head });
  if (typeof r.dati === "string") return new Response(r.dati, { status: r.codice, headers: head });
  head["Content-Type"] = "application/json; charset=utf-8";
  return new Response(JSON.stringify(r.dati), { status: r.codice, headers: head });
});


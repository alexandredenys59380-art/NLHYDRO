import json, re, html
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import quote
import feedparser

OUTPUT = Path("docs/articles.json")

# Flux RSS publics : compléter cette liste avec les flux fiables de vos sources métier.
QUERY_1 = quote('"EDF Hydro" OR "EDF hydroélectricité"')
QUERY_2 = quote('("EDF Hydro" OR EDF) (barrage OR turbine OR centrale hydroélectrique OR hydroélectricité)')
SOURCES = [
    ("Google Actualités — EDF Hydro", f"https://news.google.com/rss/search?q={QUERY_1}&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google Actualités — projets hydroélectriques", f"https://news.google.com/rss/search?q={QUERY_2}&hl=fr&gl=FR&ceid=FR:fr"),
    ("France Hydro Électricité", "https://www.france-hydro-electricite.fr/feed/"),
    ("Connaissance des Énergies", "https://www.connaissancedesenergies.org/rss.xml"),
    ("EDF — communiqués", "https://www.edf.fr/tous-les-communiques/feed"),
]
KEYWORDS = [
    "edf hydro", "hydroélectricité", "hydro-électricité", "hydraulique",
    "barrage", "centrale hydroélectrique", "turbine", "step",
    "pompage-turbinage", "durance", "verdon", "rhône", "rhone",
    "concession hydroélectrique", "groupe de production"
]

def clean(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    return re.sub(r"\s+", " ", s).strip()

def category(text):
    t = text.lower()
    groups = [
        ("Environnement & biodiversité", ["biodivers", "poisson", "faune", "flore", "écologique", "environnement", "continuité écologique"]),
        ("Projets & chantiers", ["chantier", "travaux", "construction", "projet", "modernisation", "rénovation"]),
        ("Investissements & appels d'offres", ["investissement", "investit", "appel d'offres", "marché public", "millions d'euros"]),
        ("Exploitation & production", ["production", "exploitation", "crue", "débit", "étiage", "maintenance", "incident"]),
        ("Technologies & innovation", ["innovation", "turbine", "numérique", "digital", "automatisation", "stockage", "step"]),
        ("Réglementation & concessions", ["réglementation", "concession", "décret", "arrêté", "loi", "autorisation"]),
        ("Entreprise & ressources humaines", ["recrut", "emploi", "alternance", "salarié", "formation", "nomination"]),
    ]
    for label, words in groups:
        if any(w in t for w in words): return label
    return "Actualités du secteur"

def published(entry):
    p = entry.get("published_parsed") or entry.get("updated_parsed")
    if p:
        return datetime(*p[:6], tzinfo=timezone.utc).isoformat()
    return None

def main():
    old = {}
    if OUTPUT.exists():
        try:
            old = {a["url"]: a for a in json.loads(OUTPUT.read_text(encoding="utf-8")).get("articles", [])}
        except Exception:
            old = {}
    for source, url in SOURCES:
        try:
            feed = feedparser.parse(url)
            if getattr(feed, "bozo", False):
                print(f"Flux à vérifier ({source}): {getattr(feed, 'bozo_exception', 'erreur RSS')}")
            for entry in feed.entries:
                title = clean(entry.get("title", "Publication sans titre"))
                summary = clean(entry.get("summary", entry.get("description", "")))
                link = (entry.get("link") or "").strip()
                haystack = f"{title} {summary} {source}".lower()
                if not link or not any(k in haystack for k in KEYWORDS):
                    continue
                old[link] = {
                    "url": link, "title": title, "summary": summary,
                    "source": source, "published": published(entry),
                    "category": category(f"{title} {summary}")
                }
        except Exception as exc:
            print(f"Erreur source {source}: {exc}")
    articles = list(old.values())
    articles.sort(key=lambda a: a.get("published") or "", reverse=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "articles": articles
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(articles)} publication(s) conservée(s).")

if __name__ == "__main__":
    main()

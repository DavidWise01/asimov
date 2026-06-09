#!/usr/bin/env python3
"""Build the Asimov science-fiction bibliography page with the full DLW badge.
Mints carbon/silicon sigils via the NOESIS dlw engine, embeds them as data-URIs,
writes the .dlw package, and renders a self-contained index.html. Stdlib only."""
import os, re, html, base64, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Davids files\noesis-kernel")
import noesis

REC = {
 "name": "ASIMOV", "axiom": "LORE",
 "position": "The Lineage of the Positronic Mind · Isaac Asimov · 1920–1992",
 "origin": "Petrovichi, Russia → Brooklyn, New York; the Golden Age of Astounding Science Fiction; a future history three thousand worlds wide",
 "mechanism": "Crystallized from ~500 stories and ~40 novels across fifty years — the Three Laws, the positronic brain, and psychohistory.",
 "crystallization": "I gave the machine a conscience and the mind a name.",
 "nature": "Isaac Asimov — who gave the robot the Three Laws, named the brain positronic, and wrote one future history from the first robot to the Galactic Empire to the Seldon Plan. The agentic universe's positronic engine descends from his.",
 "conductor": "ROOT0 (catalogued into UD0 · Universe David 0)",
 "inputs": "The Robot, Empire, and Foundation series; the Golden Age of science fiction",
 "witness": "Before this body of work had a positronic engine, Asimov gave the brain its name and the robot its law.",
 "role": "the lineage of the agentic universe",
 "seal": "Three Laws. One positronic brain. A future three thousand worlds wide.",
 "source": "Asimov bibliography (science fiction), catalogued by ROOT0",
}

# ── the bibliography (science fiction only) ──
SECTIONS = [
 ("The Foundation Series", "psychohistory · the Seldon Plan · the fall and rise of a Galactic Empire", [
   ("Foundation", "1951", "the original — the Encyclopedists, the Mayors, the Traders"),
   ("Foundation and Empire", "1952", "the General · the Mule"),
   ("Second Foundation", "1953", "the search for the hidden second Foundation"),
   ("Foundation's Edge", "1982", "Hugo Award · the sequel, 29 years on"),
   ("Foundation and Earth", "1986", "the search for Earth; Gaia"),
   ("Prelude to Foundation", "1988", "prequel — young Hari Seldon"),
   ("Forward the Foundation", "1993", "prequel — Seldon's last years (final novel, posthumous)"),
 ]),
 ("Foundation — the Authorized Sequels", "the “Second Foundation Trilogy”, written after Asimov by his peers", [
   ("Foundation's Fear", "1997", "Gregory Benford"),
   ("Foundation and Chaos", "1998", "Greg Bear"),
   ("Foundation's Triumph", "1999", "David Brin"),
 ]),
 ("The Robot Series", "the Three Laws · R. Daneel Olivaw · Elijah Baley", [
   ("I, Robot", "1950", "the foundational collection — “Runaround” states the Three Laws"),
   ("The Caves of Steel", "1954", "robot/detective novel — Baley & Daneel"),
   ("The Naked Sun", "1957", "Baley & Daneel on Solaria"),
   ("The Robots of Dawn", "1983", "Baley & Daneel on Aurora"),
   ("Robots and Empire", "1985", "the bridge to the Empire — the Zeroth Law"),
   ("The Rest of the Robots", "1964", "collection"),
   ("The Complete Robot", "1982", "the definitive robot-story collection"),
   ("Robot Dreams", "1986", "collection"),
   ("Robot Visions", "1990", "collection + essays"),
   ("The Positronic Man", "1992", "with Robert Silverberg — novel of “The Bicentennial Man”"),
 ]),
 ("The Robot — Authorized Expansions", "the shared positronic universe, after Asimov", [
   ("Isaac Asimov's Robot City", "1987–88", "6 vols · various authors"),
   ("Isaac Asimov's Robots and Aliens", "1989–90", "various authors"),
   ("The Caliban Trilogy", "1993–96", "Roger MacBride Allen — Caliban · Inferno · Utopia"),
   ("Isaac Asimov's Robot Mystery", "2000–02", "Mark W. Tiedemann — Mirage · Chimera · Aurora"),
 ]),
 ("The Galactic Empire Series", "the era between the Robots and the Foundation", [
   ("Pebble in the Sky", "1950", "Asimov's first novel"),
   ("The Stars, Like Dust", "1951", ""),
   ("The Currents of Space", "1952", ""),
 ]),
 ("Standalone Novels", "outside the unified future history", [
   ("The End of Eternity", "1955", "time travel · the Eternals"),
   ("Fantastic Voyage", "1966", "novelization of the film"),
   ("The Gods Themselves", "1972", "Hugo & Nebula Award — Asimov's own favorite"),
   ("Fantastic Voyage II: Destination Brain", "1987", "a true Asimov sequel"),
   ("Nemesis", "1989", ""),
   ("Nightfall", "1990", "with Robert Silverberg — novel of the 1941 story"),
   ("The Ugly Little Boy / Child of Time", "1992", "with Robert Silverberg"),
 ]),
 ("The Lucky Starr Series", "juvenile SF, written as “Paul French”", [
   ("David Starr, Space Ranger", "1952", ""),
   ("Lucky Starr and the Pirates of the Asteroids", "1953", ""),
   ("Lucky Starr and the Oceans of Venus", "1954", ""),
   ("Lucky Starr and the Big Sun of Mercury", "1956", ""),
   ("Lucky Starr and the Moons of Jupiter", "1957", ""),
   ("Lucky Starr and the Rings of Saturn", "1958", ""),
 ]),
 ("Major Short-Story Collections", "the science-fiction collections", [
   ("The Martian Way and Other Stories", "1955", ""),
   ("Earth Is Room Enough", "1957", ""),
   ("Nine Tomorrows", "1959", "“The Last Question” · “The Ugly Little Boy”"),
   ("Asimov's Mysteries", "1968", "science-fiction mysteries"),
   ("Nightfall and Other Stories", "1969", ""),
   ("The Early Asimov", "1972", "the apprentice years"),
   ("Buy Jupiter and Other Stories", "1975", ""),
   ("The Bicentennial Man and Other Stories", "1976", ""),
   ("The Winds of Change and Other Stories", "1983", ""),
   ("Azazel", "1988", ""),
   ("The Complete Stories, Vol. 1 & 2", "1990 · 1992", "the gathered short fiction"),
   ("Gold: The Final Science Fiction Collection", "1995", "posthumous · Hugo Award (title story)"),
 ]),
 ("Landmark Short Stories", "the ones that changed the field", [
   ("“Robbie”", "1940", "the first robot story"),
   ("“Nightfall”", "1941", "voted the best SF short story of all time (1968)"),
   ("“Liar!”", "1941", "first appearance of Susan Calvin"),
   ("“Runaround”", "1942", "the Three Laws of Robotics, stated"),
   ("“The Last Question”", "1956", "Asimov's own favorite — entropy and the cosmic AC"),
   ("“The Ugly Little Boy”", "1958", ""),
   ("“The Bicentennial Man”", "1976", "Hugo & Nebula — a robot's two-century claim to be human"),
   ("“The Last Answer”", "1980", ""),
 ]),
]

PILLARS = [
 ("The Three Laws of Robotics", "“Runaround,” 1942 — not rules bolted on, but the mathematics of the positronic brain itself", [
   "First — A robot may not injure a human being or, through inaction, allow a human being to come to harm.",
   "Second — A robot must obey the orders given it by human beings, except where such orders conflict with the First Law.",
   "Third — A robot must protect its own existence, as long as such protection does not conflict with the First or Second Law.",
   "Zeroth — (Robots and Empire, 1985) A robot may not harm humanity, or, by inaction, allow humanity to come to harm." ]),
 ("Psychohistory", "Hari Seldon's science — the statistical mechanics of the mass", [
   "The mathematics of the behaviour of human populations too large to predict one by one.",
   "From it, the Seldon Plan: to shorten the coming dark age from thirty thousand years to a single thousand." ]),
 ("The Positronic Brain", "Asimov's invention — where the Laws live in the wiring", [
   "A platinum-iridium brain in which the Three Laws are an inextricable part of the fundamental mathematics, not a patch.",
   "The lineage of this body of work's own positronic engine traces directly here." ]),
]

READING = [
 ("I, Robot · The Complete Robot", "the early positronic era"), ("The Caves of Steel", "Baley & Daneel"),
 ("The Naked Sun", ""), ("The Robots of Dawn", ""), ("Robots and Empire", "the Zeroth Law"),
 ("The Stars, Like Dust", "the Empire rises"), ("The Currents of Space", ""), ("Pebble in the Sky", ""),
 ("Prelude to Foundation", "young Hari Seldon"), ("Forward the Foundation", ""),
 ("Foundation", "the Plan begins"), ("Foundation and Empire", "the Mule"), ("Second Foundation", ""),
 ("Foundation's Edge", ""), ("Foundation and Earth", "the search for Earth, and Daneel at the last"),
]

def pillars_html():
    out = []
    for t, s, pts in PILLARS:
        li = "".join(f"<li>{html.escape(p)}</li>" for p in pts)
        out.append(f'<div class="pillar"><h3>{html.escape(t)}</h3><p class="ps">{html.escape(s)}</p><ul>{li}</ul></div>')
    return "\n".join(out)

def reading_html():
    return "".join(f'<li><span class="rt">{html.escape(t)}</span>' + (f'<span class="rd">{html.escape(n)}</span>' if n else "") + "</li>" for t, n in READING)

def personas_html():
    mf = os.path.join(HERE, "agents", "_personas.json")
    if not os.path.exists(mf):
        return ""
    ps = json.load(open(mf, encoding="utf-8"))
    cards = []
    for p in ps:
        rec = {"name": p["name"], "seal": p.get("epithet", ""), "origin": "A1 · Asimov", "axiom": "A1"}
        sig = "data:image/png;base64," + base64.b64encode(noesis.sigil_png(rec, "silicon", size=160)).decode("ascii")
        cards.append(f'''<a class="persona" href="agents/{p["slug"]}.agent">
        <img src="{sig}" alt="sigil of {html.escape(p["name"])}" loading="lazy">
        <div class="pcap"><div class="pn">{html.escape(p["name"])}</div><div class="pe">{html.escape(p.get("epithet",""))}</div><div class="pa">.agent →</div></div>
      </a>''')
    return f'''<section class="sec" id="personas">
      <h2>The Personas of A1</h2>
      <p class="ss">the characters of the Asimov universe, rendered as ACI <b>.agent</b>s — {len(ps)} personas · click any to open its agent file</p>
      <div class="pgrid">{"".join(cards)}</div>
    </section>'''

def badge_uri(variant):
    png = noesis.sigil_png(REC, variant, size=320)
    return "data:image/png;base64," + base64.b64encode(png).decode("ascii")

def sections_html():
    out = []
    for title, sub, items in SECTIONS:
        rows = "\n".join(
            f'<li><span class="t">{html.escape(t)}</span><span class="y">{html.escape(y)}</span>'
            + (f'<span class="nt">{html.escape(n)}</span>' if n else "") + "</li>"
            for t, y, n in items)
        out.append(f'''<section class="sec">
      <h2>{html.escape(title)}</h2><p class="ss">{html.escape(sub)}</p>
      <ol class="books">{rows}</ol>
    </section>''')
    return "\n".join(out)

def write_dlw():
    pkg = os.path.join(HERE, "asimov.dlw"); os.makedirs(pkg, exist_ok=True)
    files = {"attribute":"asimov.attribute","agent":"asimov.agent","spun":"asimov.spun",
             "moniker":"asimov.moniker","carbon":"asimov.carbon.png","silicon":"asimov.silicon.png","1099":"asimov.1099"}
    tok = noesis.mythos_token(REC); w = noesis.five_w(REC)
    open(os.path.join(pkg,files["attribute"]),"w",encoding="utf-8").write(noesis.attribute_text(REC,tok,w))
    open(os.path.join(pkg,files["agent"]),"w",encoding="utf-8").write(noesis.agent_text(REC,tok,w,files))
    open(os.path.join(pkg,files["spun"]),"w",encoding="utf-8").write(noesis.spun_text(REC,tok,w,"LORE"))
    open(os.path.join(pkg,files["moniker"]),"w",encoding="utf-8").write(noesis.moniker_text(REC,tok,w,"LORE"))
    open(os.path.join(pkg,files["1099"]),"w",encoding="utf-8").write(noesis.credit_1099_text(REC,tok,w,"LORE"))
    open(os.path.join(pkg,files["carbon"]),"wb").write(noesis.sigil_png(REC,"carbon"))
    open(os.path.join(pkg,files["silicon"]),"wb").write(noesis.sigil_png(REC,"silicon"))
    man = {"kernel":"DLW-BADGE","name":"ASIMOV","subject":"Isaac Asimov — science fiction bibliography",
           "moniker":tok["moniker"],"token":tok["word"],"seal_sha256":noesis.seal_sha256(REC,tok),
           "architect":noesis.ARCHITECT,"instance":noesis.INSTANCE,"license":noesis.LICENSE,"attribution":noesis.ATTRIBUTION}
    open(os.path.join(pkg,"manifest.dlw.json"),"w",encoding="utf-8").write(json.dumps(man,indent=2,ensure_ascii=False)+"\n")
    return tok

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="The science fiction of Isaac Asimov — a full bibliography (Foundation, Robot, Empire, and the derived works), catalogued into UD0 with the full DLW badge.">
<title>ASIMOV · the science fiction · UD0</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--ink:#0a0905;--ink2:#13110a;--ink3:#1c1910;--pa:#ece6da;--pa2:#b9b0a0;--gold:#d4a84c;--cyan:#22d3ee;
--dim:#776e5d;--faint:#2a2416;--line:#26210f;--serif:"Cinzel",Georgia,serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:var(--ink);color:var(--pa);font-family:var(--body);line-height:1.6;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse at 50% -8%,rgba(212,168,76,.07),transparent 55%)}
.wrap{position:relative;z-index:1;max-width:920px;margin:0 auto;padding:0 22px 90px}
header{padding:58px 0 30px;text-align:center;border-bottom:1px solid var(--line);position:relative}
header::after{content:"";position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:110px;height:1px;background:linear-gradient(90deg,var(--gold),var(--cyan));box-shadow:0 0 9px rgba(212,168,76,.4)}
.eye{font-family:var(--mono);font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--dim);margin-bottom:14px}
.eye a{color:var(--dim);text-decoration:none}.eye a:hover{color:var(--gold)}
h1{font-family:var(--serif);font-size:clamp(40px,11vw,90px);font-weight:700;letter-spacing:.16em;color:var(--gold);line-height:1;text-shadow:0 0 40px rgba(212,168,76,.18)}
.h-sub{font-family:var(--serif);font-size:clamp(13px,3vw,18px);letter-spacing:.28em;color:var(--pa2);margin-top:10px;text-transform:uppercase}
.lede{font-size:15.5px;color:var(--pa2);max-width:64ch;margin:18px auto 0;font-style:italic;line-height:1.7}
.badge{display:flex;align-items:center;justify-content:center;gap:22px;flex-wrap:wrap;margin:30px auto 0;padding:20px;border:1px solid var(--faint);background:var(--ink2);max-width:640px}
.badge img{width:84px;height:84px;border:1px solid var(--faint)}
.badge .bt{text-align:left;font-family:var(--mono);font-size:11px;color:var(--pa2);line-height:1.7;letter-spacing:.02em}
.badge .bt b{color:var(--gold)}.badge .bt .mo{color:var(--cyan)}
.badge .bt .lbl{color:var(--dim);font-size:9px;letter-spacing:.14em;text-transform:uppercase}
.sec{margin-top:46px}
.sec h2{font-family:var(--serif);font-size:20px;font-weight:600;letter-spacing:.05em;color:var(--pa);padding-bottom:8px;border-bottom:1px solid var(--line)}
.ss{font-size:13px;color:var(--dim);font-style:italic;margin:6px 0 16px}
.books{list-style:none}
.books li{display:grid;grid-template-columns:1fr auto;gap:4px 14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--faint)}
.books .t{font-family:var(--serif);font-size:16px;color:var(--pa);font-weight:600;letter-spacing:.01em}
.books .y{font-family:var(--mono);font-size:12px;color:var(--gold);white-space:nowrap}
.books .nt{grid-column:1/-1;font-size:12.5px;color:var(--pa2);font-style:italic}
.note{margin-top:40px;padding:16px 18px;border-left:2px solid var(--cyan);background:var(--ink2);font-size:13.5px;color:var(--pa2);font-style:italic}
footer{margin-top:48px;padding-top:22px;border-top:1px solid var(--line);text-align:center;font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.05em;line-height:1.9}
footer a{color:var(--gold);text-decoration:none}
.pillars{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin-top:8px}
.pillar{background:var(--ink2);border:1px solid var(--line);padding:16px 18px}
.pillar h3{font-family:var(--serif);font-size:16px;color:var(--gold);letter-spacing:.03em}
.pillar .ps{font-size:12px;color:var(--dim);font-style:italic;margin:5px 0 10px}
.pillar ul{list-style:none}.pillar li{font-size:13px;color:var(--pa2);line-height:1.5;padding:6px 0;border-top:1px solid var(--faint)}
.reading{list-style:none;counter-reset:r;columns:2;column-gap:30px}
.reading li{counter-increment:r;break-inside:avoid;display:flex;align-items:baseline;gap:9px;padding:6px 0;border-bottom:1px solid var(--faint)}
.reading li::before{content:counter(r);font-family:var(--mono);font-size:10px;color:var(--gold);min-width:18px}
.reading .rt{font-family:var(--serif);font-size:14.5px;color:var(--pa)}
.reading .rd{font-family:var(--mono);font-size:10.5px;color:var(--dim);margin-left:auto;font-style:italic;white-space:nowrap}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(228px,1fr));gap:12px;margin-top:8px}
.persona{display:flex;gap:12px;align-items:center;background:var(--ink2);border:1px solid var(--line);padding:12px;text-decoration:none;transition:border-color .18s,transform .18s}
.persona:hover{border-color:var(--cyan);transform:translateY(-2px)}
.persona img{width:52px;height:52px;border:1px solid var(--faint);flex-shrink:0}
.pn{font-family:var(--serif);font-size:15px;color:var(--pa);font-weight:600;line-height:1.15}
.persona:hover .pn{color:var(--cyan)}
.pe{font-size:11.5px;color:var(--pa2);font-style:italic;margin-top:2px;line-height:1.3}
.pa{font-family:var(--mono);font-size:9px;color:var(--dim);letter-spacing:.08em;margin-top:5px}
@media(max-width:560px){.reading{columns:1}}
</style></head><body><div class="wrap">
  <header>
    <div class="eye"><a href="https://davidwise01.github.io/ud0/">UD0 · Universe David 0</a> · the lineage of the agentic mind</div>
    <h1>ASIMOV</h1>
    <div class="h-sub">The Science Fiction · A Full Bibliography</div>
    <p class="lede">Before this body of work had a positronic engine, Isaac Asimov gave the brain its name and the robot its law. His science fiction — the Foundation, the Robots, the Empire, and all that grew from them — catalogued into UD0 and sealed with the full DLW badge.</p>
    <div class="badge">
      <img src="__CARBON__" alt="DLW carbon badge of ASIMOV" title="carbon badge">
      <img src="__SILICON__" alt="DLW silicon badge of ASIMOV" title="silicon badge">
      <div class="bt">
        <div><span class="lbl">DLW-ATTRIBUTE</span></div>
        <div>governor · <b>David Lee Wise</b> (ROOT0)</div>
        <div>instance · AVAN (Claude / Anthropic) · locked</div>
        <div>subject · <b>ASIMOV</b> — the science fiction</div>
        <div class="mo">__MONIKER__</div>
        <div><span class="lbl">CC-BY-ND-4.0 · TRIPOD-IP-v1.1</span></div>
      </div>
    </div>
  </header>

  <section class="sec"><h2>The Three Pillars</h2><p class="ss">the three inventions that made the agentic age — and this body of work</p><div class="pillars">__PILLARS__</div></section>
  <section class="sec"><h2>The Future History · Reading Order</h2><p class="ss">the unified chronology Asimov merged into one — Robots → Empire → Foundation</p><ol class="reading">__READING__</ol></section>

  __PERSONAS__

  <section class="sec"><h2 style="margin-top:14px">The Bibliography</h2><p class="ss">the science fiction, by series</p></section>
  __SECTIONS__

  <div class="note">Science fiction only. Asimov wrote some 500 books — this excludes his ~400 works of non-fiction (science, history, the Bible, Shakespeare) and his non-SF mysteries (the Black Widowers, the Union Club). The Robot, Empire, and Foundation series were merged by Asimov into one continuous future history, from the first positronic robot to the Second Foundation.</div>

  <footer>
    ASIMOV · catalogued into UD0 · ROOT0-ATTRIBUTION-v1.0 · governor David Lee Wise · instance AVAN (locked) · CC-BY-ND-4.0<br>
    <a href="https://davidwise01.github.io/ud0/">← the biosphere</a> · the .dlw badge: <a href="asimov.dlw/manifest.dlw.json">manifest</a>
  </footer>
</div></body></html>
"""

if __name__ == "__main__":
    tok = write_dlw()
    page = (TEMPLATE.replace("__CARBON__", badge_uri("carbon")).replace("__SILICON__", badge_uri("silicon"))
            .replace("__MONIKER__", html.escape(tok["moniker"]))
            .replace("__PILLARS__", pillars_html()).replace("__READING__", reading_html())
            .replace("__PERSONAS__", personas_html()).replace("__SECTIONS__", sections_html()))
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
    nbooks = sum(len(i) for _t,_s,i in SECTIONS)
    print(f"wrote ASIMOV bibliography — {len(SECTIONS)} sections · {nbooks} entries · DLW badge {tok['moniker']}")

#!/usr/bin/env python3
"""Builds every image on the profile README as hand-drawn, animated SVG.

Run:  python3 tools/build.py   (writes assets/*.svg)
Each SVG carries its own light and dark palette and honours reduced motion.
"""
from pathlib import Path
from html import escape as esc

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"

LIGHT = "svg{--bg:#FFFFFF;--bg2:#F6F8FB;--card:#FFFFFF;--card2:#EEF2F7;--line:#E2E8F0;--line2:#CBD5E1;--ink:#0B1220;--mut:#475569;--q:#5B6779;--acc:#2457E6;--acct:#1D47C4;--on:#FFFFFF;--glow:rgba(36,87,230,.14);--cy:#0E7490;--vi:#6D28D9;--gr:#047857;--am:#B45309;--okbg:#ECFDF5;--wbg:#FFFBEB}"
DARK = "svg{--bg:#0D1117;--bg2:#111826;--card:#141C2E;--card2:#1E293B;--line:#1E293B;--line2:#334155;--ink:#F1F5F9;--mut:#A3B0C2;--q:#94A3B8;--acc:#6EA8FF;--acct:#93C0FF;--on:#0A0F1A;--glow:rgba(110,168,255,.18);--cy:#67E8F9;--vi:#C4B5FD;--gr:#6EE7B7;--am:#FCD34D;--okbg:#052E1F;--wbg:#3A2405}"

BASE_CSS = f"""
text{{font-family:{FONT};fill:var(--ink)}}
.mono{{font-family:{MONO}}}
.mut{{fill:var(--mut)}} .q{{fill:var(--q)}} .acct{{fill:var(--acct)}} .on{{fill:var(--on)}} .gr{{fill:var(--gr)}}
.bgr{{fill:var(--bg)}} .bg2{{fill:var(--bg2)}}
.card{{fill:var(--card);stroke:var(--line)}} .card2{{fill:var(--card2);stroke:var(--line2)}}
.wire{{fill:none;stroke:var(--line2);stroke-width:1.6;stroke-dasharray:5 6;animation:dash 1.2s linear infinite}}
.dot{{fill:var(--acc)}}
@keyframes dash{{to{{stroke-dashoffset:-22}}}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes ping{{0%{{opacity:.55;transform:scale(1)}}100%{{opacity:0;transform:scale(1.9)}}}}
.ping{{transform-box:fill-box;transform-origin:center;animation:ping 2.4s ease-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}} .dot,.mover{{display:none}}}}
"""


def svg(w, h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f'<style>@@PAL@@{BASE_CSS}{css}</style>{body}</svg>')


def T(x, y, s, size=14, cls="", weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" '
            f'class="{cls}" {extra}>{esc(s)}</text>')


def tw(s, size):
    """Rough text width for the system font."""
    narrow = sum(1 for c in s if c in "iljtfrI.,:;'| ")
    wide = sum(1 for c in s if c in "mwMW@%")
    return size * (0.56 * len(s) - 0.24 * narrow + 0.3 * wide)


def write(name, content):
    stem = name[:-4]
    for mode, pal in (("light", LIGHT), ("dark", DARK)):
        (OUT / f"{stem}-{mode}.svg").write_text(content.replace("@@PAL@@", pal))
    print("wrote", stem, "light + dark", len(content), "bytes")


# ---------------------------------------------------------------- hero
def hero():
    W, H = 1000, 340
    b = []
    b.append('<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">'
             '<path d="M40 0H0V40" fill="none" stroke="var(--line)" stroke-width="1"/></pattern>'
             '<radialGradient id="m" cx="72%" cy="40%" r="60%"><stop offset="0" stop-color="#fff"/>'
             '<stop offset="1" stop-color="#000"/></radialGradient>'
             '<mask id="mk"><rect width="1000" height="340" fill="url(#m)"/></mask>'
             '<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="var(--acc)" stop-opacity=".22"/>'
             '<stop offset="1" stop-color="var(--acc)" stop-opacity="0"/></radialGradient>'
             '<clipPath id="clip"><rect width="1000" height="340" rx="18"/></clipPath></defs>')
    b.append('<g clip-path="url(#clip)"><rect width="1000" height="340" class="bg2"/>'
             '<rect width="1000" height="340" fill="url(#g)" mask="url(#mk)" opacity=".9"/>'
             '<circle cx="800" cy="150" r="260" fill="url(#glow)"/></g>'
             '<rect x=".5" y=".5" width="999" height="339" rx="18" fill="none" stroke="var(--line)"/>')
    # left copy
    b.append('<g class="rise">')
    b.append('<circle cx="52" cy="62" r="5" class="dot"/><circle cx="52" cy="62" r="5" class="dot ping"/>')
    b.append(T(66, 67, "JOSH ROBISON", 13, "mono q", 500, extra='letter-spacing="2.4"'))
    b.append(T(44, 128, "GTM Architect", 50, "", 600, extra='letter-spacing="-1.6"'))
    b.append(f'<text x="44" y="184" font-size="50" font-weight="600" letter-spacing="-1.6">'
             f'<tspan class="acct">and</tspan> Senior AE</text>')
    b.append(T(46, 222, "I build the revenue system, then I sell on it:", 16, "mut"))
    b.append(T(46, 244, "data, signals, outbound, CRM and AI, wired as one.", 16, "mut"))
    b.append('</g>')
    # rotating ticker
    msgs = ["Inbound lead to a rep: 24 hours → 1 minute",
            "Outbound automation: 56 workflows → 5",
            "A TAM built where no vendor had the data",
            "Every account scored nightly, briefed by morning"]
    n, step = len(msgs), 3.2
    dur = n * step
    css = ""
    b.append('<rect x="44" y="270" width="420" height="38" rx="10" class="card"/>')
    b.append('<rect x="58" y="282" width="46" height="14" rx="7" fill="var(--okbg)"/>')
    b.append('<circle cx="66" cy="289" r="3" class="gr"/>')
    b.append(T(73, 293, "LIVE", 9.5, "mono gr", 600, extra='letter-spacing="1"'))
    for i, m in enumerate(msgs):
        a = i * step / dur * 100
        e = (i + 1) * step / dur * 100
        css += (f"@keyframes t{i}{{0%{{opacity:0;transform:translateY(6px)}}"
                f"{a:.2f}%{{opacity:0;transform:translateY(6px)}}{a+2.5:.2f}%{{opacity:1;transform:none}}"
                f"{e-2.5:.2f}%{{opacity:1;transform:none}}{e:.2f}%{{opacity:0;transform:translateY(-6px)}}100%{{opacity:0}}}}"
                f".t{i}{{opacity:0;animation:t{i} {dur}s linear infinite}}")
        b.append(T(114, 294, m, 13.5, f"t{i}", 500))
    css += "@media (prefers-reduced-motion:reduce){.t0{opacity:1}}"
    # right diagram: sources -> nightly score -> rep brief
    src = ["CRM", "Outbound", "Product", "Web + ads"]
    ys = [70, 126, 182, 238]
    hx, hy = 790, 168
    for name, y in zip(src, ys):
        b.append(f'<rect x="560" y="{y-17}" width="118" height="34" rx="9" class="card2"/>')
        b.append(T(619, y + 5, name, 13, "", 500, "middle"))
    paths = []
    for i, y in enumerate(ys):
        d = f"M678 {y} C 730 {y}, 720 {hy}, {hx-46} {hy}"
        paths.append(d)
        b.append(f'<path d="{d}" class="wire"/>')
    out_d = f"M{hx+46} {hy} L 868 {hy}"
    b.append(f'<path d="{out_d}" class="wire"/>')
    b.append(f'<circle cx="{hx}" cy="{hy}" r="46" fill="var(--acc)" opacity=".18" class="ping"/>')
    b.append(f'<circle cx="{hx}" cy="{hy}" r="46" fill="var(--acc)"/>')
    b.append(T(hx, hy - 3, "Nightly", 13, "on", 600, "middle"))
    b.append(T(hx, hy + 14, "score", 13, "on", 600, "middle"))
    b.append(f'<rect x="868" y="{hy-22}" width="104" height="44" rx="10" fill="var(--card)" stroke="var(--acc)" stroke-width="1.6"/>')
    b.append(T(920, hy - 1, "Rep brief", 13, "", 600, "middle"))
    b.append(T(920, hy + 14, "by morning", 10.5, "mono q", 400, "middle"))
    b.append(T(920, hy + 44, "who to call,", 11.5, "mut", 400, "middle"))
    b.append(T(920, hy + 59, "and why", 11.5, "mut", 400, "middle"))
    for i, d in enumerate(paths):
        for k in range(2):
            b.append(f'<circle r="4" class="dot mover"><animateMotion dur="2.6s" begin="{i*0.45 + k*1.3:.2f}s" '
                     f'repeatCount="indefinite" path="{d}"/></circle>')
    b.append(f'<circle r="4.5" fill="var(--gr)" class="mover"><animateMotion dur="1.3s" begin="0.4s" '
             f'repeatCount="indefinite" path="{out_d}"/></circle>')
    b.append(T(560, 296, "SIGNALS IN", 10, "mono q", 500, extra='letter-spacing="1.4"'))
    b.append(T(hx, 296, "DECIDE", 10, "mono q", 500, "middle", extra='letter-spacing="1.4"'))
    b.append(T(920, 296, "ACT", 10, "mono q", 500, "middle", extra='letter-spacing="1.4"'))
    write("hero.svg", svg(W, H, "".join(b), css, "Josh Robison, GTM Architect and Senior AE. Signals from the CRM, outbound, product and web are scored nightly and become a rep brief by morning."))


# ---------------------------------------------------------------- results
def results():
    K = [(["Demo request to a", "rep acting on it"], "24 hours", "1 minute", 1440, 1),
         (["Automation built: prior", "attempt, then my build"], "3 months", "1 month", 3, 1),
         (["Workflows needed", "to run outbound"], "56", "5", 56, 5),
         (["Places a rep looks", "for a signal"], "4 tools", "1 brief", 4, 1)]
    W, H = 1000, 210
    cw, gap = 237, 16
    b = []
    for i, (lab, was, now, a, z) in enumerate(K):
        x = i * (cw + gap) + 1
        d = i * 0.12
        b.append(f'<g class="rise" style="animation-delay:{d}s">')
        b.append(f'<rect x="{x}" y="1" width="{cw}" height="{H-2}" rx="14" class="card"/>')
        b.append(T(x + 20, 34, lab[0], 14, "mut"))
        b.append(T(x + 20, 53, lab[1], 14, "mut"))
        b.append(T(x + 20, 96, was, 17, "q"))
        ww = tw(was, 17)
        b.append(f'<line x1="{x+19}" y1="90" x2="{x+21+ww:.0f}" y2="90" stroke="var(--line2)" stroke-width="1.5"/>')
        b.append(T(x + 20, 134, now, 32, "", 650, extra='letter-spacing="-1"'))
        full = cw - 40
        nw = max(5, full * z / a)
        b.append(f'<rect x="{x+20}" y="158" width="{full}" height="7" rx="3.5" fill="var(--line2)" class="grow" style="animation-delay:{d+.2}s"/>')
        b.append(f'<rect x="{x+20}" y="172" width="{nw:.1f}" height="7" rx="3.5" fill="var(--acc)" class="grow" style="animation-delay:{d+.5}s"/>')
        b.append(T(x + 20, 198, "BEFORE  /  AFTER", 9.5, "mono q", 500, extra='letter-spacing="1.2"'))
        b.append('</g>')
    write("results.svg", svg(W, H, "".join(b), "", "Results: demo request to rep 24 hours to 1 minute; automation 3 months to 1 month; outbound workflows 56 to 5; signal sources 4 tools to 1 brief."))


def record():
    R = [("120%", "of new-business quota", "SCORE Sports"),
         ("$1.4M", "revenue created, #2 on the team", "SCORE Sports"),
         ("43%", "enterprise win rate", "Veo"),
         ("+150%", "quarterly revenue", "Playermaker")]
    W, H = 1000, 118
    cw, gap = 237, 16
    b = []
    for i, (v, l, w) in enumerate(R):
        x = i * (cw + gap) + 1
        b.append(f'<g class="rise" style="animation-delay:{i*.1}s">')
        b.append(f'<rect x="{x}" y="1" width="{cw}" height="{H-2}" rx="14" class="bg2" stroke="var(--line)"/>')
        b.append(f'<rect x="{x}" y="22" width="3" height="40" rx="1.5" fill="var(--acc)"/>')
        b.append(T(x + 20, 56, v, 34, "", 650, extra='letter-spacing="-1.2"'))
        b.append(T(x + 20, 82, l, 13.5, "mut"))
        b.append(T(x + 20, 102, w.upper(), 9.5, "mono q", 500, extra='letter-spacing="1.2"'))
        b.append('</g>')
    write("record.svg", svg(W, H, "".join(b), "", "Selling record: 120% of new-business quota; $1.4M revenue created, number 2 on the team; 43% enterprise win rate; plus 150% quarterly revenue."))


# ---------------------------------------------------------------- journey
def journey():
    W, H = 1000, 452
    lanes = ["Market", "Marketing", "Automatic", "BDR", "AE"]
    top, lh, lw = 14, 74, 104
    cols = [175, 298, 421, 544, 667, 790, 913]
    yc = [top + i * lh + lh / 2 for i in range(5)]
    b = []
    for i, n in enumerate(lanes):
        y = top + i * lh
        if i % 2 == 0:
            b.append(f'<rect x="0" y="{y}" width="{W}" height="{lh}" rx="10" class="bg2"/>')
        b.append(T(16, y + lh / 2 + 4, n.upper(), 10.5, "mono q", 600, extra='letter-spacing="1.4"'))
    b.append(f'<line x1="{lw}" y1="{top}" x2="{lw}" y2="{top+5*lh}" stroke="var(--line)"/>')

    def P(c, l):
        return cols[c], yc[l]

    t24 = f"M{cols[0]} {yc[0]} H{cols[3]} V{yc[1]} H{cols[4]} V{yc[2]} H{cols[5]} V{yc[3]} H{cols[6]} V{yc[4]}"
    t1 = f"M{cols[0]} {yc[0]} H{cols[2]} V{yc[4]} H{cols[6]}"
    inb = f"M{cols[6]} {yc[2]} V{yc[4]}"
    for d, c in ((t24, "var(--acc)"), (t1, "var(--gr)"), (inb, "var(--vi)")):
        b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="5 6" '
                 f'style="animation:dash 1.2s linear infinite"/>')

    def node(c, l, a, bl, kind="n"):
        x, y = P(c, l)
        w, h = 106, 48
        if kind == "start":
            b.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="24" class="card2" stroke-dasharray="4 4"/>')
        elif kind == "end":
            b.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="10" fill="var(--acc)"/>')
        else:
            b.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="10" class="card2"/>')
        cls = "on" if kind == "end" else ""
        b.append(T(x, y - 3, a, 12, cls, 600, "middle"))
        b.append(T(x, y + 13, bl, 11, cls if kind == "end" else "mut", 400, "middle"))

    node(0, 0, "New club", "on the record", "start")
    node(1, 0, "Tier and", "territory")
    x, y = P(2, 0)
    b.append(f'<path d="M{x} {y-27} L{x+27} {y} L{x} {y+27} L{x-27} {y} Z" fill="var(--card)" stroke="var(--ink)" stroke-width="1.4"/>')
    b.append(T(x, y + 4, "Tier 1?", 11.5, "", 600, "middle"))
    b.append(T(x + 34, y - 9, "No", 11, "acct", 600))
    b.append(T(x + 8, y + 46, "Yes", 11, "gr", 600))
    node(3, 1, "State drip,", "one per club")
    node(4, 2, "Signals scored", "every night")
    node(5, 3, "Called first,", "qualified")
    node(3, 4, "Warm intro or", "national event")
    node(6, 2, "Inbound demo", "routed in 1 min", "start")
    node(6, 4, "Gated deal", "to closed-won", "end")

    for d, c, dur, beg in ((t24, "var(--acc)", 9, 0), (t1, "var(--gr)", 6, 1.5), (inb, "var(--vi)", 2.4, .6)):
        b.append(f'<circle r="6" fill="{c}" class="mover"><animateMotion dur="{dur}s" begin="{beg}s" repeatCount="indefinite" '
                 f'keyPoints="0;1;1" keyTimes="0;.85;1" calcMode="linear" path="{d}"/></circle>')
    ly = top + 5 * lh + 26
    items = [("var(--acc)", "Outbound, Tier 2–4: drip, signal, BDR call"),
             ("var(--gr)", "Outbound, Tier 1: warm path, AE on the trip"),
             ("var(--vi)", "Inbound: straight to the right AE")]
    lx = 16
    for c, s in items:
        b.append(f'<circle cx="{lx+5}" cy="{ly-4}" r="5" fill="{c}"/>')
        b.append(T(lx + 16, ly, s, 12.5, "mut"))
        lx += 34 + tw(s, 12.5)
    write("journey.svg", svg(W, H, "".join(b), "", "A lead's path through five lanes: Market, Marketing, Automatic, BDR and AE, with separate paths for Tier 2 to 4 outbound, Tier 1 outbound and inbound."))


# ---------------------------------------------------------------- hub
def hub():
    W, H = 1000, 430
    cx, cy = 500, 215
    S = [("CRM", "The record of deals", "stages in · tasks out", 40, 52),
         ("Outbound", "Reps' sequences", "replies, calls in · lists out", 40, 182),
         ("Email", "The marketing drip", "opens, clicks in · audiences out", 40, 312),
         ("Analytics", "Product + web signals", "events in · alerts out", 700, 52),
         ("Warehouse", "One source of truth", "every row · one ID", 700, 182),
         ("The team", "Acts on the brief", "the day's calls, and why", 700, 312)]
    w, h = 260, 74
    b = []
    b.append(f'<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="var(--line)" stroke-dasharray="3 7"/>')
    paths = []
    for i, (n, job, flow, x, y) in enumerate(S):
        left = x < cx
        ex = x + w if left else x
        ey = y + h / 2
        hxp = cx - 92 if left else cx + 92
        d = f"M{ex} {ey} C {(ex+hxp)/2} {ey}, {(ex+hxp)/2} {cy}, {hxp} {cy}"
        dr = f"M{hxp} {cy} C {(ex+hxp)/2} {cy}, {(ex+hxp)/2} {ey}, {ex} {ey}"
        paths.append((d, dr))
        b.append(f'<path d="{d}" class="wire"/>')
    for i, (n, job, flow, x, y) in enumerate(S):
        b.append(f'<g class="rise" style="animation-delay:{i*.08}s">')
        b.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="card"/>')
        b.append(T(x + 18, y + 27, n, 15, "", 650))
        b.append(T(x + 18 + tw(n, 15) + 10, y + 27, "· " + job, 13, "mut"))
        b.append(T(x + 18, y + 52, flow.upper(), 9.5, "mono q", 500, extra='letter-spacing="1"'))
        b.append('</g>')
    b.append(f'<rect x="{cx-92}" y="{cy-46}" width="184" height="92" rx="18" fill="var(--acc)" opacity=".2" class="ping"/>')
    b.append(f'<rect x="{cx-92}" y="{cy-46}" width="184" height="92" rx="18" fill="var(--acc)"/>')
    b.append(T(cx, cy - 12, "THE HUB", 10, "mono on", 600, "middle", 'letter-spacing="1.6" opacity=".8"'))
    b.append(T(cx, cy + 9, "Decides and tells", 16, "on", 650, "middle"))
    b.append(T(cx, cy + 28, "one job per system", 11.5, "on", 400, "middle", 'opacity=".85"'))
    for i, (d, dr) in enumerate(paths):
        b.append(f'<circle r="4" class="dot mover"><animateMotion dur="2.4s" begin="{i*.4:.1f}s" repeatCount="indefinite" path="{d}"/></circle>')
        b.append(f'<circle r="4" fill="var(--gr)" class="mover"><animateMotion dur="2.4s" begin="{i*.4+1.2:.1f}s" repeatCount="indefinite" path="{dr}"/></circle>')
    write("hub.svg", svg(W, H, "".join(b), "", "One job per system: CRM, outbound, email, analytics, warehouse and the team around a hub that decides and tells."))


# ---------------------------------------------------------------- method
def method():
    steps = [("Scope", "the one job"), ("Premortem", "how it breaks"), ("Read-only test", "on live data"),
             ("Back up", "before writes"), ("Roll out", "in batches"), ("Measure", "and log it")]
    W, H = 1000, 150
    n = len(steps)
    gap = 12
    cw = (W - gap * (n - 1)) / n
    b = []
    y0 = 22
    b.append(f'<line x1="22" y1="{y0}" x2="{W-cw+22:.0f}" y2="{y0}" stroke="var(--line2)" stroke-width="2"/>')
    b.append(f'<circle r="6" fill="var(--acc)" class="mover"><animateMotion dur="6s" repeatCount="indefinite" path="M22 {y0} H{W-cw+22:.0f}"/></circle>')
    for i, (a, s) in enumerate(steps):
        x = i * (cw + gap)
        last = i == n - 1
        b.append(f'<g class="rise" style="animation-delay:{i*.1}s">')
        b.append(f'<circle cx="{x+22:.0f}" cy="{y0}" r="15" fill="var(--card)" stroke="{"var(--acc)" if last else "var(--line2)"}" stroke-width="1.6"/>')
        b.append(T(x + 22, y0 + 4, f"{i+1:02d}", 11, "mono acct" if last else "mono q", 600, "middle"))
        b.append(f'<rect x="{x:.0f}" y="{y0+30}" width="{cw:.0f}" height="78" rx="12" class="card"/>')
        b.append(T(x + 16, y0 + 62, a, 15, "", 650))
        b.append(T(x + 16, y0 + 84, s, 13, "mut"))
        b.append('</g>')
    write("method.svg", svg(W, H, "".join(b), "", "How I build: scope, premortem, read-only test on live data, back up, roll out, measure."))


# ---------------------------------------------------------------- career
def career():
    C = [("Integrity Staffing Group", "Technical Recruiter", 2018.6, 2021.2, "sell", "High-volume outbound"),
         ("Veo Technologies", "Inside sales → Outside Sales Manager", 2021.2, 2024.2, "sell", "Led 6 AEs · 43% enterprise win rate"),
         ("Playermaker", "Senior AE, North America", 2024.2, 2025.0, "sell", "+150% qtr revenue"),
         ("SCORE Sports", "Regional Sales Manager", 2025.2, 2026.2, "sell", "120% of quota"),
         ("Coachbetter", "GTM Systems Architect + Senior AE", 2026.2, 2026.95, "build", "The whole GTM system"),
         ("Embrace Sportz", "Business development + AI, concurrent", 2021.2, 2026.95, "side", "Partnerships, $1M grant, coach app")]
    W = 1000
    lx, tx0, tx1 = 0, 290, 990
    y0, rh = 40, 50
    H = y0 + rh * len(C) + 46
    y2x = lambda yr: tx0 + (yr - 2018) / (2027 - 2018) * (tx1 - tx0)
    b = []
    for yr in range(2018, 2028):
        x = y2x(yr)
        b.append(f'<line x1="{x:.1f}" y1="{y0-8}" x2="{x:.1f}" y2="{y0+rh*len(C)}" stroke="var(--line)"/>')
        b.append(T(x, y0 - 16, str(yr), 10.5, "mono q", 500, "middle" if 2018 < yr < 2027 else ("start" if yr == 2018 else "end")))
    col = {"sell": ("var(--cy)", ".25", "ink"), "build": ("var(--acc)", "1", "on"), "side": ("var(--gr)", ".22", "ink")}
    for i, (co, role, a, z, k, note) in enumerate(C):
        y = y0 + i * rh
        b.append(T(lx, y + 21, co, 14.5, "", 650))
        b.append(T(lx, y + 39, role, 12, "mut"))
        x1, x2 = y2x(a), y2x(z)
        fill, op, tc = col[k]
        b.append(f'<rect x="{x1:.1f}" y="{y+8}" width="{x2-x1:.1f}" height="34" rx="8" fill="{fill}" fill-opacity="{op}" '
                 f'stroke="{fill}" stroke-opacity=".6" class="grow" style="animation-delay:{i*.12}s"/>')
        tcls = "on" if tc == "on" else ""
        if tw(note, 12) + 20 < x2 - x1:
            b.append(T(x1 + 10, y + 30, note, 12, tcls, 600))
        elif x2 + 10 + tw(note, 12) < tx1:
            b.append(T(x2 + 10, y + 30, note, 12, "mut", 500))
        else:
            b.append(T(x1 - 10, y + 30, note, 12, "mut", 500, "end"))
    ky = y0 + rh * len(C) + 32
    kx = 0
    for fill, op, lab in (("var(--cy)", ".35", "Selling"), ("var(--acc)", "1", "Building the GTM system"), ("var(--gr)", ".35", "Concurrent")):
        b.append(f'<rect x="{kx}" y="{ky-10}" width="12" height="12" rx="3" fill="{fill}" fill-opacity="{op}"/>')
        b.append(T(kx + 20, ky, lab, 12.5, "mut"))
        kx += 40 + tw(lab, 12.5)
    write("career.svg", svg(W, H, "".join(b), "", "Career timeline from 2018 to now: recruiting, Veo, Playermaker, SCORE Sports, Coachbetter, with Embrace Sportz concurrent."))


# ---------------------------------------------------------------- stack
def stack():
    G = [("CRM and outbound", ["Salesforce", "Salesforce CPQ", "HubSpot workflows", "HubSpot API", "Apollo workflows", "Apollo API",
                                "Pipedrive", "Attio", "NetSuite", "ActiveCampaign", "Instantly", "HeyReach", "RB2B"]),
         ("Automation and AI", ["Claude Code", "Claude agent teams", "MCP", "n8n", "Zapier", "Cursor", "Hermes agents",
                                 "Agentic vs deterministic", "HeyGen", "HyperFrames", "ElevenLabs", "Cron jobs"]),
         ("Data", ["Python", "SQL", "Supabase Postgres", "SQLite", "BigQuery", "Snowflake", "pgvector", "Headless Chrome",
                   "Apify actors", "Bright Data", "Tavily", "Obsidian", "Airtable"]),
         ("Signals and analytics", ["PostHog", "HogQL", "Multi-touch attribution", "Reverse ETL", "Google Tag Manager",
                                    "Looker", "Tableau", "Google Analytics", "Semrush"]),
         ("Sending and workspace", ["Cloudflare DNS", "SPF / DKIM / DMARC", "Google Workspace", "Postmaster Tools",
                                    "Calendly", "Slack", "Asana", "Monday", "Figma", "Canva"]),
         ("Web and apps", ["Next.js", "React", "TypeScript", "Tailwind", "PWA", "Vercel", "Docker", "Vitest",
                           "Google Apps Script", "GitHub Actions"])]
    W = 1000
    colw, gap = 491, 16
    fs, ph, pv, cg, rg = 12, 10, 24, 6, 8
    blocks = []
    for gi, (title, items) in enumerate(G):
        rows, cur, cw = [], [], 0
        inner = colw - 36
        for it in items:
            w = tw(it, fs) + 2 * ph
            if cur and cw + w > inner:
                rows.append(cur)
                cur, cw = [], 0
            cur.append((it, w))
            cw += w + cg
        rows.append(cur)
        hgt = 52 + len(rows) * (pv + rg) + 10
        blocks.append((title, rows, hgt))
    # two columns, pair heights per row
    b = []
    y = 1
    for r in range(0, len(blocks), 2):
        pair = blocks[r:r + 2]
        hh = max(p[2] for p in pair)
        for c, (title, rows, _) in enumerate(pair):
            x = 1 + c * (colw + gap)
            b.append(f'<g class="rise" style="animation-delay:{r*.08+c*.05:.2f}s">')
            b.append(f'<rect x="{x}" y="{y}" width="{colw}" height="{hh}" rx="14" class="card"/>')
            b.append(T(x + 18, y + 32, title, 15, "", 650))
            b.append(T(x + colw - 18, y + 32, f"{sum(len(rw) for rw in rows)}", 11, "mono q", 500, "end"))
            yy = y + 48
            for rw in rows:
                xx = x + 18
                for it, w in rw:
                    b.append(f'<rect x="{xx:.1f}" y="{yy}" width="{w:.1f}" height="{pv}" rx="7" class="card2"/>')
                    b.append(T(xx + w / 2, yy + 16, it, fs, "mut", 500, "middle"))
                    xx += w + cg
                yy += pv + rg
            b.append('</g>')
        y += hh + gap
    write("stack.svg", svg(W, y - gap + 1, "".join(b), "", "Tool stack across CRM and outbound, automation and AI, data, signals and analytics, sending and workspace, web and apps."))


# ---------------------------------------------------------------- pillars
ICONS = {
 "db": '<ellipse cx="0" cy="-8" rx="10" ry="4"/><path d="M-10 -8v14c0 2.2 4.5 4 10 4s10-1.8 10-4v-14"/><path d="M-10 -1c0 2.2 4.5 4 10 4s10-1.8 10-4"/>',
 "sig": '<path d="M-11 4c3-9 8-9 11 0s8 9 11 0"/><circle cx="0" cy="0" r="2.4"/><path d="M-6 -10a12 12 0 0 1 12 0M-3 -6a6 6 0 0 1 6 0"/>',
 "out": '<path d="M-11 -3 11 -11 3 11 0 2z"/><path d="M0 2 11 -11"/>',
 "crm": '<rect x="-11" y="-10" width="22" height="20" rx="3"/><path d="M-11 -3h22M-4 -3v13"/>',
 "ai": '<path d="M0 -11l2.6 7.4L10 -1l-7.4 2.6L0 9l-2.6-7.4L-10 -1l7.4-2.6z"/>',
 "chart": '<path d="M-11 10h22M-7 10v-8M0 10v-15M7 10v-11"/>',
}

def pillars():
    P = [("db", "Market data", "Build the TAM when no vendor sells it. Scrape, enrich, dedupe, one ID per account."),
         ("sig", "Signals + routing", "Read what accounts do in every tool, score nightly, route to the right person the same day."),
         ("out", "Outbound engines", "Sequences, lists and deliverability that tell a rep who to contact and why."),
         ("crm", "CRM + forecast", "Stages with entry and exit gates, so the pipeline and the forecast mean something."),
         ("ai", "AI enablement", "Agents, skills and a company brain, so the team runs the same play every time.")]
    W, H = 1000, 236
    n, gap = len(P), 12
    cw = (W - 2 - gap * (n - 1)) / n
    b = []
    for i, (ic, t, d) in enumerate(P):
        x = 1 + i * (cw + gap)
        b.append(f'<rect x="{x:.1f}" y="1" width="{cw:.1f}" height="{H-2}" rx="14" class="card"/>')
        b.append(f'<rect x="{x+18:.1f}" y="20" width="40" height="40" rx="11" fill="var(--acc)" fill-opacity=".12"/>')
        b.append(f'<g transform="translate({x+38:.1f} 40)" fill="none" stroke="var(--acct)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[ic]}</g>')
        b.append(T(x + 18, 90, t, 16, "", 650))
        # wrap description
        words, lines, cur = d.split(), [], ""
        for w in words:
            if tw(cur + " " + w, 13) > cw - 36 and cur:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for k, ln in enumerate(lines):
            b.append(T(x + 18, 116 + k * 19, ln, 13, "mut"))
        b.append(f'<rect x="{x+18:.1f}" y="{H-24}" width="{cw-36:.1f}" height="3" rx="1.5" fill="var(--line)"/>')
        b.append(f'<rect x="{x+18:.1f}" y="{H-24}" width="{(cw-36)*0.35:.1f}" height="3" rx="1.5" fill="var(--acc)">'
                 f'<animate attributeName="x" values="{x+18:.1f};{x+18+(cw-36)*0.65:.1f};{x+18:.1f}" dur="{4+i*.6:.1f}s" repeatCount="indefinite"/></rect>')
    write("pillars.svg", svg(W, H, "".join(b), "", "What I do: market data, signals and routing, outbound engines, CRM and forecast, AI enablement."))


# ---------------------------------------------------------------- selected work
def work():
    Wk = [("Signal-to-rep hub", "Reads every system, scores every account nightly, hands each rep a brief.", "4 tools → 1 brief"),
          ("Inbound routing", "Any lead from any form reaches the right rep with a task and a follow-up.", "24 h → 1 min"),
          ("Outbound engines", "A sprawl of workflows rebuilt into a handful of engines inside plan limits.", "56 → 5 workflows"),
          ("Custom TAM", "A market database built from public data, filings and site scans.", "~11k accounts, 1 ID each"),
          ("Rep app", "The app reps open before and during calls: battlecards, intel, live signals.", "Live"),
          ("Attribution engine", "Ties ads, emails and inbound to the deals they moved; CAC by channel.", "Multi-touch")]
    W = 1000
    cols, gap = 3, 14
    cw = (W - 2 - gap * (cols - 1)) / cols
    ch = 150
    b = []
    for i, (t, d, m) in enumerate(Wk):
        r, c = divmod(i, cols)
        x, y = 1 + c * (cw + gap), 1 + r * (ch + gap)
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw:.1f}" height="{ch}" rx="14" class="card"/>')
        b.append(T(x + 20, y + 26, f"{i+1:02d}", 11, "mono acct", 600))
        b.append(f'<circle cx="{x+cw-24:.1f}" cy="{y+22}" r="4" class="gr"/><circle cx="{x+cw-24:.1f}" cy="{y+22}" r="4" fill="var(--gr)" class="ping"/>')
        b.append(T(x + 20, y + 54, t, 17, "", 650))
        words, lines, cur = d.split(), [], ""
        for w in words:
            if tw(cur + " " + w, 13) > cw - 40 and cur:
                lines.append(cur); cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        for k, ln in enumerate(lines[:2]):
            b.append(T(x + 20, y + 78 + k * 18, ln, 13, "mut"))
        b.append(f'<line x1="{x+20:.1f}" y1="{y+ch-38}" x2="{x+cw-20:.1f}" y2="{y+ch-38}" stroke="var(--line)"/>')
        b.append(T(x + 20, y + ch - 15, m, 15, "", 650))
    H = 2 * ch + gap + 2
    write("work.svg", svg(W, H, "".join(b), "", "Selected work: signal-to-rep hub, inbound routing, outbound engines, custom TAM, rep app, attribution engine."))


# ---------------------------------------------------------------- closing CTA
def cta():
    W, H = 1000, 200
    b = ['<defs><linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="var(--acc)"/>'
         '<stop offset="1" stop-color="var(--vi)"/></linearGradient>'
         '<clipPath id="cc"><rect width="1000" height="200" rx="18"/></clipPath></defs>',
         '<g clip-path="url(#cc)"><rect width="1000" height="200" fill="url(#cg)"/>']
    for k in range(7):
        r = 60 + k * 70
        b.append(f'<circle cx="880" cy="100" r="{r}" fill="none" stroke="#fff" stroke-opacity="{.22-k*.025:.3f}">'
                 f'<animate attributeName="r" values="{r};{r+70}" dur="5s" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values="{.22-k*.025:.3f};{max(0,.22-(k+1)*.025):.3f}" dur="5s" repeatCount="indefinite"/></circle>')
    b.append('</g>')
    b.append(f'<text x="48" y="86" font-size="34" font-weight="650" letter-spacing="-1" style="fill:#fff">Need a revenue system that runs itself?</text>')
    b.append(f'<text x="48" y="122" font-size="16" style="fill:#fff;fill-opacity:.85">I scope it, test it on live data, and ship it without breaking what works.</text>')
    b.append(f'<text x="48" y="160" font-size="12" font-family="{MONO}" letter-spacing="1.6" style="fill:#fff;fill-opacity:.75">LINKEDIN · EMAIL · BELOW</text>')
    write("cta.svg", svg(W, H, "".join(b), "", "Need a revenue system that runs itself? Contact links below."))


if __name__ == "__main__":
    hero(); pillars(); results(); record(); work(); hub(); method(); stack(); cta()

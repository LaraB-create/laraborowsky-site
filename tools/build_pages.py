#!/usr/bin/env python3
"""Generates index.html and about.html for laraborowsky.com from shared parts."""
import html, sys, os

OUT = sys.argv[1]
LI = "https://www.linkedin.com/in/lara-borowsky-52627a161/"
e = html.escape

HEAD_SCRIPT = """<script>(function(){var s={};try{s=JSON.parse(localStorage.getItem('lb-settings')||'{}')||{}}catch(e){}var d=document.documentElement;var dark=s.theme==='dark'||((!s.theme||s.theme==='auto')&&window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches);d.setAttribute('data-theme',dark?'dark':'light');var hc=s.contrast==='high'||((!s.contrast||s.contrast==='auto')&&window.matchMedia&&window.matchMedia('(prefers-contrast: more)').matches);d.setAttribute('data-contrast',hc?'high':'standard');if(s.weight)d.setAttribute('data-weight',s.weight);if(s.font)d.setAttribute('data-font',s.font);if(s.size)d.setAttribute('data-size',s.size);if(s.spacing)d.setAttribute('data-spacing',s.spacing);if(s.motion&&s.motion!=='auto')d.setAttribute('data-motion',s.motion);d.setAttribute('data-depth',s.depth||'tldr');})();</script>"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200;12..96,300;12..96,700;12..96,800&family=Fraunces:ital,opsz,wght@1,9..144,300;1,9..144,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@300;400;500&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet">'

def head(title, desc, path):
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light" data-depth="tldr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#F5F4F0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0E1013" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="https://www.laraborowsky.com{path}">
<link rel="canonical" href="https://www.laraborowsky.com{path}">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
{HEAD_SCRIPT}
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
"""

MOON = '<svg class="moon" aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z"/></svg>'
SUN = '<svg class="sun" aria-hidden="true" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
SLIDERS = '<svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12"/><circle cx="16" cy="6" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="18" r="2"/></svg>'

def header(current):
    def nav(href, label, key):
        cur = ' aria-current="page"' if key == current else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f"""<header class="site-header">
<div class="wrap">
<a class="wordmark" href="/"><span class="b">Lara</span><span class="t">Borowsky</span></a>
<nav class="site-nav" aria-label="Main">
{nav('/#method','Method','method')}
{nav('/#work','Work','work')}
{nav('/about','About','about')}
{nav('/lavalou','Lavalou','lavalou')}
{nav('/contact','Contact','contact')}
<button class="icon-btn theme-btn" type="button" data-action="toggle-theme" aria-label="Switch to dark mode">{MOON}{SUN}</button>
<button class="settings-btn" type="button" data-action="toggle-settings" aria-expanded="false" aria-controls="reading-settings">{SLIDERS} Reading settings</button>
</nav>
</div>
</header>
""" + settings()

def settings():
    groups = [
        ('Theme', 'theme', [('auto', 'Match my device'), ('light', 'Light'), ('dark', 'Dark')]),
        ('Contrast', 'contrast', [('auto', 'Match my device'), ('standard', 'Standard'), ('high', 'High')]),
        ('Text weight', 'weight', [('standard', 'Standard'), ('bold', 'Bolder')]),
        ('Typeface', 'font', [('default', 'Default'), ('dyslexic', 'OpenDyslexic'), ('hyper', 'Hyperlegible')]),
        ('Text size', 'size', [('standard', 'Standard'), ('large', 'Large'), ('xlarge', 'Extra large')]),
        ('Spacing', 'spacing', [('standard', 'Standard'), ('roomy', 'Roomy')]),
        ('Motion', 'motion', [('auto', 'Match my device'), ('on', 'On'), ('off', 'Still')]),
        ('Default depth', 'depth', [('tldr', 'TL;DR'), ('deep', 'Rabbit Hole')]),
    ]
    out = ['<section id="reading-settings" class="settings" aria-label="Reading settings" hidden>', '<div class="wrap">',
           '<p class="settings-intro">Make this site work the way your brain does. Changes apply right away, and stay in this browser only.</p>',
           '<div class="settings-grid">']
    for label, key, opts in groups:
        out.append(f'<fieldset class="setting"><legend>{label}</legend><div class="opts">')
        for val, l in opts:
            out.append(f'<button class="pill" type="button" data-set="{key}" data-val="{val}" aria-pressed="false">{l}</button>')
        out.append('</div></fieldset>')
    out += ['</div>', '<button class="settings-reset" type="button" data-action="reset-settings">Reset to defaults</button>', '</div>', '</section>']
    return '\n'.join(out) + '\n'

def footer(second_link):
    return f"""<footer class="site-footer">
<div class="wrap">
<p class="the-end">The end. (Or is it?)</p>
<p class="display bottom"><span class="b">You've reached the bottom of the rabbit hole.</span> <span class="t">Most people don't. Hi.</span></p>
<div class="footer-links">
<a href="/contact">Say hello →</a>
<a href="{LI}">LinkedIn</a>
{second_link}
<a href="/lavalou">Lavalou →</a>
<a href="/accessibility">Accessibility</a>
</div>
<div class="footer-legal">
<span>© <span data-year>2026</span> Lara Borowsky · Read books. Be kind. Stay weird.</span>
<span>Built with curiosity, Claude, and too many open tabs.</span>
</div>
</div>
</footer>
<script src="/assets/site.js"></script>
</body>
</html>
"""

ORNAMENT = '<div class="ornament" aria-hidden="true"><svg width="120" height="16" viewBox="0 0 120 16" fill="none" stroke="currentColor" stroke-width="1"><path d="M0 8 H46 M74 8 H120"/><path d="M60 2 L66 8 L60 14 L54 8 Z" fill="currentColor"/><circle cx="50" cy="8" r="1.5" fill="currentColor"/><circle cx="70" cy="8" r="1.5" fill="currentColor"/></svg></div>'

DEPTH_SWITCH = """<div class="depth">
<div class="seg" role="group" aria-label="How much detail">
<button type="button" data-set="depth" data-val="tldr" aria-pressed="true">TL;DR</button>
<button type="button" data-set="depth" data-val="deep" aria-pressed="false">Rabbit Hole</button>
</div>
<div class="drink" aria-hidden="true"><span>drink me</span><span>eat me</span></div>
</div>"""

HOLE = """<figure class="hole">
<div class="hole-art">
<svg class="hole-rings" role="img" aria-label="Line drawing looking down a rabbit hole, marked with depths: surface, TL;DR, rabbit hole, footnotes. A rabbit's ears peek over the rim and small objects fall inside." viewBox="0 0 440 440">
<g fill="none" stroke="currentColor" stroke-width="1">
<ellipse cx="220" cy="96" rx="196" ry="42" opacity=".9"/><ellipse cx="220" cy="160" rx="166" ry="35" opacity=".7"/><ellipse cx="220" cy="219" rx="138" ry="29" opacity=".55"/><ellipse cx="220" cy="272" rx="111" ry="23" opacity=".42"/><ellipse cx="220" cy="319" rx="85" ry="18" opacity=".32"/><ellipse cx="220" cy="360" rx="61" ry="13" opacity=".24"/><ellipse cx="220" cy="395" rx="39" ry="8" opacity=".18"/>
<path d="M24 96 L181 395 M416 96 L259 395" opacity=".3"/>
</g>
<ellipse cx="220" cy="219" rx="138" ry="29" fill="none" stroke="var(--accent)" stroke-width="2"/>
<g font-family="JetBrains Mono, monospace" font-size="10" letter-spacing="1.2" fill="var(--muted)">
<text x="430" y="92" text-anchor="end">0 FT · SURFACE</text>
<text x="398" y="223" text-anchor="end" fill="var(--accent-text)">TL;DR</text>
<text x="340" y="323" text-anchor="end">RABBIT HOLE</text>
<text x="292" y="399" text-anchor="end">FOOTNOTES</text>
</g>
</svg>
<svg class="ears" aria-hidden="true" viewBox="0 0 80 70">
<g fill="var(--bg)" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
<path d="M28 58 C18 40 16 16 22 6 C27 -1 34 6 33 18 C32 32 32 44 34 58"/>
<path d="M44 58 C46 42 50 22 58 12 C64 5 72 10 68 20 C63 33 56 46 52 58"/>
<path d="M14 70 C14 56 26 52 40 52 C54 52 66 56 66 70"/>
</g>
<path d="M27 16 C25 28 27 40 30 52 M58 18 C54 30 50 42 48 52" fill="none" stroke="var(--accent)" stroke-width="1" opacity=".7"/>
</svg>
<svg class="fall" aria-hidden="true" viewBox="0 0 40 40" style="left:30%;top:18%;width:9%;animation-delay:0s"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M4 9 C10 6 16 7 20 10 C24 7 30 6 36 9 V32 C30 29 24 30 20 33 C16 30 10 29 4 32 Z"/><path d="M20 10 V33"/></g></svg>
<svg class="fall" aria-hidden="true" viewBox="0 0 40 40" style="left:56%;top:14%;width:8%;animation-delay:-3s"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"><circle cx="20" cy="23" r="12"/><path d="M20 8 V11 M17 6 H23 M20 23 V16 M20 23 L25 26"/></g></svg>
<svg class="fall" aria-hidden="true" viewBox="0 0 40 40" style="left:43%;top:10%;width:7%;animation-delay:-6s"><g fill="none" stroke="var(--accent)" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="20" r="6"/><path d="M17 20 H35 M29 20 V25 M33 20 V24"/></g></svg>
<svg class="fall" aria-hidden="true" viewBox="0 0 40 40" style="left:66%;top:22%;width:8%;animation-delay:-1.5s"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 15 H30 V22 C30 29 25 33 18 33 C11 33 6 29 6 22 Z"/><path d="M30 18 C35 18 36 25 30 26"/><path d="M14 9 C13 7 15 6 14 4 M20 9 C19 7 21 6 20 4"/></g></svg>
<svg class="fall" aria-hidden="true" viewBox="0 0 40 40" style="left:36%;top:26%;width:7%;animation-delay:-4.5s"><rect x="10" y="5" width="20" height="30" rx="2" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M20 15 C18 11 13 13 15 17 L20 22 L25 17 C27 13 22 11 20 15 Z" fill="var(--accent)"/></svg>
<svg class="fall" aria-hidden="true" viewBox="0 0 40 40" style="left:50%;top:30%;width:6%;animation-delay:-7.5s"><g fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"><path d="M12 12 H28 V33 C28 35 26 36 24 36 H16 C14 36 12 35 12 33 Z"/><path d="M11 8 H29 V12 H11 Z"/><path d="M15 22 H25"/></g></svg>
</div>
<figcaption><span>Plate I. Curiouser and curiouser.</span><button class="motion-btn" type="button" data-action="toggle-motion" aria-pressed="false">Pause the falling</button></figcaption>
</figure>"""

CARDS = [
  ('794.8 CLU', 'Lavalou · Games', 'Cluck Quest 1 &amp; 2', 'Built because math practice should involve a jester pumpkin.', 'Two browser games that sneak math and spelling practice into a night of chasing loose chickens. They work offline on an iPad.', 'Read-aloud, grown-up settings, custom spelling lists, and a progress report for the adults. Each game is a single file, so it runs anywhere.', 'Every chicken gets home by sunrise. Every time.', ['HTML', 'Games', 'Accessibility'], ('/lavalou', 'Play them')),
  ('006.3 ACA', 'From the lab', 'Claude Mastery Academy', 'Built because motivation is a design problem.', 'A gamified learning portal I built for myself, complete with XP. It’s where I learn the tools that build the other tools.', 'Phases, quizzes, flashcards, and a deep-dive button on every concept, so curiosity is the curriculum instead of a distraction from it.', 'I learn by falling into things. So I built something worth falling into.', ['React', 'Learning design'], None),
  ('005.1 COD', 'From the lab', 'Coding Academy', 'Built because I wanted to read my own tools, not just use them.', 'A from-scratch coding course I built for myself, from HTML to React in four phases, with quizzes, flashcards, and XP.', 'Every concept has a deep-dive button that explains it for a marketer, not a developer, plus a glossary, a cheat sheet, and free resources for going further.', 'I don’t need to write the code. I need to be capable of reading it.', ['React', 'Learning design'], None),
  ('028.9 LIB', 'Personal · In progress', 'Lara’s Library', 'Built because 150 books a year needs a system.', 'A home library and reading tracker: books, authors, series, tropes, the TBR pile, and stats.', 'A real database underneath, so series, authors and tropes connect to each other instead of living in a very long spreadsheet.', 'Tropes are data. I will not be taking questions.', ['Database', 'In progress'], None),
  ('813.6 IND', 'Personal · Book events', 'Indies Invade Philly', 'Built because a signing with dozens of indie authors is a lot of books to plan for.', 'A preorder portal for an indie author signing event: browse every author, move books from wishlist to final picks, track preorders, and plan the big day.', 'The 2026 version is a single-page web app that remembers your picks in your browser. The 2027 version is in the works: a real site with logins, so friends can keep their own lists.', 'This is what happens when a reader with a spreadsheet habit gets a ticket.', ['HTML', 'Research', 'Excel'], None),
  ('641.5 DIN', 'Personal · Family', 'Dinner Spinner', 'Built because “I don’t know, what do you want?” is not a dinner plan.', 'A kid-friendly wheel that picks where to eat, plus a second spinner for what to make at home.', 'Two wheels, one for going out and one for staying in, built so the kids can spin it themselves.', 'The wheel has the final say. That’s the whole point.', ['HTML', 'Family tools'], None),
  ('741.6 LAV', 'Brand &amp; Design', 'Lavalou Brand Kit', 'Built because my side projects deserved a real brand.', 'A full identity for my creative label: logo, palette, favicons, social images, and a short guide.', 'Vector masters, web and print versions, and color tokens that the Lavalou pages actually use.', 'A little molten. A little strange. The drips are non-negotiable.', ['Brand systems', 'Design'], ('/lavalou', 'See it in use')),
  ('006.7 LAR', 'You are here', 'This website', 'Built because a portfolio should let you choose your own depth.', 'Light and dark modes, three typefaces including OpenDyslexic, adjustable spacing, and a TL;DR or Rabbit Hole version of everything.', 'Plain HTML and CSS, no tracking, and settings that stay in your own browser.', 'Yes, the rabbit is wiggling its ears on purpose.', ['HTML', 'CSS', 'Accessibility'], None),
]

WARREN = """<article class="card warren">
<div class="card-meta"><span>By request</span><span class="accent">Behind the little door</span></div>
<h3>Professional work</h3>
<p class="hook">There’s a little door. Ask me for the golden key.</p>
<p class="summary">Case studies and working demos from my marketing and business development work, rebuilt with made-up data and shared privately with people who ask.</p>
<a class="btn btn-ink" href="https://www.linkedin.com/in/lara-borowsky-52627a161/" style="align-self: flex-start; margin-top: .6rem">Request access →</a>
</article>"""

def card(c):
    call, area, title, hook, tldr, how, note, tags, link = c
    t = ''.join(f'<li>{x}</li>' for x in tags)
    lk = f'<a class="card-link" href="{link[0]}">{link[1]}<span class="sr-only">: {title}</span> <span aria-hidden="true">→</span></a>' if link else ''
    tags_html = f'<ul class="tags" aria-label="Tools">{t}</ul>' 
    return f"""<article class="card">
<div class="card-meta"><span>{call}</span><span class="accent">{area}</span></div>
<h3>{title}</h3>
<p class="hook">{hook}</p>
<p class="summary">{tldr}</p>
<div class="deep">
<h4>How it works</h4><p>{how}</p>
<h4>Margin note</h4><p class="note">{note}</p>
</div>
{lk}
<ul class="tags" aria-label="Tools">{t}</ul>
</article>"""

STEPS = [('01 · 0 ft', 'Fall in', 'Start with the question nobody has time for, and follow it past the point where it’s comfortable.'),
         ('02 · 40 ft', 'Keep receipts', 'Every finding gets a source. If I can’t trace it, it doesn’t go in.'),
         ('03 · 80 ft', 'Build the ladder', 'Turn what I found into a tool someone else can use without me in the room.'),
         ('04 · Surface', 'Climb out', 'Lead with the TL;DR. Leave the burrow open for anyone who wants the footnotes.')]
VERBS = [('01', 'Find', 'Lead Management', 'Surface the opportunities worth a second look.'),
         ('02', 'Screen', 'Go/No-Go Portal', 'Decide which ones to chase, and say why.'),
         ('03', 'Position', 'Positioning Discovery', 'Know what you want to be known for before the RFP drops.'),
         ('04', 'Express', 'Brand Design System', 'Make every deliverable look like it came from the same firm.'),
         ('05', 'Prove', 'Data Portal', 'Back every claim with a record someone can check.')]
NOTES = [('Nutshell', 'Read books. Be kind. Stay weird.'), ('Reading', '150+ books a year. Yes, really.'),
         ('Mode', 'Systems thinker, research nerd, science enthusiast'), ('Building with', 'Claude, ChatGPT, Perplexity, Python, a lot of HTML'),
         ('Approach', 'Human-in-the-loop. Citations or it didn’t happen.'), ('Brain', 'Neurodivergent, curious, frequently three tabs deep')]

def index():
    steps = '\n'.join(f'<li><span class="num">{n}</span><h3>{t}</h3><p>{d}</p></li>' for n, t, d in STEPS)
    verbs = '\n'.join(f'<li><span class="num">{n}</span><h3>{v}</h3><p class="tool">{tool}</p><p>{d}</p></li>' for n, v, tool, d in VERBS)
    notes = '\n'.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in NOTES)
    cards = '\n'.join(card(c) for c in CARDS)
    body = f"""<main id="main">
<div class="wrap hero">
<div class="hero-copy">
<p class="chapter opening-chapter">Chapter the First, <span class="t">in which a marketer follows a question somewhere it probably shouldn’t go</span></p>
<h1 class="display"><span class="b">Six improbable things</span><span class="t">before <span class="accent">breakfast.</span></span></h1>
<p class="opening">Lara was beginning to get very tired of doing the same task twice, and of hunting for answers in folders with no pictures or conversations in them. So when a curious question hopped past, she followed it down the rabbit hole, and climbed back out with a tool instead of a headache.</p>
<p class="lede">I’m a marketing and business development strategist who builds human-in-the-loop AI tools, research systems, and the occasional wildly over-engineered spreadsheet. Curiosity, with receipts. This is where I keep them.</p>
<p class="apology">With apologies to Lewis Carroll.</p>
<div class="hero-ctas">
<a class="btn btn-primary" href="#work" data-set="depth" data-val="tldr">Start at the surface</a>
<a class="btn" href="#method" data-set="depth" data-val="deep">Take me down the rabbit hole <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M12 4v14M6 12l6 6 6-6"/></svg></a>
</div>
<p class="stats"><span><b>8</b> things I built for fun (two were after lunch)</span><span><b>2</b> games starring chickens</span><span><b>3</b> typefaces to choose from</span><span><b>∞</b> open tabs</span></p>
</div>
{HOLE}
</div>

<section class="band" aria-labelledby="depth-title">
<div class="wrap">
<div style="flex: 1 1 480px">
<h2 id="depth-title" class="display"><span class="b">How deep</span> <span class="t">do you want to go?</span></h2>
<p>Everything here comes in two sizes. TL;DR gives you the point in about a minute. Rabbit Hole shows the reasoning, the dead ends, and the footnotes. Switch any time.</p>
</div>
{DEPTH_SWITCH}
</div>
</section>

<section id="method" class="wrap section" aria-labelledby="method-title">
<p class="chapter">Chapter I · Down the rabbit hole</p>
<div class="section-head">
<h2 id="method-title" class="display h2"><span class="b stack">Rabbit hole</span><span class="t stack">research.</span></h2>
<p>It’s how I work on anything: follow the question further than is strictly reasonable, keep every receipt, then climb back out with something other people can use.</p>
</div>
<ol class="steps">
{steps}
</ol>
</section>

{ORNAMENT}

<section id="work" class="wrap section tight" aria-labelledby="work-title">
<p class="chapter">Chapter II · The card catalog</p>
<div class="section-head">
<h2 id="work-title" class="display h2"><span class="b stack">Things I built for fun,</span><span class="t stack">filed properly.</span></h2>
<p>Each one gets a real Dewey call number, because I’m the kind of person who would. The professional work is in the next chapter, behind a little door.</p>
</div>
<div class="catalog">
{cards}
</div>
</section>



<section id="door" class="wrap section" aria-labelledby="door-title">
<p class="chapter">Chapter III · Behind the little door</p>
<div class="door-wrap">
<div class="door-art" aria-hidden="true">
<svg class="door-frame" viewBox="0 0 200 260"><path d="M30 250 V110 A70 70 0 0 1 170 110 V250 Z" style="fill:var(--door-dark)"/><path d="M30 250 V110 A70 70 0 0 1 170 110 V250" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M14 250 H186" stroke="currentColor" stroke-width="1"/><g style="fill:var(--accent)" opacity=".55"><circle cx="100" cy="150" r="1.6"/><circle cx="88" cy="190" r="1.2"/><circle cx="116" cy="210" r="1.4"/></g></svg>
<svg class="door-leaf" viewBox="0 0 200 260"><path d="M30 250 V110 A70 70 0 0 1 170 110 V250 Z" style="fill:var(--surface)" stroke="currentColor" stroke-width="1.5"/><path d="M48 238 V116 A52 52 0 0 1 152 116 V238 Z" fill="none" stroke="currentColor" stroke-width="1" opacity=".6"/><path d="M100 64 V238 M48 170 H152" stroke="currentColor" stroke-width="1" opacity=".35"/><circle cx="140" cy="176" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M140 190 a3 3 0 1 1 0.01 0 M138.6 192 L137.4 199 H142.6 L141.4 192" style="fill:var(--ink)"/></svg>
<svg class="door-key" viewBox="0 0 120 50"><g fill="none" style="stroke:var(--accent)" stroke-width="2" stroke-linecap="round"><circle cx="16" cy="25" r="11"/><circle cx="16" cy="25" r="4.5"/><path d="M27 25 H104 M88 25 V35 M96 25 V33 M104 25 V36"/></g><path d="M8 4 C20 10 22 12 24 15" fill="none" stroke="currentColor" stroke-width=".8" opacity=".6"/></svg>
</div>
<div class="door-copy">
<h2 id="door-title" class="display h2"><span class="b stack">Professional work,</span><span class="t stack">behind the little door.</span></h2>
<p>Case studies and working demos from my marketing and business development work, reimagined and rebuilt with made-up data.</p>
<a class="btn btn-primary" href="/contact?topic=key">Request a key</a>
<p class="door-note">Ask, and I’ll send you the way in.</p>
</div>
</div>
</section>

<section id="about" class="wrap section" aria-labelledby="about-title">
<div class="split">
<div class="main">
<p class="chapter">Chapter IV · “Who are you?” said the Caterpillar</p>
<h2 id="about-title" class="display" style="font-size: clamp(2rem, 3.6vw, 3rem); line-height: 1.02; margin-bottom: .8em"><span class="b">I follow questions further</span> <span class="t">than is strictly reasonable.</span></h2>
<p style="margin: 0 0 1.4em; max-width: 36em">With one public-sector consulting firm since 2012, on and off, from project-based help to marketing director, and three-plus years building with AI. I design workflows where the AI does the heavy lifting and a person makes the call.</p>
<a class="btn" href="/about">The long version →</a>
</div>
<dl class="notes" aria-label="Field notes">
{notes}
</dl>
</div>
</section>

<section class="wrap" style="padding-top: 4rem; padding-bottom: 6rem" aria-labelledby="otc-title">
<div class="lavalou-card">
<span class="ooze one" aria-hidden="true"></span>
<span class="ooze two" aria-hidden="true"></span>
<div class="copy">
<span class="label">Off the clock</span>
<img src="/lavalou/assets/brand/lavalou-horizontal-lime.svg" alt="Lavalou" width="300" height="123">
<h2 id="otc-title" class="display"><span class="b">I also make games for my kids.</span> <span class="t">Two so far. Both star chickens.</span></h2>
<p>Math and spelling adventures, plus whatever else my family needs a tool for. A little molten. A little strange.</p>
</div>
<a class="lavalou-btn" href="/lavalou">Visit Lavalou <svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
</div>
</section>
</main>
"""
    return head('Lara Borowsky: curiosity, with receipts', 'Lara Borowsky: marketing and BD strategist, AI systems builder, and maker of games starring chickens. Rabbit hole research, with receipts.', '/') + header(None) + body + footer('<a href="/about">About me</a>')

FACTS = [('Since 2012', 'with one public-sector consulting firm, in stretches, from project-based help to marketing director.'),
         ('3+ years', 'building with AI, with a human making every final call.'),
         ('1 person', 'marketing department. Hence the systems.')]
PATH = [('2025 to now', 'Marketing Director', 'at a public-sector consulting firm', 'Brand, website, content, and the systems that keep a one-person marketing department running.', 'This is where building with AI went from experiment to everyday practice, always with a person making the final call.'),
        ('2023 to 2025', 'Marketing Manager', 'same firm', 'Moved marketing in-house and designed just about everything with a logo on it.', 'Also planned an in-person retreat for a fully remote team, travel logistics included.'),
        ('2022 to 2023', 'Associate Consultant', 'same firm', 'Research and pursuit analysis to support strategic planning.', 'This is where the rabbit holes started: agency research, teaming partners, procurement trends.'),
        ('2018 to 2019', 'Business Manager', 'same firm', 'Operations, systems, and keeping the trains running.', 'Learning how a firm actually runs turned out to be the best marketing training I could have had.'),
        ('2012 to 2015', 'Independent consultant', 'same firm, project by project', 'Built the firm’s first website, pulled together its business certification applications, and was the IT help before there was IT help.', 'On and off, as projects came up. It’s how I met the firm, and how I learned that I like building the thing more than just using it.'),
        ('2009 to 2011', 'Client services', 'at a call center', 'One of the voices behind 50+ client contracts: pet doors, solar panels, college directory assistance, high-end butcher orders, IT help desks, restaurant delivery confirmations, and more.', 'Contract lead for one of them: a wine company’s direct-to-consumer program. That meant customer service and ordering, day-to-day operations, and keeping customers, the warehouse, and the client in sync. Our team also supported the company’s first online direct-to-consumer wine sale.'),
        ('Since I was 15', 'A little bit of everything,', 'all of it useful', 'Swim club office, lifeguard, swim teacher, camp counselor, photographer’s assistant, retail, café, and catering.', 'At 15 I helped a swim club move its membership management and check-in from paper to digital. I taught swim lessons to kids, parent-and-baby classes, and a student with a disability, and lifeguarded at two pools. I assisted a school photographer, worked retail at a cooking supply store and a hat shop (where I also kept up her web store), opened a café on my own to make breakfast for the morning ferry commuters in Hoboken (lots of egg sandwiches, occasional baking included), and served weddings and events for 150+ guests at a catering hall before moving to front of house. Customer service, it turns out, is systems thinking with a smile.')]
SKILLS = ['Public-sector infrastructure marketing', 'AI-assisted content systems and workflow design', 'Responsible AI use and governance',
          'Brand strategy, visual and verbal design systems', 'Proposal, capability and BD content', 'Marketing strategy and digital engagement',
          'Capture and pursuit operations', 'Enterprise systems and process improvement', 'Process standardization and knowledge management']
RULES = [('A person makes the call.', 'AI drafts, sorts, and screens. A human reviews and decides. Every time.'),
         ('Citations or it didn’t happen.', 'If a tool can’t trace a claim to a source, the claim doesn’t ship.'),
         ('Systems over one-offs.', 'If I’m doing it twice, I’m building something so I don’t do it a third time.'),
         ('Accessible by default.', 'Built into the template, not checked at the end. If the default is accessible, nobody has to remember to be.'),
         ('Fellow traveler, not guru.', 'I share what I’ve tried and what broke. I don’t have this all figured out, and I say so.')]
OFF = [('Reading', '150+ books a year.', 'Mostly romance.', 'Audiobook narration is on the someday list.'),
       ('Halloween', 'Jurassic Park, in the front yard.', 'Gate, fence, T. rex.', 'Plus a skeleton in a yellow raincoat holding a Barbasol can, if you know, you know. Past builds: an 11-foot sinking pirate ship and Ghoul-a-palooza, a music festival for the undead.'),
       ('Kitchen &amp; table', 'Baker, cook,', 'Lego builder.', 'If it can be made from scratch or built from a box of bricks, I’m in.'),
       ('Advocacy', 'Disability advocate.', 'Always.', 'It’s why accessibility is a house rule here and not a feature: change the font, the spacing, or how deep you go.'),
       ('Lavalou', 'Games for my kids.', 'Both star chickens.', 'Math and spelling adventures, plus whatever tools my family needs. <a href="/lavalou">They live under my creative label.</a>')]

def chap(n, label):
    return f'<p class="eyebrow"><span class="chapter-tag">Chapter {n} · </span>{label}</p>'

def about():
    facts = '\n'.join(f'<li><span class="big">{b}</span><span class="small">{s}</span></li>' for b, s in FACTS)
    path = '\n'.join(f'<li><span class="when">{w}</span><div><h3><span class="b">{r}</span> <span class="t">{wh}</span></h3><p>{d}</p>' + (f'<p class="deep">{dp}</p>' if dp else '') + '</div></li>' for w, r, wh, d, dp in PATH)
    skills = '\n'.join(f'<li><span class="num">{i+1:02d}</span><span>{s}</span></li>' for i, s in enumerate(SKILLS))
    rules = '\n'.join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in RULES)
    off = '\n'.join(f'<div><span class="label">{l}</span><h3><span class="b">{b}</span> <span class="t">{t}</span></h3><p>{d}</p></div>' for l, b, t, d in OFF)
    body = f"""<main id="main">
<section class="wrap about-hero" aria-labelledby="about-title">
<div style="flex: 999 1 560px; min-width: 0">
<p class="chapter">“Who are you?” said the Caterpillar.</p>
<h1 id="about-title" class="display"><span class="b">I follow questions further</span><span class="t">than is strictly reasonable.</span></h1>
</div>
<div class="depth">
<div class="seg" role="group" aria-label="How much detail">
<button type="button" data-set="depth" data-val="tldr" aria-pressed="true">TL;DR</button>
<button type="button" data-set="depth" data-val="deep" aria-pressed="false">Rabbit Hole</button>
</div>
<p class="muted" style="margin: 0; font-size: .9rem">Short version or the whole story. Your call.</p>
</div>
</section>

<section class="intro" aria-label="Introduction">
<div class="wrap">
<ul class="facts shallow">
{facts}
</ul>
<div class="deep">
<div class="long">
<div class="story">
<p>Public-sector infrastructure consulting is where I’ve spent most of my career, at one small firm, working in operations, research, business development, marketing, and whatever IT problem landed on my desk that week. These days I’m a marketing and business development strategist.</p>
<p>I’m the whole marketing department there, which is exactly why I started building tools. When you’re one person, you either do less or you build systems that do more. I chose systems.</p>
<p>For the last three-plus years I’ve been building with AI: research pipelines, screening tools, content systems, a brand kit an AI can actually follow. The rule I don’t bend: the AI does the heavy lifting, and a person makes the call.</p>
<p>I’m openly neurodivergent, and that shows up in the work. I see systems where other people see tasks, I go deep on whatever hooks me, and I care a lot about making information easy to take in. That’s why this site lets you change the font, the spacing, and how much detail you get.</p>
<p>I’m still figuring a lot of this out. These are my field notes so far.</p>
</div>
<aside class="margin-note" aria-label="Margin note">
<span class="label">Margin note</span>
<p>“Rabbit hole research” started as a joke about how I work. Then I noticed it was an accurate description of how I work.</p>
</aside>
</div>
</div>
</div>
</section>

<section class="wrap nutshell" aria-labelledby="nutshell-title">
<h2 id="nutshell-title" class="eyebrow" style="font-weight: 400">Me, in a nutshell</h2>
<p class="display"><span class="b">Read books.</span> <span class="t">Be kind.</span> <span class="b accent">Stay weird.</span></p>
</section>

<section class="path-section" aria-labelledby="path-title">
<div class="wrap">
{chap('I', 'The path')}
<h2 id="path-title" class="display h2"><span class="b">Operations to marketing,</span> <span class="t">by way of every department.</span></h2>
<ol class="path">
{path}
</ol>
</div>
</section>

<section class="wrap section" aria-labelledby="good-title" style="padding-top: 5rem">
{chap('II', 'What I’m good at')}
<h2 id="good-title" class="display h2"><span class="b">Nine things</span> <span class="t">I’d put on an index card.</span></h2>
<ul class="skills">
{skills}
</ul>
</section>

<section class="wrap section" aria-labelledby="how-title" style="padding-top: 5rem">
{chap('III', 'How I work')}
<h2 id="how-title" class="display h2"><span class="b">House rules.</span> <span class="t">I break them less than you’d think.</span></h2>
<div class="rules">
{rules}
</div>
</section>

<section class="wrap section" aria-labelledby="off-title" style="padding-top: 5rem; padding-bottom: 6rem">
{chap('IV', 'Off the clock')}
<h2 id="off-title" class="display h2"><span class="b">Things I build</span> <span class="t">that nobody asked for.</span></h2>
<div class="offclock">
{off}
</div>
</section>
</main>
"""
    return head('About Lara Borowsky', 'Marketing and business development strategist, AI systems builder, disability advocate, and Halloween over-achiever. Read books. Be kind. Stay weird.', '/about') + header('about') + body + footer('<a href="/">Back to the surface</a>')

def access():
    def sec(n, label, title_b, title_t, inner):
        return f"""<section class="wrap section" style="padding-top: 4rem" aria-labelledby="a{n}">
{chap(n, label)}
<h2 id="a{n}" class="display h2"><span class="b">{title_b}</span> <span class="t">{title_t}</span></h2>
{inner}
</section>
"""
    def ul(items):
        return '<ul class="a11y-list">' + ''.join(f'<li><strong>{a}</strong> {b}</li>' for a, b in items) + '</ul>'
    body = f"""<main id="main">
<section class="wrap about-hero" aria-labelledby="a11y-title">
<div style="flex: 999 1 560px; min-width: 0">
<p class="chapter">A note on the door, and who it’s for.</p>
<h1 id="a11y-title" class="display"><span class="b">Accessible by default.</span> <span class="t">Not by accident.</span></h1>
<p class="lede" style="max-width: 36em">I’m a disability advocate, and this site is meant to work for as many people as possible, however you read, see, hear, move, or think. Here’s what that means in practice, how I check it, and what still needs work.</p>
</div>
</section>
{sec('I', 'The standard', 'The floor,', 'not the ceiling.', '<p class="a11y-p">I aim for the Web Content Accessibility Guidelines (WCAG) 2.2 at Level AA as the minimum, and go further where I can.</p>')}
{sec('II', 'What you can change', 'Make it yours.', 'Settings stay in your browser.', ul([
  ('Theme:', 'light, dark, or match your device.'),
  ('Contrast:', 'standard or high, or match your device.'),
  ('Text weight:', 'standard or bolder, for anyone who finds thin type hard to read.'),
  ('Typeface:', 'the default, OpenDyslexic, or Atkinson Hyperlegible.'),
  ('Text size and spacing:', 'three sizes, plus roomier line and letter spacing.'),
  ('Motion:', 'animation follows your device, or you can stop it. The falling objects on the home page also have their own pause button.'),
  ('Depth:', 'a short TL;DR version of everything, or the full Rabbit Hole.'),
]))}
{sec('III', 'How it’s built', 'Under the hood.', 'The parts you don’t see.', ul([
  ('Structure:', 'real headings, landmarks, buttons and labels, so screen readers can move around the page.'),
  ('Keyboard:', 'everything works without a mouse, with a visible focus outline and a skip link.'),
  ('Images:', 'meaningful drawings have descriptions; decorative ones are hidden from screen readers.'),
  ('Color:', 'nothing depends on color alone, and text meets contrast requirements in both themes.'),
  ('Zoom:', 'pages reflow at 400% zoom without sideways scrolling.'),
  ('Your device settings:', 'dark mode, reduced motion, higher contrast and Windows high-contrast mode are respected.'),
  ('Privacy:', 'no tracking, and your reading settings never leave your browser.'),
]))}
{sec('IV', 'How it’s checked', 'Receipts,', 'naturally.', ul([
  ('Automated scans', 'with axe on the home, About, accessibility and Lavalou pages, in light, dark and high-contrast modes and both depths.'),
  ('A manual pass', 'by keyboard only, for heading and label structure, at 400% zoom, with extra text spacing, and in high-contrast mode.'),
  ('Last reviewed:', 'November 15, 2026.'),
]))}
{sec('V', 'Still on the list', 'Honest gaps.', 'I’m working on them.', ul([
  ('The Cluck Quest games', 'haven’t had a full accessibility review yet.'),
  ('Real-world testing:', 'I haven’t yet tested with disabled people using their own assistive technology. That’s the gold standard, and it’s next.'),
  ('Web fonts', 'load from Google Fonts. If they don’t load, the site falls back to standard fonts and stays fully usable.'),
]))}
<section class="wrap section" style="padding-top: 4rem; padding-bottom: 6rem" aria-labelledby="a6">
{chap('VI', 'Found a problem?')}
<h2 id="a6" class="display h2"><span class="b">Tell me.</span> <span class="t">I’ll fix it.</span></h2>
<p class="a11y-p">If something on this site doesn’t work for you, <a href="{LI}">send me a message on LinkedIn</a> with the page and what happened. I’d rather know.</p>
</section>
</main>
"""
    return head('Accessibility · Lara Borowsky', 'How laraborowsky.com is built and tested for accessibility, what you can change, and what still needs work.', '/accessibility') + header('accessibility') + body + footer('<a href="/">Back to the surface</a>')

W3F_KEY = '678b8a04-71b7-43ca-8624-11052452c4d5'

def contact():
    body = f"""<main id="main">
<section class="wrap about-hero" aria-labelledby="contact-title">
<div style="flex: 999 1 560px; min-width: 0">
<p class="chapter">Knock, knock.</p>
<h1 id="contact-title" class="display"><span class="b">Say hello.</span><span class="t">Or ask for a key.</span></h1>
<p class="lede" style="max-width: 34em">Whether you’d like a key to the little door or just want to trade rabbit holes, leave a note here. It comes straight to my inbox.</p>
</div>
</section>
<section class="wrap" style="padding-bottom: 6rem" aria-label="Contact form">
<div class="contact-wrap">
<form id="contact-form" class="contact-form" action="https://api.web3forms.com/submit" method="POST">
<input type="hidden" name="access_key" value="{W3F_KEY}">
<input type="hidden" name="from_name" value="laraborowsky.com">
<input type="hidden" name="subject" id="cf-subject" value="laraborowsky.com: new note">
<input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="field">
<label for="cf-name">Your name</label>
<input id="cf-name" name="name" type="text" autocomplete="name" required>
</div>
<div class="field">
<label for="cf-email">Your email</label>
<input id="cf-email" name="email" type="email" autocomplete="email" required aria-describedby="cf-email-hint">
<span id="cf-email-hint" class="hint">So I can write back. I won’t use it for anything else.</span>
</div>
<fieldset class="field">
<legend>What brings you here?</legend>
<div class="choices">
<label class="choice"><input type="radio" name="topic" value="Request a key" checked> Request a key to the professional work</label>
<label class="choice"><input type="radio" name="topic" value="Just saying hello"> Just saying hello</label>
<label class="choice"><input type="radio" name="topic" value="Something else"> Something else</label>
</div>
</fieldset>
<div class="field">
<label for="cf-message">Your message <span class="hint-inline">(optional)</span></label>
<textarea id="cf-message" name="message" rows="6"></textarea>
</div>
<button class="btn btn-primary" type="submit">Send it down the rabbit hole</button>
<p id="cf-status" class="cf-status" role="status" aria-live="polite"></p>
</form>
<aside class="margin-note contact-aside" aria-label="Other ways to reach me">
<span class="label">Margin note</span>
<p>Prefer LinkedIn? <a href="{LI}">Find me there</a>. Either way, I read everything.</p>
</aside>
</div>
</section>
</main>
<script src="/assets/contact.js"></script>
"""
    return head('Contact · Lara Borowsky', 'Say hello to Lara Borowsky, or request a key to her professional work.', '/contact') + header('contact') + body + footer('<a href="/">Back to the surface</a>')

open(os.path.join(OUT, 'index.html'), 'w').write(index())
open(os.path.join(OUT, 'about.html'), 'w').write(about())
open(os.path.join(OUT, 'accessibility.html'), 'w').write(access())
open(os.path.join(OUT, 'contact.html'), 'w').write(contact())
import re as _re
for _f in ['index.html','about.html','accessibility.html','contact.html']:
    _p=os.path.join(OUT,_f); _s=open(_p).read()
    _s=_re.sub(r'</span><span class="(t|b)', r'</span> <span class="\1', _s)
    _s=_re.sub(r' →</a>', ' <span aria-hidden="true">→</span></a>', _s)
    _s=_re.sub(r' (fill|stroke)="var\((--[a-z-]+)\)"', r' style="\1:var(\2)"', _s)
    open(_p,'w').write(_s)
print('built')

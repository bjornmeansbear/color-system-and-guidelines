"""Contact sheet: forty candidates, ninety seconds, one click to pick.

Styled to the kit — warm ground, dark brown line work, pink accent, solid
borders, no radius on structural elements.
"""
import html
import json

CSS = """
:root{
  --gray-0:rgb(247,248,238); --gray-1:rgb(234,234,224); --gray-6:rgb(83,83,72);
  --brown-1:rgb(238,232,229); --brown-8:rgb(25,21,19); --brown-9:rgb(8,5,4);
  --pink-3:rgb(255,129,169); --pink-5:rgb(214,0,97); --pink-6:rgb(164,0,65);
  --bg:var(--gray-0); --text:var(--brown-8); --accent:var(--pink-5);
  --font:system-ui,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,'SFMono-Regular',Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font);
  font-size:1rem;line-height:1.5rem}
header{position:sticky;top:0;z-index:5;background:var(--bg);
  border-bottom:2px solid var(--text);padding:1.125rem 1.5rem}
h1{font-size:1.75rem;line-height:2.25rem;margin:0 0 .375rem}
.brief{font-size:1.125rem;line-height:1.5rem;color:var(--accent);margin:0}
.meta{font-size:.8125rem;line-height:1.125rem;color:var(--gray-6);
  margin:.375rem 0 0;font-family:var(--mono)}
main{display:grid;grid-template-columns:1fr;gap:1.5rem;padding:1.5rem}
@media(min-width:40rem){main{grid-template-columns:repeat(2,1fr)}}
@media(min-width:55rem){main{grid-template-columns:repeat(3,1fr)}}
figure{margin:0;border:2px solid var(--text);display:flex;flex-direction:column;
  background:var(--gray-1)}
figure.picked{border-color:var(--accent);border-width:4px}
.imgwrap{aspect-ratio:4/3;background:var(--brown-9);display:grid;place-items:center;
  overflow:hidden}
.imgwrap img{width:100%;height:100%;object-fit:contain;display:block}
figcaption{padding:.75rem;border-top:2px solid var(--text);flex:1;
  display:flex;flex-direction:column;gap:.375rem}
.t{font-weight:600;line-height:1.125rem}
.a{font-size:.875rem;line-height:1.125rem;color:var(--gray-6)}
.tags{display:flex;flex-wrap:wrap;gap:.375rem;margin-top:auto;padding-top:.375rem}
.tag{border:1px solid var(--text);border-radius:999px;padding:.0625rem .5rem;
  font-size:.75rem;line-height:1.125rem;font-family:var(--mono)}
.tag.src{background:var(--text);color:var(--gray-0)}
.tag.small{border-color:var(--accent);color:var(--pink-6)}
.row{display:flex;gap:.375rem;align-items:center}
button,a.src{font:inherit;font-size:.8125rem;line-height:1.125rem;
  border:2px solid var(--text);background:var(--bg);color:var(--text);
  padding:.375rem .75rem;cursor:pointer;text-decoration:none;display:inline-block}
button:hover,a.src:hover{background:var(--text);color:var(--bg)}
button.pick{border-color:var(--accent);color:var(--pink-6);font-weight:600}
button.pick:hover,figure.picked button.pick{background:var(--accent);
  color:var(--gray-0);border-color:var(--accent)}
:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
#out{position:fixed;left:0;right:0;bottom:0;background:var(--text);
  color:var(--gray-0);padding:.75rem 1.5rem;font-family:var(--mono);
  font-size:.8125rem;line-height:1.125rem;display:none}
#out.on{display:block}
#out code{color:var(--pink-3);user-select:all}
"""

JS = """
document.addEventListener('click', function (e) {
  var b = e.target.closest('button.pick'); if (!b) return;
  document.querySelectorAll('figure.picked').forEach(function(f){f.classList.remove('picked')});
  var fig = b.closest('figure'); fig.classList.add('picked');
  var out = document.getElementById('out');
  out.className = 'on';
  out.innerHTML = 'Run this to fill the slot: <code>' + b.dataset.cmd + '</code>';
  navigator.clipboard && navigator.clipboard.writeText(b.dataset.cmd);
});
"""


def render(slot, brief, cands, deck_path, out_path):
    cards = []
    for c in cands:
        w, h = c.get("width"), c.get("height")
        dim = f"{w}×{h}" if w and h else "size unknown"
        cmd = (f"python3 tools/commons/commons.py pick {deck_path} "
               f"{slot} {c['source']}:{c['id']}")
        page = (f'<a class="src" href="{html.escape(c["page_url"])}" target="_blank" '
                f'rel="noopener">source</a>' if c.get("page_url") else "")
        cards.append(f"""<figure>
  <div class="imgwrap"><img loading="lazy" src="{html.escape(c['thumb_url'])}" alt=""></div>
  <figcaption>
    <span class="t">{html.escape(c['title'][:90])}</span>
    <span class="a">{html.escape((c.get('artist') or '')[:70])}{
      ' · ' + html.escape(c['date'][:24]) if c.get('date') else ''}</span>
    <div class="tags">
      <span class="tag src">{html.escape(c['source'])}</span>
      <span class="tag">{dim}</span>
      <span class="tag">{html.escape((c.get('license') or '')[:28])}</span>
    </div>
    <div class="row">
      <button class="pick" data-cmd="{html.escape(cmd)}">Pick this</button>{page}
    </div>
  </figcaption>
</figure>""")

    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(slot)} — contact sheet</title><style>{CSS}</style></head><body>
<header>
  <h1>{html.escape(slot)}</h1>
  <p class="brief">{html.escape(brief or '(no brief)')}</p>
  <p class="meta">{len(cands)} candidates · all public domain · all &ge;2000px ·
     {html.escape(deck_path)}</p>
</header>
<main>{''.join(cards)}</main>
<div id="out"></div>
<script>{JS}</script></body></html>"""
    with open(out_path, "w") as f:
        f.write(doc)
    return out_path

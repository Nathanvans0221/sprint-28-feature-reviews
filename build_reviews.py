#!/usr/bin/env python3
"""Generate the Sprint 28 Feature Reviews page (branded cards + embedded videos)."""
import html, os

PRODUCT_COLORS = {
    'RESTOCK': '#2563EB', 'PRODUCE': '#DB6E14', 'FULFILL': '#BA3636', 'FORECAST/DBR': '#0891B2',
    'PLATFORM': '#6B7280', 'DEV-TOOLS': '#7C3AED', 'REPORTS': '#059669', 'MOBILE': '#0EA5E9',
    'AVAILABILITY': '#10B981', 'INVENTORY': '#F59E0B', 'OTHER': '#9CA3AF',
}
PR = "https://dev.azure.com/teamsilverfern/SilverFern/_git/{repo}/pullrequest/{id}"

REVIEWS = __import__("json").load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "reviews_copy.json")))

def card(r):
    c = PRODUCT_COLORS.get(r["product"], "#6B7280")
    url = PR.format(repo=r["repo"], id=r["id"])
    vpath = os.path.join(os.path.dirname(__file__), "videos", r.get("video") or "")
    if r.get("video") and os.path.exists(vpath):
        media = (f'<video controls preload="metadata" playsinline '
                 f'style="width:100%; border-radius:8px; background:#000; display:block;">'
                 f'<source src="videos/{r["video"]}" type="video/webm"></video>')
    elif r.get("no_video_reason"):
        media = (f'<div style="padding:26px; text-align:center; background:#F2F2F2; border-radius:8px; color:#6B7280;">'
                 f'<div style="font-weight:600; letter-spacing:0.08em; font-size:11px; text-transform:uppercase; color:#69936C; margin-bottom:6px;">Shipped — no UI demo</div>'
                 f'<div style="font-weight:300; font-size:14px;">{html.escape(r["no_video_reason"])}</div></div>')
    else:
        media = ('<div style="padding:40px; text-align:center; background:#F2F2F2; border-radius:8px; '
                 'color:#B3B3B3; font-style:italic;">Recording being re-shot — video coming shortly</div>')
    return f'''
    <div class="sf-card review-card" data-product="{html.escape(r["product"])}" style="overflow:hidden;">
      <div style="display:flex; flex-wrap:wrap; gap:10px; align-items:center; justify-content:space-between; padding:16px 18px; border-bottom:1px solid #F2F2F2;">
        <div style="display:flex; align-items:center; gap:10px;">
          <span class="chip" style="background:{c}">{html.escape(r["product"])}</span>
          <span class="sf-h3" style="font-size:16px;">{html.escape(r["title"])}</span>
        </div>
        <a href="{url}" target="_blank" style="color:#69936C; font-family:monospace; font-size:13px; text-decoration:none;">#{r["id"]} ↗</a>
      </div>
      <div style="padding:18px;">
        <div style="margin-bottom:16px;">{media}</div>
        <div class="sf-eyebrow" style="margin-bottom:4px;">What it does</div>
        <p style="color:#3F4948; font-weight:300; margin-bottom:12px;">{html.escape(r["desc"])}</p>
        {f'<div class="sf-eyebrow" style="margin-bottom:4px;">What to look for</div><p style="color:#3F4948; font-weight:300;">{html.escape(r["look_for"])}</p>' if r.get("look_for") else ''}
      </div>
    </div>'''

cards = "\n".join(card(r) for r in REVIEWS)
_prods = []
for _r in REVIEWS:
    if _r["product"] not in _prods: _prods.append(_r["product"])
def _chip(label, value, color):
    return (f'<button class="filter-chip chip" onclick="filterProduct(\'{value}\', this)" '
            f'style="background:{color}; border:none; cursor:pointer; opacity:{1 if value=="ALL" else 0.45};">{label}</button>')
chips = _chip("All", "ALL", "#3F4948") + "".join(_chip(p, p, PRODUCT_COLORS.get(p, "#6B7280")) for p in _prods)
recorded = sum(1 for r in REVIEWS if r.get("video") and os.path.exists(os.path.join(os.path.dirname(__file__), "videos", r["video"])))
TOTAL_HIGHLIGHTS = recorded

HTML = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Sprint 28 Feature Reviews — Silver Fern</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300&family=PT+Serif:ital@1&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<style>
  :root {{ --sf-rich-soil:#3F4948; --sf-fern:#69936C; --sf-stirling:#B3B3B3; --sf-light-silver:#F2F2F2; --sf-spring-green:#A1DBA6; }}
  body {{ font-family:'Montserrat',Arial,sans-serif; font-weight:300; color:var(--sf-rich-soil); background:var(--sf-light-silver); line-height:1.6; }}
  .sf-h2 {{ font-family:'PT Serif',Georgia,serif; font-style:italic; color:var(--sf-fern); }}
  .sf-h3 {{ font-family:'Montserrat',Arial,sans-serif; font-weight:600; color:var(--sf-rich-soil); }}
  .sf-eyebrow {{ font-family:'Montserrat',Arial,sans-serif; font-weight:600; text-transform:uppercase; letter-spacing:0.15em; font-size:11px; color:var(--sf-fern); }}
  .chip {{ display:inline-flex; align-items:center; padding:2px 10px; border-radius:9999px; font-size:11px; font-weight:600; color:white; letter-spacing:0.04em; }}
  .sf-card {{ background:white; border:1px solid #E5E7E5; border-radius:8px; box-shadow:0 1px 2px rgba(63,73,72,0.04); }}
</style>
</head>
<body>
<header class="shadow-lg" style="background:linear-gradient(135deg,#3F4948 0%,#2E3635 100%); color:white;">
  <div class="max-w-5xl mx-auto px-6 py-7">
    <div class="sf-eyebrow" style="color:#A1DBA6;">Silver Fern · Sprint Review</div>
    <h1 style="font-weight:700; text-transform:uppercase; letter-spacing:0.125em; font-size:30px; margin-top:6px;">Sprint 28 — Feature Reviews</h1>
    <div class="sf-h2" style="font-size:18px; margin-top:4px; color:#A1DBA6;">Recorded walkthroughs of the highlighted features — {recorded} of {TOTAL_HIGHLIGHTS}</div>
  </div>
</header>
<div class="max-w-5xl mx-auto px-6 pt-8" style="display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
  <span class="sf-eyebrow" style="margin-right:6px;">Filter</span>
  {chips}
</div>
<main class="max-w-5xl mx-auto px-6 py-6" style="display:flex; flex-direction:column; gap:22px;">
{cards}
</main>
<script>
  function filterProduct(prod, el) {{
    document.querySelectorAll('.review-card').forEach(c => {{
      c.style.display = (prod === 'ALL' || c.dataset.product === prod) ? '' : 'none';
    }});
    document.querySelectorAll('.filter-chip').forEach(ch => {{
      ch.style.opacity = (ch === el) ? '1' : '0.45';
      ch.style.outline = (ch === el) ? '2px solid #2E3635' : 'none';
    }});
  }}
</script>
<footer style="background:#3F4948; color:white; margin-top:24px;">
  <div class="max-w-5xl mx-auto px-6 py-5 flex justify-between items-center flex-wrap gap-3">
    <div class="text-sm" style="color:rgba(255,255,255,0.85);">Recorded against red (worksuite.silverfern.red) · SFG tenant · June 9 build</div>
    <div class="text-xs italic" style="color:#A1DBA6; font-family:'PT Serif',serif;">Authentic · Innovative · Expert</div>
  </div>
</footer>
</body></html>'''

out = os.path.join(os.path.dirname(__file__), "index.html")
open(out, "w", encoding="utf-8").write(HTML)
print(f"wrote {out} ({len(HTML)} bytes), {recorded}/{len(REVIEWS)} cards with video")

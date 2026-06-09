#!/usr/bin/env python3
"""Generate the Sprint 28 Feature Reviews page (branded cards + embedded videos)."""
import html, os

PRODUCT_COLORS = {
    'RESTOCK': '#2563EB', 'PRODUCE': '#DB6E14', 'FULFILL': '#BA3636', 'FORECAST/DBR': '#0891B2',
    'PLATFORM': '#6B7280', 'DEV-TOOLS': '#7C3AED', 'REPORTS': '#059669', 'MOBILE': '#0EA5E9',
    'AVAILABILITY': '#10B981', 'INVENTORY': '#F59E0B', 'OTHER': '#9CA3AF',
}
PR = "https://dev.azure.com/teamsilverfern/SilverFern/_git/{repo}/pullrequest/{id}"
TOTAL_HIGHLIGHTS = 33

REVIEWS = [
    {"id": 8975, "product": "FULFILL", "video": "8975.webm", "repo": "worksuite-pwa",
     "title": "Fulfill Orders grid — server-side per-column + set filters",
     "desc": "Phase 1 of Fulfill Orders SSRM: per-column server-side filtering and sorting on the Orders grid "
             "(combinedOrders), filter-aware Status/Type set filters, and the server-persisted Week Number column.",
     "look_for": "The Orders grid loads server-side; filtering and sorting round-trip to the server rather than just "
                 "the page in memory. Note the Week Number and Days-to-Pay columns that shipped this sprint."},
    {"id": 9212, "product": "FULFILL", "video": "9212.webm", "repo": "worksuite-pwa",
     "title": "Orders search wired to server-side searchText",
     "desc": "The Fulfill orders search box now sends searchText in the agGridRows request and refreshes the SSRM cache "
             "(debounced) as you type — so it searches the full tenant order set, not just already-loaded blocks.",
     "look_for": "Type in the search box: the grid refetches from the server across every order, not just the rows "
                 "currently loaded in the browser."},
    {"id": 9111, "product": "FULFILL", "video": "9111.webm", "repo": "worksuite-pwa",
     "title": "Credit Order — create a credit from an existing order",
     "desc": "New 'Credit Order' ribbon action on the Fulfill order screen. Credit the entire order, or specific lines "
             "(checkbox per line + a clamped quantity). Confirm calls the dedicated creditExistingOrder mutation.",
     "look_for": "Open an order and hit Credit Order in the ribbon — the dialog offers crediting the whole order or "
                 "picking specific lines and quantities."},
    {"id": 7904, "product": "FULFILL", "video": "7904.webm", "repo": "worksuite-pwa",
     "title": "Duplicate Order action",
     "desc": "Single-row Duplicate Order, from the order-detail ribbon and the orders-list right-click menu. Creates a "
             "new draft order carrying the source's customer, terms, PO, type, delivery date, sales person, and lines.",
     "look_for": "Right-click an order → Duplicate Order. A new draft is created from the source (watch the "
                 "“created from #…” confirmation) and opens ready to edit."},
    {"id": 7901, "product": "FULFILL", "video": "7901.webm", "repo": "worksuite-pwa",
     "title": "Bulk Download Invoices ribbon action",
     "desc": "New ribbon button on Fulfill > Orders that downloads a ZIP of invoice PDFs for the multi-selected orders — "
             "replacing the one-at-a-time download workflow.",
     "look_for": "Select one or more orders and the Download Invoices button enables, bundling their invoice PDFs into a "
                 "single ZIP (it guards against orders with no invoice yet)."},
    {"id": 9182, "product": "PRODUCE", "video": "9182.webm", "repo": "worksuite-pwa",
     "title": "Order-line Upgrades panel (Value Adds)",
     "desc": "A new Upgrades column on the order line-items grid opens a per-line modal to see current upgrades, add an "
             "upgrade from the item, or add an ad-hoc upgrade — with the line total recomputed live.",
     "look_for": "Scroll the line items to the new Upgrades column; opening a line shows the per-line Upgrades modal with "
                 "“add from item”, “ad-hoc upgrade”, and the running base/adjustment/line total."},
    {"id": 9060, "product": "FULFILL", "video": "9060.webm", "repo": "worksuite-pwa",
     "title": "Add Integration — accounting platforms with brand logos",
     "desc": "The Add Integration picker now enables the 11 accounting platforms active in our Merge.dev workspace "
             "(QuickBooks, Xero, NetSuite, Sage Intacct, FreshBooks, …), routed through Merge Link, with official logos.",
     "look_for": "Add Integration → the picker shows the accounting platforms with real brand logos and category filters "
                 "(Accounting, E-commerce, Shipping, CRM …)."},
    {"id": 7920, "product": "FULFILL", "video": "7920.webm", "repo": "worksuite-pwa",
     "title": "Fulfill Maintenance — Containers + Shipping Config Categories",
     "desc": "Containers use a CardView with a sidebar grouped by container code and parent/child hierarchy. The Container "
             "tab edits intrinsic fields (cascading across configs sharing the code); the Configurations tab shows the per-config grid.",
     "look_for": "Pick a container in the left sidebar; the Container tab edits shared fields while the Configurations tab "
                 "lists its per-config rows (sites, trays/layer, max layers, ship factor)."},
    {"id": 9217, "product": "PRODUCE", "video": "9217.webm", "repo": "worksuite-pwa",
     "title": "Space Category dimension variations (master-detail)",
     "desc": "Rebuilds the Space Categories screen (Produce → Capacity → Categories & Types) as a master-detail: category "
             "list on the left, a per-category variations grid on the right, with an editable default (all sites/all customers) row plus overrides.",
     "look_for": "A category is created, then selected on the left — its dimension variations load on the right, including "
                 "the editable default “All sites / All customers” row."},
]

def card(r):
    c = PRODUCT_COLORS.get(r["product"], "#6B7280")
    url = PR.format(repo=r["repo"], id=r["id"])
    vpath = os.path.join(os.path.dirname(__file__), "videos", r.get("video") or "")
    if r.get("video") and os.path.exists(vpath):
        media = (f'<video controls preload="metadata" playsinline '
                 f'style="width:100%; border-radius:8px; background:#000; display:block;">'
                 f'<source src="videos/{r["video"]}" type="video/webm"></video>')
    else:
        media = ('<div style="padding:40px; text-align:center; background:#F2F2F2; border-radius:8px; '
                 'color:#B3B3B3; font-style:italic;">Recording pending / blocked — no test data on this tenant</div>')
    return f'''
    <div class="sf-card" style="overflow:hidden;">
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
        <div class="sf-eyebrow" style="margin-bottom:4px;">What to look for</div>
        <p style="color:#3F4948; font-weight:300;">{html.escape(r["look_for"])}</p>
      </div>
    </div>'''

cards = "\n".join(card(r) for r in REVIEWS)
recorded = sum(1 for r in REVIEWS if r.get("video") and os.path.exists(os.path.join(os.path.dirname(__file__), "videos", r["video"])))

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
<main class="max-w-5xl mx-auto px-6 py-10" style="display:flex; flex-direction:column; gap:22px;">
{cards}
</main>
<footer style="background:#3F4948; color:white; margin-top:24px;">
  <div class="max-w-5xl mx-auto px-6 py-5 flex justify-between items-center flex-wrap gap-3">
    <div class="text-sm" style="color:rgba(255,255,255,0.85);">Recorded against red (worksuite.silverfern.red) · BPF test tenant · June 9 build</div>
    <div class="text-xs italic" style="color:#A1DBA6; font-family:'PT Serif',serif;">Authentic · Innovative · Expert</div>
  </div>
</footer>
</body></html>'''

out = os.path.join(os.path.dirname(__file__), "index.html")
open(out, "w", encoding="utf-8").write(HTML)
print(f"wrote {out} ({len(HTML)} bytes), {recorded}/{len(REVIEWS)} cards with video")

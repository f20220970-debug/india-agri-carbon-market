"""Rebuild docs/index.html from the model.  python src/build_docs.py"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import market_model as M  # noqa: E402

OUT = ROOT / "docs" / "index.html"


def main() -> int:
    rm, bc = M.rice_methane(), M.biochar()
    per_ha_rm = rm.credit_yield * rm.price
    per_ha_bc = bc.credit_yield * bc.price
    rm_lo, rm_hi = M.implied_developer_share(rm.credit_yield, rm.price)
    bc_lo, bc_hi = M.implied_developer_share(bc.credit_yield, bc.price)
    bc_cal = M.biochar(developer_share=(bc_lo + bc_hi) / 2)

    scen = []
    for share, label in [(0.01, "bear"), (0.03, "base"), (0.08, "bull")]:
        scen.append((label, share,
                     M.rice_methane(enrolled_share=share).developer_usd / 1e6,
                     M.biochar(enrolled_share=share,
                               developer_share=bc_cal.developer_share).developer_usd / 1e6))

    levers = [("Enrolled share", "1% - 8%",
               M.swing(M.sensitivity(M.rice_methane, "enrolled_share", [0.01, 0.03, 0.08]))),
              ("Credit yield", "0.7 - 1.8 t/ha",
               M.swing(M.sensitivity(M.rice_methane, "credit_yield", [0.7, 1.1, 1.8]))),
              ("Price", "$16 - $46/t",
               M.swing(M.sensitivity(M.rice_methane, "price", [16, 31, 46]))),
              ("Developer share", "35% - 65%",
               M.swing(M.sensitivity(M.rice_methane, "developer_share", [0.35, 0.50, 0.65])))]
    levers.sort(key=lambda r: -r[2])
    peak = levers[0][2]

    lever_rows = "".join(
        f"<div class='bar-row'><span class='bar-label'>{n}</span>"
        f"<span class='bar-track'><span class='bar-fill{' hot' if i == 0 else ''}' "
        f"style='width:{s / peak * 100:.1f}%'></span></span>"
        f"<span class='bar-value'>${s:.1f}m</span></div>"
        for i, (n, _, s) in enumerate(levers))

    scen_rows = "".join(
        f"<tr{' class=hi' if l == 'base' else ''}><td>{l} — {sh * 100:.0f}% of rice area</td>"
        f"<td class='n'>${r:,.1f}m</td><td class='n'>${b:,.1f}m</td></tr>"
        for l, sh, r, b in scen)

    comp = [("Sow&amp;Reap Agro (Telangana)", "~35,000", "37,405", "—", "Paddy, Gold Standard"),
            ("Boomitra India", "12,000+", "—", "10,117", "Soil carbon"),
            ("UP state programme", "25,000+", "—", "—", "Tree planting"),
            ("Grow Indigo", "—", "—", "—", "Soil, biochar, rice, agroforestry"),
            ("Varaha", "—", "—", "—", "Biochar")]
    comp_rows = "".join(
        f"<tr><td>{n}</td><td class='n'>{f}</td><td class='n'>{c}</td>"
        f"<td class='n'>{h}</td><td>{p}</td></tr>" for n, f, c, h, p in comp)

    html = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>India Agri Carbon Market</title>
<style>
:root{{--bg:#fbfaf8;--panel:#fff;--ink:#1a1a1a;--muted:#6b6b6b;--line:#e6e3de;
  --accent:#1f6f54;--warn:#b4531f;--rule:#d8d4cd}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --bg:#15161a;--panel:#1d1f24;--ink:#eceae6;--muted:#9c9a95;--line:#2d3038;
  --accent:#53b78f;--warn:#e08a4e;--rule:#343842}}}}
:root[data-theme="dark"]{{--bg:#15161a;--panel:#1d1f24;--ink:#eceae6;--muted:#9c9a95;
  --line:#2d3038;--accent:#53b78f;--warn:#e08a4e;--rule:#343842}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Inter,system-ui,sans-serif}}
.wrap{{max-width:900px;margin:0 auto;padding:48px 16px 80px}}
h1{{font-size:clamp(1.6rem,4vw,2.3rem);line-height:1.2;margin:0 0 8px;letter-spacing:-.02em}}
h2{{font-size:1.15rem;margin:44px 0 6px;letter-spacing:-.01em}}
.sub{{color:var(--muted);margin:0 0 6px}}
.lede{{color:var(--muted);max-width:64ch;margin:0 0 26px}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:18px 20px;margin:14px 0;overflow-x:auto}}
.flag{{border-left:3px solid var(--warn)}}
.kpis{{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));margin:24px 0}}
.kpi{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.kpi .n{{font-size:1.5rem;font-weight:650;letter-spacing:-.02em;font-variant-numeric:tabular-nums}}
.kpi .l{{color:var(--muted);font-size:.82rem;margin-top:2px}}
table{{width:100%;border-collapse:collapse;font-size:.9rem;font-variant-numeric:tabular-nums}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);white-space:nowrap}}
td.n{{text-align:right}}
th{{color:var(--muted);font-weight:600;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em}}
tbody tr:last-child td{{border-bottom:none}}
tr.hi td{{color:var(--warn);font-weight:600}}
.note{{font-size:.86rem;color:var(--muted);max-width:66ch}}
.bar-row{{display:grid;grid-template-columns:minmax(130px,1fr) 3fr 64px;gap:10px;
  align-items:center;padding:3px 0;font-size:.88rem}}
.bar-label{{color:var(--muted)}}
.bar-track{{background:var(--bg);border:1px solid var(--line);border-radius:999px;height:10px;overflow:hidden}}
.bar-fill{{display:block;height:100%;background:var(--rule);border-radius:999px}}
.bar-fill.hot{{background:var(--warn)}}
.bar-value{{text-align:right;color:var(--muted);font-variant-numeric:tabular-nums}}
a{{color:var(--accent)}}
</style></head><body><div class="wrap">

<h1>India Smallholder Carbon Removal</h1>
<p class="sub">Market sizing · pathway economics · where to play</p>
<p class="lede">Sizing India's agricultural carbon-removal opportunity on a base of
<strong>44.16 Mha</strong> of kharif rice. The useful finding is not the market size —
it is that the two leading pathways are different businesses, and a cross-check
against published farmer earnings is what shows it.</p>

<div class="kpis">
  <div class="kpi"><div class="n">${per_ha_rm:.0f}</div><div class="l">rice methane, gross credit per ha/yr</div></div>
  <div class="kpi"><div class="n">${per_ha_bc:.0f}</div><div class="l">biochar, gross credit per ha/yr</div></div>
  <div class="kpi"><div class="n">{per_ha_bc / per_ha_rm:.0f}×</div><div class="l">difference per hectare</div></div>
  <div class="kpi"><div class="n">{M.current_disclosed_share() * 100:.3f}%</div><div class="l">of the rice base enrolled today</div></div>
</div>

<h2>The cross-check that broke the first model</h2>
<div class="panel flag">
<table><thead><tr><th>Pathway</th><th class='n'>Gross $/ha/yr</th>
<th class='n'>Farmer at 50/50</th><th class='n'>Implied developer share</th></tr></thead><tbody>
<tr><td>Rice methane</td><td class='n'>${per_ha_rm:.1f}</td><td class='n'>${rm.farmer_usd_per_ha:.1f}</td>
<td class='n'>{rm_lo * 100:.0f}% to {rm_hi * 100:.0f}%</td></tr>
<tr><td>Biochar</td><td class='n'>${per_ha_bc:.1f}</td><td class='n'>${bc.farmer_usd_per_ha:.1f}</td>
<td class='n'>{bc_lo * 100:.0f}% to {bc_hi * 100:.0f}%</td></tr>
</tbody></table>
</div>
<p class="note">Published smallholder pilots earn <strong>US$20–70 per hectare per year</strong>.
A flat 50/50 split puts rice-methane farmers <em>below</em> that band and biochar farmers at
roughly three times its top — so the same split cannot describe both.</p>
<p class="note"><strong>The negative share is the finding.</strong> To pay a farmer $70/ha from
rice methane, the developer would have to pay out more than the credit is worth: the whole
credit generates ${per_ha_rm:.0f}/ha. Biochar's {bc_lo * 100:.0f}–{bc_hi * 100:.0f}% is what a
pyrolysis business looks like — the processor carries the equipment cost, so the credit cannot
be split like a land-based one. <strong>Biochar is a processing business that sources from farms;
rice methane is a farmer-aggregation business.</strong></p>

<h2>Size, under honest enrolment assumptions</h2>
<div class="panel">
<table><thead><tr><th>Scenario</th><th class='n'>Rice methane</th><th class='n'>Biochar</th></tr></thead>
<tbody>{scen_rows}</tbody></table>
</div>
<p class="note">Developer-side revenue per year. The only Indian programme publishing a hectare
figure covers <strong>10,117 ha — {M.current_disclosed_share() * 100:.3f}% of the rice base</strong>.
Even the bear case is roughly a 40× expansion on disclosed enrolment, so read these as
<em>if-then</em>, not as a forecast.</p>

<h2>What moves the answer</h2>
<div class="panel">{lever_rows}</div>
<p class="note">Swing in rice-methane developer revenue, one lever at a time.
<strong>Enrolment dominates — and it has the least evidence behind it.</strong> Price and yield
can be bounded from published data; enrolment cannot, because nobody has demonstrated it at
scale in India. That is where diligence belongs.</p>

<h2>Who is already doing this</h2>
<div class="panel">
<table><thead><tr><th>Programme</th><th class='n'>Farmers</th><th class='n'>Credits</th>
<th class='n'>Hectares</th><th>Practice</th></tr></thead><tbody>{comp_rows}</tbody></table>
</div>
<p class="note">Published figures only; dashes are undisclosed, not zero. Sow&amp;Reap's
<strong>1.07 credits per farmer</strong> is the only bottom-up check available on the
credit-yield assumption anywhere in this market — and it is credits per <em>farmer</em>,
not per hectare. That one missing conversion is the weakest link in every sizing of this
market, including this one.</p>

<p class="note" style="margin-top:40px">
Rice area from Ministry of Agriculture kharif sowing data via BigMint; emissions from
<a href="https://github.com/owid/co2-data">Our World in Data</a>; credit prices from the
Senken Q4 2026 benchmark; programme figures from the Institute for Competitiveness.
Every input is labelled fact or assumption in
<a href="https://github.com/f20220970-debug/india-agri-carbon-market/blob/main/data/SOURCES.md">SOURCES.md</a>. ·
<a href="https://github.com/f20220970-debug/india-agri-carbon-market">Model, memo and tests on GitHub</a>
</p>
</div></body></html>"""

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

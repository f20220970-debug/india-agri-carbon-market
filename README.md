# India Smallholder Agricultural Carbon Removal

**Market sizing, pathway economics and a competitive map for India's agricultural carbon-removal opportunity — built on a 44.16 Mha rice base, with every input labelled fact or assumption.**

Built for a Varaha application.

📊 **[Results](https://f20220970-debug.github.io/india-agri-carbon-market/)** · [Strategy memo](reports/strategy_memo.md) · [Workbook](model/india_agri_carbon_market.xlsx) · [Sources and assumptions](data/SOURCES.md)

---

## The finding

**Rice methane and biochar are not one market.** At base assumptions, one enrolled hectare generates:

| Pathway | Credit yield | Price | Gross credit value |
| --- | --- | --- | --- |
| Rice methane | 1.1 tCO₂e/ha/yr | $31/t | **$34/ha/yr** |
| Biochar | 2.5 tCO₂e/ha/yr | $180/t | **$450/ha/yr** |

A **13× difference per hectare**, driven by published Q4 2026 prices of $16–46/t for soil and agricultural credits against $150–210/t for biochar — which in turn reflect storage of 10–40 years against 100–1,000. The market is paying for permanence.

## The cross-check that broke the first version

My first pass split credit revenue 50/50 between developer and farmer for both pathways. Checked against published smallholder pilot earnings of **US$20–70/ha/yr**:

- Rice methane paid the farmer **$17.1/ha/yr** — below the band.
- Biochar paid **$225/ha/yr** — about three times its top.

Both cannot be right. Solving for the developer share the published band implies:

| Pathway | Implied developer share |
| --- | --- |
| Rice methane | **−105% to 41%** |
| Biochar | **84% to 96%** |

**The negative figure is the finding.** To pay a farmer $70/ha from rice methane, the developer would have to pay out more than the credit is worth — the whole credit generates $34/ha. Rice methane at these assumptions cannot reach the top of the published band at all.

Biochar's 84–96% is not developers taking advantage; it is what a pyrolysis business looks like, because the processor carries equipment and operating cost. **Biochar is a processing business that sources from farms. Rice methane is a farmer-aggregation business.** Different teams, different capital, different unit economics — and a blended "agri carbon" market size hides all of it.

## Size, under honest enrolment assumptions

Developer-side revenue per year:

| Enrolled share of rice area | Rice methane | Biochar |
| --- | --- | --- |
| 1% (bear) | $7.5m | $178.8m |
| **3% (base)** | **$22.6m** | **$536.5m** |
| 8% (bull) | $60.2m | $1,430.8m |

The only Indian programme publishing a hectare figure covers **10,117 ha — 0.023% of the rice base**. Even the bear case is roughly a 40× expansion on disclosed enrolment. These are *if-then*, not forecasts.

## What moves the answer

| Lever | Range tested | Swing in developer revenue |
| --- | --- | --- |
| **Enrolled share** | 1% → 8% | **$52.7m** |
| Credit yield | 0.7 → 1.8 t/ha | $22.6m |
| Price | $16 → $46/t | $21.8m |
| Developer share | 35% → 65% | $13.6m |

Enrolment dominates — and it is the input with the least evidence behind it. Price and yield can be bounded from published data; enrolment cannot, because nobody has demonstrated it at scale in India. **That is where diligence effort belongs, not in refining the price assumption.**

## Competitive map

Published figures only; dashes are undisclosed, not zero.

| Programme | Farmers | Credits issued | Hectares | Practice |
| --- | --- | --- | --- | --- |
| Sow&Reap Agro (Telangana) | ~35,000 | **37,405** (Gold Standard) | — | Paddy |
| Boomitra India | 12,000+ (6,000+ issued) | — | **10,117** | Soil carbon |
| UP state programme | 25,000+ | — | — | Tree planting |
| Grow Indigo | — | — | — | Soil, biochar, rice, agroforestry |
| Varaha | — | — | — | Biochar |

Sow&Reap's **1.07 credits per farmer** is the only bottom-up check available on the credit-yield assumption anywhere in this market — and it is credits per *farmer*, not per hectare. That one missing conversion is the weakest link in every sizing of this market, including this one.

## Run it

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python src/get_data.py        # ~15 MB, OWID emissions
python src/build_workbook.py  # 5-sheet Excel model, 64 live formulas
python src/build_docs.py
pytest                        # 15 tests
```

## Tests

Written against the claims the memo makes, not against a previous run: the pathway identities hold, developer and farmer shares reconcile to gross, revenue scales linearly with enrolment, biochar stays an order of magnitude above rice methane per hectare, **a flat 50/50 split still puts rice methane below and biochar above the published farmer band**, rice methane's implied developer share is still negative at the top of that band, and **enrolment is still the largest swing** — because the memo tells the reader to spend diligence there. If any of those stop holding, the recommendation is wrong and CI says so.

## What this does not claim

- Area and emissions figures are published and cited. **Credit yield, enrolment and the revenue split are assumptions**, each with its tested range in [SOURCES.md](data/SOURCES.md).
- No forecast of adoption — the scenarios are if-then.
- No position on permanence, additionality or MRV quality, which are the substantive debates in this market and ones a spreadsheet cannot settle.
- The model sizes supply-side revenue at a price; it does not establish that volume clears at that price. The 2022–23 collapse from $15–20/t to low single digits is what that risk looks like.
- One crop, one country, one year of prices.

# India smallholder carbon removal — where the business actually is

**To:** Growth / strategy
**Question:** How large is India's agricultural carbon-removal opportunity, and which pathway is the business?
**Base:** India's kharif rice area, 44.16 Mha (2025-26). All inputs sourced or labelled in [SOURCES.md](../data/SOURCES.md).

---

## Answer first

**Rice methane and biochar are not one market, and sizing them together hides the decision.**

At base assumptions, one enrolled hectare generates:

| Pathway | Credit yield | Price | **Gross credit value** |
| --- | --- | --- | --- |
| Rice methane | 1.1 tCO₂e/ha/yr | $31/t | **$34/ha/yr** |
| Biochar | 2.5 tCO₂e/ha/yr | $180/t | **$450/ha/yr** |

**13× difference per hectare.** That gap is not a modelling artefact — it comes from published Q4 2026 prices of **$16–46/t for soil and agricultural credits against $150–210/t for biochar**, which in turn reflect storage of 10–40 years versus 100–1,000 years. The market is paying for permanence, and permanence is the product.

## The cross-check that broke the first version of this model

My first pass split credit revenue 50/50 between developer and farmer for both pathways — the obvious assumption. Then I checked it against published smallholder pilot earnings of **US$20–70 per hectare per year**:

- Rice methane paid the farmer **$17.1/ha/yr** — below the band.
- Biochar paid **$225/ha/yr** — roughly three times its top.

Both cannot be right. Solving for the developer share the published band implies:

| Pathway | Implied developer share |
| --- | --- |
| Rice methane | **−105% to 41%** |
| Biochar | **84% to 96%** |

**The negative figure is the finding.** To pay a farmer $70/ha from rice methane, the developer would have to pay out more than the credit is worth — the whole credit generates $34/ha. Rice methane at these assumptions **cannot reach the top of the published farmer band at all.**

Biochar's 84–96% is not developers taking advantage; it is what a pyrolysis business looks like. The processor carries equipment and operating cost, so the credit cannot be split like a land-based one. **Biochar is a processing business that happens to source from farms. Rice methane is a farmer-aggregation business.** They need different teams, different capital and different unit economics, and a blended "agri carbon" market size obscures that.

## Size, under honest enrolment assumptions

Developer-side revenue at each enrolled share of the rice base:

| Enrolled share of rice area | Rice methane | Biochar |
| --- | --- | --- |
| 1% (bear) | $7.5m | $178.8m |
| **3% (base)** | **$22.6m** | **$536.5m** |
| 8% (bull) | $60.2m | $1,430.8m |

For scale: the only Indian programme publishing a hectare figure covers **10,117 ha — 0.023% of the rice base.** Even the bear case is roughly a 40× expansion on disclosed enrolment. This market is not mature; it has barely started, and every number above should be read as *what the opportunity becomes if enrolment happens*, not as a forecast that it will.

## What moves the answer

Rice methane, one lever at a time, developer revenue:

| Lever | Range tested | Swing |
| --- | --- | --- |
| **Enrolled share** | 1% → 8% | **$52.7m** |
| Credit yield | 0.7 → 1.8 t/ha | $22.6m |
| Price | $16 → $46/t | $21.8m |
| Developer share | 35% → 65% | $13.6m |

**Enrolment dominates, and it is the input with the least evidence behind it.** Price and yield can be bounded from published data; enrolment cannot, because nobody has demonstrated it at scale in India. That is where diligence effort belongs, not in refining the price assumption to the nearest dollar.

## Competitive picture

Only published figures. Blanks are genuinely undisclosed:

| Programme | Farmers | Credits issued | Hectares | Practice |
| --- | --- | --- | --- | --- |
| Sow&Reap Agro (Telangana) | ~35,000 | **37,405** (Gold Standard) | — | Paddy |
| Boomitra India | 12,000+ (6,000+ issued) | — | **10,117** | Soil carbon |
| UP state programme | 25,000+ | — | — | Tree planting |
| Grow Indigo | — | — | — | Soil, biochar, rice, agroforestry |
| Varaha | — | — | — | Biochar |

Sow&Reap's **1.07 credits per farmer** is the only bottom-up check available on the credit-yield assumption anywhere in this market — and it is credits per *farmer*, not per hectare. Converting it needs an enrolled-hectares-per-farmer figure nobody publishes. That single missing number is the weakest link in every sizing of this market, including this one.

## What I would check next

1. **Enrolled hectares per farmer**, from any programme willing to share it. It converts the one real yield datapoint into a usable per-hectare figure and tightens the largest assumption in the model.
2. **Biochar feedstock economics per tonne of residue**, not per hectare. If biochar revenue is set by residue processed, the per-hectare framing used here is the wrong unit and the sizing should be rebuilt on processing capacity.
3. **Whether CCTS offsets will admit agricultural methods, and on what terms.** A domestic compliance buyer changes the price floor, and the 2022–23 collapse from $15–20/t to low single digits is what a market without one looks like.
4. **Land tenure concentration by district.** Registries require clear land-use rights; leased land creates uncertainty over who receives proceeds. This caps enrolment in ways no price assumption captures.
5. **Buyer concentration.** The model sizes supply-side revenue at a price. It does not establish that volume clears at that price.

## What this does not claim

- Emissions and area figures are published and cited. **Credit yield, enrolment and revenue split are assumptions**, each with its tested range in [SOURCES.md](../data/SOURCES.md).
- No forecast of adoption. The scenarios are *if-then*, not predictions.
- No position on permanence, additionality or MRV quality — the substantive debates in this market, and ones a spreadsheet cannot settle.
- One crop, one country, one year of prices.

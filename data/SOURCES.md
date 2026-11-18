# Inputs, sources and what is assumed

Every number this model uses is listed here with its provenance and a label.
**Fact** means a published figure with a citation. **Assumption** means a
judgement I made, with the reasoning and the range tested in the sensitivity.
Nothing in the model is a number without one of those two labels.

Retrieved 18 November 2026.

## Facts

| Input | Value | Source |
| --- | --- | --- |
| India kharif rice sown area, 2025-26 | **44.16 Mha** (441.58 lakh ha) | [BigMint, kharif 2025-26 sowing](https://www.bigmint.co/insights/detail/india-rice-sowing-hits-fresh-peak-in-kharif-season-2025-26-acreage-expands-by-5-91-lakh-hectares-686073) |
| India kharif rice area, prior year | 43.57 Mha (435.68 lakh ha) | same |
| India kharif rice area, 5-year normal (FY20–FY24) | 40.31 Mha | same |
| India total methane emissions, 2024 | **859.3 Mt CO₂e** | [Our World in Data, CO₂ and GHG dataset](https://github.com/owid/co2-data) |
| India total methane, 2016 | 781.6 Mt CO₂e | same |
| India total GHG, 2024 | 4,262.4 Mt CO₂e | same |
| Agricultural / soil carbon credit price, Q4 2026 | **US$16–46 / tCO₂e** | [Senken price benchmark](https://www.senken.io/academy/carbon-credit-price) |
| Biochar credit price, Q4 2026 | **US$150–210 / tCO₂e** | same |
| Afforestation / reforestation price | US$21–40 / tCO₂e | same |
| Sow&Reap Agro (Telangana): paddy farmers | ~35,000 | [Institute for Competitiveness](https://competitiveness.in/climate-performance-as-income-how-carbon-credits-are-reaching-indian-farms/) |
| Sow&Reap Agro: credits issued | **37,405** (Gold Standard) | same |
| Boomitra India: farmers supported / with credits issued | 12,000+ / 6,000+ | same |
| Boomitra India: area | 25,000 acres (~10,117 ha) | same |
| Uttar Pradesh state tree programme | 25,000+ farmers, ~₹10,000 advance each | same |
| Smallholder pilot farmer earnings (global, outside India) | US$20–70 / ha / year | same |
| VCM price history | fell from US$15–20/t to low single digits in 2022–23, partial recovery in methane and biochar | same |

## Assumptions

| Input | Base | Range tested | Reasoning |
| --- | --- | --- | --- |
| Credit yield, rice methane (AWD and similar) | **1.1 tCO₂e / ha / yr** | 0.7 – 1.8 | Cross-checked against Sow&Reap's revealed **37,405 credits across ~35,000 farmers ≈ 1.07 credits per farmer**. Assumes roughly one hectare of enrolled paddy per farmer, which is the weak link in this chain and is flagged in the memo. |
| Credit yield, biochar | 2.5 tCO₂e / ha / yr | 1.5 – 4.0 | Constrained by crop-residue availability per hectare rather than by land area, which is why it does not scale with enrolment the way methane does. |
| Enrolled share of rice area by FY31 | 3.0% | 1.0% – 8.0% | Today's disclosed programmes total well under 0.1% of the 44.16 Mha rice base. Even the bull case is a large multiple of the current level. |
| Developer share of credit revenue | 50% | 35% – 65% | Split between farmer payments and the developer covering MRV, aggregation and sales. No published Indian benchmark found; the farmer-side figure is sanity-checked against the US$20–70/ha/yr pilot range. |
| USD / INR | 88 | — | Rounded spot rate, used only for presentation. |

## What is deliberately not modelled

- **Registry issuance lag.** Credits take seasons to verify and issue; the model
  values an annual run-rate, not cash timing.
- **Buyer demand.** The model sizes supply-side revenue at a given price. It
  does not claim that volume clears at that price, and the 2022–23 price
  collapse is the reason that caveat matters.
- **Permanence and reversal risk**, which is the substantive difference between
  soil carbon (10–40 year storage) and biochar (100–1,000 years) and is a large
  part of why the prices differ by roughly an order of magnitude.
- **Land tenure.** Registries generally require clear land-use rights, and
  leased land creates uncertainty over who receives proceeds. This is a real
  constraint on enrolment that no spreadsheet captures.

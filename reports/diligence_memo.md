# Screening six Indian agri-carbon programmes — and what they do to my own model

**To:** Growth / strategy
**Question:** Which publicly documented Indian agricultural carbon programmes are worth engaging with, and do their disclosures support the assumptions in [the sizing model](strategy_memo.md)?
**Method:** Six programmes screened on geography, pathway, registry, methodology, farmers, hectares, credits issued, farmer revenue share, disclosed payments, commercial risk and the next diligence question. Published figures only; every blank is "not disclosed", never zero. Sources in [SOURCES.md](../data/SOURCES.md), code in [`src/diligence.py`](../src/diligence.py), checks in [`tests/test_diligence.py`](../tests/test_diligence.py).

---

## Answer first

**The screen broke two assumptions in my own sizing model, and they push in opposite directions — so neither is a one-line fix.**

| Model assumption | What operators disclose | Effect |
| --- | --- | --- |
| Farmer takes **50%** of credit revenue | **55% – 75%** (Boomitra 55%, Varaha 70%, Grow Indigo 75%) | Developer revenue in the model is **overstated by 10%–50%** |
| Credit yield **1.1 tCO₂e/ha/yr** | **3.71 – 4.20 t/ha** implied by the published 1.5–1.7 credits/acre estimate for VM0042 | Developer revenue is **understated by ~3.4×** |

Netting the two off would be a coincidence, not an answer. The model keeps its sourced assumptions and records the disagreement, because **the two conflicts are different kinds of uncertainty**: the split is a disclosure problem (the number exists, operators just define it differently), and the yield is a measurement problem (nobody publishes credits per hectare at all).

## The split conflict: "net" is doing all the work

Three programmes publish a farmer share. Two of the three — Varaha's 70% and Grow Indigo's 75% — are promised on **net** revenue, with no published definition of the cost base deducted first. Boomitra's 55% is on **gross**.

A 75% share of net is not comparable to a 55% share of gross, and without the cost definition it cannot be converted. **So the headline number a developer markets to farmers is not a number an outside analyst can underwrite.** That is the single most important thing this screen found about how this market communicates.

It also means my model's 50/50 is not conservative, as I had assumed when I set it: it is below every disclosed share, so the $22.6m base case for rice methane is optimistic on this input.

## The yield conflict: still no credits per hectare

**Not one of the six programmes publishes both hectares and credits issued.** That is enforced as a test, because it is the structural gap in this market:

- Sow&Reap publishes credits (37,405) and farmers (~35,000) → **1.07 credits per farmer**, but no hectares.
- Boomitra publishes hectares (10,117) and farmers (12,000+), but no credits.
- Grow Indigo publishes farmers paid (2,550+) and mean payment (₹11,478 ≈ **$130**), but neither hectares nor credits.

The one directional figure available, 1.5–1.7 credits per acre per year under VM0042, is an expert estimate for soil carbon, not rice methane, and is explicitly site-dependent. It bounds my 1.1 t/ha assumption rather than replacing it — but it bounds it from **well above**, and that is worth knowing before quoting a per-hectare economics to anyone.

## Commercial risk the financial model does not price

Reporting on the two largest Verra grouped projects in Uttar Pradesh found enrolled farmers who did not know they were enrolled: of 15 farmers interviewed in Hardoi, none knew about the carbon project, and at least 10 gram panchayat heads were also unaware. One farmer asked whom he should approach to have his name removed.

This is not only a reputational matter. **Issuance under these methodologies is driven by documented evidence, and weak records can reduce issuance toward zero.** Consent and record quality are therefore an input to revenue, not a compliance afterthought — and no sizing model that starts from hectares captures it.

## Policy gate

Agriculture is a **Phase 1 sector** under India's CCTS offset mechanism, and BEE's Version 1 procedure requires a project start date **no earlier than 1 January 2025**. For a developer, that cuts both ways: it is a potential domestic compliance buyer, which would put a floor under a price band currently quoted at **$15–45/tCO₂e**, and it is a hard eligibility cut-off that excludes earlier-vintage project starts. Worth tracking as the single policy variable that could change the price assumption rather than the volume one.

## Ranked by what they let you check

| Programme | Discloses | Registry | Farmer share | Verdict |
| --- | --- | --- | --- | --- |
| Grow Indigo (Aadi) | 4 of 6 | Verra, VM0042 | 75% of net | **The one to study.** Only programme to issue *and* pay at scale under VM0042. |
| Boomitra | 4 of 6 | Verra (2889) | 55% of gross | Comparable unit economics, but UP consent risk is live. |
| Sow&Reap Agro | 3 of 6 | Gold Standard | — | Holds the only bottom-up yield datapoint in the market. |
| Varaha ClimateAg | 2 of 6 | Verra (3346) | 70% of net | Highest farmer share promised; cost base undefined. |
| UP state programme | 1 of 6 | — | — | Pays ~₹10,000 advances against unissued credits — sets the farmer price expectation a private developer must match in the same districts. |
| EKI Energy Services | 1 of 6 | Verra (pipeline) | — | Cannot be unit-checked, so cannot be benchmarked against. |

## The five questions I would ask next, in order

1. **Mean enrolled area per paid farmer at Grow Indigo.** It converts the only real payment datapoint ($130/farmer) into a per-hectare figure and closes the largest gap in the sizing model.
2. **What "net" deducts**, at Varaha and Grow Indigo. Until this is defined, no disclosed farmer share is comparable to any other.
3. **Hectares behind Sow&Reap's 37,405 credits**, and over how many crop years. It is the only route to a bottom-up credits-per-hectare figure.
4. **Whether any verification cycle has cut issuance on consent or records grounds.** This prices the risk above.
5. **Whether CCTS Version 1 admits rice methane and biochar methods specifically**, not just "agriculture".

## What this screen does not claim

- Six programmes is not the market. It is the set that publishes enough to be screened at all, which is itself the point.
- Promised revenue shares are promises. No public source verifies payment against them.
- The reporting on consent in Uttar Pradesh concerns two named projects and 15 interviewed farmers; it is not a measured rate.
- No view on permanence, additionality or MRV quality.

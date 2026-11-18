"""Sizing model for India's smallholder agricultural carbon-removal market.

Every input carries a label in data/SOURCES.md: a published figure with a
citation, or an assumption with the range tested here. The model itself is
deliberately simple arithmetic -- the work is in which quantities are chosen
and which are varied, not in the formula.

Structure:

    enrolled hectares  = rice area x enrolled share
    credits per year   = enrolled hectares x credit yield per hectare
    gross credit value = credits x price per tonne
    developer revenue  = gross value x developer share

Two pathways are modelled separately because they behave differently:

  * RICE METHANE scales with enrolled land. Cheap per tonne, abundant per
    hectare, short storage.
  * BIOCHAR is capped by crop residue available per hectare, not by land. Dear
    per tonne, scarce per hectare, long storage.

Treating them as one blended market hides the thing a strategy team needs to
decide, which is which of the two the business is actually in.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, replace

# --- facts (see data/SOURCES.md) --------------------------------------------
RICE_AREA_MHA = 44.16          # kharif 2025-26 sown area
RICE_AREA_PRIOR_MHA = 43.57
RICE_AREA_NORMAL_MHA = 40.31   # FY20-FY24 five-year average
INDIA_METHANE_2024_MT = 859.294
INDIA_METHANE_2016_MT = 781.626
INDIA_TOTAL_GHG_2024_MT = 4262.411

PRICE_SOIL_LOW, PRICE_SOIL_HIGH = 16.0, 46.0        # USD / tCO2e
PRICE_BIOCHAR_LOW, PRICE_BIOCHAR_HIGH = 150.0, 210.0
SOWREAP_CREDITS = 37_405
SOWREAP_FARMERS = 35_000
BOOMITRA_HECTARES = 10_117
USD_INR = 88.0


@dataclass(frozen=True)
class Pathway:
    """One carbon-removal pathway, with the levers that move its revenue."""
    name: str
    credit_yield: float        # tCO2e per enrolled hectare per year
    price: float               # USD per tCO2e
    enrolled_share: float      # share of the rice-area base enrolled
    developer_share: float = 0.50
    area_mha: float = RICE_AREA_MHA

    @property
    def enrolled_ha(self) -> float:
        return self.area_mha * 1e6 * self.enrolled_share

    @property
    def credits(self) -> float:
        return self.enrolled_ha * self.credit_yield

    @property
    def gross_usd(self) -> float:
        return self.credits * self.price

    @property
    def developer_usd(self) -> float:
        return self.gross_usd * self.developer_share

    @property
    def farmer_usd_per_ha(self) -> float:
        """What reaches the farmer per hectare per year.

        The sanity check on the whole model: published smallholder pilots
        outside India report US$20-70/ha/yr. A pathway that implies far more
        than that is assuming away either the revenue split or the yield.
        """
        if self.enrolled_ha == 0:
            return 0.0
        return (self.gross_usd * (1 - self.developer_share)) / self.enrolled_ha

    def summary(self) -> dict:
        return {
            **asdict(self),
            "enrolled_ha": round(self.enrolled_ha),
            "credits_tco2e": round(self.credits),
            "gross_usd_m": round(self.gross_usd / 1e6, 1),
            "developer_usd_m": round(self.developer_usd / 1e6, 1),
            "developer_inr_cr": round(self.developer_usd * USD_INR / 1e7, 0),
            "farmer_usd_per_ha": round(self.farmer_usd_per_ha, 1),
        }


# --- base cases --------------------------------------------------------------

def rice_methane(**kw) -> Pathway:
    return replace(Pathway("Rice methane", 1.1, 31.0, 0.03), **kw)


def biochar(**kw) -> Pathway:
    return replace(Pathway("Biochar", 2.5, 180.0, 0.03), **kw)


def revealed_yield_per_farmer() -> float:
    """Credits per farmer actually issued by a disclosed Indian paddy programme.

    This is the only bottom-up check available on the credit-yield assumption,
    and it is weaker than it looks: it is credits per FARMER, and converting it
    to credits per hectare needs an enrolled-hectares-per-farmer figure that
    nobody publishes.
    """
    return SOWREAP_CREDITS / SOWREAP_FARMERS


def current_disclosed_share() -> float:
    """Disclosed programme area as a share of the rice base.

    Deliberately conservative: it counts only the one programme that published
    a hectare figure, so it understates the true enrolled area. Even generous
    reworkings leave the answer far below one percent, which is the point.
    """
    return BOOMITRA_HECTARES / (RICE_AREA_MHA * 1e6)


def scenarios() -> list[Pathway]:
    out = []
    for share, label in [(0.01, "bear"), (0.03, "base"), (0.08, "bull")]:
        out.append(rice_methane(enrolled_share=share, name=f"Rice methane ({label})"))
        out.append(biochar(enrolled_share=share, name=f"Biochar ({label})"))
    return out


def sensitivity(path_fn, lever: str, values: list[float]) -> list[dict]:
    """Vary one lever, hold everything else, and report the swing."""
    rows = []
    for v in values:
        p = path_fn(**{lever: v})
        rows.append({"lever": lever, "value": v,
                     "developer_usd_m": round(p.developer_usd / 1e6, 1),
                     "farmer_usd_per_ha": round(p.farmer_usd_per_ha, 1)})
    return rows


def swing(rows: list[dict]) -> float:
    """Range of developer revenue across a lever's tested values, in USD m."""
    vals = [r["developer_usd_m"] for r in rows]
    return round(max(vals) - min(vals), 1)


# --- the cross-check that broke the first version of this model --------------

FARMER_USD_PER_HA_LOW, FARMER_USD_PER_HA_HIGH = 20.0, 70.0   # published pilots


def implied_developer_share(credit_yield: float, price: float,
                            farmer_low: float = FARMER_USD_PER_HA_LOW,
                            farmer_high: float = FARMER_USD_PER_HA_HIGH
                            ) -> tuple[float, float]:
    """Developer share consistent with published farmer earnings per hectare.

    Rearranges farmer_per_ha = yield x price x (1 - developer_share).

    This exists because a flat 50/50 split -- the obvious first assumption --
    puts rice-methane farmers slightly BELOW the published US$20-70/ha/yr band
    and biochar farmers at roughly three times its top. Both cannot be right,
    and the gap is not noise: it says biochar is not a per-hectare business at
    all. Its revenue is set by residue processed, and the processor carries
    pyrolysis cost, so the developer necessarily keeps far more of the credit.

    Returns the (low, high) developer share implied by the farmer band.
    """
    per_ha = credit_yield * price
    if per_ha <= 0:
        return (float("nan"), float("nan"))
    # A higher farmer payment implies a lower developer share.
    return (1 - farmer_high / per_ha, 1 - farmer_low / per_ha)


def farmer_check(p: Pathway) -> dict:
    """Does this pathway's implied farmer payment sit in the published band?"""
    v = p.farmer_usd_per_ha
    return {"pathway": p.name, "farmer_usd_per_ha": round(v, 1),
            "below_band": v < FARMER_USD_PER_HA_LOW,
            "above_band": v > FARMER_USD_PER_HA_HIGH,
            "in_band": FARMER_USD_PER_HA_LOW <= v <= FARMER_USD_PER_HA_HIGH}

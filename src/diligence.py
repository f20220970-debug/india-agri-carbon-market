"""Screening tracker for publicly documented Indian agri-carbon programmes.

Every field below is a published figure with a citation in data/SOURCES.md, or
an explicit None. None means "not disclosed", never zero -- the gaps are part
of the finding, because a programme that does not publish its hectares cannot
be unit-checked by anyone outside it.

The tracker exists to test the sizing model in market_model.py against what
operators actually disclose. Two of its assumptions do not survive that test:
the revenue split and the credit yield.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict

USD_INR = 88.0
ACRE_PER_HA = 2.47105


@dataclass(frozen=True)
class Programme:
    name: str
    operator_type: str          # startup | corporate | state programme
    geography: str
    pathway: str
    registry: str | None
    methodology: str | None
    project_id: str | None
    status: str
    farmers: int | None
    hectares: float | None
    credits_issued: int | None
    farmer_share_pct: float | None   # share of revenue promised to the farmer
    share_basis: str | None          # "net" | "gross" | None
    farmer_paid_inr: float | None    # mean payment actually disclosed
    commercial_risk: str
    next_question: str

    @property
    def farmer_paid_usd(self) -> float | None:
        if self.farmer_paid_inr is None:
            return None
        return round(self.farmer_paid_inr / USD_INR, 1)

    @property
    def credits_per_farmer(self) -> float | None:
        if self.credits_issued is None or not self.farmers:
            return None
        return round(self.credits_issued / self.farmers, 3)

    @property
    def disclosure_score(self) -> int:
        """How many of the six unit-economics fields the programme publishes."""
        fields = (self.registry, self.methodology, self.farmers, self.hectares,
                  self.credits_issued, self.farmer_share_pct)
        return sum(1 for f in fields if f is not None)


PROGRAMMES: list[Programme] = [
    Programme(
        name="Varaha ClimateAg",
        operator_type="startup",
        geography="Punjab, Haryana; expanding to Uttar Pradesh",
        pathway="Biochar, soil carbon, regenerative rice, agroforestry",
        registry="Verra", methodology=None, project_id="3346",
        status="Registered, grouped project",
        farmers=None, hectares=None, credits_issued=None,
        farmer_share_pct=70.0, share_basis="net",
        farmer_paid_inr=None,
        commercial_risk=(
            "Farmer share is promised on NET revenue with no public definition "
            "of the cost base, so the realised split is unverifiable from outside."),
        next_question=(
            "What costs are deducted before 'net', and what did the realised "
            "per-hectare farmer payment come to on the first issuance?"),
    ),
    Programme(
        name="Boomitra (India grouped project)",
        operator_type="startup",
        geography="Uttar Pradesh and others",
        pathway="Soil carbon",
        registry="Verra", methodology=None, project_id="2889",
        status="Registered; UP component under verification",
        farmers=12_000, hectares=10_117.0, credits_issued=None,
        farmer_share_pct=55.0, share_basis="gross",
        farmer_paid_inr=None,
        commercial_risk=(
            "Reporting found enrolled farmers and gram panchayat heads in Hardoi "
            "unaware of the project; consent and records quality are the input "
            "to issuance, so weak documentation can cut issuance toward zero."),
        next_question=(
            "What share of enrolled farmers can evidence informed consent, and "
            "has any verification cycle reduced issuance on that ground?"),
    ),
    Programme(
        name="Grow Indigo - Aadi",
        operator_type="startup (Mahyco / Indigo Ag JV)",
        geography="Punjab, Haryana",
        pathway="Soil carbon, regenerative rice",
        registry="Verra", methodology="VM0042", project_id=None,
        status="Issued and paid out",
        farmers=2_550, hectares=None, credits_issued=None,
        farmer_share_pct=75.0, share_basis="net",
        farmer_paid_inr=11_478.0,
        commercial_risk=(
            "The only programme that has actually paid at scale, but it pays per "
            "FARMER and publishes no hectares, so cost per hectare -- the unit a "
            "developer is underwriting -- cannot be derived."),
        next_question=(
            "What is the mean enrolled area per paid farmer? It converts the one "
            "real payment datapoint into a per-hectare figure."),
    ),
    Programme(
        name="Sow&Reap Agro",
        operator_type="startup",
        geography="Telangana",
        pathway="Paddy",
        registry="Gold Standard", methodology=None, project_id=None,
        status="Credits issued",
        farmers=35_000, hectares=None, credits_issued=37_405,
        farmer_share_pct=None, share_basis=None,
        farmer_paid_inr=None,
        commercial_risk=(
            "1.07 credits per farmer is the only bottom-up yield check in the "
            "market, and it is per farmer, not per hectare."),
        next_question=(
            "Enrolled hectares behind the 37,405 credits, and over how many "
            "crop years they were earned."),
    ),
    Programme(
        name="Uttar Pradesh state tree programme",
        operator_type="state programme",
        geography="Uttar Pradesh",
        pathway="Tree planting",
        registry=None, methodology=None, project_id=None,
        status="Advances paid against future credits",
        farmers=25_000, hectares=None, credits_issued=None,
        farmer_share_pct=None, share_basis=None,
        farmer_paid_inr=10_000.0,
        commercial_risk=(
            "Pays an advance against credits not yet issued, so the state carries "
            "issuance risk. Sets a farmer price expectation a private developer "
            "then has to match in the same districts."),
        next_question=(
            "Have any credits actually been issued against the advances, and on "
            "what standard?"),
    ),
    Programme(
        name="EKI Energy Services",
        operator_type="corporate",
        geography="India (unspecified)",
        pathway="Reforestation, land management",
        registry="Verra", methodology=None, project_id=None,
        status="In pipeline, not registered",
        farmers=None, hectares=None, credits_issued=None,
        farmer_share_pct=None, share_basis=None,
        farmer_paid_inr=None,
        commercial_risk=(
            "Discloses nothing beyond pipeline presence. Included deliberately: "
            "a competitor that cannot be unit-checked is a competitor whose costs "
            "cannot be benchmarked either."),
        next_question="Any registered AFOLU project, or is this pipeline only?",
    ),
]

# --- published figures used as tests of the sizing model ---------------------

# Expert estimate for VM0042 soil carbon, credits per ACRE per year.
VM0042_CREDITS_PER_ACRE = (1.5, 1.7)
# Late-2025 price band quoted for these Indian projects, USD per tCO2e.
PRICE_BAND_USD = (15.0, 45.0)
# CCTS offset mechanism: agriculture is a Phase 1 sector, and a project's start
# date must be no earlier than this to be eligible.
CCTS_EARLIEST_START = "2025-01-01"


def vm0042_credits_per_ha() -> tuple[float, float]:
    """The acre-based published yield, converted to hectares."""
    lo, hi = VM0042_CREDITS_PER_ACRE
    return (round(lo * ACRE_PER_HA, 2), round(hi * ACRE_PER_HA, 2))


def disclosed_farmer_shares() -> list[tuple[str, float, str]]:
    """Every programme that publishes a farmer revenue share."""
    return [(p.name, p.farmer_share_pct, p.share_basis)
            for p in PROGRAMMES if p.farmer_share_pct is not None]


def split_assumption_verdict(assumed_farmer_share: float = 0.50) -> dict:
    """Does the model's revenue split sit inside what operators disclose?

    The sizing model assumes a flat 50/50. Every programme that publishes a
    number promises the farmer MORE than half. If those promises are kept, the
    model overstates developer revenue -- by a third at the extreme.
    """
    shares = [s for _, s, _ in disclosed_farmer_shares()]
    lo, hi = min(shares) / 100, max(shares) / 100
    assumed_dev = 1 - assumed_farmer_share
    return {
        "assumed_farmer_share": assumed_farmer_share,
        "disclosed_farmer_share_low": lo,
        "disclosed_farmer_share_high": hi,
        "model_inside_disclosed_range": lo <= assumed_farmer_share <= hi,
        "developer_revenue_overstated_low_pct": round(
            (assumed_dev - (1 - lo)) / assumed_dev * 100, 1),
        "developer_revenue_overstated_high_pct": round(
            (assumed_dev - (1 - hi)) / assumed_dev * 100, 1),
        "caveat": ("Two of the three shares are promised on 'net' revenue with "
                   "no published cost base, so they are not comparable to a "
                   "gross-revenue split without that definition."),
    }


def yield_assumption_verdict(model_credit_yield: float = 1.1) -> dict:
    """Does the model's credit yield sit inside the published estimate?"""
    lo, hi = vm0042_credits_per_ha()
    return {
        "model_credit_yield_t_per_ha": model_credit_yield,
        "published_low_t_per_ha": lo,
        "published_high_t_per_ha": hi,
        "model_inside_published_range": lo <= model_credit_yield <= hi,
        "model_understates_by_x": round(lo / model_credit_yield, 2),
        "caveat": ("The published figure is a directional, site-dependent "
                   "expert estimate for VM0042 soil carbon, not rice methane, "
                   "so it bounds the assumption rather than replacing it."),
    }


def ranked_by_disclosure() -> list[Programme]:
    return sorted(PROGRAMMES, key=lambda p: -p.disclosure_score)


def rows() -> list[dict]:
    out = []
    for p in PROGRAMMES:
        d = asdict(p)
        d["farmer_paid_usd"] = p.farmer_paid_usd
        d["credits_per_farmer"] = p.credits_per_farmer
        d["disclosure_score"] = p.disclosure_score
        out.append(d)
    return out

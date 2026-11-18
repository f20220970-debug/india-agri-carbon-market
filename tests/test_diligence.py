"""Tests on the screening tracker.

These fail if a published figure is edited without its citation, and -- more
usefully -- if someone quietly "fixes" the sizing model's assumptions so that
the two conflicts the tracker found disappear. The conflicts are the finding.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import diligence as D  # noqa: E402
import market_model as M  # noqa: E402


def test_six_programmes_screened():
    assert len(D.PROGRAMMES) == 6
    assert len({p.name for p in D.PROGRAMMES}) == 6


def test_undisclosed_fields_are_none_not_zero():
    """A blank must never be read as zero: it is the gap, not a value."""
    for p in D.PROGRAMMES:
        for v in (p.farmers, p.hectares, p.credits_issued,
                  p.farmer_share_pct, p.farmer_paid_inr):
            assert v is None or v > 0


def test_every_programme_has_a_risk_and_a_next_question():
    for p in D.PROGRAMMES:
        assert len(p.commercial_risk) > 40
        assert p.next_question.endswith(("?", "."))


def test_only_one_programme_has_paid_at_scale_with_a_mean():
    paid = [p for p in D.PROGRAMMES if p.farmer_paid_inr and p.farmers]
    assert {p.name for p in paid} == {"Grow Indigo - Aadi",
                                      "Uttar Pradesh state tree programme"}


def test_no_programme_publishes_both_hectares_and_credits():
    """The missing conversion, stated as a test.

    Credits per hectare is the number every sizing of this market rests on,
    and not one disclosed Indian programme publishes both halves of it.
    """
    assert not any(p.hectares and p.credits_issued for p in D.PROGRAMMES)


def test_sowreap_credits_per_farmer():
    p = next(p for p in D.PROGRAMMES if p.name == "Sow&Reap Agro")
    assert p.credits_per_farmer == 1.069
    assert abs(p.credits_per_farmer - M.revealed_yield_per_farmer()) < 1e-3


def test_grow_indigo_mean_payment_in_usd():
    p = next(p for p in D.PROGRAMMES if p.name == "Grow Indigo - Aadi")
    assert p.farmer_paid_usd == 130.4


# --- the two conflicts with the sizing model --------------------------------

def test_model_revenue_split_sits_below_every_disclosed_share():
    v = D.split_assumption_verdict(assumed_farmer_share=0.50)
    assert v["model_inside_disclosed_range"] is False
    assert v["disclosed_farmer_share_low"] == 0.55
    assert v["disclosed_farmer_share_high"] == 0.75
    # Developer revenue in the sizing model is overstated by 10%-50%.
    assert v["developer_revenue_overstated_low_pct"] == 10.0
    assert v["developer_revenue_overstated_high_pct"] == 50.0


def test_model_credit_yield_sits_below_the_published_estimate():
    v = D.yield_assumption_verdict(M.rice_methane().credit_yield)
    assert v["model_inside_published_range"] is False
    assert v["published_low_t_per_ha"] == 3.71
    assert v["model_understates_by_x"] == 3.37


def test_the_two_conflicts_push_in_opposite_directions():
    """Why neither is a one-line fix.

    The split conflict cuts developer revenue; the yield conflict raises it.
    Netting them off would be a coincidence, not an answer, so the model keeps
    its sourced assumptions and the tracker records the disagreement.
    """
    split = D.split_assumption_verdict(0.50)
    yield_ = D.yield_assumption_verdict(M.rice_methane().credit_yield)
    assert split["developer_revenue_overstated_low_pct"] > 0   # revenue too high
    assert yield_["model_understates_by_x"] > 1                # revenue too low


def test_price_band_overlaps_the_models_soil_price():
    lo, hi = D.PRICE_BAND_USD
    assert lo <= M.rice_methane().price <= hi


def test_ccts_start_date_gate_is_recorded():
    assert D.CCTS_EARLIEST_START == "2025-01-01"


def test_disclosure_ranking_puts_the_opaque_last():
    ranked = D.ranked_by_disclosure()
    assert ranked[-1].name == "EKI Energy Services"
    assert ranked[0].disclosure_score >= 4


def test_rows_are_serialisable_and_complete():
    rows = D.rows()
    assert len(rows) == 6
    assert all("disclosure_score" in r and "farmer_paid_usd" in r for r in rows)

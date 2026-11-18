"""Tests for the sizing model.

The model is arithmetic, so these check the things that would silently produce
a wrong answer: the identities holding, the published cross-checks still
failing/passing the way the memo says, and the sourced constants being what
SOURCES.md claims.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import market_model as M  # noqa: E402


def test_sourced_constants_match_sources_md():
    """If a cited figure is edited, SOURCES.md must be edited with it."""
    assert M.RICE_AREA_MHA == 44.16
    assert M.INDIA_METHANE_2024_MT == pytest.approx(859.294)
    assert (M.PRICE_SOIL_LOW, M.PRICE_SOIL_HIGH) == (16.0, 46.0)
    assert (M.PRICE_BIOCHAR_LOW, M.PRICE_BIOCHAR_HIGH) == (150.0, 210.0)
    assert M.SOWREAP_CREDITS == 37_405


def test_pathway_identities_hold():
    p = M.rice_methane()
    assert p.credits == pytest.approx(p.enrolled_ha * p.credit_yield)
    assert p.gross_usd == pytest.approx(p.credits * p.price)
    assert p.developer_usd == pytest.approx(p.gross_usd * p.developer_share)


def test_developer_and_farmer_shares_sum_to_gross():
    p = M.biochar()
    farmer_total = p.farmer_usd_per_ha * p.enrolled_ha
    assert p.developer_usd + farmer_total == pytest.approx(p.gross_usd)


def test_zero_enrolment_is_zero_everywhere():
    p = M.rice_methane(enrolled_share=0.0)
    assert p.credits == 0 and p.gross_usd == 0 and p.farmer_usd_per_ha == 0


def test_revenue_scales_linearly_with_enrolment():
    a = M.rice_methane(enrolled_share=0.01).developer_usd
    b = M.rice_methane(enrolled_share=0.08).developer_usd
    assert b == pytest.approx(a * 8)


def test_biochar_is_worth_an_order_of_magnitude_more_per_hectare():
    """The memo's headline. If this stops holding, the recommendation changes."""
    rm, bc = M.rice_methane(), M.biochar()
    per_ha_rm = rm.credit_yield * rm.price
    per_ha_bc = bc.credit_yield * bc.price
    assert per_ha_bc / per_ha_rm > 10


def test_flat_split_puts_rice_methane_below_the_published_farmer_band():
    """The cross-check that broke the first version of the model."""
    p = M.rice_methane(developer_share=0.50)
    assert M.farmer_check(p)["below_band"]


def test_flat_split_puts_biochar_far_above_the_published_farmer_band():
    p = M.biochar(developer_share=0.50)
    chk = M.farmer_check(p)
    assert chk["above_band"]
    assert chk["farmer_usd_per_ha"] > 3 * M.FARMER_USD_PER_HA_LOW


def test_rice_methane_cannot_fund_the_top_of_the_farmer_band():
    """Implied developer share goes negative: the credit is worth less than
    the payment it would have to fund. This is the memo's sharpest claim."""
    low, high = M.implied_developer_share(1.1, 31.0)
    assert low < 0
    assert 0 < high < 0.5


def test_biochar_implied_share_is_processor_shaped():
    low, high = M.implied_developer_share(2.5, 180.0)
    assert 0.80 < low < high < 1.0


def test_calibrated_biochar_lands_inside_the_band():
    low, high = M.implied_developer_share(2.5, 180.0)
    p = M.biochar(developer_share=(low + high) / 2)
    assert M.farmer_check(p)["in_band"]


def test_disclosed_enrolment_is_a_tiny_share_of_the_base():
    """If this ever exceeds 1%, the 'barely started' framing is wrong."""
    assert 0 < M.current_disclosed_share() < 0.01


def test_revealed_yield_per_farmer_is_about_one_credit():
    assert 1.0 < M.revealed_yield_per_farmer() < 1.2


def test_enrolment_is_the_largest_swing_for_rice_methane():
    """The memo tells the reader to spend diligence on enrolment. If another
    lever overtakes it, that advice is wrong."""
    swings = {
        "enrolled_share": M.swing(M.sensitivity(
            M.rice_methane, "enrolled_share", [0.01, 0.03, 0.08])),
        "price": M.swing(M.sensitivity(
            M.rice_methane, "price", [16, 31, 46])),
        "credit_yield": M.swing(M.sensitivity(
            M.rice_methane, "credit_yield", [0.7, 1.1, 1.8])),
        "developer_share": M.swing(M.sensitivity(
            M.rice_methane, "developer_share", [0.35, 0.50, 0.65])),
    }
    assert max(swings, key=swings.get) == "enrolled_share"


def test_scenarios_cover_all_three_enrolment_levels_per_pathway():
    names = [p.name for p in M.scenarios()]
    assert len(names) == 6
    assert sum("Rice methane" in n for n in names) == 3
    assert sum("Biochar" in n for n in names) == 3

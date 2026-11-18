"""Build the sizing workbook.  python src/build_workbook.py

Colour code: blue = sourced figure or assumption you may change,
black = live formula, yellow fill = the levers meant to be moved.
Every derived number is a formula referencing its inputs.
"""
from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import market_model as M  # noqa: E402
import diligence as D  # noqa: E402

ACRE = D.ACRE_PER_HA

OUT = ROOT / "model" / "india_agri_carbon_market.xlsx"

F = "Arial"
BLUE = Font(name=F, size=10, color="0000FF")
BLACK = Font(name=F, size=10)
BOLD = Font(name=F, size=10, bold=True)
TITLE = Font(name=F, size=14, bold=True)
H2 = Font(name=F, size=11, bold=True)
MUTED = Font(name=F, size=9, italic=True, color="595959")
WARN = Font(name=F, size=10, bold=True, color="B4531F")
YELLOW = PatternFill("solid", fgColor="FFFF00")
HEAD = PatternFill("solid", fgColor="D9D9D9")
BOX = Border(bottom=Side(style="thin", color="BFBFBF"))

USD = '$#,##0;($#,##0);-'
USDM = '$#,##0.0,,"m"'
PCT = "0.0%"
NUM = "#,##0"
T2 = "0.00"


def put(ws, r, c, v, font=BLACK, fmt=None, fill=None):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = font
    if fmt:
        cell.number_format = fmt
    if fill:
        cell.fill = fill
    return cell


def header(ws, r, labels, start=2):
    for i, lab in enumerate(labels):
        c = put(ws, r, start + i, lab, BOLD, fill=HEAD)
        c.border = BOX
        c.alignment = Alignment(horizontal="center", wrap_text=True)


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[get_column_letter(col)].width = w


def main() -> int:
    wb = Workbook()
    wb.remove(wb.active)

    # ---------------- Cover ----------------
    ws = wb.create_sheet("Cover")
    widths(ws, {1: 3, 2: 48, 3: 15, 4: 15, 5: 46})
    put(ws, 2, 2, "India Smallholder Agricultural Carbon Removal", TITLE)
    put(ws, 3, 2, "Market sizing, pathway economics and where to play", MUTED)

    put(ws, 5, 2, "Question", H2)
    put(ws, 6, 2, "How big is the opportunity, and which pathway is the business?", BLACK)

    put(ws, 8, 2, "Answer", H2)
    put(ws, 9, 2, "Rice methane and biochar are not one market. At base", BLACK)
    put(ws, 10, 2, "assumptions a hectare of rice methane generates a credit", BLACK)
    put(ws, 11, 2, "worth about $34/yr in total; biochar generates about $450.", BLACK)
    put(ws, 12, 2, "That difference decides the operating model, not the pitch.", BLACK)

    put(ws, 14, 2, "Gross credit value per hectare per year", H2)
    put(ws, 15, 2, "Rice methane", BLACK)
    put(ws, 15, 3, "=Pathways!D6*Pathways!E6", BLACK, USD)
    put(ws, 16, 2, "Biochar", BLACK)
    put(ws, 16, 3, "=Pathways!D7*Pathways!E7", BLACK, USD)
    put(ws, 17, 2, "Ratio", BOLD)
    put(ws, 17, 3, "=C16/C15", BOLD, "0.0x")

    put(ws, 19, 2, "Enrolment today, as a share of the rice base", H2)
    put(ws, 20, 2, "Disclosed programme area (ha)", BLACK)
    put(ws, 20, 3, M.BOOMITRA_HECTARES, BLUE, NUM)
    put(ws, 21, 2, "India kharif rice area (ha)", BLACK)
    put(ws, 21, 3, M.RICE_AREA_MHA * 1e6, BLUE, NUM)
    put(ws, 22, 2, "Share", BOLD)
    put(ws, 22, 3, "=C20/C21", BOLD, "0.000%")
    put(ws, 23, 2, "The market is not mature; it is barely started.", MUTED)

    put(ws, 25, 2, "Colour code", H2)
    put(ws, 26, 2, "Blue", BLUE); put(ws, 26, 3, "sourced figure or assumption", MUTED)
    put(ws, 27, 2, "Black", BLACK); put(ws, 27, 3, "live formula", MUTED)
    put(ws, 28, 2, "Yellow", BLACK, fill=YELLOW); put(ws, 28, 3, "lever to move", MUTED)
    put(ws, 30, 2, "Every input is listed with its source or its reasoning in "
                   "data/SOURCES.md. Facts are cited; assumptions carry the "
                   "range tested on the Sensitivity sheet.", MUTED)

    # ---------------- Pathways ----------------
    ws = wb.create_sheet("Pathways")
    widths(ws, {1: 3, 2: 18, 3: 13, 4: 13, 5: 11, 6: 13, 7: 14, 8: 14, 9: 15, 10: 15})
    put(ws, 2, 2, "Pathway economics", TITLE)
    put(ws, 3, 2, "Yellow cells are the levers. Everything right of them is a formula.", MUTED)
    header(ws, 5, ["Pathway", "Enrolled share", "Credit yield (t/ha/yr)",
                   "Price ($/t)", "Developer share", "Enrolled ha",
                   "Credits (t/yr)", "Gross ($)", "Developer ($)",
                   "Farmer ($/ha/yr)"])
    rows = [("Rice methane", 0.03, 1.1, 31.0, 0.50),
            ("Biochar", 0.03, 2.5, 180.0, 0.90)]
    r = 6
    for name, share, yld, price, dev in rows:
        put(ws, r, 2, name, BLUE)
        put(ws, r, 3, share, BLUE, PCT, YELLOW)
        put(ws, r, 4, yld, BLUE, T2, YELLOW)
        put(ws, r, 5, price, BLUE, USD, YELLOW)
        put(ws, r, 6, dev, BLUE, PCT, YELLOW)
        put(ws, r, 7, f"=$C${r}*Cover!$C$21", BLACK, NUM)
        put(ws, r, 8, f"=G{r}*D{r}", BLACK, NUM)
        put(ws, r, 9, f"=H{r}*E{r}", BLACK, USD)
        put(ws, r, 10, f"=I{r}*F{r}", BLACK, USD)
        put(ws, r, 11, f"=I{r}*(1-F{r})/G{r}", BLACK, USD)
        r += 1

    put(ws, 9, 2, "Published smallholder pilot earnings, US$/ha/yr", H2)
    put(ws, 10, 2, "Low", BLACK);  put(ws, 10, 3, M.FARMER_USD_PER_HA_LOW, BLUE, USD)
    put(ws, 11, 2, "High", BLACK); put(ws, 11, 3, M.FARMER_USD_PER_HA_HIGH, BLUE, USD)
    put(ws, 12, 2, "Rice methane farmer payment in band?", BLACK)
    put(ws, 12, 3, "=IF(AND(K6>=C10,K6<=C11),\"yes\",\"NO\")", WARN)
    put(ws, 13, 2, "Biochar farmer payment in band?", BLACK)
    put(ws, 13, 3, "=IF(AND(K7>=C10,K7<=C11),\"yes\",\"NO\")", WARN)
    put(ws, 15, 2, "This check is why the two developer shares differ. A flat "
                   "50/50 split puts rice-methane farmers below the published "
                   "band and biochar farmers at roughly three times its top.", MUTED)

    put(ws, 17, 2, "Developer share implied by the farmer band", H2)
    header(ws, 18, ["Pathway", "Gross $/ha/yr", "Implied share, low", "Implied share, high"])
    put(ws, 19, 2, "Rice methane", BLUE)
    put(ws, 19, 3, "=D6*E6", BLACK, USD)
    put(ws, 19, 4, "=1-$C$11/C19", BLACK, PCT)
    put(ws, 19, 5, "=1-$C$10/C19", BLACK, PCT)
    put(ws, 20, 2, "Biochar", BLUE)
    put(ws, 20, 3, "=D7*E7", BLACK, USD)
    put(ws, 20, 4, "=1-$C$11/C20", BLACK, PCT)
    put(ws, 20, 5, "=1-$C$10/C20", BLACK, PCT)
    put(ws, 22, 2, "A negative implied share means the credit is worth less than "
                   "the farmer payment it would have to fund. Rice methane cannot "
                   "reach the top of the published band at these assumptions.", MUTED)

    # ---------------- Scenarios ----------------
    ws = wb.create_sheet("Scenarios")
    widths(ws, {1: 3, 2: 18, 3: 14, 4: 14, 5: 16, 6: 16, 7: 16})
    put(ws, 2, 2, "Enrolment scenarios", TITLE)
    put(ws, 3, 2, "Developer revenue at each enrolled share of the rice base.", MUTED)
    header(ws, 5, ["Enrolled share", "Rice methane ($)", "Biochar ($)",
                   "Rice credits (t)", "Biochar credits (t)"])
    r = 6
    for share in (0.01, 0.03, 0.08):
        put(ws, r, 2, share, BLUE, PCT, YELLOW)
        put(ws, r, 3, f"=$B{r}*Cover!$C$21*Pathways!$D$6*Pathways!$E$6*Pathways!$F$6", BLACK, USD)
        put(ws, r, 4, f"=$B{r}*Cover!$C$21*Pathways!$D$7*Pathways!$E$7*Pathways!$F$7", BLACK, USD)
        put(ws, r, 5, f"=$B{r}*Cover!$C$21*Pathways!$D$6", BLACK, NUM)
        put(ws, r, 6, f"=$B{r}*Cover!$C$21*Pathways!$D$7", BLACK, NUM)
        r += 1
    put(ws, r + 1, 2, "Today's disclosed share", BOLD)
    put(ws, r + 1, 3, "=Cover!C22", BOLD, "0.000%")

    # ---------------- Sensitivity ----------------
    ws = wb.create_sheet("Sensitivity")
    widths(ws, {1: 3, 2: 26, 3: 14, 4: 14, 5: 14, 6: 14, 7: 16})
    put(ws, 2, 2, "What moves the answer", TITLE)
    put(ws, 3, 2, "Rice-methane developer revenue across price and credit yield.", MUTED)
    put(ws, 5, 3, "credit yield (t/ha/yr) across the top", MUTED)
    for i, y in enumerate([0.7, 1.1, 1.4, 1.8]):
        put(ws, 6, 4 + i, y, BLUE, T2, YELLOW)
    for j, price in enumerate([16, 31, 38, 46]):
        row = 7 + j
        put(ws, row, 3, price, BLUE, USD, YELLOW)
        for i in range(4):
            col = get_column_letter(4 + i)
            put(ws, row, 4 + i,
                f"=Pathways!$C$6*Cover!$C$21*{col}$6*$C{row}*Pathways!$F$6",
                BLACK, USD)
    put(ws, 12, 2, "price down the side, credit yield across the top", MUTED)

    put(ws, 14, 2, "Swing in developer revenue, one lever at a time", H2)
    header(ws, 15, ["Lever", "Low", "Base", "High", "Swing ($)"])
    levers = [
        ("Enrolled share (1%/3%/8%)", "=Scenarios!C6", "=Scenarios!C7", "=Scenarios!C8"),
        ("Price ($16/$31/$46)", "=D7", "=D8", "=D10"),
        ("Credit yield (0.7/1.1/1.8)", "=D8", "=E8", "=G8"),
    ]
    r = 16
    for name, lo, base, hi in levers:
        put(ws, r, 2, name, BLUE)
        put(ws, r, 3, lo, BLACK, USD)
        put(ws, r, 4, base, BLACK, USD)
        put(ws, r, 5, hi, BLACK, USD)
        put(ws, r, 6, f"=D{r}-C{r}" if False else f"=E{r}-C{r}", BOLD, USD)
        r += 1
    put(ws, r + 1, 2, "Enrolment moves the answer most, and it is the lever "
                      "with the least evidence behind it: today's disclosed "
                      "programmes sit far below one percent of the base.", MUTED)

    # ---------------- Competitors ----------------
    ws = wb.create_sheet("Competitive map")
    widths(ws, {1: 3, 2: 22, 3: 16, 4: 16, 5: 14, 6: 30, 7: 16})
    put(ws, 2, 2, "Disclosed Indian agricultural carbon programmes", TITLE)
    put(ws, 3, 2, "Published figures only. Blanks are blanks, not zeros.", MUTED)
    header(ws, 5, ["Programme", "Farmers", "Credits issued", "Hectares",
                   "Practice", "Credits / farmer"])
    comp = [
        ("Sow&Reap Agro", 35000, 37405, None, "Paddy, Gold Standard"),
        ("Boomitra India", 12000, None, 10117, "Soil carbon"),
        ("UP state programme", 25000, None, None, "Tree planting"),
        ("Grow Indigo", None, None, None, "Soil, biochar, rice, agroforestry"),
        ("Varaha", None, None, None, "Biochar"),
    ]
    r = 6
    for name, farmers, credits, ha, practice in comp:
        put(ws, r, 2, name, BLUE)
        put(ws, r, 3, farmers if farmers else "not disclosed",
            BLUE if farmers else MUTED, NUM if farmers else None)
        put(ws, r, 4, credits if credits else "not disclosed",
            BLUE if credits else MUTED, NUM if credits else None)
        put(ws, r, 5, ha if ha else "not disclosed",
            BLUE if ha else MUTED, NUM if ha else None)
        put(ws, r, 6, practice, BLUE)
        if farmers and credits:
            put(ws, r, 7, f"=D{r}/C{r}", BLACK, T2)
        r += 1
    put(ws, r + 1, 2, "Sow&Reap's 1.07 credits per farmer is the only bottom-up "
                      "check available on the credit-yield assumption -- and it "
                      "is credits per FARMER, not per hectare.", MUTED)

    # ---- Diligence tracker -------------------------------------------------
    ws = wb.create_sheet("Diligence tracker")
    widths(ws, {1: 3, 2: 26, 3: 26, 4: 24, 5: 22, 6: 11, 7: 11, 8: 11,
                9: 10, 10: 13, 11: 48, 12: 44})
    put(ws, 2, 2, "Carbon project opportunity screen", TITLE)
    put(ws, 3, 2, "Six publicly documented Indian programmes. Published figures "
                  "only; 'n/d' is a gap, never a zero.", MUTED)
    header(ws, 5, ["Programme", "Geography", "Pathway", "Registry / method",
                   "Farmers", "Hectares", "Credits", "Share %", "Basis",
                   "Commercial risk", "Next diligence question"])
    r = 6
    for p in D.ranked_by_disclosure():
        reg = p.registry or "n/d"
        if p.methodology:
            reg += f" / {p.methodology}"
        if p.project_id:
            reg += f" (ID {p.project_id})"
        put(ws, r, 2, p.name, BOLD)
        put(ws, r, 3, p.geography, BLUE)
        put(ws, r, 4, p.pathway, BLUE)
        put(ws, r, 5, reg, BLUE)
        for col, v, fmt in ((6, p.farmers, NUM), (7, p.hectares, NUM),
                            (8, p.credits_issued, NUM),
                            (9, p.farmer_share_pct, NUM)):
            put(ws, r, col, v if v is not None else "n/d",
                BLUE if v is not None else MUTED, fmt if v is not None else None)
        put(ws, r, 10, p.share_basis or "n/d",
            WARN if p.share_basis == "net" else MUTED)
        put(ws, r, 11, p.commercial_risk, BLUE).alignment = Alignment(wrap_text=True)
        put(ws, r, 12, p.next_question, BLUE).alignment = Alignment(wrap_text=True)
        r += 1
    last = r - 1

    r += 1
    put(ws, r, 2, "What the screen does to this model's assumptions", H2)
    r += 1
    header(ws, r, ["Assumption", "In the model", "Published low",
                   "Published high", "Model inside range?"])
    r += 1
    put(ws, r, 2, "Farmer share of credit revenue", BOLD)
    put(ws, r, 3, 1 - M.rice_methane().developer_share, BLUE, PCT)
    put(ws, r, 4, f"=MIN(I6:I{last})/100", BLACK, PCT)
    put(ws, r, 5, f"=MAX(I6:I{last})/100", BLACK, PCT)
    put(ws, r, 6, f'=IF(AND(C{r}>=D{r},C{r}<=E{r}),"yes","NO")', WARN)
    split_row = r

    r += 1
    put(ws, r, 2, "Credit yield, rice methane (t/ha/yr)", BOLD)
    put(ws, r, 3, M.rice_methane().credit_yield, BLUE, T2)
    put(ws, r, 4, f"=ROUND({D.VM0042_CREDITS_PER_ACRE[0]}*{ACRE},2)", BLACK, T2)
    put(ws, r, 5, f"=ROUND({D.VM0042_CREDITS_PER_ACRE[1]}*{ACRE},2)", BLACK, T2)
    put(ws, r, 6, f'=IF(AND(C{r}>=D{r},C{r}<=E{r}),"yes","NO")', WARN)
    yield_row = r

    r += 2
    put(ws, r, 2, "Developer revenue here is OVERSTATED by", BOLD)
    put(ws, r, 3, f"=1-(1-D{split_row})/(1-C{split_row})", BLACK, PCT)
    put(ws, r, 4, f"=1-(1-E{split_row})/(1-C{split_row})", BLACK, PCT)
    put(ws, r, 6, "on the revenue split", MUTED)
    r += 1
    put(ws, r, 2, "...and UNDERSTATED by", BOLD)
    put(ws, r, 3, f"=D{yield_row}/C{yield_row}", BLACK, '0.0"x"')
    put(ws, r, 6, "on the credit yield. They do not cancel.", MUTED)

    r += 2
    put(ws, r, 2, "The two conflicts point in opposite directions, so neither is "
                  "a one-line fix. The split is a disclosure problem -- two of the "
                  "three published shares are promised on undefined 'net' revenue. "
                  "The yield is a measurement problem -- no disclosed Indian "
                  "programme publishes both hectares and credits issued.", MUTED)
    r += 2
    put(ws, r, 2, "CCTS offset mechanism: agriculture is a Phase 1 sector, and a "
                  f"project start date must be on or after {D.CCTS_EARLIEST_START} "
                  "to be eligible.", MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

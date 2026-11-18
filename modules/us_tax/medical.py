"""TY2025 federal Schedule A medical workpaper, for reviewed synthetic inputs."""
import re
from decimal import Decimal, ROUND_HALF_UP

SOURCE = "https://www.irs.gov/pub/irs-prior/i1040sca--2025.pdf"
RULE = "US-FED-2025-IRC213-v1"
CENT = Decimal("0.01")


def amount(text):
    if not isinstance(text, str) or not re.fullmatch(r"[0-9]{1,13}(?:\.[0-9]{1,2})?", text.strip()):
        raise ValueError("Enter a nonnegative USD amount with up to two decimal places.")
    return Decimal(text.strip())


def calculate(year, agi, eligible_paid, reimbursements):
    if str(year) != "2025":
        raise ValueError("Only tax year 2025 is supported by this rule.")
    income, paid, refunded = map(amount, (agi, eligible_paid, reimbursements))
    if refunded > paid:
        raise ValueError("Review reimbursements exceeding the eligible payments.")
    net = paid - refunded
    floor = income * Decimal("0.075")
    excess = max(Decimal(0), net - floor)
    return {
        "rule": RULE, "authority": "26 USC 213(a)", "instructions": SOURCE,
        "year": 2025, "jurisdiction": "US federal", "status": "Pending reviewer approval",
        "eligible_paid": str(paid), "same_year_reimbursements": str(refunded),
        "line_1_net_medical": str(net), "line_2_agi": str(income),
        "line_3_threshold_exact": str(floor),
        "line_4_excess_usd": str(excess.quantize(CENT, rounding=ROUND_HALF_UP)),
    }

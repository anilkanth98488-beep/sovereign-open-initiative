# Sovereign Tax Systems | Founder's pilot brief

## Purpose and offer

Help small accounting firms review an exception and reproduce a calculation from its inputs and sources. Offer one supervised ledger reconciliation pilot with one exception report and one reviewer walkthrough. Keep the medical rule as a separate synthetic demonstration of how federal tax rules are maintained. Start with founder time, the existing code and standard-library calculations. Spend on AI only when a buyer values the explanation.

## Operating responsibilities

| Owner role | Decision and evidence |
|---|---|
| Founder and product owner (Deva) | Agree scope, price, due date and acceptance criteria. Track revenue collected, time spent and direct delivery cost per pilot. |
| Rule author (Deva initially) | Specify jurisdiction, tax year, authority, form lines, exclusions, source inputs, rounding and examples. Preserve prior versions. |
| Independent tax reviewer (to recruit) | Recalculate boundary cases, inspect supporting authority, sign and date the release or return it for correction. |
| Engineering owner (Deva initially) | Run regression tests, link release commit to rule version, keep an issue log and restore a prior version during a rehearsal. |
| Data owner (Deva initially) | Use synthetic records in the demo. Before client use, agree access, retention, deletion, handling and incident contacts with the firm. |
| Delivery reviewer (firm nominee) | Confirm inputs against records, resolve exceptions, approve the workpaper and record who accepted it. |

## Fifteen days starting November 18, 2026

| Dates | Deliverable | Acceptance evidence |
|---|---|---|
| Nov 18–20 | Freeze pilot scope and synthetic ledger demo. Verify inputs and workpaper output. Address the potential credential exposure in the legacy public archive. | A three-minute demonstration, a downloadable example and an owner for outstanding risks. |
| Nov 21–23 | Interview five prospective firm reviewers. Ask how they document differences and what evidence they retain. | Two walkthroughs targeted; record the buyer's exact acceptance criteria and objections. |
| Nov 24–26 | Recreate one buyer's preferred format with synthetic data. Have a second reviewer independently check the medical rule examples. | Expected vs actual results and dated review notes. |
| Nov 27–29 | Quote a fixed fee for one ledger, one exception report and one review call. Use estimated delivery hours, a target hourly rate, direct costs and rework allowance. | Written scope and price accepted, or a recorded reason for declining. |
| Nov 30–Dec 2 | Deliver an accepted pilot under agreed data controls, or revise the offer using objections. Rehearse restoring a tagged release. | Signed acceptance or documented gaps, actual hours, amount collected and a repeat-work decision. |

## Keeping the company maintainable

For each tax year, inventory changed authorities and affected rules. Preserve the exact source, effective dates, test fixtures, reviewer decision and Git commit with each release. Keep explanations downstream of deterministic calculations. Give AI only approved inputs, mark narrative as draft and have a reviewer verify each number and source. If AI is offline, the workpaper must still calculate. Halt an affected rule when a source changes until review is complete. Keep a release and recovery runbook that a second operator can use. Review margins and customer renewals quarterly and test handover annually.

## First federal rule

In the Streamlit US & Canadian Tax Centre choose United States, leave State blank, select 2025 and enable the Schedule A medical rule. Use AGI 80000, eligible paid 9000 and same-year reimbursements 1000. Expected lines 1–4 are 8000, 80000, 6000 and 2000. Confirm eligibility manually. The demonstration excludes negative AGI, expense classification, prior-year recoveries, itemization choice, return filing and state rules. Retain precision through the threshold calculation and round only the final workpaper amount to cents. The output records pending review. Run python -m unittest discover -s tests -p test_medical_2025.py.

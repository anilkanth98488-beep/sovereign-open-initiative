"""Original learning tracks and practice questions."""

LEARNING_TRACKS = {
    "IRS VITA/TCE": [
        "Intake, interview, and identity-protection principles",
        "Filing status and dependency concepts",
        "Income and common information documents",
        "Credits, deductions, and quality review",
    ],
    "Enrolled Agent (EA) preparation": [
        "Individuals: income, adjustments, deductions, and credits",
        "Businesses: entity concepts and business income",
        "Representation: practice, procedure, and ethics",
        "Build a weekly review and practice-exam schedule",
    ],
    "CPA learning roadmap": [
        "Review current board and exam-provider requirements",
        "Map a study schedule to the current exam blueprint",
        "Practice financial accounting and reporting",
        "Track weak areas and review cadence",
    ],
    "US tax technical learning": [
        "Read the primary source before secondary commentary",
        "Record the tax year and authority for each conclusion",
        "Separate facts, assumptions, and unresolved questions",
    ],
    "Canadian tax learning": [
        "Identify the relevant CRA form and tax year",
        "Distinguish federal and provincial/territorial considerations",
        "Check CRA guidance and keep source notes",
    ],
}

PRACTICE_QUESTIONS = {
    "A client record is missing a source document. What is the best next step?": {
        "options": [
            "Estimate the amount and file without disclosure",
            "Ask for evidence, document the gap, and follow applicable review procedures",
            "Copy a prior-year amount without checking",
        ],
        "answer": "Ask for evidence, document the gap, and follow applicable review procedures",
        "explanation": "Reliable workpapers distinguish verified facts from missing evidence and assumptions.",
    },
    "Why should a tax workpaper name its tax year?": {
        "options": [
            "Tax rules and source materials can vary by year",
            "It makes the workpaper look complete",
            "Tax years never affect calculations",
        ],
        "answer": "Tax rules and source materials can vary by year",
        "explanation": "The applicable year is a core fact; rules should not be silently carried forward.",
    },
    "What does a ledger arithmetic PASS establish?": {
        "options": [
            "The records are complete and tax compliant",
            "The supplied arithmetic agrees within the configured tolerance",
            "Every transaction is genuine",
        ],
        "answer": "The supplied arithmetic agrees within the configured tolerance",
        "explanation": "An arithmetic check does not establish source accuracy, classification, or tax treatment.",
    },
}

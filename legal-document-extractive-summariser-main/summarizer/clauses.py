CLAUSE_TYPES = {

    "Payment": [
        "payment",
        "rent",
        "fee",
        "amount",
        "salary",
        "compensation"
    ],

    "Termination": [
        "termination",
        "terminate",
        "terminated",
        "cancel",
        "end the agreement"
    ],

    "Liability": [
        "liability",
        "liable",
        "damages",
        "indemnity"
    ],

    "Confidentiality": [
        "confidential",
        "confidentiality",
        "disclosure",
        "secret"
    ],

    "Rights & Obligations": [
        "rights",
        "obligation",
        "obligations",
        "duty",
        "shall",
        "responsible"
    ],

    "Dispute & Jurisdiction": [
        "dispute",
        "court",
        "jurisdiction",
        "arbitration"
    ]
}


def detect_clauses(text):
    """
    Detect important legal clause categories
    present in the document.
    """

    lower_text = text.lower()

    detected_clauses = []

    for clause_name, keywords in CLAUSE_TYPES.items():

        for keyword in keywords:

            if keyword in lower_text:

                detected_clauses.append(
                    clause_name
                )

                break

    return detected_clauses
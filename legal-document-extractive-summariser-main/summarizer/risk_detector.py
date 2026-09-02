import re


def detect_risks(text):

    risks = []

    if not text:
        return risks

    text_lower = text.lower()

    # ==========================================
    # HELPER FUNCTION
    # ==========================================

    def add_risk(
        category,
        level,
        score,
        sentence
    ):

        risks.append({
            "categories": [category],
            "level": level,
            "score": score,
            "sentence": sentence
        })

    # ==========================================
    # TERMINATION RISK
    # ==========================================

    termination_patterns = [
        "terminate",
        "termination",
        "terminate this agreement",
        "termination of this agreement"
    ]

    if any(
        pattern in text_lower
        for pattern in termination_patterns
    ):

        add_risk(
            "Termination",
            "High",
            8,
            "Termination clause detected. "
            "Review the conditions and notice period "
            "required to terminate the agreement."
        )

    # ==========================================
    # PENALTY / FINE RISK
    # ==========================================

    penalty_patterns = [
        "penalty",
        "penalties",
        "fine",
        "fines",
        "late fee",
        "late fees"
    ]

    if any(
        pattern in text_lower
        for pattern in penalty_patterns
    ):

        add_risk(
            "Penalty / Fine",
            "High",
            8,
            "Penalty or financial consequence detected. "
            "Review the applicable amount and conditions."
        )

    # ==========================================
    # AUTOMATIC RENEWAL RISK
    # ==========================================

    renewal_patterns = [
        "automatically renew",
        "automatic renewal",
        "auto-renew",
        "renewal"
    ]

    if any(
        pattern in text_lower
        for pattern in renewal_patterns
    ):

        add_risk(
            "Automatic Renewal",
            "Medium",
            6,
            "Renewal clause detected. "
            "Check whether the agreement renews automatically "
            "and how cancellation must be provided."
        )

    # ==========================================
    # PAYMENT RISK
    # ==========================================

    payment_patterns = [
        "payment",
        "payable",
        "installment",
        "instalment",
        "invoice",
        "due date"
    ]

    if any(
        pattern in text_lower
        for pattern in payment_patterns
    ):

        add_risk(
            "Payment",
            "High",
            8,
            "Payment obligation detected. "
            "Review payment dates, amounts and "
            "consequences of late payment."
        )

    # ==========================================
    # LIABILITY RISK
    # ==========================================

    liability_patterns = [
        "liability",
        "liable",
        "indemnity",
        "indemnification",
        "damages"
    ]

    if any(
        pattern in text_lower
        for pattern in liability_patterns
    ):

        add_risk(
            "Liability / Indemnification",
            "High",
            9,
            "Liability or indemnification clause detected. "
            "Review which party is responsible for losses "
            "or damages."
        )

    # ==========================================
    # NOTICE RISK
    # ==========================================

    notice_patterns = [
        "notice",
        "written notice",
        "notice period"
    ]

    if any(
        pattern in text_lower
        for pattern in notice_patterns
    ):

        add_risk(
            "Notice Requirement",
            "Medium",
            5,
            "Notice requirement detected. "
            "Check the required notice method and "
            "notice period."
        )

    # ==========================================
    # CONFIDENTIALITY RISK
    # ==========================================

    confidentiality_patterns = [
        "confidential",
        "confidentiality",
        "non-disclosure",
        "nda"
    ]

    if any(
        pattern in text_lower
        for pattern in confidentiality_patterns
    ):

        add_risk(
            "Confidentiality",
            "Medium",
            6,
            "Confidentiality obligation detected. "
            "Review what information must remain confidential "
            "and the duration of the obligation."
        )

    # ==========================================
    # DISPUTE / JURISDICTION RISK
    # ==========================================

    dispute_patterns = [
        "dispute",
        "arbitration",
        "jurisdiction",
        "governing law",
        "court"
    ]

    if any(
        pattern in text_lower
        for pattern in dispute_patterns
    ):

        add_risk(
            "Dispute / Jurisdiction",
            "Medium",
            6,
            "Dispute resolution or jurisdiction clause detected. "
            "Review where and how disputes will be resolved."
        )

    # ==========================================
    # DATA / PRIVACY RISK
    # ==========================================

    privacy_patterns = [
        "personal data",
        "personal information",
        "privacy",
        "data protection",
        "data processing"
    ]

    if any(
        pattern in text_lower
        for pattern in privacy_patterns
    ):

        add_risk(
            "Data / Privacy",
            "Medium",
            6,
            "Data or privacy-related clause detected. "
            "Review how personal information may be collected, "
            "used or shared."
        )

    # ==========================================
    # LIMITATION OF LIABILITY
    # ==========================================

    limitation_patterns = [
        "limitation of liability",
        "limit liability",
        "limited liability"
    ]

    if any(
        pattern in text_lower
        for pattern in limitation_patterns
    ):

        add_risk(
            "Limitation of Liability",
            "High",
            8,
            "Limitation of liability detected. "
            "Review whether liability is capped or excluded."
        )

    # ==========================================
    # NON-COMPETE
    # ==========================================

    non_compete_patterns = [
        "non-compete",
        "non compete",
        "noncompetition",
        "restrictive covenant"
    ]

    if any(
        pattern in text_lower
        for pattern in non_compete_patterns
    ):

        add_risk(
            "Non-Compete / Restriction",
            "High",
            8,
            "Restrictive or non-compete clause detected. "
            "Review the scope, duration and applicable restrictions."
        )

    # ==========================================
    # INTELLECTUAL PROPERTY
    # ==========================================

    ip_patterns = [
        "intellectual property",
        "copyright",
        "trademark",
        "patent",
        "ownership of intellectual property"
    ]

    if any(
        pattern in text_lower
        for pattern in ip_patterns
    ):

        add_risk(
            "Intellectual Property",
            "Medium",
            6,
            "Intellectual property provision detected. "
            "Review ownership and permitted use of intellectual property."
        )

    # ==========================================
    # DEPOSIT / SECURITY
    # ==========================================

    deposit_patterns = [
        "security deposit",
        "deposit",
        "refundable deposit"
    ]

    if any(
        pattern in text_lower
        for pattern in deposit_patterns
    ):

        add_risk(
            "Deposit / Security",
            "Medium",
            5,
            "Deposit-related provision detected. "
            "Review the deposit amount, refund conditions "
            "and deductions."
        )

    # ==========================================
    # FORCE MAJEURE
    # ==========================================

    force_majeure_patterns = [
        "force majeure",
        "act of god",
        "unforeseen circumstances"
    ]

    if any(
        pattern in text_lower
        for pattern in force_majeure_patterns
    ):

        add_risk(
            "Force Majeure",
            "Low",
            4,
            "Force majeure provision detected. "
            "Review circumstances that may excuse "
            "a party from performing its obligations."
        )

    # ==========================================
    # REMOVE DUPLICATE CATEGORIES
    # ==========================================

    unique_risks = []

    categories_seen = set()

    for risk in risks:

        category = risk["categories"][0]

        if category not in categories_seen:

            unique_risks.append(risk)

            categories_seen.add(category)

    return unique_risks
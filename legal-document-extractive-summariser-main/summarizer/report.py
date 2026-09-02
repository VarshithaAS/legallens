from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors


def create_report(
    filepath,
    filename,
    summary,
    keywords,
    clauses,
    risks,
    word_count,
    sentence_count
):

    styles = getSampleStyleSheet()

    # ==========================================
    # STYLES
    # ==========================================

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = colors.HexColor("#29245e")

    subtitle_style = styles["Heading3"]
    subtitle_style.alignment = TA_CENTER
    subtitle_style.textColor = colors.HexColor("#6754e8")

    heading_style = styles["Heading2"]
    heading_style.textColor = colors.HexColor("#29245e")

    normal_style = styles["BodyText"]

    document = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    content = []

    # ==========================================
    # TITLE
    # ==========================================

    content.append(
        Paragraph(
            "LegalLens",
            title_style
        )
    )

    content.append(
        Spacer(1, 8)
    )

    content.append(
        Paragraph(
            "Legal Document Extractive Summariser",
            subtitle_style
        )
    )

    content.append(
        Spacer(1, 25)
    )

    # ==========================================
    # DOCUMENT
    # ==========================================

    content.append(
        Paragraph(
            "Analyzed Document",
            heading_style
        )
    )

    content.append(
        Paragraph(
            str(filename),
            normal_style
        )
    )

    content.append(
        Spacer(1, 18)
    )

    # ==========================================
    # DOCUMENT STATISTICS
    # ==========================================

    content.append(
        Paragraph(
            "Document Statistics",
            heading_style
        )
    )

    statistics = [
        f"Words: {word_count}",
        f"Sentences: {sentence_count}",
        f"Key Sentences: {len(summary)}"
    ]

    content.append(
        ListFlowable(
            [
                ListItem(
                    Paragraph(
                        item,
                        normal_style
                    )
                )
                for item in statistics
            ],
            bulletType="bullet"
        )
    )

    content.append(
        Spacer(1, 18)
    )

    # ==========================================
    # LEGAL CLAUSES
    # ==========================================

    content.append(
        Paragraph(
            "Legal Clauses Detected",
            heading_style
        )
    )

    if clauses:

        content.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            str(clause),
                            normal_style
                        )
                    )
                    for clause in clauses
                ],
                bulletType="bullet"
            )
        )

    else:

        content.append(
            Paragraph(
                "No major legal clauses detected.",
                normal_style
            )
        )

    content.append(
        Spacer(1, 18)
    )

    # ==========================================
    # KEYWORDS
    # ==========================================

    content.append(
        Paragraph(
            "Key Legal Terms",
            heading_style
        )
    )

    if keywords:

        content.append(
            ListFlowable(
                [
                    ListItem(
                        Paragraph(
                            str(keyword),
                            normal_style
                        )
                    )
                    for keyword in keywords
                ],
                bulletType="bullet"
            )
        )

    else:

        content.append(
            Paragraph(
                "No keywords detected.",
                normal_style
            )
        )

    content.append(
        Spacer(1, 18)
    )

    # ==========================================
    # RISK AREAS
    # ==========================================

    content.append(
        Paragraph(
            "Potential Legal Risk Areas",
            heading_style
        )
    )

    if risks:

        for index, risk in enumerate(
            risks,
            start=1
        ):

            categories = ", ".join(
                risk.get(
                    "categories",
                    []
                )
            )

            level = risk.get(
                "level",
                "Low"
            )

            score = risk.get(
                "score",
                0
            )

            sentence = risk.get(
                "sentence",
                ""
            )

            content.append(
                Paragraph(
                    f"<b>{index}. "
                    f"{categories}</b>",
                    normal_style
                )
            )

            content.append(
                Paragraph(
                    f"Importance Level: {level}",
                    normal_style
                )
            )

            content.append(
                Paragraph(
                    f"Importance Score: {score}",
                    normal_style
                )
            )

            content.append(
                Paragraph(
                    sentence,
                    normal_style
                )
            )

            content.append(
                Spacer(1, 10)
            )

    else:

        content.append(
            Paragraph(
                "No potentially important risk areas detected.",
                normal_style
            )
        )

    content.append(
        Spacer(1, 18)
    )

    # ==========================================
    # EXTRACTIVE SUMMARY
    # ==========================================

    content.append(
        Paragraph(
            "Extractive Summary",
            heading_style
        )
    )

    if summary:

        for index, sentence in enumerate(
            summary,
            start=1
        ):

            content.append(
                Paragraph(
                    f"<b>{index}.</b> {sentence}",
                    normal_style
                )
            )

            content.append(
                Spacer(1, 8)
            )

    else:

        content.append(
            Paragraph(
                "No summary sentences generated.",
                normal_style
            )
        )

    content.append(
        Spacer(1, 20)
    )

    # ==========================================
    # DISCLAIMER
    # ==========================================

    content.append(
        Paragraph(
            "<b>Disclaimer:</b> This report is generated "
            "for document understanding and extractive "
            "summarisation. The risk highlighting feature "
            "is rule-based and does not constitute "
            "professional legal advice.",
            normal_style
        )
    )

    # ==========================================
    # CREATE PDF
    # ==========================================

    document.build(content)

    return filepath
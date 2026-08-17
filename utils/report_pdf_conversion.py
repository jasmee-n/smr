# report pdf formatting
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)

def save_report_as_pdf(report, output_path):

    pdf = SimpleDocTemplate(
        str(output_path),
        pagesize = A4,
        rightMargin = 18 * mm,
        leftMargin = 18 * mm,
        topMargin = 18 * mm,
        bottomMargin = 18 * mm
    )

    title_style = ParagraphStyle(
        'Title',
        fontName = 'Times-Bold',
        fontSize = 16,
        leading = 20,
        alignment = TA_CENTER,
        spaceAfter = 12
    )

    heading_style = ParagraphStyle(
        'Heading',
        fontName = 'Times-Bold',
        fontSize = 11,
        leading = 14,
        spaceBefore = 8,
        spaceAfter = 5
    )

    subheading_style = ParagraphStyle(
        'Subheading',
        fontName = 'Times-Bold',
        fontSize = 9.5,
        leading = 12,
        spaceBefore = 5,
        spaceAfter = 3
    )

    body_style = ParagraphStyle(
        'Body',
        fontName = 'Times-Roman',
        fontSize = 9,
        leading = 13,
        spaceAfter = 3
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        fontName = 'Times-Roman',
        fontSize = 9,
        leading = 13,
        leftIndent = 12,
        firstLineIndent = -8,
        spaceAfter = 3
    )

    content = []

    section_headings = [
        'OVERVIEW:',
        'CLINICAL PRIORITIES:',
        'PATIENT INFORMATION:',
        'CLINICAL INFORMATION:',
        'LABORATORY RESULTS:',
        'CONDITIONS:',
        'CURRENT MEDICATIONS:',
        'INDICATIONS:',
        'DRUG-DRUG INTERACTIONS:',
        'RISK ASSESSMENT:',
        'DEPRESCRIBING OPPORTUNITIES:',
        'MONITORING REQUIREMENTS:',
        'RECOMMENDATIONS:',
        'VALIDATION SUMMARY:',
        'CONCLUSION:'
    ]

    for line in report.splitlines():
        line = line.strip()

        if not line:
            content.append(Spacer(1, 3))
            continue

        if line == '-' * 60:
            content.append(
                HRFlowable(
                    width = '100%',
                    thickness = 0.5,
                    color = colors.grey,
                    spaceBefore = 5,
                    spaceAfter = 7
                )
            )
            continue

        if line == 'STRUCTURED MEDICATION REVIEW':
            content.append(Paragraph(line, title_style))
            continue

        if line in section_headings:
            content.append(Paragraph(line.rstrip(':'), heading_style))
            continue

        if line.endswith('PRIORITY:'):
            content.append(Paragraph(line.rstrip(':'), subheading_style))
            continue

        if line.startswith('* '):
            content.append(
                Paragraph(
                    f'• {line[2:]}',
                    bullet_style
                )
            )
            continue

        if line.startswith(('TYPE:', 'PRIORITY SCORE:', 'SOURCE:', 'SEVERITY:',
                            'RATIONALE:', 'ISSUE:', 'SUGGESTED ACTION:',
                            'TIMEFRAME:', 'PRIORITY:', 'MONITORING REQUIRED:',
                            'RECOMMENDATION:', 'MEDICATION:', 'MEDICATION/CONDITION:')):
            content.append(Paragraph(line, body_style))
            continue

        content.append(Paragraph(line, body_style))

    pdf.build(content)
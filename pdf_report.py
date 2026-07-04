from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os


def generate_pdf_report(
    question,
    transcript,
    relevance_score,
    speaking_speed,
    overall_score,
    feedback,
    strengths,
    improvements
):

    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/interview_report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Interview Analysis Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Interview Question",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            question,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Candidate Response",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            transcript,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Evaluation Metrics",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Relevance Score: {relevance_score:.2f}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Speaking Speed: {speaking_speed} WPM",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Overall Score: {overall_score:.2f}/100",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "AI Feedback",
            styles["Heading2"]
        )
    )

    for item in feedback:
        story.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Strengths",
            styles["Heading2"]
        )
    )

    for item in strengths:
        story.append(
            Paragraph(
                f"✓ {item}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Areas for Improvement",
            styles["Heading2"]
        )
    )

    for item in improvements:
        story.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Recruiter Notes",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "_____________________________________",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "_____________________________________",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "_____________________________________",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "Note: This report is generated using AI and should be used as an assistive evaluation tool.",
            styles["BodyText"]
        )
    )

    doc.build(story)

    return pdf_path

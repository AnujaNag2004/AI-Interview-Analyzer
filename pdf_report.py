from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
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

    # Create reports folder if not present
    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/interview_report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    # --------------------------------------------------
    # Title
    # --------------------------------------------------
    story.append(
        Paragraph(
            "Interview Performance Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # Date and Time
    # --------------------------------------------------
    story.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # Question
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Candidate Response
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------
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
            f"Overall Interview Score: {overall_score:.2f}/100",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # Performance Category
    # --------------------------------------------------
    if overall_score >= 85:
        performance = "Excellent"

    elif overall_score >= 70:
        performance = "Good"

    elif overall_score >= 50:
        performance = "Average"

    else:
        performance = "Needs Improvement"

    story.append(
        Paragraph(
            "Performance Summary",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Performance Level: <b>{performance}</b>",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # Feedback
    # --------------------------------------------------
    story.append(
        Paragraph(
            "Feedback",
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

    # --------------------------------------------------
    # Strengths
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Improvements
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Recruiter Remarks
    # --------------------------------------------------
    if overall_score >= 85:
        recruiter_remark = (
            "Candidate demonstrated excellent communication "
            "skills and strong understanding of the topic."
        )

    elif overall_score >= 70:
        recruiter_remark = (
            "Candidate showed good understanding with minor "
            "areas for improvement."
        )

    elif overall_score >= 50:
        recruiter_remark = (
            "Candidate demonstrated average performance and "
            "would benefit from more detailed responses."
        )

    else:
        recruiter_remark = (
            "Candidate requires improvement in both technical "
            "depth and communication effectiveness."
        )

    story.append(
        Paragraph(
            "Recruiter Remarks",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            recruiter_remark,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1, 20))

    # --------------------------------------------------
    # Final Note
    # --------------------------------------------------
    story.append(
        Paragraph(
            "Note: The evaluation is based on communication "
            "effectiveness, response quality and interview "
            "performance indicators.",
            styles["BodyText"]
        )
    )

    # --------------------------------------------------
    # Build PDF
    # --------------------------------------------------
    doc.build(story)

    return pdf_path

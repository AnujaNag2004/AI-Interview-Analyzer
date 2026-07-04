from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf_report(question, transcript, relevance_score):

    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/interview_report.pdf"

    doc = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    story = []

    story.append(
        Paragraph("AI Interview Report", styles['Title'])
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph("Interview Question", styles['Heading2'])
    )

    story.append(
        Paragraph(question, styles['BodyText'])
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph("Candidate Answer", styles['Heading2'])
    )

    story.append(
        Paragraph(transcript, styles['BodyText'])
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Relevance Score: {relevance_score:.2f}%",
            styles['BodyText']
        )
    )

    doc.build(story)

    return pdf_path

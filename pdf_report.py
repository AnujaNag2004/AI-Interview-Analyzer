from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer # type: ignore
from reportlab.lib.styles import getSampleStyleSheet # type: ignore

doc = SimpleDocTemplate("reports/interview_report.pdf")
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("AI Interview Report", styles['Title']))
story.append(Spacer(1, 20))

story.append(Paragraph("Question:", styles['Heading2']))
story.append(Paragraph(
    "What is Machine Learning?",
    styles['BodyText']
))

story.append(Spacer(1, 10))

story.append(Paragraph("Candidate Answer:", styles['Heading2']))
story.append(Paragraph(
    "Machine learning is a subset of artificial intelligence that enables computers to learn from data.",
    styles['BodyText']
))

story.append(Spacer(1, 10))

story.append(Paragraph("Relevance Score: 82.97%", styles['BodyText']))
story.append(Paragraph("Speaking Speed: 126 WPM", styles['BodyText']))
story.append(Paragraph("Filler Words: 2", styles['BodyText']))
story.append(Paragraph("Final Interview Score: 85/100", styles['BodyText']))

doc.build(story)

print("PDF report generated successfully!")
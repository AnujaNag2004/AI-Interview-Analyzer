question = "What is Machine Learning?"

transcript = """
Machine learning is a subset of artificial intelligence
that enables computers to learn from data.
"""

relevance_score = 82.97
wpm = 126
filler_words = 2
final_score = 85

report = f"""
====================================
        AI INTERVIEW REPORT
====================================

Question:
{question}

Candidate Answer:
{transcript}

Relevance Score: {relevance_score:.2f}%
Speaking Speed: {wpm} WPM
Filler Words: {filler_words}

Final Interview Score: {final_score}/100

Feedback:
- Good technical understanding.
- Reduce filler words slightly.
- Maintain current speaking pace.
"""

with open("reports/interview_report.txt", "w") as file:
    file.write(report)

print("Interview report generated successfully!")
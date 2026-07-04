import streamlit as st
from sentence_transformers import SentenceTransformer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

# Load NLP model only once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Page Title
st.title("🎤 AI Interview Analyzer")
st.write("Analyze candidate answers using NLP and Machine Learning")

# Input fields
question = st.text_input(
    "Enter Interview Question"
)

answer = st.text_area(
    "Enter Candidate Answer"
)

# Analyze Button
if st.button("Analyze Answer"):

    if question.strip() == "" or answer.strip() == "":
        st.warning("Please enter both question and answer.")
    else:
        # Generate embeddings
        question_embedding = model.encode([question])
        answer_embedding = model.encode([answer])

        # Calculate similarity score
        score = cosine_similarity(
            question_embedding,
            answer_embedding
        )[0][0]

        relevance_percentage = score * 100

        # Display results
        st.success("Analysis Complete!")

        st.subheader("Results")

        st.write(
            f"📌 Relevance Score: {relevance_percentage:.2f}%"
        )

        # Feedback based on score
        if relevance_percentage >= 85:
            st.success("Excellent Answer ✅")
        elif relevance_percentage >= 70:
            st.info("Good Answer 👍")
        elif relevance_percentage >= 50:
            st.warning("Average Answer ⚠️")
        else:
            st.error("Needs Improvement ❌")
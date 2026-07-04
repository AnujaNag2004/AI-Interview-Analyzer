import streamlit as st
import whisper
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import tempfile
import os

# ---------------------------
# Load models only once
# ---------------------------
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("base")
    similarity_model = SentenceTransformer("all-MiniLM-L6-v2")
    return whisper_model, similarity_model


whisper_model, similarity_model = load_models()

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(
    page_title="AI Interview Analyzer",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Interview Analyzer")
st.write("Analyze candidate interview responses using AI and NLP")

# ---------------------------
# Inputs
# ---------------------------
question = st.text_input(
    "Enter Interview Question"
)

uploaded_file = st.file_uploader(
    "Upload Candidate Audio Answer (.wav)",
    type=["wav"]
)

# ---------------------------
# Analyze Button
# ---------------------------
if st.button("Analyze Interview"):

    if question.strip() == "":
        st.warning("Please enter an interview question.")

    elif uploaded_file is None:
        st.warning("Please upload an audio file.")

    else:

        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            ) as temp_file:

                temp_file.write(uploaded_file.read())
                temp_audio_path = temp_file.name

            st.info("Transcribing audio...")

            # Speech-to-text using Whisper
            result = whisper_model.transcribe(
                temp_audio_path,
                language="en"
            )

            transcript = result["text"]

            st.subheader("Transcript")
            st.write(transcript)

            # Similarity Analysis
            question_embedding = similarity_model.encode([question])
            answer_embedding = similarity_model.encode([transcript])

            score = cosine_similarity(
                question_embedding,
                answer_embedding
            )[0][0]

            relevance_percentage = score * 100

            st.subheader("Analysis Results")

            st.metric(
                "Relevance Score",
                f"{relevance_percentage:.2f}%"
            )

            # Feedback
            if relevance_percentage >= 85:
                st.success("Excellent Answer ✅")

            elif relevance_percentage >= 70:
                st.info("Good Answer 👍")

            elif relevance_percentage >= 50:
                st.warning("Average Answer ⚠️")

            else:
                st.error("Needs Improvement ❌")

        except Exception as e:
            st.error(f"Error occurred: {e}")

        finally:
            # Delete temporary file
            if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
            

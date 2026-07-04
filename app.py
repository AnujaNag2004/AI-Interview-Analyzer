import streamlit as st
import whisper # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
import os

# Load models only once
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("base")
    similarity_model = SentenceTransformer("all-MiniLM-L6-v2")
    return whisper_model, similarity_model

whisper_model, similarity_model = load_models()

# Page configuration
st.set_page_config(
    page_title="AI Interview Analyzer",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Interview Analyzer")
st.write("Analyze candidate interview responses using AI and NLP")

# Interview question input
question = st.text_input(
    "Enter Interview Question"
)

# Audio upload
uploaded_file = st.file_uploader(
    "Upload Candidate Audio Answer (.wav)",
    type=["wav"]
)

if st.button("Analyze Interview"):

    if question.strip() == "":
        st.warning("Please enter an interview question.")
    
    elif uploaded_file is None:
        st.warning("Please upload an audio file.")
    
    else:
        # Save uploaded audio temporarily
        with open("temp_audio.wav", "wb") as f:
            f.write(uploaded_file.read())

        st.info("Transcribing audio...")

        # Speech to text
        result = whisper_model.transcribe(
            "temp_audio.wav",
            language="en"
        )

        transcript = result["text"]

        st.subheader("Transcript")
        st.write(transcript)

        # NLP similarity analysis
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

        # Remove temporary file
        if os.path.exists("temp_audio.wav"):
            os.remove("temp_audio.wav")

    
            

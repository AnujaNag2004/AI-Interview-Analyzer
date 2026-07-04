import streamlit as st
import whisper
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pdf_report import generate_pdf_report
import tempfile
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="AI Interview Analyzer",
    page_icon="🎤",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
    color: white;
}

.main-title{
    font-size:55px;
    font-weight:800;
    text-align:center;
    color:#f8fafc;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:20px;
    margin-bottom:30px;
}

.transcript-box{
    background:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #334155;
}

div.stButton > button{
    width:100%;
    height:55px;
    border-radius:12px;
    font-size:18px;
    font-weight:600;
    background: linear-gradient(90deg,#6366f1,#8b5cf6);
    color:white;
    border:none;
}

div.stButton > button:hover{
    background: linear-gradient(90deg,#7c3aed,#6366f1);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Models
# --------------------------------------------------
@st.cache_resource
def load_models():
    whisper_model = whisper.load_model("base")
    similarity_model = SentenceTransformer("all-MiniLM-L6-v2")
    return whisper_model, similarity_model


whisper_model, similarity_model = load_models()

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    "<div class='main-title'>🎤 AI Interview Analyzer</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Analyze interview responses using Speech Recognition, NLP and Machine Learning</div>",
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Inputs
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    question = st.text_input(
        "💼 Interview Question",
        placeholder="Example: Explain Machine Learning"
    )

with col2:
    uploaded_file = st.file_uploader(
        "🎧 Upload Candidate Audio (.wav)",
        type=["wav"]
    )

st.write("")

# --------------------------------------------------
# Analyze Button
# --------------------------------------------------
if st.button("🚀 Analyze Interview"):

    if question.strip() == "":
        st.warning("Please enter an interview question.")
        st.stop()

    if uploaded_file is None:
        st.warning("Please upload an audio file.")
        st.stop()

    try:

        # Save audio temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_file:

            temp_file.write(uploaded_file.read())
            temp_audio_path = temp_file.name

        # Whisper Transcription
        with st.spinner("🎙️ Transcribing audio using Whisper..."):
            result = whisper_model.transcribe(
                temp_audio_path,
                language="en"
            )

        transcript = result["text"]

        # NLP Similarity
        question_embedding = similarity_model.encode([question])
        answer_embedding = similarity_model.encode([transcript])

        score = cosine_similarity(
            question_embedding,
            answer_embedding
        )[0][0]

        relevance_percentage = score * 100

        # -----------------------------------------
        # Speaking Speed
        # -----------------------------------------
        word_count = len(transcript.split())

        duration_seconds = result["segments"][-1]["end"]

        speaking_speed = int(
            (word_count / duration_seconds) * 60
        )

        # -----------------------------------------
        # Overall Score
        # -----------------------------------------
        overall_score = (
            relevance_percentage * 0.8
            + min(speaking_speed, 150) * 0.2
        )

        if overall_score > 100:
            overall_score = 100

        # -----------------------------------------
        # Feedback
        # -----------------------------------------
        feedback = []

        if relevance_percentage >= 85:
            feedback.append(
                "The candidate demonstrated strong understanding of the topic."
            )

        elif relevance_percentage >= 70:
            feedback.append(
                "The answer was relevant but could include more depth and examples."
            )

        else:
            feedback.append(
                "The answer lacked sufficient relevance to the question."
            )

        if speaking_speed < 100:
            feedback.append(
                "The candidate spoke slower than average."
            )

        elif speaking_speed > 160:
            feedback.append(
                "The candidate spoke faster than ideal."
            )

        else:
            feedback.append(
                "The speaking pace was appropriate."
            )

        # -----------------------------------------
        # Strengths
        # -----------------------------------------
        strengths = []

        if relevance_percentage >= 70:
            strengths.append("Relevant answer.")

        if 100 <= speaking_speed <= 160:
            strengths.append("Good speaking pace.")

        if len(strengths) == 0:
            strengths.append(
                "Candidate attempted the answer confidently."
            )

        # -----------------------------------------
        # Improvements
        # -----------------------------------------
        improvements = []

        if relevance_percentage < 70:
            improvements.append(
                "Provide more detailed and structured explanations."
            )

        if speaking_speed > 160:
            improvements.append(
                "Reduce speaking speed slightly."
            )

        if speaking_speed < 100:
            improvements.append(
                "Increase speaking pace slightly."
            )

        if len(improvements) == 0:
            improvements.append(
                "Continue maintaining communication quality."
            )

        # -----------------------------------------
        # Transcript
        # -----------------------------------------
        st.markdown("## 📝 Transcript")

        st.markdown(
            f"""
            <div class='transcript-box'>
            {transcript}
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------------------
        # Metrics
        # -----------------------------------------
        st.markdown("## 📊 Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Relevance Score",
                f"{relevance_percentage:.2f}%"
            )

        with col2:
            st.metric(
                "Speaking Speed",
                f"{speaking_speed} WPM"
            )

        with col3:
            st.metric(
                "Overall Score",
                f"{overall_score:.2f}/100"
            )

        # -----------------------------------------
        # Performance Badge
        # -----------------------------------------
        if overall_score >= 85:
            st.success("🌟 Excellent Interview Performance")

        elif overall_score >= 70:
            st.info("👍 Good Interview Performance")

        elif overall_score >= 50:
            st.warning("⚠️ Average Interview Performance")

        else:
            st.error("❌ Needs Improvement")

        # -----------------------------------------
        # Feedback Display
        # -----------------------------------------
        st.markdown("## 🤖 AI Feedback")

        for item in feedback:
            st.write("•", item)

        st.markdown("## ✅ Strengths")

        for item in strengths:
            st.write("•", item)

        st.markdown("## 📌 Areas for Improvement")

        for item in improvements:
            st.write("•", item)

        # -----------------------------------------
        # Generate PDF
        # -----------------------------------------
        pdf_path = generate_pdf_report(
            question,
            transcript,
            relevance_percentage,
            speaking_speed,
            overall_score,
            feedback,
            strengths,
            improvements
        )

        st.success("📄 Interview report generated successfully!")

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Interview Report",
                data=pdf_file,
                file_name="interview_report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error occurred: {e}")

    finally:
        if (
            'temp_audio_path' in locals()
            and os.path.exists(temp_audio_path)
        ):
            os.remove(temp_audio_path)

st.divider()

st.caption(
    "Built with Whisper • Sentence Transformers • Streamlit • ReportLab"
)

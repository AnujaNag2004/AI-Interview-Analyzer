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

.metric-card{
    background:#1e293b;
    padding:25px;
    border-radius:20px;
    border:1px solid #334155;
}

.transcript-box{
    background:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #334155;
}

.score-box{
    text-align:center;
    padding:20px;
    border-radius:20px;
    background:#1e293b;
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
        placeholder="Example: Tell me about yourself"
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

        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
        ) as temp_file:

            temp_file.write(uploaded_file.read())
            temp_audio_path = temp_file.name

        with st.spinner("🎙️ Transcribing audio using Whisper..."):
            result = whisper_model.transcribe(
                temp_audio_path,
                language="en"
            )

        transcript = result["text"]

        question_embedding = similarity_model.encode([question])
        answer_embedding = similarity_model.encode([transcript])

        score = cosine_similarity(
            question_embedding,
            answer_embedding
        )[0][0]

        relevance_percentage = score * 100

        # ---------------------------------------
        # Transcript
        # ---------------------------------------
        st.markdown("## 📝 Transcript")

        st.markdown(
            f"""
            <div class='transcript-box'>
            {transcript}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # ---------------------------------------
        # Score Card
        # ---------------------------------------
        st.markdown("## 📊 Analysis Results")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Relevance Score",
                f"{relevance_percentage:.2f}%"
            )

        with col2:
            if relevance_percentage >= 85:
                st.success("Excellent Answer ✅")
                final_feedback = "Excellent"

            elif relevance_percentage >= 70:
                st.info("Good Answer 👍")
                final_feedback = "Good"

            elif relevance_percentage >= 50:
                st.warning("Average Answer ⚠️")
                final_feedback = "Average"

            else:
                st.error("Needs Improvement ❌")
                final_feedback = "Needs Improvement"

        # ---------------------------------------
        # Generate PDF
        # ---------------------------------------
        pdf_path = generate_pdf_report(
            question,
            transcript,
            relevance_percentage
        )

        st.write("")
        st.success("Interview report generated successfully!")

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📄 Download Interview Report",
                data=pdf_file,
                file_name="interview_report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        if (
            'temp_audio_path' in locals()
            and os.path.exists(temp_audio_path)
        ):
            os.remove(temp_audio_path)

st.divider()

st.caption(
    "Built using OpenAI Whisper • Sentence Transformers • Streamlit"
)

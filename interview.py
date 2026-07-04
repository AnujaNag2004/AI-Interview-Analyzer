import whisper # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

# Interview Question
question = input("Enter Interview Question: ")

# Load Whisper model
print("\nLoading Whisper model...")
whisper_model = whisper.load_model("base")

# Convert audio to text
print("Converting speech to text...")
result = whisper_model.transcribe("audio/answer2.wav", language="en")

candidate_answer = result["text"]

print("\nCandidate Answer:")
print(candidate_answer)

# Load NLP model
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
question_embedding = similarity_model.encode([question])
answer_embedding = similarity_model.encode([candidate_answer])

# Calculate similarity score
score = cosine_similarity(
    question_embedding,
    answer_embedding
)[0][0]

percentage = score * 100

print(f"\nRelevance Score: {percentage:.2f}%")

if percentage >= 85:
    print("Excellent Answer")
elif percentage >= 70:
    print("Good Answer")
elif percentage >= 50:
    print("Average Answer")
else:
    print("Needs Improvement")
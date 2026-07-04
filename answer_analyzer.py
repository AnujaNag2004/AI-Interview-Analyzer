from sentence_transformers import SentenceTransformer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore

model = SentenceTransformer("all-MiniLM-L6-v2")

question = input("Enter Interview Question: ")
candidate_answer = input("Enter Candidate Answer: ")

question_embedding = model.encode([question])
answer_embedding = model.encode([candidate_answer])

score = cosine_similarity(
    question_embedding,
    answer_embedding
)[0][0]

print(f"\nSimilarity Score: {score:.2f}")
print(f"Relevance Percentage: {score*100:.2f}%")
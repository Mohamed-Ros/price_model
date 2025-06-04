from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import json
import uvicorn
import os

model = SentenceTransformer('all-MiniLM-L6-v2')

qa_data_all = {
    "en": json.load(open("qa_data_en.json", encoding="utf-8")),
    "ar": json.load(open("qa_data_ar.json", encoding="utf-8"))
}

question_sets = {}
embedding_sets = {}

for lang, qa in qa_data_all.items():
    questions = list(qa.keys())
    question_sets[lang] = questions
    embedding_sets[lang] = model.encode(questions, convert_to_tensor=True)

app = FastAPI()

class QuestionInput(BaseModel):
    question: str
    lang: str  

@app.post("/chat")
async def chat(data: QuestionInput):
    user_question = data.question.strip()
    lang = data.lang.strip().lower()

    if lang not in ["en", "ar"]:
        return {"answer": "Please select a valid language (en or ar)."}

    if not user_question:
        greeting = "Hello! How can I help you today?" if lang == "en" else "مرحبًا! كيف يمكنني مساعدتك اليوم؟"
        return {"answer": greeting}

    questions = question_sets[lang]
    embeddings = embedding_sets[lang]
    qa_data = qa_data_all[lang]

    user_embedding = model.encode(user_question, convert_to_tensor=True)
    similarity_scores = util.pytorch_cos_sim(user_embedding, embeddings)[0]
    best_match_idx = similarity_scores.argmax().item()
    best_match_score = similarity_scores[best_match_idx].item()

    if best_match_score > 0.6:
        matched_question = questions[best_match_idx]
        answer = qa_data[matched_question]
    else:
        answer = "Try again." if lang == "en" else "حاول مرة أخرى."

    return {"answer": answer}
if __name__ == "__main__":
    uvicorn.run("model_chatbot:app", host="0.0.0.0", port=8000, reload=True)

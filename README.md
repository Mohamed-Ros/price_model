#  AI Arabic/English Chatbot & Smart Product Price Predictor using FastAPI

This repository contains two FastAPI-based microservices:

1. **AI Chatbot**: A multilingual (Arabic/English) Q&A chatbot using semantic search with Sentence Transformers.
2. **Smart Discount System**: Predicts product price based on expiry date using a dynamic discounting algorithm.

---

##  1. AI Chatbot (Arabic/English Support)

### Description
This service answers user questions in **Arabic** or **English** by computing semantic similarity between the user's question and a predefined Q&A dataset.

### Features
- Supports Arabic and English questions.
- Uses [SentenceTransformers (`all-mpnet-base-v2`)](https://www.sbert.net/docs/pretrained_models.html).
- Handles typos and diacritics.
- Suggests similar questions if confidence is low.

### Endpoint

```
POST /chat
```

#### Request Body
```json
{
  "question": "ما هو يابلاش؟",
  "lang": "ar"
}
```

#### Response
```json
{
  "answer": "يابلاش هو..."
}
```

### File Requirements
- `qa_data_ar.json`: Arabic Q&A pairs
- `qa_data_en.json`: English Q&A pairs

### Run Locally

```bash
pip install fastapi uvicorn sentence-transformers pydantic
uvicorn model_chatbot:app --reload --port 8000
```

---

##  2. Smart Product Price Predictor

### Description
This service calculates a **discounted product price** based on its **expiry date**, using linear interpolation for discount rates.

### Features
- Calculates remaining time until expiry (in months/days).
- Applies smart discount rules based on proximity to expiry.
- Supports Arabic date formatting in output.

### Endpoint

```
POST /predict_price
```

#### Request Body
```json
{
  "production_date": "2024-06-01",
  "expiry_date": "2025-06-01",
  "price_fresh": 100.0
}
```

#### Response
```json
{
  "price_fresh": 100.0,
  "time_left_until_expiry": "11 شهر و 8 يوم",
  "days_left": 338,
  "discount_applied_percent": 0.0,
  "predicted_price": 100.0,
  "current_date": "2024-07-27",
  "production_date": "2024-06-01",
  "expiry_date": "2025-06-01"
}
```

### Run Locally

```bash
pip install fastapi uvicorn pandas pydantic
uvicorn main:app --reload --port 8001
```

---

##  Project Structure

```
├── model_chatbot.py         # Chatbot service (port 8000)
├── main.py                  # Price predictor service (port 8001)
├── qa_data_ar.json          # Arabic Q&A dataset
├── qa_data_en.json          # English Q&A dataset
├── README.md                # Project documentation
```

---

## ⚠ Notes
- Ensure your environment has Python 3.7+.
- For Arabic processing, proper encoding (UTF-8) is used.
- You can deploy these services independently using Docker or any cloud backend (Heroku, AWS, etc.).

---

##  Contact
Developed by   
For inquiries: 


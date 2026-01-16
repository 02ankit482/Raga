# Raga — Retrieval Augmented Generation (RAG) Chatbot 🚀

Raga is a **document-aware AI chatbot** that allows users to upload PDFs and ask questions strictly based on the uploaded content.  
It is built using **Flask**, **LangChain**, **FAISS**, and **Hugging Face Inference APIs**, containerized with **Docker**, and deployed on **AWS EC2**.

The project focuses on **correct system design**, **session isolation**, and **real-world deployment challenges**, rather than just model usage.

---

## ✨ Features

- 📄 Upload PDF documents
- 🤖 Ask questions based only on document content (RAG)
- 🧠 Semantic search using embeddings + FAISS
- 🔒 Per-user session isolation (no cross-device leakage)
- ♻️ Fresh sessions & documents on app restart (demo-safe)
- 🐳 Fully Dockerized
- ☁️ Deployed on AWS EC2 with Elastic IP
- 📜 Clean logging and error handling
- 🖥️ Minimal and user-friendly UI

---

## 🏗️ Project Architecture

```

Raga/
├── app/
│   ├── main/               # UI & chat routes
│   │   └── routes.py
│   ├── rag/                # RAG pipeline
│   │   ├── loaders.py      # PDF loading & chunking
│   │   ├── retriever.py    # FAISS vector store
│   │   ├── generator.py   # LLM response generation
│   │   └── pipeline.py    # End-to-end RAG flow
│   ├── static/             # CSS
│   ├── templates/          # HTML
│   └── **init**.py         # App factory & session config
│
├── uploads/                # Session-scoped uploads
├── run.py                  # App entry point
├── requirements.txt
├── Dockerfile
├── .env                    # HF_API_TOKEN
└── README.md

````

---

## 🧠 How RAG Works in This Project

1. User uploads a PDF
2. Text is extracted and chunked
3. Chunks are embedded using Sentence Transformers
4. FAISS performs similarity search
5. Relevant context is sent to an LLM
6. LLM generates an answer **only from document context**

If the answer is not present in the document, the model explicitly says so.

---

## 🔐 Session Handling (Important)

- Server-side sessions using **Flask-Session**
- Each user gets:
  - A unique session
  - A unique upload directory
- Sessions and uploads are **reset on app restart**
- Prevents:
  - Cross-user document leakage
  - Stale demo data
  - Cookie size issues

---

## 🚀 Running Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/Raga.git
cd Raga
````

### 2️⃣ Create `.env`

```env
HF_API_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx
```

### 3️⃣ Run with Docker

```bash
docker build -t student-ai-rag .
docker run -d \
  --name student-ai-rag \
  -p 5000:5000 \
  --env-file .env \
  student-ai-rag
```

Open:

```
http://localhost:5000
```

---

## ☁️ Deployment (AWS EC2)

* EC2 Ubuntu instance
* Docker installed
* Elastic IP attached (stable URL)
* App exposed on port `5000`

---
## 📌 Tech Stack

* **Backend**: Flask
* **RAG**: LangChain, FAISS
* **Embeddings**: Sentence Transformers
* **LLM**: Hugging Face Inference API
* **Sessions**: Flask-Session
* **Deployment**: Docker, AWS EC2
* **OS**: Linux (Ubuntu)

## 👨‍💻 Author

**Ankit Yadav**
Built with ❤️ while learning real-world ML systems and deployment.

---

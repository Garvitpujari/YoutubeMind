# YouTubeMind 🎥🧠

YouTubeMind is an AI-powered application that lets you ask questions about YouTube videos.

It uses Retrieval-Augmented Generation (RAG) to:

1. Fetch the YouTube transcript
2. Split the transcript into chunks
3. Generate embeddings
4. Store the embeddings in FAISS
5. Retrieve the most relevant transcript sections
6. Use Groq to generate an answer grounded in the transcript

## 🚀 Live Demo

Frontend:
https://youtube-mind-alpha.vercel.app

Backend:
https://youtubemind-backend.onrender.com

> The deployed backend may not be able to retrieve transcripts for every YouTube video because YouTube can restrict transcript access from cloud-hosted IP addresses.
>
> For reliable testing, run the project locally using your own API keys.

---

## 📁 Project Structure

```text
YouTubeMind/
│
├── backend/
│   ├── main.py
│   ├── youtube_service.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── .gitignore

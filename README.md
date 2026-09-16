# YouTubeMind

> Don't watch the whole video. Ask YouTubeMind.

YouTubeMind is an AI-powered YouTube video assistant that lets users provide a YouTube video URL and ask questions about its content.

The project uses a Retrieval-Augmented Generation (RAG) pipeline to retrieve relevant parts of a video's transcript and generate answers using an LLM.

## Live Demo

**Frontend:**  
https://youtube-mind-alpha.vercel.app

**Backend API:**  
https://youtubemind-backend.onrender.com

**API Documentation:**  
https://youtubemind-backend.onrender.com/docs

> The frontend is the user-facing application. The backend URL exposes the FastAPI API.

## Features

- YouTube URL input
- Transcript-based question answering
- Automatic transcript chunking
- Hugging Face embeddings
- FAISS vector similarity search
- Context-aware answers using Groq
- React frontend
- FastAPI backend

## Architecture

```text
React Frontend
       ↓
FastAPI Backend
       ↓
YouTube Transcript
       ↓
Text Chunking
       ↓
Hugging Face Embeddings
       ↓
FAISS Vector Store
       ↓
Similarity Retrieval
       ↓
Groq LLM
       ↓
Answer
       ↓
React Frontend

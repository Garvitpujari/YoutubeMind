from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.youtube_service import (
    extract_video_id,
    get_transcript,
    create_vector_store,
    create_chain
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://youtube-mind-alpha.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chain = None
video_id = None

class YouTubeRequest(BaseModel):
    url: str
    question: str


@app.get("/")
def home():
    return {
        "message": "YouTubeMind backend is running!"
    }


@app.post("/ask")
def ask_question(request: YouTubeRequest):

    global chain, video_id

    try:
        current_video_id = extract_video_id(request.url)

        # Process the video only if it is new
        if current_video_id != video_id:

            transcript = get_transcript(current_video_id)

            vector_store = create_vector_store(transcript)

            chain = create_chain(vector_store)

            video_id = current_video_id

        # Ask the question using the existing chain
        answer = chain.invoke(request.question)

        return {
            "video_id": video_id,
            "question": request.question,
            "answer": answer
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
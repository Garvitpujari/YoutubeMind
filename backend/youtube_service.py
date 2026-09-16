# from dotenv import load_dotenv

# load_dotenv()

# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api._errors import TranscriptsDisabled

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.vectorstores import FAISS

# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from langchain_core.runnables import (
#     RunnableParallel,
#     RunnablePassthrough,
#     RunnableLambda
# )
# from langchain_core.output_parsers import StrOutputParser


# def extract_video_id(url: str):
#     if "youtu.be/" in url:
#         return url.split("youtu.be/")[1].split("?")[0]

#     if "youtube.com/watch?v=" in url:
#         return url.split("v=")[1].split("&")[0]

#     raise ValueError("Invalid YouTube URL")


# # def get_transcript(video_id: str):
# #     try:
# #         youtube = YouTubeTranscriptApi()
# #         transcript = youtube.fetch(video_id)

# #         return " ".join(
# #             chunk.text for chunk in transcript
# #         )

# #     except TranscriptsDisabled:
# #         raise ValueError("No captions available for this video")


# # def get_transcript(video_id: str):
# #     try:
# #         youtube = YouTubeTranscriptApi()
# #         transcript_list = youtube.list(video_id)

# #         try:
# #             transcript = transcript_list.find_transcript(["en"])
# #         except Exception:
# #             transcript = next(iter(transcript_list))

# #         fetched_transcript = transcript.fetch()

# #         return " ".join(
# #             chunk.text for chunk in fetched_transcript
# #         )

# #     except TranscriptsDisabled:
# #         raise ValueError("No captions available for this video")

# #     except Exception as e:
# #         raise ValueError(f"Could not retrieve transcript: {str(e)}")

# def get_transcript(video_id: str):
#     try:
#         youtube = YouTubeTranscriptApi()
#         transcript_list = youtube.list(video_id)

#         transcript = None

#         for t in transcript_list:
#             if t.language_code == "en":
#                 transcript = t
#                 break

#         if transcript is None:
#             transcript = next(iter(transcript_list))

#         fetched_transcript = transcript.fetch()

#         return " ".join(
#             chunk.text for chunk in fetched_transcript
#         )

#     except TranscriptsDisabled:
#         raise ValueError("No captions available for this video")

#     except Exception as e:
#         raise ValueError(f"Could not retrieve transcript: {str(e)}")


# def create_vector_store(transcript_text: str):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=200
#     )

#     chunks = splitter.create_documents([transcript_text])

#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     return FAISS.from_documents(chunks, embeddings)


# def create_chain(vector_store):
#     retriever = vector_store.as_retriever(
#         search_type="similarity",
#         search_kwargs={"k": 4}
#     )

#     llm = ChatGroq(
#         model="openai/gpt-oss-120b"
#     )

#     prompt = PromptTemplate(
#         template="""
# You are a helpful assistant.
# Answer only from provided transcript context.
# If context is insufficient, just say you don't know.

# {context}

# Question: {question}
# """,
#         input_variables=["context", "question"]
#     )

#     def format_docs(docs):
#         return "\n\n".join(
#             doc.page_content for doc in docs
#         )

#     parallel_chain = RunnableParallel({
#         "context": retriever | RunnableLambda(format_docs),
#         "question": RunnablePassthrough()
#     })

#     return parallel_chain | prompt | llm | StrOutputParser()


from dotenv import load_dotenv

load_dotenv()

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import TFIDFRetriever

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda
)
from langchain_core.output_parsers import StrOutputParser


def extract_video_id(url: str):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    if "youtube.com/watch?v=" in url:
        return url.split("v=")[1].split("&")[0]

    raise ValueError("Invalid YouTube URL")


def get_transcript(video_id: str):
    try:
        youtube = YouTubeTranscriptApi()
        transcript_list = youtube.list(video_id)

        transcript = None

        for t in transcript_list:
            if t.language_code == "en":
                transcript = t
                break

        if transcript is None:
            transcript = next(iter(transcript_list))

        fetched_transcript = transcript.fetch()

        return " ".join(
            chunk.text for chunk in fetched_transcript
        )

    except TranscriptsDisabled:
        raise ValueError("No captions available for this video")

    except Exception as e:
        raise ValueError(f"Could not retrieve transcript: {str(e)}")


def create_vector_store(transcript_text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents([transcript_text])

    return TFIDFRetriever.from_documents(chunks)


def create_chain(retriever):

    llm = ChatGroq(
        model="openai/gpt-oss-120b"
    )

    prompt = PromptTemplate(
        template="""
You are a helpful assistant.
Answer only from provided transcript context.
If context is insufficient, just say you don't know.

{context}

Question: {question}
""",
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(
            doc.page_content for doc in docs
        )

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    return parallel_chain | prompt | llm | StrOutputParser()
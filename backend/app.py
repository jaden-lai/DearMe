from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.chat_message_histories import RedisChatMessageHistory
from dotenv import load_dotenv

from routers import tts
from convollm import raggy
from journallllm import journalrag

import datetime, redis, os

load_dotenv()

app = FastAPI()

# Add CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session is YYYYMMDD
session = datetime.datetime.now().strftime("%Y%m%d")

REDIS_URL = os.getenv("REDIS_URL")

# Define the input data model
class QueryRequest(BaseModel):
    query: str
    session_id: str

class JournalRequest(BaseModel):
    session_id: str

def log_messages(session_id: str, user_query: str, response: str):
    """
    Log user queries and responses to Redis
    Args:
        session_id (str): The session ID
        user_query (str): The user query
        response (str): The AI response
    Returns:
        None
    """
    try:
        message_log = RedisChatMessageHistory(session_id, REDIS_URL)
        message_log.add_user_message(user_query)
        message_log.add_ai_message(response)
        return
    except Exception as e:
        print(f"Error in log_chat_history: {e}")
        raise

@app.get("/history/{session_id}")
def get_session_history(session_id: str):
    """
    Get the session history from Redis
    Args:
        session_id (str): The session ID
    Returns:
        List[BaseMessage]: The list of chat messages
    """
    return {"message": RedisChatMessageHistory(session_id, REDIS_URL).messages}

@app.get("/")
def read_root():
    return {"message": f"Hello World @ {session}"}

@app.get("/dbhealth")
def ping_db():
    try:
        r = redis.Redis.from_url(REDIS_URL)
        assert r.ping()
        return {"message": "Database connection successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")


def convert_to_speech(text: str):
    """
    Text to speech
    """
    try:
        tts.generateVoice(text, "data/output.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Success"}

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    query = request.query
    session_id = request.session_id
    try:
        response = raggy.query_chroma(query, session_id)
        print(response)
        log_messages(session_id, query, response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{str(e)} at /query")
    
@app.post("/journal")
async def create_journal(request: JournalRequest):
    session_id = request.session_id
    try:
        print(session_id)
        response = journalrag.query_chroma(session_id)
        print(response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
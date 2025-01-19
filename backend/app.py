from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from routers import tts, audio_to_text
from convollm import raggy

import shutil

app = FastAPI()

# Add CORS middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input data model
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}


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
    try:
        response = raggy.query_chroma(query)
        print(response)
        convert_to_speech(response)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
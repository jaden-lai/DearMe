from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from routers import tts
from convollm import raggy

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
    return {"message": "Hello "}

@app.post("/convert_to_speech")
def convert_to_speech(text: str):
    try:
        tts.generateVoice(text, "./")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"message": "Success"}

@app.post("/convert_to_text")
def convert_to_text():
    return {"message": "Success"}

@app.get("/get_text")
def get_text():
    return {"message": "Success"}

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    query = request.query
    try:
        response = raggy.query_chroma(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
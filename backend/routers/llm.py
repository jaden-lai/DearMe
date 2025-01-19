from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import FastEmbedEmbeddings
import ssl

# Ensure SSL context works for NLTK if needed
ssl._create_default_https_context = ssl._create_unverified_context

CHROMA_PATH = "chroma"

# Define the input data model
class QueryRequest(BaseModel):
    query: str

# Initialize FastAPI app
app = FastAPI()

def query_chroma(query):
    try:
        # Embedding function
        embedding = FastEmbedEmbeddings()

        # Create Chroma DB and retriever
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding)
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,  # Adjust based on the number of relevant docs you want to retrieve
                "score_threshold": 0.7,
            },
        )

        # Define the prompt template
        prompt = PromptTemplate.from_template(
            """
            <s> [INST] You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences 
            maximum and keep the answer concise.
            Response format should say "YUH" after every sentence. 
            [/INST] </s> 
            [INST] Question: {question} 
            Context: {context} 
            Answer: [/INST]
            """
        )

        # Initialize the model
        model = ChatOllama(model="mistral")

        # Retrieve relevant documents based on the query using invoke
        documents = retriever.invoke(query)
        if not documents:
            return "No relevant documents found."

        # Prepare context by joining the document contents
        context_text = "\n".join([doc.page_content for doc in documents])

        # Format the prompt with the question and context
        input_data = prompt.format(question=query, context=context_text)

        # Create a list of messages as strings
        messages = [input_data]

        # Pass the list of messages (strings) to model.invoke
        response = model.invoke(messages)

        # Access the content of the response
        return response.content  # Accessing the content directly

    except Exception as e:
        return f"Error during query: {e}"

@app.post("/query")
async def query_endpoint(request: QueryRequest):
    query = request.query
    try:
        response = query_chroma(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
import os
import shutil
import ssl
import nltk 
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
from nltk import word_tokenize, sent_tokenize
# Ensure SSL context works for NLTK if needed
ssl._create_default_https_context = ssl._create_unverified_context

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {DATA_PATH}.")
    return documents


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_chroma(chunks):
    try:
        if os.path.exists(CHROMA_PATH):  # Clear existing database
            shutil.rmtree(CHROMA_PATH)

        # Split chunks into smaller batches for more manageable processing
        batch_size = 1000  # Adjust as needed based on memory constraints
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            db = Chroma.from_documents(
                batch, FastEmbedEmbeddings(), persist_directory=CHROMA_PATH
            )
            db.persist()
            print(f"Saved batch {i//batch_size + 1} with {len(batch)} chunks.")
        
        print(f"Saved {len(chunks)} total chunks to {CHROMA_PATH}.")
    except Exception as e:
        print(f"Error saving to Chroma: {e}")


if __name__ == "__main__":
    generate_data_store()

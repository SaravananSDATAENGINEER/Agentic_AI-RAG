import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import chromadb

# PostgreSQL Connection Pipeline
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/rag_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ChromaDB Connection Pipeline
CHROMA_DB_URL = os.getenv("CHROMA_DB_URL", "http://localhost:8000")
try:
    chroma_client = chromadb.HttpClient(host="vectordb", port=8000)
except Exception as e:
    # Fallback to ephemeral client for testing outside docker
    print(f"Failed to connect to Chroma HTTP Client. Error: {e}")
    chroma_client = chromadb.Client()
    
# Get or create collection
collection = chroma_client.get_or_create_collection(name="pdf_documents")

def get_chroma_collection():
    return collection

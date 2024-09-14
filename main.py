from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db, init_db
from models import document_model, user_model
from utils.rate_limiter import check_rate_limit
from utils.similarity import search_documents

app = FastAPI()

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "API is active"}

# Search endpoint
# @app.post("/search")
# def search_documents_endpoint(
#     text: str, top_k: int = 5, threshold: float = 0.5, user_id: str = Depends(check_rate_limit), db: Session = Depends(get_db)
# ):
#     results = search_documents(db, text, top_k, threshold)
#     return results
@app.post("/search")
def search_documents_endpoint(
    text: str, top_k: int = 5, threshold: float = 0.5, user_id: str = Depends(check_rate_limit), db: Session = Depends(get_db)
):
    results = search_documents(db, text, top_k, threshold)
    return results


# Start database
@app.on_event("startup")
def on_startup():
    init_db()

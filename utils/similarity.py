from sqlalchemy.orm import Session
from models.document_model import Document
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def search_documents(db: Session, text: str, top_k: int = 5, threshold: float = 0.5):
    documents = db.query(Document).all()
    contents = [doc.content for doc in documents]

    # Apply TF-IDF encoding
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(contents)
    query_vector = vectorizer.transform([text])

    similarities = cosine_similarity(query_vector, doc_vectors).flatten()
    results = []

    for idx, score in enumerate(similarities):
        if score >= threshold:
            results.append({"title": documents[idx].title, "similarity": score})

    # Sort and return top_k results
    results = sorted(results, key=lambda x: x['similarity'], reverse=True)[:top_k]
    return results

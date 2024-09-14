from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_model import User
from db import SessionLocal

def check_rate_limit(user_id: str, db: Session = SessionLocal()):
    user = db.query(User).filter(User.user_id == user_id).first()

    if user:
        if user.api_calls >= 5:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        user.api_calls += 1
    else:
        user = User(user_id=user_id, api_calls=1)
        db.add(user)

    db.commit()
    return user_id

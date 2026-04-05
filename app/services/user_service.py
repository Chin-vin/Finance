from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.user_model import User


def get_user(db: Session, username: str):
    return db.query(User).filter(
        func.lower(User.username) == username.lower()
    ).first()


def activate_user_service(db: Session, username: str, current_user):
    user = get_user(db, username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins allowed")

    if user.is_deleted:
        raise HTTPException(status_code=400, detail="User is deleted")

    if user.is_active:
        raise HTTPException(status_code=400, detail="User is already active")

    user.is_active = True
    db.commit()

    return {"message": "User activated"}


def deactivate_user_service(db: Session, username: str, current_user):
    user = get_user(db, username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins allowed")

    if user.is_deleted:
        raise HTTPException(status_code=400, detail="User already deleted")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="User already inactive")

    if user.username == current_user.username:
        raise HTTPException(status_code=400, detail="Cannot deactivate yourself")

    if user.role == "admin":
        raise HTTPException(status_code=400, detail="Cannot deactivate another admin")

    user.is_active = False
    db.commit()

    return {"message": "User deactivated"}
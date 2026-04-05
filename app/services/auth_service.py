from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.user_model import User
from app.core.security import hash_password, verify_password, create_token


def register_user_service(db: Session, user):
    # validation
    if not user.username or not user.password or not user.role:
        raise HTTPException(status_code=400, detail="All fields are required")

    # check existing user
    existing = db.query(User).filter(
        func.lower(User.username) == user.username.lower()
    ).first()

    if existing:
        if existing.is_deleted:
            raise HTTPException(
                status_code=400,
                detail="User exists but is deactivated. Please contact admin to activate."
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="User already exists"
            )

    # create user
    new_user = User(
        username=user.username.lower(),
        password=hash_password(user.password),
        role=user.role.lower()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "username": new_user.username,
        "role": new_user.role
    }


def login_user_service(db: Session, username: str, password: str):
    # validation
    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Username and password required"
        )

    user = db.query(User).filter(
        func.lower(User.username) == username.lower(),
        User.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is deactivated. Contact admin."
        )
    # token
    token = create_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role
    }
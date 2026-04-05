from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.schemas.user_schema import UserCreate
from app.services.auth_service import register_user_service, login_user_service

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.post("/register")
@limiter.limit("3/minute")
def register(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user_service(db, user)


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user_service(
        db,
        form_data.username,
        form_data.password
    )
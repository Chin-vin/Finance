from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user_model import User
from app.core.deps import role_required
from sqlalchemy import func

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import activate_user_service, deactivate_user_service
from app.core.deps import role_required

from fastapi import HTTPException
from app.core.deps import get_current_user

router = APIRouter(prefix="/users")

@router.get("/")
def get_users(db: Session = Depends(get_db),
              user=Depends(role_required(["admin"]))):
    return db.query(User).filter(User.is_deleted == False).all()


@router.delete("/by-username/{username}")
def delete_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["admin"]))  
):
    user = db.query(User).filter(
        func.lower(User.username) == username.lower()
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_deleted:
        raise HTTPException(status_code=400, detail="User already deleted")

  
    if user.username == current_user.username:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    user.is_deleted = True
    db.commit()

    return {
        "message": "User soft deleted",
        "username": user.username
    }
    
@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }
    




@router.put("/activate/{username}")
def activate(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["admin"]))
):
    return activate_user_service(db, username, current_user)


@router.put("/deactivate/{username}")
def deactivate(
    username: str,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["admin"]))
):
    return deactivate_user_service(db, username, current_user)
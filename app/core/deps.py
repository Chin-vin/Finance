from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt,ExpiredSignatureError
from sqlalchemy import func
from app.core.security import SECRET_KEY, ALGORITHM
from app.models.user_model import User
from app.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid token payload")


    user = db.query(User).filter(
        func.lower(User.username) == username.lower(),
        User.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

   
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is deactivated")

    return user

def role_required(roles: list):
    def checker(user=Depends(get_current_user)):
        if user.role not in roles:  
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return checker
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.deps import get_current_user
from app.core.enums import ScopeEnum
from app.database import get_db
from app.models.record_model import Record
from app.services.dashboard_service import summary_service

router = APIRouter(prefix="/dashboard")

@router.get("/summary")
def summary(
    scope: ScopeEnum = ScopeEnum.SELF,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return summary_service(db, user, scope)
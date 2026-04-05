from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.enums import ScopeEnum
from app.database import get_db
from app.schemas.record_schema import RecordCreate
from app.core.deps import get_current_user, role_required
from app.services.record_service import create_record_service
from app.services.record_service import get_records_service
from app.services.record_service import search_records_service
from app.services.record_service import update_record_service
from app.services.record_service import delete_record_service
from app.services.record_service import monthly_service
from app.services.record_service import recent_service
from app.services.record_service import category_summary_service

router = APIRouter(prefix="/records")


@router.post("/")
def create(record: RecordCreate,
           db: Session = Depends(get_db),
           user=Depends(get_current_user)):
    return create_record_service(db, record, user)


@router.get("/")
def get_all(limit: int = 10, offset: int = 0,
            db: Session = Depends(get_db),
            user=Depends(role_required(["admin","analyst","viewer"]))):
    return get_records_service(db, user, limit, offset)


@router.get("/search")
def search(type: str = None, category: str = None,
           start_date: str = None, end_date: str = None,
           query: str = None,
           db: Session = Depends(get_db),
           user=Depends(role_required(["admin", "analyst"]))):
    return search_records_service(db, user, type, category, start_date, end_date, query)


@router.put("/{id}")
def update(id: int, record: RecordCreate,
           db: Session = Depends(get_db),
           user=Depends(role_required(["admin"]))):
    return update_record_service(db, id, record, user)


@router.delete("/{id}")
def delete(id: int,
           db: Session = Depends(get_db),
           user=Depends(role_required(["admin"]))):
    return delete_record_service(db, id, user)


@router.get("/monthly")
def monthly(db: Session = Depends(get_db)):
    return monthly_service(db)


@router.get("/recent")
def recent(db: Session = Depends(get_db)):
    return recent_service(db)



@router.get("/category-summary")
def category_summary(
    scope: ScopeEnum = ScopeEnum.SELF,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return category_summary_service(db, user, scope)

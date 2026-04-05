from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func
from datetime import datetime
from app.models.record_model import Record
from app.models.user_model import User

def create_record_service(db: Session, data, user):
    r = Record(**data.dict(), user_id=user.id)
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


def get_records_service(db: Session, user, limit, offset):
    if user.role == "admin":
        records = db.query(Record, User.username)\
            .join(User, Record.user_id == User.id)\
            .filter(Record.is_deleted == False)\
            .offset(offset).limit(limit).all()
    else:
        records = db.query(Record, User.username)\
            .join(User, Record.user_id == User.id)\
            .filter(
                Record.is_deleted == False,
                Record.user_id == user.id
            )\
            .offset(offset).limit(limit).all()

    return [
        {
            "id": r.Record.id,
            "amount": r.Record.amount,
            "type": r.Record.type,
            "category": r.Record.category,
            "date": r.Record.date,
            "notes": r.Record.notes,
            "username": r.username
        }
        for r in records
    ]


def search_records_service(db: Session, user, type, category, start_date, end_date, query):
    if user.role == "admin":
        q = db.query(Record, User.username)\
            .join(User, Record.user_id == User.id)\
            .filter(Record.is_deleted == False)
    else:
        q = db.query(Record, User.username)\
            .join(User, Record.user_id == User.id)\
            .filter(
                Record.is_deleted == False,
                Record.user_id == user.id
            )

    if type:
        q = q.filter(Record.type == type)

    if category:
        q = q.filter(Record.category == category)

    try:
        if start_date:
            q = q.filter(Record.date >= datetime.strptime(start_date, "%d-%m-%Y").date())

        if end_date:
            q = q.filter(Record.date <= datetime.strptime(end_date, "%d-%m-%Y").date())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format (DD-MM-YYYY)")

    if query:
        q = q.filter(
            Record.category.ilike(f"%{query}%") |
            Record.notes.ilike(f"%{query}%")
        )

    records = q.all()

    return [
        {
            "id": r.Record.id,
            "amount": r.Record.amount,
            "type": r.Record.type,
            "category": r.Record.category,
            "date": r.Record.date,
            "notes": r.Record.notes,
            "username": r.username
        }
        for r in records
    ]


def update_record_service(db: Session, id, data, user):
    r = db.query(Record).filter(
        Record.id == id,
        Record.user_id == user.id,
        Record.is_deleted == False
    ).first()

    if not r:
        raise HTTPException(status_code=404, detail="Record not found")

    for k, v in data.dict().items():
        setattr(r, k, v)

    db.commit()
    db.refresh(r)
    return r


def delete_record_service(db: Session, id, user):
    r = db.query(Record).filter(
        Record.id == id,
        Record.user_id == user.id,
        Record.is_deleted == False
    ).first()

    if not r:
        raise HTTPException(status_code=404, detail="Record not found")

    r.is_deleted = True
    db.commit()

    return {"message": "Record deleted"}





def category_summary_service(db: Session, user, scope: str = "self"):
    if scope not in ["self", "all"]:
        raise HTTPException(400, "Invalid scope")

    if user.role == "viewer" and scope == "all":
        raise HTTPException(403, "Viewer cannot access all users data")

    if scope == "self" or user.role == "viewer":
        data = db.query(
            Record.category,
            Record.type,
            func.sum(Record.amount)
        ).filter(
            Record.is_deleted == False,
            Record.user_id == user.id
        ).group_by(
            Record.category,
            Record.type
        ).all()

        result = {}

        for category, type_, amount in data:
            if category not in result:
                result[category] = {"income": 0, "expense": 0}

            result[category][type_] = amount

        return {
            "scope": "self",
            "categories": result
        }

    data = db.query(
        User.username,
        Record.category,
        Record.type,
        func.sum(Record.amount)
    ).join(User, Record.user_id == User.id)\
     .filter(Record.is_deleted == False)\
     .group_by(User.username, Record.category, Record.type)\
     .all()

    result = {}
    overall = {}

    for username, category, type_, amount in data:

        # per user
        if username not in result:
            result[username] = {}

        if category not in result[username]:
            result[username][category] = {"income": 0, "expense": 0}

        result[username][category][type_] = amount

        # overall
        if category not in overall:
            overall[category] = {"income": 0, "expense": 0}

        overall[category][type_] += amount

    return {
        "scope": "all",
        "users": result,
        "overall": overall
    }
def monthly_service(db: Session):
    data = db.query(
        func.strftime("%m", Record.date),
        Record.type,
        func.sum(Record.amount)
    ).filter(
        Record.is_deleted == False
    ).group_by(
        func.strftime("%m", Record.date),
        Record.type
    ).all()

    months = {
        "01": "Jan", "02": "Feb", "03": "Mar",
        "04": "Apr", "05": "May", "06": "Jun",
        "07": "Jul", "08": "Aug", "09": "Sep",
        "10": "Oct", "11": "Nov", "12": "Dec"
    }

    result = {}

    for m, type_, amount in data:
        month = months[m]

        if month not in result:
            result[month] = {"income": 0, "expense": 0}

        result[month][type_] = amount

    return result


def recent_service(db: Session):
    return db.query(Record)\
        .filter(Record.is_deleted == False)\
        .order_by(Record.date.desc())\
        .limit(5).all()



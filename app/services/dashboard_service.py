from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.record_model import Record
from app.models.user_model import User


def summary_service(db: Session, user, scope: str = "self"):
    if scope not in ["self", "all"]:
        raise HTTPException(400, "Invalid scope")

    if user.role == "viewer" and scope == "all":
        raise HTTPException(403, "Viewer cannot access all users data")

    if scope == "self" or user.role == "viewer":
        base_query = db.query(Record).filter(
            Record.is_deleted == False,
            Record.user_id == user.id
        )

        income = base_query.filter(Record.type == "income")\
            .with_entities(func.sum(Record.amount)).scalar() or 0

        expense = base_query.filter(Record.type == "expense")\
            .with_entities(func.sum(Record.amount)).scalar() or 0

        return {
            "scope": "self",
            "income": income,
            "expense": expense,
            "balance": income - expense
        }

    data = db.query(
        User.username,
        Record.type,
        func.sum(Record.amount)
    ).join(User, Record.user_id == User.id)\
     .filter(Record.is_deleted == False)\
     .group_by(User.username, Record.type).all()

    result = {}
    total_income = 0
    total_expense = 0

    for username, type_, amount in data:
        if username not in result:
            result[username] = {
                "income": 0,
                "expense": 0,
                "balance": 0
            }

        result[username][type_] = amount
        result[username]["balance"] = (
            result[username]["income"] - result[username]["expense"]
        )

        if type_ == "income":
            total_income += amount
        else:
            total_expense += amount

    return {
        "scope": "all",
        "users": result,
        "overall": {
            "income": total_income,
            "expense": total_expense,
            "balance": total_income - total_expense
        }
    }
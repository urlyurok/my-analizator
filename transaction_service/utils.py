import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from transaction_service.models import Transaction


logger = logging.getLogger(__name__)


def categorize_transaction(description: str) -> str:
    description = description.lower()
    categories = {
        "Food": ["restaurant", "cafe", "grocery", "food"],
        "Transport": ["taxi", "bus", "train", "fuel"],
        "Entertainment": ["cinema", "concert", "game"],
        "Utilities": ["electricity", "water", "internet"],
        "Other": []
    }
    for category, keywords in categories.items():
        if any(keyword in description for keyword in keywords):
            return category
    return "Other"


def check_limits(session: Session, user_id: int, transaction: Transaction):
    day_limit = 10000  # Дневной лимит в RUB
    week_limit = 50000  # Недельный лимит в RUB

    # Дневные траты
    day_start = transaction.timestamp.replace(
        hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    daily_spent = session.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.amount < 0,
        Transaction.timestamp >= day_start,
        Transaction.timestamp < day_end
    ).with_entities(sum(Transaction.amount)).scalar() or 0

    # Недельные траты
    week_start = transaction.timestamp - \
        timedelta(days=transaction.timestamp.weekday())
    week_end = week_start + timedelta(days=7)
    weekly_spent = session.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.amount < 0,
        Transaction.timestamp >= week_start,
        Transaction.timestamp < week_end
    ).with_entities(sum(Transaction.amount)).scalar() or 0

    if abs(daily_spent) > day_limit:
        logger.warning(
            f"User {user_id} exceeded daily limit: {abs(daily_spent)} RUB")
    if abs(weekly_spent) > week_limit:
        logger.warning(
            f"User {user_id} exceeded weekly limit: {abs(weekly_spent)} RUB")

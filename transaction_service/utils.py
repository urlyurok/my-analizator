from datetime import datetime, timedelta
import logging
from sqlalchemy.sql import func
from .models import Transaction

logger = logging.getLogger(__name__)


def categorize_transaction(description: str) -> str:
    description = description.lower()
    if any(word in description for word in ["coffee", "restaurant", "grocery", "food"]):
        return "Food"
    elif any(word in description for word in ["taxi", "transport", "bus", "train"]):
        return "Transport"
    elif any(word in description for word in ["movie", "concert", "game"]):
        return "Entertainment"
    elif any(word in description for word in ["electricity", "water", "internet", "bill"]):
        return "Utilities"
    return "Other"


def check_limits(session, user_id: int, transaction):
    DAILY_LIMIT = 10000
    WEEKLY_LIMIT = 50000

    day_start = transaction.timestamp.replace(
        hour=0, minute=0, second=0, microsecond=0)
    week_start = day_start - timedelta(days=day_start.weekday())

    # Use func.sum to ensure proper aggregation
    daily_spent = session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.amount < 0,
        Transaction.timestamp >= day_start
    ).scalar() or 0

    weekly_spent = session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.amount < 0,
        Transaction.timestamp >= week_start
    ).scalar() or 0

    if abs(daily_spent) > DAILY_LIMIT:
        logger.warning(
            f"Daily spending limit exceeded for user {user_id}: {abs(daily_spent)} RUB")
    if abs(weekly_spent) > WEEKLY_LIMIT:
        logger.warning(
            f"Weekly spending limit exceeded for user {user_id}: {abs(weekly_spent)} RUB")

from transaction_service.utils import categorize_transaction, check_limits
from transaction_service.models import Transaction, User
from transaction_service.database import SessionLocal, init_db
from sqlalchemy.sql import func
import logging
from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

# Настройка логгирования
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация FastAPI
app = FastAPI(title="Transaction Analysis Service")

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель для API


class TransactionInput(BaseModel):
    id: str
    user_id: int
    amount: float
    currency: str
    description: str
    timestamp: str

# Инициализация базы данных


@app.on_event("startup")
async def startup_event():
    init_db()


@app.get("/")
async def read_root():
    return {"title": "Transaction Analysis Service"}

# Импорт транзакций


@app.post("/transactions/import")
async def import_transactions(transactions: List[TransactionInput]):
    session = SessionLocal()
    try:
        for tx in transactions:
            try:
                timestamp = datetime.fromisoformat(tx.timestamp)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"Invalid timestamp format: {tx.timestamp}")
            if tx.currency != "RUB":
                raise HTTPException(
                    status_code=400, detail="Only RUB currency is supported")
            if not session.query(User).filter_by(id=tx.user_id).first():
                raise HTTPException(
                    status_code=400, detail=f"User {tx.user_id} not found")
            # Check for existing transaction
            if session.query(Transaction).filter_by(id=tx.id).first():
                raise HTTPException(
                    status_code=400, detail=f"Transaction ID {tx.id} already exists")

            category = categorize_transaction(tx.description)

            db_transaction = Transaction(
                id=tx.id,
                user_id=tx.user_id,
                amount=tx.amount,
                currency=tx.currency,
                category=category,
                description=tx.description,
                timestamp=timestamp
            )
            session.add(db_transaction)
            check_limits(session, tx.user_id, db_transaction)

        session.commit()
        return {"status": "success", "imported": len(transactions)}
    except Exception as e:
        session.rollback()
        logger.error(f"Error importing transactions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

# Получение статистики


@app.get("/users/{user_id}/stats")
async def get_stats(user_id: int, from_date: str, to_date: str):
    session = SessionLocal()
    try:
        start = datetime.fromisoformat(from_date)
        end = datetime.fromisoformat(to_date) + timedelta(days=1)
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    try:
        if not session.query(User).filter_by(id=user_id).first():
            raise HTTPException(status_code=404, detail="User not found")

        total_spent = session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.amount < 0,
            Transaction.timestamp >= start,
            Transaction.timestamp < end
        ).scalar() or 0

        by_category = session.query(Transaction.category, func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.amount < 0,
            Transaction.timestamp >= start,
            Transaction.timestamp < end
        ).group_by(Transaction.category).all()
        by_category = {cat: abs(amount) for cat, amount in by_category}

        days = (end - start).days
        daily_average = abs(total_spent) / days if days > 0 else 0

        return {
            "total_spent": abs(total_spent),
            "by_category": by_category,
            "daily_average": daily_average
        }
    except Exception as e:
        logger.error(f"Error retrieving stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

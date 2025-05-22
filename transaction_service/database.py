from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Transaction
import random
from datetime import datetime, timedelta
from utils import categorize_transaction
import logging

logger = logging.getLogger(__name__)

# Настройка подключения к PostgreSQL
DATABASE_URL = "postgresql+psycopg2://user:password@db:5432/transactions"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        # Проверка, есть ли пользователи
        if not session.query(User).first():
            # Создание тестового пользователя
            user = User(id=1, name="Test User")
            session.add(user)

            # Генерация тестовых транзакций
            descriptions = [
                "Taxi to airport", "Grocery store", "Cinema ticket",
                "Electricity bill", "Coffee at cafe", "Train ticket",
                "Concert ticket", "Internet bill", "Restaurant dinner"
            ]
            for i in range(50):
                tx = Transaction(
                    id=f"tx{i+1001}",
                    user_id=1,
                    amount=-random.uniform(100, 5000),
                    currency="RUB",
                    description=random.choice(descriptions),
                    category=categorize_transaction(
                        random.choice(descriptions)),
                    timestamp=datetime(2024, 11, 1) +
                    timedelta(days=random.randint(0, 30))
                )
                session.add(tx)
            session.commit()
            logger.info("Test data generated")
    except Exception as e:
        session.rollback()
        logger.error(f"Error generating test data: {str(e)}")
    finally:
        session.close()

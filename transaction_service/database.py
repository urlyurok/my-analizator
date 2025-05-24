import time
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from transaction_service.models import Base, User, Transaction
from transaction_service.utils import categorize_transaction

DATABASE_URL = "postgresql+psycopg2://user:password@db:5432/transactions"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    time.sleep(5)  # ⏳ Подождать, пока PostgreSQL полностью запустится
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        user_count = db.query(User).count()
        if user_count == 0:
            for i in range(5):
                user = User(id=i + 1, name=f"User {i + 1}")
                db.add(user)

            start_date = datetime(2024, 11, 1)
            for user_id in range(1, 6):
                for _ in range(20):
                    amount = round(random.uniform(-1000, 1000), 2)
                    description = random.choice(
                        ["Coffee shop", "Grocery store", "Online purchase", "Restaurant", "Taxi"])
                    timestamp = start_date + timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(0, 23)
                    )
                    category = categorize_transaction(description)
                    transaction = Transaction(
                        id=f"tx{user_id}{random.randint(1000, 9999)}",
                        user_id=user_id,
                        amount=amount,
                        currency="RUB",
                        description=description,
                        timestamp=timestamp,
                        category=category
                    )
                    db.add(transaction)
            db.commit()
            print("Test data generated for users and transactions")

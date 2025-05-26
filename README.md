# Сервис анализа транзакций

Это микросервис на Python.  
Бэкенд построен на FastAPI, SQLAlchemy и PostgreSQL.

---

## 📌 Основные возможности

- **Импорт транзакций** — через API или форму на фронтенде с валидацией.  
- **Категоризация** — автоматическое определение категории транзакции по ключевым словам (Еда, Транспорт, Развлечения, Коммунальные услуги, Другое).  
- **Проверка лимитов** — логирование предупреждений при превышении дневного (10 000 ₽) или недельного (50 000 ₽) лимита расходов.  
- **REST API** — получение статистики по пользователю, датам и категориям.  
- **Фронтенд** — импорт транзакций и просмотр статистики с помощью круговой диаграммы.  
- **База данных** — PostgreSQL для хранения пользователей и транзакций.  
- **Docker** — удобный деплой с помощью Docker Compose.

---

## 🗂️ Структура проекта

- `transaction_service/main.py` — приложение FastAPI с API-эндпоинтами.  
- `transaction_service/models.py` — модели SQLAlchemy (User, Transaction).  
- `transaction_service/utils.py` — функции категоризации и проверки лимитов.  
- `transaction_service/database.py` — настройка БД и генерация тестовых данных.  
- `frontend/index.html` — фронтенд.  
- `Dockerfile` — Docker-конфигурация для бэкенда.  
- `frontend/Dockerfile` — Docker-конфигурация для фронтенда.  
- `docker-compose.yml` — оркестрация бэкенда, фронтенда и PostgreSQL.  
- `requirements.txt` — зависимости Python.  
- `postman_collection.json` — коллекция Postman для тестирования API.

---

## 📦 Требования

- Установленные **Docker** и **Docker Compose**.  
- **Python 3.11**, если запускать бэкенд без Docker.

---

## 🚀 Установка и запуск

### Вариант 1: Через Docker Compose (рекомендую)

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/urlyurok/my-analizator
   cd transaction-service
   ```

2. Запустите сервисы:
   ```bash
   docker-compose up --build -d
   ```

3. Проверьте доступность:
   - Бэкенд: `http://localhost:8000` (API)  
   - Фронтенд: `http://localhost:3000` (веб-интерфейс)  
   - PostgreSQL: `localhost:5432` (база `transactions`, пользователь `user`, пароль `password`)

4. Остановите сервисы:
   ```bash
   docker-compose down
   ```

### Вариант 2: Локальный запуск бэкенда (без Docker)

1. Установите **Python 3.11** и **PostgreSQL**.

2. Клонируйте репозиторий:
   ```bash
   git clone <repository-url>
   cd transaction-service
   ```

3. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

5. Настройте PostgreSQL:
   - Создайте базу данных `transactions`.  
   - Обновите `DATABASE_URL` в `transaction_service/database.py`:
     ```python
     DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/transactions"
     ```

6. Запустите бэкенд:
   ```bash
   uvicorn transaction_service.main:app --host 0.0.0.0 --port 8000
   ```

7. Проверьте: `http://localhost:8000`.

### Запуск фронтенда локально
- Фронтенд требует веб-сервера (например, nginx). Проще использовать Docker:
  ```bash
  docker-compose up frontend
  ```

  

контакты: yura_kurilin@bk.ru
tg: urlyura
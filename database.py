from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Строка подключения к базе данных
DATABASE_URL = "sqlite:///example.db"  # Укажите путь к вашей базе данных

# Создание подключения к базе данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Для SQLite добавляем параметр connect_args

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для инициализации базы данных
def init_db():
    """
    Инициализирует базу данных, создавая все таблицы, если они не существуют.
    """
    Base.metadata.create_all(bind=engine)

# Функция для получения новой сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

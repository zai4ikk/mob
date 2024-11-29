from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Базовый класс для всех моделей
Base = declarative_base()

# Модель пользователя
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    role = Column(String, default="user")  # Роль пользователя: 'user' или 'admin'

    # Связи с другими таблицами
    wishes = relationship("Wish", back_populates="user")
    categories = relationship("Category", back_populates="user")


# Модель категории
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))  # Внешний ключ на пользователя, который создал категорию

    # Связи с другими таблицами
    wishes = relationship("Wish", back_populates="category")
    user = relationship("User", back_populates="categories")


# Модель желания
class Wish(Base):
    __tablename__ = 'wishes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)  # Внешний ключ на категорию
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Связи с другими таблицами
    user = relationship("User", back_populates="wishes")
    category = relationship("Category", back_populates="wishes")

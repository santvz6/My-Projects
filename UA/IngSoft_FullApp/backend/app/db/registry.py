"""Database registry for managing database connections and sessions."""

import os
from typing import Optional

from sqlalchemy import Engine
from sqlmodel import create_engine, Session
import time
from sqlalchemy.exc import OperationalError


class DatabaseRegistry:
    """Registers and manages the database session."""

    DB_HOST = os.getenv("DB_HOST", "db")
    DB_USER = os.getenv("DB_USER", "ecomuser")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "ecompass")
    DB_NAME = os.getenv("DB_NAME", "proyecto_ecommerce")
    __session: Optional[Session] = None

    @staticmethod
    def session() -> Session:
        """Returns the database session."""
        if DatabaseRegistry.__session is None:
            DatabaseRegistry.__session = DatabaseRegistry.__create_session()
        return DatabaseRegistry.__session

    @classmethod
    def get_engine(cls) -> Engine:
        """Returns the engine for the database with retry logic."""
        engine = create_engine(
            f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:3306/{cls.DB_NAME}",
            echo=True,
        )
        for _ in range(10):  # 10 intentos, espera 1s entre ellos
            try:
                with engine.connect():
                    break
            except OperationalError:
                print("Esperando a que la base de datos esté lista...")
                time.sleep(1)
        return engine

    @classmethod
    def __create_session(cls) -> Session:
        """Returns the session for the database."""
        return Session(cls.get_engine())

        

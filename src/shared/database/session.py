import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config.settings import settings

# 1. Identifica se a conexão atual exige um driver assíncrono (FastAPI) ou síncrono (Worker)
IS_ASYNC = "asyncpg" in settings.DATABASE_URL

# 2. Cria o Engine correto dinamicamente para o container atual
if IS_ASYNC:
    # Engine assíncrono para a API FastAPI
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )
    # Fábrica de sessões assíncronas
    SessionLocal = sessionmaker(
        bind=engine, 
        class_=AsyncSession, 
        autocommit=False, 
        autoflush=False
    )
else:
    # Engine síncrono clássico para o pipeline de Ingestão
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )
    # Fábrica de sessões síncronas
    SessionLocal = sessionmaker(
        bind=engine, 
        autocommit=False, 
        autoflush=False
    )

# 3. Gerenciador de contexto síncrono (Usado pelo Worker de Ingestão)
@contextmanager
def get_db_session():
    """
    Gerenciador de Contexto Síncrono para sessões do banco.
    Utilizado pelo pipeline de ingestão de arquivos.
    """
    if IS_ASYNC:
        raise RuntimeError(
            "get_db_session cannot be used with async database URLs; use get_async_db instead."
        )

    session: Session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def get_async_db():
    """
    Yield comum do FastAPI para injetar sessões assíncronas nas rotas da API.
    """
    if not IS_ASYNC:
        raise RuntimeError("Tentativa de criar sessão assíncrona usando uma URL de banco síncrona.")
        
    async with SessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SQLALCHEMY_DATABASE_URL = 'postgres://postgresql_pgadmin_moat_user:CCfVVcSRpMgusmMXUUgmG9s8JSHoffve@dpg-ceapfoha6gdichj3d6q0-a/postgresql_pgadmin_moat'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgresql_pgadmin_moat_user:CCfVVcSRpMgusmMXUUgmG9s8JSHoffve@dpg-ceapfoha6gdichj3d6q0-a/postgresql_pgadmin_moat'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

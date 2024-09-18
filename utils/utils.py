from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.avatar import Base

# Oracle 데이터베이스 연결 설정 (SQLite로 대체 가능)
SQLALCHEMY_DATABASE_URL = "oracle+cx_oracle://c##dressmyfit:ss1911856@DESKTOP-GQR7PO6:1521/orcl"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

# 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, TIMESTAMP, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 기본 클래스
Base = declarative_base()

# 모델들
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nickname = Column(String(50), nullable=False)
    session_id = Column(String(255), unique=True, nullable=False)

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    respondent_count = Column(Integer, nullable=False)
    share_link = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(Enum('objective', 'subjective', name='item_type'), nullable=False)

class Respondent(Base):
    __tablename__ = 'respondents'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    nickname = Column(String(50), nullable=False)

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    respondent_id = Column(Integer, ForeignKey('respondents.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    response = Column(Text, nullable=False)

# 데이터베이스 URL
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# 엔진과 세션
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 테이블 생성
Base.metadata.create_all(bind=engine) 
# backend/database.py

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import json

Base = declarative_base()
DB_URL = "sqlite:///osint_reports.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    parsed_query = Column(Text)
    task_plan = Column(Text)
    retrieved_chunks = Column(Text)
    pivot_insights = Column(Text)
    final_report = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def save_investigation(state: dict):
    db = SessionLocal()
    try:
        inv = Investigation(
            query=state.get("input", ""),
            parsed_query=json.dumps(state.get("parsed_query", {})),
            task_plan=json.dumps(state.get("task_plan", {})),
            retrieved_chunks=json.dumps(state.get("retrieved_chunks", [])),
            pivot_insights=json.dumps(state.get("pivot_insights", {})),
            final_report=state.get("final_report", "")
        )
        db.add(inv)
        db.commit()
    except Exception as e:
        print("❌ DB Save Error:", str(e))
        db.rollback()
    finally:
        db.close()

def get_all_investigations():
    db = SessionLocal()
    try:
        return db.query(Investigation).order_by(Investigation.created_at.desc()).all()
    finally:
        db.close()


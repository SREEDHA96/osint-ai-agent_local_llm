from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import json

# Database setup
DB_URL = "sqlite:///osint_reports.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ORM Model
class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False)
    parsed_query = Column(Text)
    task_plan = Column(Text)
    retrieved_chunks = Column(Text)
    pivot_insights = Column(Text)
    final_report = Column(Text)
    evaluation_score = Column(Integer)             
    evaluation_verdict = Column(Text) 
    created_at = Column(DateTime, default=datetime.utcnow)
    accuracy = Column(Integer, nullable=True)
    coherence = Column(Integer, nullable=True)
    completeness = Column(Integer, nullable=True)
    reliability = Column(Integer, nullable=True)
    verdict = Column(Text, nullable=True)

Base.metadata.create_all(bind=engine)

# Save full LangGraph state
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

# Insert investigation with evaluation
def insert_investigation(query, final_report, evaluation):
    db = SessionLocal()
    try:
        inv = Investigation(
            query=query,
            final_report=final_report,
            evaluation_score=evaluation.get("score"),
            evaluation_verdict=evaluation.get("verdict"),
            accuracy=evaluation.get("accuracy"),
            coherence=evaluation.get("coherence"),
            completeness=evaluation.get("completeness"),
            reliability=evaluation.get("reliability"),
            verdict=evaluation.get("verdict"),
        )
        db.add(inv)
        db.commit()
        return inv
    except Exception as e:
        print("❌ Insert Error:", str(e))
        db.rollback()
    finally:
        db.close()

# Retrieve all past investigations
def get_all_investigations():
    db = SessionLocal()
    try:
        return db.query(Investigation).order_by(Investigation.created_at.desc()).all()
    finally:
        db.close()

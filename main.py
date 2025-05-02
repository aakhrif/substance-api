# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import OperationalError
from datetime import datetime
import uuid
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/stoffe")
Base = declarative_base()
engine = None
SessionLocal = None

class Substance(Base):
    __tablename__ = "substance"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    formula = Column(String)
    cas_number = Column(String, unique=True)
    melting_point = Column(Float)
    boiling_point = Column(Float)
    density = Column(Float)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class SubstanceCreate(BaseModel):
    name: str
    formula: Optional[str] = None
    cas_number: Optional[str] = None
    melting_point: Optional[float] = None
    boiling_point: Optional[float] = None
    density: Optional[float] = None
    category: Optional[str] = None

class SubstanceRead(SubstanceCreate):
    id: str
    created_at: datetime

app = FastAPI()

@app.on_event("startup")
def startup():
    global engine, SessionLocal
    for _ in range(10):
        try:
            engine = create_engine(DATABASE_URL)
            SessionLocal = scoped_session(sessionmaker(bind=engine))
            Base.metadata.create_all(bind=engine)
            print("✅ Database ready.")
            return
        except OperationalError as e:
            print("⏳ Waiting for database...", str(e))
            time.sleep(2)
    raise Exception("❌ Database connection failed after multiple retries.")

@app.get("/substances", response_model=List[SubstanceRead])
def list_substances():
    with SessionLocal() as db:
        return db.query(Substance).all()

@app.post("/substances", response_model=SubstanceRead)
def create_substance(substance: SubstanceCreate):
    with SessionLocal() as db:
        obj = Substance(**substance.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

@app.get("/substances/{id}", response_model=SubstanceRead)
def get_substance(id: str):
    with SessionLocal() as db:
        obj = db.query(Substance).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

@app.put("/substances/{id}", response_model=SubstanceRead)
def update_substance(id: str, substance: SubstanceCreate):
    with SessionLocal() as db:
        obj = db.query(Substance).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        for key, value in substance.dict().items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
        return obj

@app.delete("/substances/{id}")
def delete_substance(id: str):
    with SessionLocal() as db:
        obj = db.query(Substance).get(id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(obj)
        db.commit()
        return {"deleted": True}

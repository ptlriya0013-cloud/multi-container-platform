from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.redis_client import redis_client

app = FastAPI(title="Multi-Container Platform API")


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/items")
def create_item(name: str, db: Session = Depends(get_db)):
    item = Item(name=name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name}


@app.get("/items")
def list_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return [{"id": i.id, "name": i.name} for i in items]


@app.get("/visits")
def visits():
    count = redis_client.incr("visit_count")
    return {"visits": count}
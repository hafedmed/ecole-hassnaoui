from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db

router = APIRouter(prefix="/classes", tags=["classes"])

@router.post("/", response_model=schemas.ClassOut)
def create_class(classe: schemas.ClassCreate, db: Session = Depends(get_db)):
    db_class = db.query(models.Class).filter(models.Class.name == classe.name).first()
    if db_class:
        raise HTTPException(status_code=400, detail="Classe déjà existante")
    new_class = models.Class(**classe.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@router.get("/", response_model=list[schemas.ClassOut])
def list_classes(db: Session = Depends(get_db)):
    return db.query(models.Class).all()

@router.get("/{class_id}", response_model=schemas.ClassOut)
def get_class(class_id: int, db: Session = Depends(get_db)):
    classe = db.query(models.Class).get(class_id)
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")
    return classe

@router.delete("/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    classe = db.query(models.Class).get(class_id)
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")
    db.delete(classe)
    db.commit()
    return {"message": "Classe supprimée"}


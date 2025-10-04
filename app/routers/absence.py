from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db


router = APIRouter(prefix="/absences", tags=["Absences"])



@router.get("/", response_model=list[schemas.AbsenceOut])
def get_absences(db: Session = Depends(get_db)):
    return db.query(models.Absence).all()

@router.get("/{absence_id}", response_model=schemas.AbsenceOut)
def get_absence(absence_id: int, db: Session = Depends(get_db)):
    absence = db.query(models.Absence).filter(models.Absence.id == absence_id).first()
    if not absence:
        raise HTTPException(status_code=404, detail="Absence non trouvée")
    return absence

@router.post("/", response_model=schemas.AbsenceOut)
def create_absence(absence: schemas.AbsenceCreate, db: Session = Depends(get_db)):
    db_abs = models.Absence(**absence.dict())
    db.add(db_abs)
    db.commit()
    db.refresh(db_abs)
    return db_abs

@router.put("/{absence_id}", response_model=schemas.AbsenceOut)
def update_absence(absence_id: int, absence: schemas.AbsenceUpdate, db: Session = Depends(get_db)):
    db_abs = get_by_id(db, absence_id)
    if db_abs:
        for field, value in absence.dict().items():
            setattr(db_abs, field, value)
        db.commit()
        db.refresh(db_abs)
    return db_abs

@router.delete("/{absence_id}")
def delete_absence(absence_id: int, db: Session = Depends(get_db)):
    db_abs = get_by_id(db, absence_id)
    if db_abs:
        db.delete(db_abs)
        db.commit()
    return db_abs

def get_by_id(db: Session, absence_id: int):
    return db.query(models.Absence).filter(models.Absence.id == absence_id).first()
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db

router = APIRouter(prefix="/inscriptions", tags=["inscriptions"])

@router.post("/", response_model=schemas.InscriptionOut)
def create_inscription(insc: schemas.InscriptionCreate, db: Session = Depends(get_db)):
    # Vérifier que student existe
    student = db.query(models.Student).get(insc.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")

    # Vérifier que class existe
    classe = db.query(models.Class).get(insc.class_id)
    if not classe:
        raise HTTPException(status_code=404, detail="Classe introuvable")

    new_insc = models.Inscription(**insc.dict())
    db.add(new_insc)
    db.commit()
    db.refresh(new_insc)
    return new_insc

@router.get("/", response_model=list[schemas.InscriptionOut])
def list_inscriptions(db: Session = Depends(get_db)):
    return db.query(models.Inscription).all()

@router.get("/{insc_id}", response_model=schemas.InscriptionOut)
def get_inscription(insc_id: int, db: Session = Depends(get_db)):
    insc = db.query(models.Inscription).get(insc_id)
    if not insc:
        raise HTTPException(status_code=404, detail="Inscription introuvable")
    return insc

@router.delete("/{insc_id}")
def delete_inscription(insc_id: int, db: Session = Depends(get_db)):
    insc = db.query(models.Inscription).get(insc_id)
    if not insc:
        raise HTTPException(status_code=404, detail="Inscription introuvable")
    db.delete(insc)
    db.commit()
    return {"message": "Inscription supprimée"}

# ➤ Modifier un élève
@router.put("/{insc_id}", response_model=schemas.InscriptionOut)
def update_inscription(insc_id: int, updated: schemas.InscriptionCreate, db: Session = Depends(get_db)):
    insc = db.query(models.Inscription).get(insc_id)
    if not insc:
        raise HTTPException(status_code=404, detail="Inscription introuvable")
    
    for key, value in updated.dict().items():
        setattr(insc, key, value)

    db.commit()
    db.refresh(insc)
    return insc

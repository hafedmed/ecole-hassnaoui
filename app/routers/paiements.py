from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db

router = APIRouter(prefix="/paiements", tags=["paiements"])

# ➤ Créer un paiement
@router.post("/", response_model=schemas.PaiementOut)
def create_paiement(paiement: schemas.PaiementCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(paiement.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    new_paiement = models.Paiement(**paiement.dict())
    db.add(new_paiement)
    db.commit()
    db.refresh(new_paiement)
    return new_paiement

# ➤ Lister tous les paiements
@router.get("/", response_model=list[schemas.PaiementOut])
def list_paiements(db: Session = Depends(get_db)):
    return db.query(models.Paiement).all()

# ➤ Récupérer un paiement par ID
@router.get("/{paiement_id}", response_model=schemas.PaiementOut)
def get_paiement(paiement_id: int, db: Session = Depends(get_db)):
    paiement = db.query(models.Paiement).get(paiement_id)
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    return paiement

@router.put("/{paiement_id}", response_model=schemas.PaiementOut)
def update_paiement(paiement_id: int, updated: schemas.PaiementUpdate, db: Session = Depends(get_db)):
    paiement = db.query(models.Paiement).get(paiement_id)
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(paiement, key, value)

    db.commit()
    db.refresh(paiement)
    return paiement


# ➤ Supprimer un paiement
@router.delete("/{paiement_id}")
def delete_paiement(paiement_id: int, db: Session = Depends(get_db)):
    paiement = db.query(models.Paiement).get(paiement_id)
    if not paiement:
        raise HTTPException(status_code=404, detail="Paiement introuvable")
    db.delete(paiement)
    db.commit()
    return {"message": "Paiement supprimé"}

# ➤ Lister les paiements d’un élève
@router.get("/student/{student_id}", response_model=list[schemas.PaiementOut])
def list_paiements_by_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    return student.paiements

@router.get("/impayee", response_model=list[schemas.PaiementOut])
def paiements_impayes_par_nature(nature: str = Query(...), db: Session = Depends(get_db)):
    """
    Retourne la liste des paiements d'une nature donnée où le reste > 0
    """
    return db.query(models.Paiement)\
             .filter(models.Paiement.nature == nature)\
             .filter(models.Paiement.reste > 0)\
             .all()


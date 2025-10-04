from fastapi import APIRouter, Depends, UploadFile, File, HTTPException,Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.deps import get_db
import os
import shutil


router = APIRouter(prefix="/students", tags=["students"])
UPLOAD_DIR = "photos"

# S'assurer que le dossier existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/{student_id}/upload-photo")
async def upload_student_photo(student_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Élève non trouvé")

    # Extraire l'extension (jpg/png)
    ext = os.path.splitext(file.filename)[1]
    if ext.lower() not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Format de fichier non supporté")

    # Construire le nom du fichier
    filename = f"{student.id}_{student.nom}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Sauvegarder le fichier
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Mettre à jour l’URL en base
    student.photo_url = f"/{UPLOAD_DIR}/{filename}"
    db.commit()
    db.refresh(student)

    return {"message": "Photo uploadée avec succès", "photo_url": student.photo_url}

# ➤ Créer un élève
@router.post("/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# ➤ Lister tous les élèves
@router.get("/", response_model=list[schemas.StudentOut])
def list_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@router.get("/impayee", response_model=list[schemas.StudentOut])
def get_students_impayee(nature: str = Query(...), db: Session = Depends(get_db)):
    """
    Retourne les élèves n'ayant pas payé ou partiellement payé une nature donnée
    """
    all_students = db.query(models.Student).all()

    # Paiements de cette nature
    paiements = db.query(models.Paiement).filter(models.Paiement.nature == nature).all()

    ids_paiement_partiel = [p.student_id for p in paiements if p.reste > 0]
    ids_paiement_total = [p.student_id for p in paiements if p.reste == 0]

    # Élèves sans paiement du tout
    ids_avec_paiement = set(p.student_id for p in paiements)
    ids_sans_paiement = [s.id for s in all_students if s.id not in ids_avec_paiement]

    # Résultat = partiels + sans paiement
    ids_concernes = set(ids_paiement_partiel + ids_sans_paiement)

    return db.query(models.Student).filter(models.Student.id.in_(ids_concernes)).all()

# ➤ Récupérer un élève par ID
@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    return student

# ➤ Modifier un élève
@router.put("/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, updated: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    
    for key, value in updated.dict().items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return student

# ➤ Supprimer un élève
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    
    db.delete(student)
    db.commit()
    return {"message": "Élève supprimé"}

@router.get("/{student_id}/photo-url")
def get_student_photo_url(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Élève introuvable")
    
    return {"photo_url": student.photo_url}

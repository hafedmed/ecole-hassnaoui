from pydantic import BaseModel, EmailStr
from datetime import date
from pydantic import BaseModel
from datetime import date
from typing import Optional

# --- User ---
class UserBase(BaseModel):
    email: EmailStr
    role: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True


# --- Student ---
class StudentBase(BaseModel):
    code_massar: str
    nom: str
    prenom: str
    date_naissance: date
    nom_parent1: str | None = None
    tel_parent1: str | None = None
    nom_parent2: str | None = None
    tel_parent2: str | None = None
    email: str | None = None
    status: str = "actif"
    photo_url: str | None = None

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    photo_url: Optional[str] = None
    class Config:
        orm_mode = True


# --- Class ---
class ClassBase(BaseModel):
    name: str

class ClassCreate(ClassBase):
    pass

class ClassOut(ClassBase):
    id: int
    class Config:
        orm_mode = True


# --- Inscription ---
class InscriptionBase(BaseModel):
    student_id: int
    class_id: int
    frais_inscription: float
    frais_scolarite: float
    date_inscription: date

class InscriptionCreate(InscriptionBase):
    pass

class InscriptionOut(InscriptionBase):
    id: int
    class Config:
        orm_mode = True
# --- Paiement ---
class PaiementBase(BaseModel):
    student_id: int
    nature: str
    avance: float
    reste: float
    date_paiement:date

class PaiementCreate(PaiementBase):
    pass

class PaiementOut(PaiementBase):
    id: int
    class Config:
        orm_mode = True

class PaiementUpdate(BaseModel):
    student_id: int | None = None
    nature: str | None = None
    avance: float | None = None
    reste: float | None = None
    date_paiement:date| None = None




class AbsenceBase(BaseModel):
    student_id: int
    date: date
    heure: Optional[str] = None
    motif: Optional[str] = None
    justifiee: bool = False

class AbsenceCreate(AbsenceBase):
    pass

class AbsenceUpdate(AbsenceBase):
    pass

class AbsenceOut(AbsenceBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: int

class LoginData(BaseModel):
    email: str
    password: str
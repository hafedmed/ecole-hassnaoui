from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float,Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "admin", "secretaire"

class Absence(Base):
    __tablename__ = "absences"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    heure = Column(String, nullable=True)  # "Matin", "Après-midi", "Toute la journée"
    motif = Column(String, nullable=True)  # ex: "Maladie", "Non justifiée"
    justifiee = Column(Boolean, default=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    code_massar = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    date_naissance = Column(Date, nullable=False)
    nom_parent1 = Column(String, nullable=True)
    tel_parent1 = Column(String, nullable=True)
    nom_parent2 = Column(String, nullable=True)
    tel_parent2 = Column(String, nullable=True)
    email = Column(String, nullable=True)
    status = Column(String, default="actif")
    photo_url = Column(String, nullable=True) 

    inscriptions = relationship("Inscription", back_populates="student")
    paiements = relationship("Paiement", back_populates="student")


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    inscriptions = relationship("Inscription", back_populates="classe")


class Inscription(Base):
    __tablename__ = "inscriptions"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    frais_inscription = Column(Float, nullable=False, default=0.0)
    frais_scolarite = Column(Float, nullable=False, default=0.0)
    date_inscription = Column(Date, nullable=False, default=date.today)

    student = relationship("Student", back_populates="inscriptions")
    classe = relationship("Class", back_populates="inscriptions")

class Paiement(Base):
    __tablename__ = "paiements"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    nature = Column(String, nullable=False)  # "inscription", "mois_septembre", etc.
    avance = Column(Float, nullable=False, default=0.0)
    reste = Column(Float, nullable=False, default=0.0)
    date_paiement = Column(Date, nullable=False, default=date.today)

    student = relationship("Student", back_populates="paiements")
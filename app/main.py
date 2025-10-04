from fastapi import FastAPI
from app.database import Base, engine
from app.routers import students, users, classes, inscriptions, paiements,absence,auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gestion École")
# Origines autorisées (ici ton Angular local)
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Les URL autorisées
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE...
    allow_headers=["*"],         # Autoriser tous les headers
)

# Servir le dossier photos
app.mount("/photos", StaticFiles(directory="photos"), name="photos")
# Inclure les routes
app.include_router(users.router)
app.include_router(students.router)
app.include_router(classes.router)
app.include_router(inscriptions.router)
app.include_router(paiements.router)
app.include_router(absence.router)
app.include_router(auth.router)

app.mount("/photos", StaticFiles(directory="photos"), name="photos")


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.database as database
from app.routes import auth, users, properties, payments, admin

# ==========================
# CREATE TABLES
# ==========================
database.Base.metadata.create_all(bind=database.engine)

# ==========================
# APP INSTANCE
# ==========================
app = FastAPI(
    title="M-IMMO Backend",
    version="1.0.0",
    description="API officielle de la plateforme M-IMMO"
)

# ==========================
# CORS CONFIGURATION
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production → mettre ton domaine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# ROUTES
# ==========================
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(properties.router)
app.include_router(payments.router)
app.include_router(admin.router)

# ==========================
# HEALTH CHECK
# ==========================
@app.get("/health")
def health_check():
    return {"status": "OK"}

# ==========================
# ROOT
# ==========================
@app.get("/")
def root():
    return {
        "message": "M-IMMO API Running 🚀",
        "status": "OK"
    }
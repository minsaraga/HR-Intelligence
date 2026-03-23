from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, employees, cv, certifications, recommendations, search
from app.db.session import Base, engine, SessionLocal
from app.db.seed import seed_db

app = FastAPI(title="AI HR Talent Intelligence API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    seed_db(db)

app.include_router(health.router, tags=["health"])
app.include_router(search.router, tags=["search"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(cv.router, prefix="/employees", tags=["cv"])
app.include_router(certifications.router, tags=["certifications"])
app.include_router(recommendations.router, prefix="/employees", tags=["recommendations"])

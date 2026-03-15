from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import alumni
from routers import jobs
from routers import events
from routers import chat
from routers import resume
from routers import auth
from routers import admin
from routers import graph


# ✅ FIRST create app
app = FastAPI(title="AlumniSphere Industry API")

# ✅ THEN add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ database
Base.metadata.create_all(bind=engine)

# ✅ routers
app.include_router(chat.router)

# Mentor recommender is now integrated into the chatbot, so we don't need a separate route for it.
app.include_router(resume.router)

# We can keep the alumni, jobs, and events routes for basic CRUD operations.
app.include_router(alumni.router)
app.include_router(jobs.router)
app.include_router(events.router)

# Authentication routes
app.include_router(auth.router)

# Admin dashboard routes
app.include_router(admin.router)

# Graph routes
app.include_router(graph.router)


@app.get("/")
def root():
    return {"message": "AlumniSphere API running 🚀"}
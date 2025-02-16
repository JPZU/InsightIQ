from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database.session import SessionLocal  # Import your SessionLocal
from .api.endpoints import auth, users

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# include the other routes
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to SoftServeAnalytics API"}
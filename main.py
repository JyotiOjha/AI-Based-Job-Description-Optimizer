from fastapi import FastAPI
from app.api.v1.endpoints import jd

app = FastAPI(title="JD Optimizer")

from fastapi.middleware.cors import CORSMiddleware



# ✅ ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # allow OPTIONS, POST, GET
    allow_headers=["*"],
)
app.include_router(jd.router, prefix="/api/v1/jd", tags=["JD"])

@app.get("/")
def root():
    return {"message": "Running with Groq 🚀"}
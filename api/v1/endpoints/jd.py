from fastapi import APIRouter
from app.services.jd_service import test_llm

router = APIRouter()

@router.get("/test")
def test():
    result = test_llm()
    return {"response": result}

from app.models.jd_model import JDRequest
from app.services.jd_service import generate_jd
from fastapi import APIRouter
from app.services.jd_service import rescore_jd

router = APIRouter()

@router.post("/rescore")
def rescore(data: dict):
    return rescore_jd(data)
@router.post("/generate")
def generate(data: JDRequest):
    return generate_jd(data)

from app.services.rag_service import get_skill_gaps

@router.post("/skill-gap")
def skill_gap(data: dict):
    jd_text = " ".join([
        data.get("summary", ""),
        " ".join(data.get("requirements", [])),
        " ".join(data.get("responsibilities", []))
    ])
    return get_skill_gaps(jd_text)
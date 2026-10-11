from groq import Groq
from app.core.config import GROQ_API_KEY
from app.services.rag_service import search_jd, add_jd

import json
import re

client = Groq(api_key=GROQ_API_KEY)


# ✅ TEST FUNCTION
def test_llm():
    try:
        models_response = client.models.list()
        available_models = [m.id for m in models_response.data]

        preferred_models = [
            "llama-3.2-11b-text-preview",
            "gemma2-9b-it"
        ]

        selected_model = next(
            (m for m in preferred_models if m in available_models),
            available_models[0]
        )

        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": "Say hello"}]
        )

        return {
            "model_used": selected_model,
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}


# ✅ SKILL ENHANCER
def enhance_skills(data, selected_model):
    try:
        prompt = f"""
You are a hiring expert.

Given a job role, suggest additional relevant and trending skills.

Return ONLY JSON:
{{
  "suggested_skills": ["skill1", "skill2", ...]
}}

Job Role:
Title: {data.title}
Current Skills: {", ".join(data.skills)}
Experience: {data.experience}
"""

        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        cleaned_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
        json_match = re.search(r"\{.*\}", cleaned_output, re.DOTALL)

        if json_match:
            return json.loads(json_match.group())
        else:
            return {"suggested_skills": []}

    except Exception as e:
        return {"suggested_skills": [], "error": str(e)}


# ✅ JD SCORER
def score_jd(jd_data, selected_model):
    try:
        prompt = f"""
You are an ATS (Applicant Tracking System) evaluator.

Analyze the given job description and return a structured evaluation.

Return ONLY JSON:
{{
  "score": 0-100,
  "ats_score": 0-100,
  "issues": ["..."],
  "improvements": ["..."]
}}

Job Description:
{json.dumps(jd_data)}
"""

        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        cleaned_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
        json_match = re.search(r"\{.*\}", cleaned_output, re.DOTALL)

        if json_match:
            return json.loads(json_match.group())
        else:
            return {"error": "Scoring failed"}

    except Exception as e:
        return {"error": str(e)}


# ✅ MAIN JD GENERATOR (WITH RAG)
def generate_jd(data):
    try:
        # 🔹 Get models
        models_response = client.models.list()
        available_models = [m.id for m in models_response.data]

        preferred_models = [
            "llama-3.2-11b-text-preview",
            "gemma2-9b-it"
        ]

        selected_model = next(
            (m for m in preferred_models if m in available_models),
            available_models[0]
        )

        # 🔥 Step 1: Enhance skills
        skill_data = enhance_skills(data, selected_model)
        enhanced_skills = list(set(data.skills + skill_data.get("suggested_skills", [])))

        # 🔥 Step 2: Retrieve similar JDs (RAG)
        query = f"{data.title} {' '.join(enhanced_skills)}"
        similar_jds_raw = search_jd(query)

# 🔥 Limit size of each JD
        similar_jds = [
    jd[:500]  # take only first 500 chars
    for jd in similar_jds_raw
]

        # 🔥 Step 3: Generate JD with context
        prompt = f"""
You are an expert HR assistant.

Use the provided similar job descriptions as reference to generate a better JD.

Return ONLY valid JSON.

Format:
{{
  "summary": "...",
  "responsibilities": ["..."],
  "requirements": ["..."],
  "nice_to_have": ["..."]
}}

Similar Job Descriptions (shortened):
{chr(10).join(similar_jds)}

Job Input:
Title: {data.title}
Experience: {data.experience}
Skills: {", ".join(enhanced_skills)}
Description: {data.description}
"""

        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        # 🔥 Clean output
        cleaned_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
        json_match = re.search(r"\{.*\}", cleaned_output, re.DOTALL)

        if not json_match:
            return {
                "error": "JSON extraction failed",
                "raw_output": raw_output
            }

        parsed_output = json.loads(json_match.group())

        # 🔥 Step 4: Store JD in RAG
        add_jd(json.dumps(parsed_output))

        # 🔥 Step 5: Score JD
        score_data = score_jd(parsed_output, selected_model)

        return {
            "model_used": selected_model,
            "enhanced_skills": enhanced_skills,
            "similar_jds_used": similar_jds,
            "generated_jd": parsed_output,
            "jd_score": score_data
        }

    except Exception as e:
        return {"error": str(e)}
    


def rescore_jd(data):
    try:
        # 🔹 Get models
        models_response = client.models.list()
        available_models = [m.id for m in models_response.data]

        preferred_models = [
            "llama-3.3-70b-versatile",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]

        selected_model = next(
            (m for m in preferred_models if m in available_models),
            available_models[0]
        )

        prompt = f"""
You are an ATS scoring system.

Evaluate the following job description and give a score out of 100.

Return ONLY JSON:
{{
  "ats_score": number,
  "feedback": ["improvement1", "improvement2"]
}}

Job Description:
Summary: {data.get("summary")}
Responsibilities: {data.get("responsibilities")}
Requirements: {data.get("requirements")}
Nice to Have: {data.get("nice_to_have")}
"""

        response = client.chat.completions.create(
            model=selected_model,
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        import re, json
        cleaned_output = re.sub(r"<think>.*?</think>", "", raw_output, flags=re.DOTALL)
        json_match = re.search(r"\{.*\}", cleaned_output, re.DOTALL)

        if json_match:
            parsed = json.loads(json_match.group())
            return {
                "model_used": selected_model,
                "ats_score": parsed.get("ats_score"),
                "feedback": parsed.get("feedback", [])
            }
        else:
            return {"error": "Parsing failed", "raw": raw_output}

    except Exception as e:
        return {"error": str(e)}
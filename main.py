from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import requests
import tempfile
from gemini_api import answer_questions_from_pdf

class QueryRequest(BaseModel):
    documents: str
    questions: list[str]

app = FastAPI()

@app.post("/api/v1/hackrx/run")
async def hackrx_run(payload: QueryRequest):
    try:
        pdf_url = payload.documents
        questions = payload.questions
        if not pdf_url or not questions:
            raise HTTPException(status_code=422, detail="Missing document URL or questions.")

        response = requests.get(pdf_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download PDF from provided URL.")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpfile:
            tmpfile.write(response.content)
            tmpfile_path = tmpfile.name

        answers = answer_questions_from_pdf(tmpfile_path, questions)
        return {"answers": answers}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
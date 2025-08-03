from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
import requests
import tempfile
import os
from gemini_api import answer_questions_from_pdf

app = FastAPI()

class QueryRequest(BaseModel):
    documents: HttpUrl
    questions: list[str]

@app.post("/api/v1/hackrx/run")
async def hackrx_run(payload: QueryRequest):
    try:
        pdf_url = str(payload.documents)
        questions = payload.questions
        if not pdf_url or not questions:
            raise HTTPException(status_code=422, detail="Missing document URL or questions.")

        # Download PDF
        resp = requests.get(pdf_url, timeout=25)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download PDF. Status {resp.status_code}")

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpfile:
            tmpfile.write(resp.content)
            tmpfile_path = tmpfile.name

        answers = answer_questions_from_pdf(tmpfile_path, questions)

        # Clean up
        try:
            os.unlink(tmpfile_path)
        except:
            pass

        return {"answers": answers}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

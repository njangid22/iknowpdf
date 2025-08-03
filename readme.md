# PDF-Ask-API (Gemini, In-Memory Vector Search, NO Pinecone)

## How it works

- Accepts PDF/DOCX URL and questions.
- Splits document, embeds with Gemini, stores vectors in memory (not Pinecone).
- Finds best-matching chunks for each question, answers with Gemini LLM.

## How to run

1. **Clone repo & install:**
    ```
    pip install -r requirements.txt
    ```

2. **Set your Gemini API key:**
   - In `app/retrieval.py`, replace `YOUR_GEMINI_API_KEY_HERE` with your real key.

3. **Run the server:**
    ```
    uvicorn app.main:app --reload
    ```

4. **POST to the API:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
      -H "Authorization: Bearer ef3dc931ae000ac130c46014463b1293c5ee653bced4ed8f3dd87e5af540a10d" \
      -H "Content-Type: application/json" \
      -d '{"documents": "<PDF_OR_DOCX_URL>", "questions": ["What is the grace period?", "Another Q?"]}'
    ```

## Notes
- **No Pinecone!** All vector search is in Python memory.
- For hackathons and demos, this is easy and deployable. For production/large docs, consider Pinecone or FAISS.
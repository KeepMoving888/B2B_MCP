# FastAPI接口
from fastapi import FastAPI, HTTPException
from .llm_client import generate_response

app = FastAPI()

@app.post("/inquiry")
async def handle_inquiry(inquiry: dict):
    try:
        response = generate_response(inquiry)
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

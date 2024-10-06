import uvicorn
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.aiservice.main.service import MessageService
from src.aiservice.main.utils import AILog
from src.aiservice.main.message import ExpenseProducer

load_dotenv()
msg = MessageService()
producer = ExpenseProducer()
ailog = AILog(name="main")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/v1/message")
async def message(request: Request):
    try:
        ailog.info("request to message endpoint")
        data = await request.json()
        data = data.get("message")
        result = msg.process(data)
        if result is None:
            return JSONResponse(content={"message": "Invalid Message"}, status_code=400)
        result = dict(result)
        result_json = json.dumps(result).encode('utf-8')

        ailog.info(f"Message: {result}")
        producer.produce(result_json)

        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        ailog.error(f"Error: {str(e)}")
        return JSONResponse(content={"message": "Message Service Down"}, status_code=500)


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "localhost")
    uvicorn.run(app, host=host, port=port)
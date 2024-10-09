import socket
import uvicorn
import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.aiservice.main.service import MessageService
from src.aiservice.main.utils import AILog
from src.aiservice.main.message import ExpenseProducer

load_dotenv()
msg = MessageService()

topic = os.getenv("KAFKA_TOPIC_NAME", "transaction")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS","localhost")
bootstrap_port = os.getenv("KAFKA_BOOTSTRAP_PORT", "9092")
conf = {
    'bootstrap.servers': bootstrap_servers + ":" + bootstrap_port,
    'client.id': socket.gethostname()
}

producer = ExpenseProducer(config=conf, topic=topic)
ailog = AILog(name="main")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/expense")

@router.get("")
async def root():
    return {"message": "Hello User"}

@router.post("/api/v1/message")
async def message(request: Request):
    try:
        # Extract the X-User-Id header from the request
        user_id = request.headers.get("X-User-Id")
        user_role = request.headers.get("X-User-Role")
        if user_id is None and user_role is None:
            return JSONResponse(content={"message": "Missing access rights"}, status_code=400)

        ailog.info("request to message endpoint by user: {x_user_id}")
        data = await request.json()
        data = data.get("message")
        result = msg.process(data)
        if result is None:
            return JSONResponse(content={"message": "Invalid Message"}, status_code=400)

        result = dict(result)
        result["user_id"] = user_id
        result_json = json.dumps(result).encode('utf-8')

        ailog.info(f"Message: {result}")
        producer.produce(result_json)

        return JSONResponse(content=result, status_code=200)

    except Exception as e:
        ailog.error(f"Error: {str(e)}")
        return JSONResponse(content={"message": "Message Service Down"}, status_code=500)

app.include_router(router)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 9040))
    host = os.getenv("HOST", "localhost")
    uvicorn.run(app, host=host, port=port)
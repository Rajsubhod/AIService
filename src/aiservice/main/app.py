import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from src.aiservice.main.service import MessageService
from src.aiservice.main import app_logger

load_dotenv()
app = FastAPI()

msg = MessageService()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/api/v1/message")
async def message(request: Request):
    try:
        data = await request.json()
        data = data.get("message")
        result = msg.process(data)
        result = dict(result)
        return JSONResponse(content=result, status_code=200)
        # return res
    except Exception as e:
        app_logger.error(f"Error: {str(e)}")
        return JSONResponse(content={"message": "Message Service Down"}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
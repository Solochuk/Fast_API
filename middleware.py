from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    method = request.method
    url = str(request.url)
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {method} {url}")

    if "X-Custom-Header" not in request.headers:
        return JSONResponse(
            status_code=400,
            content={"detail": "X-Custom-Header не знайдено!"}
        )

    response = await call_next(request)
    return response

@app.get("/")
async def read_root():
    return {"message": "Йоу!"}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
# from example import router as test_router
# from database import database
from feedback import feedback


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("서버 시작 중...")
    # 데이터베이스 연결
    # await database.connect()

    yield  # 서버가 실행되는 동안 여기서 대기

    # 서버가 종료될 때
    print("서버 종료 중...")
    # await database.disconnect()

app = FastAPI(lifespan=lifespan)

# CORS 설정 (필요한 경우)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(test_router.router, prefix="/test")
app.include_router(feedback.router, prefix="/feedback")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
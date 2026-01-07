from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.api.v1.health import router as health_router
from app.api.v1.packaging import router as packaging_router
from app.api.v1.images import router as images_router

app = FastAPI(title="AI Packaging SaaS")
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_origin_regex="https://.*\\.vercel\\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





app.include_router(health_router, prefix="/api/v1")
app.include_router(packaging_router, prefix="/api/v1")
app.include_router(images_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False
    )

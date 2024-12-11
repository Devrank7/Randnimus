import uvicorn
from fastapi import FastAPI
from fastapi_app.routers import start_router

app = FastAPI()
app.include_router(start_router.router, prefix="/profile", tags=["profile"])


@app.on_event("startup")
async def startup():
    print("startup")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1000)

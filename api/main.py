from fastapi import FastAPI
from api.router import router
app = FastAPI(
    title="Judgekit API",
    description="LLM Judget Agent",
    version="0.1.0",
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=4200, reload=True)
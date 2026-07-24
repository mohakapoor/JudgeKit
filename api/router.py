from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os 
from dotenv import load_dotenv
from config import MODEL_NAME
from src.utils import random_ques_loader, EvalInput, RetrievalMetrics, GenerationMetrics, EvalOutput
from src.agents import retrieval_eval_agent, generation_eval_agent
from src.prompt_builder import build_retrieval_prompt, build_generation_prompt
from src.deterministic import calc_metrics
from src.orchestrator import orchestrator
from dataclasses import asdict

load_dotenv()
API_TOKEN = os.getenv("TOKEN")
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

router = APIRouter()

@router.get("/health", tags=["System"])
async def health():
    return {"status": "200"}


@router.get("/status", tags=["System"],dependencies=[Depends(verify_token)])
async def status_check(request: Request):
    return{
        "title" : "JudgeKit",
        "model" : MODEL_NAME,
        "version":request.app.version
    }

@router.get("/get_input", tags=["Test"],dependencies=[Depends(verify_token)])
async def get_inputs():
    return asdict(random_ques_loader())
    
@router.post("/judge_retrieval", tags=["Eval"], dependencies=[Depends(verify_token)])
async def judge_retrieval(payload: EvalInput):
    r_prompt = build_retrieval_prompt(payload)
    result = retrieval_eval_agent(r_prompt)
    return asdict(result)
    
@router.post("/judge_generation", tags=["Eval"], dependencies=[Depends(verify_token)])
async def judge_generation(payload: EvalInput):
    g_prompt = build_generation_prompt(payload)
    result = generation_eval_agent(g_prompt)
    return asdict(result)

@router.post("/judge_deterministic", tags=["Eval"], dependencies=[Depends(verify_token)])
async def judge_deterministic(payload: EvalInput):
    h, mrr = calc_metrics(payload)
    return {"hit_at_k": h, "mrr": mrr}

@router.post("/judge_all", tags=["Eval"], dependencies=[Depends(verify_token)])
async def judge_all(payload: EvalInput):
    result = orchestrator(payload)
    return asdict(result)
from fastapi import APIRouter,HTTPException,Request,Depends,status
import os 
from config import MODEL_NAME
from src.utils import random_ques_loader, RetrievalInput, GenerationInput
from src.agent import eval_retrieval,eval_generation
from dataclasses import asdict


router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "200"}


@router.get("/status")
async def status_check(request: Request):
    return{
        "title" : "JudgeKit",
        "model" : MODEL_NAME,
        "version":request.app.version
    }

@router.get("/input")
async def get_inputs():
    r_res, g_res = random_ques_loader()
    return {
        "retrieval_input": asdict(r_res),
        "generation_input": asdict(g_res)
    }

@router.post("/eval_retrieval")
async def api_eval_retrieval(payload: RetrievalInput):
    result = eval_retrieval(payload)
    return asdict(result)
    
@router.post("/eval_generation")
async def api_eval_generation(payload: GenerationInput):
    result = eval_generation(payload)
    return asdict(result)
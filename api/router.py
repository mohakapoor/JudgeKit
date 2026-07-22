from fastapi import APIRouter,HTTPException,Request,Depends,status
import os 
from config import MODEL_NAME
from src.utils import random_ques_loader
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


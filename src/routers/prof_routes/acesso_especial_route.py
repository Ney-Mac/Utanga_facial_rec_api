from fastapi import APIRouter, HTTPException, responses, Depends
from sqlalchemy.orm import Session

from src.core.database import get_db


router = APIRouter(prefix="/autorizar-acesso")


@router.post('/')
async def autorizar_acesso():
    return
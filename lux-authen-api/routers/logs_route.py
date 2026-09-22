from fastapi import APIRouter
from fastapi.responses import Response
from config import settings
from collections import deque
router = APIRouter()


@router.get("/app/{code}", include_in_schema=False)
async def st(code: str, limit:int = 1000):
    if code == settings.CODE_CONFIRM:
        try:
            with open("logs/app.log", "r", encoding="utf-8") as f:
                last_lines = deque(f, int(limit)) 
            return Response(content="".join(last_lines), media_type="text/plain")
        except FileNotFoundError:
            return Response(content="Log file not found.", media_type="text/plain", status_code=404)


@router.get("/classify/{code}", include_in_schema=False)
async def st(code: str, limit:int = 1000):
    if code == settings.CODE_CONFIRM:
        try:
            with open("logs/model_results.log", "r", encoding="utf-8") as f:
                last_lines = deque(f, int(limit)) 
            return Response(content="".join(last_lines), media_type="text/plain")
        except FileNotFoundError:
            return Response(content="Log file not found.", media_type="text/plain", status_code=404)

@router.get("/request/{code}", include_in_schema=False)
async def st(code: str, limit:int = 1000):
    if code == settings.CODE_CONFIRM:
        try:
            with open("logs/request.log", "r", encoding="utf-8") as f:
                last_lines = deque(f, int(limit)) 
            return Response(content="".join(last_lines), media_type="text/plain")
        except FileNotFoundError:
            return Response(content="Log file not found.", media_type="text/plain", status_code=404)

@router.get("/model_results/{code}", include_in_schema=False)
async def st(code: str, limit:int = 1000):
    if code == settings.CODE_CONFIRM:
        try:
            with open("logs/model_results.log", "r", encoding="utf-8") as f:
                last_lines = deque(f, int(limit)) 
            return Response(content="".join(last_lines), media_type="text/plain")
        except FileNotFoundError:
            return Response(content="Log file not found.", media_type="text/plain", status_code=404)

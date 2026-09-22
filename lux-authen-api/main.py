"""
Lux Authentication API
Main application entry point
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.responses import JSONResponse
import uvicorn
from config import settings
from core.logging import APP_LOGGER, MODEL_RESULTS_LOGGER, REQUEST_LOGGER
from starlette.middleware.base import BaseHTTPMiddleware
import time
from routers.utils import get_system_info

# Import các routers cốt lõi đã được tinh gọn
from routers import classify, logs_route
from routers import check_part

APP_LOGGER.info("start api")
MODEL_RESULTS_LOGGER.info("start model results logger")
REQUEST_LOGGER.info("start request logger")


class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Get client IP address
        client_ip = request.headers.get("x-forwarded-for", request.client.host)

        # Create id
        request_id = str(round(time.time() * 1000))
        request.state.request_id = request_id

        # next request
        response = await call_next(request)

        # process time
        process_time = (time.time() - start_time)

        rq_path = request.url.path + "?" + (request.url.query or "")
        # Log chỉ cho các endpoint đang hoạt động
        if request.url.path.startswith(("/classify", "/logs")):
            REQUEST_LOGGER.info(f"ID: {request_id} - {response.status_code} - {client_ip} - {rq_path} - {process_time:.8f}")
        return response

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(LogRequestMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)


# Lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    print("\n" + "="*60)
    print(f"🚀 {settings.app_name} Starting...")
    print("="*60)
    
    print("\n" + "="*60)
    print("✨ API is ready to accept requests!")
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    print(f"\n👋 Shutting down {settings.app_name}...")


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - Redirect to documentation
    """
    return RedirectResponse(url="/docs/")


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "message": f"{settings.app_name} is running",
            "version": settings.app_version
        }
    )

@app.get("/ssi/{code}")
def system_info(code):
    if code == settings.CODE_CONFIRM:
        return get_system_info()
    else: return {"st": "error code"}


# Đăng ký các routers chính thức được giữ lại
app.include_router(
    classify.router,
    prefix="/classify",
    tags=["Classify"]
)

app.include_router(
    logs_route.router,
    prefix="/logs",
    tags=["Logs"]
)
app.include_router(check_part.router, prefix="", tags=["Authentication"])

# Run with uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.reload,
        log_level="info"
    )
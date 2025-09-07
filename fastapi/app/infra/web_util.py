import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse 
from app.infra.request_trace_middleware import RequestTracerMiddleware 

from app.routes.auth_routes import router as auth_router
from app.routes.settings_routes import router as settings_router

from app.routes.dag_routes import router as dag_router 
from app.routes.questions_routes import router as questions_router 
from app.routes.student_routes import router as students_router 
from app.routes.data_routes import router as data_router 
from app.routes.files_routes import router as files_router 

from app.infra.response_handlers import (
    AppBaseException,
    BadRequestException,
    ForbiddenException,
    InvalidCredentialsException, 
    ResourceNotFoundException,
    UnauthorizedException,
    bad_request_exception_handler,
    forbidden_exception_handler, 
    generic_exception_handler, 
    invalid_credentials_exception_handler, 
    resource_not_found_exception_handler,
    unauthorized_exception_handler
)

from fastapi.middleware.cors import CORSMiddleware


class WebUtil:
    @staticmethod
    def setup_logging(log_dir="logs", time_based: bool = False):
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "app.log")

        # Select the appropriate handler
        if time_based:
            handler = TimedRotatingFileHandler(
                log_file, when="midnight", interval=1, backupCount=7, encoding="utf-8", utc=True
            )
            handler.suffix = "%Y-%m-%d"
        else:
            handler = RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
            )

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)

        # Avoid adding multiple handlers on reload (e.g. during tests or dev hot reload)
        root_logger = logging.getLogger()
        if not root_logger.handlers:
            root_logger.setLevel(logging.INFO)
            root_logger.addHandler(handler)
    
    @staticmethod
    def register_middlewares(app: FastAPI): 
        if not any(isinstance(m, RequestTracerMiddleware) for m in app.user_middleware):
            app.add_middleware(RequestTracerMiddleware)
        
    
    @staticmethod
    def register_exceptionhandlers(app: FastAPI):
        handlers = {
            UnauthorizedException: unauthorized_exception_handler,
            ForbiddenException: forbidden_exception_handler,
            BadRequestException: bad_request_exception_handler,
            InvalidCredentialsException: invalid_credentials_exception_handler,
            ResourceNotFoundException: resource_not_found_exception_handler,
            AppBaseException: generic_exception_handler,
        }

        for exc, handler in handlers.items():
            app.add_exception_handler(exc, handler)

        @app.exception_handler(Exception)
        async def catch_all_exceptions(request: Request, exc: Exception):
            logger = logging.getLogger(__name__)
            logger.exception("Unexpected error")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )
    
    # @staticmethod
    # def register_exceptionhandlers(app:FastAPI):    
    #     app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)
    #     app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
    #     app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    #     app.add_exception_handler(InvalidCredentialsException, invalid_credentials_exception_handler)
    #     app.add_exception_handler(ResourceNotFoundException, resource_not_found_exception_handler)
    #     app.add_exception_handler(AppBaseException, generic_exception_handler)
        
    @staticmethod
    def register_routers(app:FastAPI):
        app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
        app.include_router(settings_router, prefix="/settings", tags=["Settings"])
        app.include_router(dag_router, prefix="/dags", tags=["DAGs"]) 
        app.include_router(questions_router, prefix="/questions", tags=["Questions"]) 
        app.include_router(students_router, prefix="/students", tags=["Students"])  
        app.include_router(data_router, prefix="/data", tags=["Data"])  
        app.include_router(files_router, prefix="/files", tags=["Data"]) 

    @staticmethod
    def configure_cors(app:FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Replace with specific origins in production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ) 

    # from fastapi import APIRouter, UploadFile, File
    # from fastapi.responses import FileResponse
    # import os
    # import shutil

    # router = APIRouter()
    # UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
    # os.makedirs(UPLOAD_DIR, exist_ok=True)

    # @router.post("/upload")
    # async def upload_file(file: UploadFile = File(...)):
    #     file_path = os.path.join(UPLOAD_DIR, file.filename)
    #     with open(file_path, "wb") as buffer:
    #         shutil.copyfileobj(file.file, buffer)
    #     return {"filename": file.filename}

    # @router.get("/download/{filename}")
    # async def download_file(filename: str):
    #     file_path = os.path.join(UPLOAD_DIR, filename)
    #     if os.path.exists(file_path):
    #         return FileResponse(path=file_path, filename=filename)
    #     return {"error": "File not found"}

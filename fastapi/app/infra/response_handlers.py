import inspect
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR, 
    HTTP_401_UNAUTHORIZED, 
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST, 
    HTTP_404_NOT_FOUND
)
import logging

class ResponseBuilder:
    @staticmethod
    def Ok(data: dict, status_code: int = 200, success: bool = True, is_list:bool =False, message: str = ""): 
        return {
            "status": status_code,
            "success": success,
            "message": message,
            "isList":is_list,
            "data": data
        } 

class AppBaseResponse(JSONResponse):
    def __init__(self, data: dict = None, status_code: int = HTTP_200_OK, 
                 success: bool = True, is_list:bool =False, message: str = ""):
        content = {
            "success": success,
            "message": message,
            "isList":is_list,
            "data": data or {}
        }
        super().__init__(content=content, status_code=status_code)

class OkResponse(AppBaseResponse):
    def __init__(self, data: dict = None, message: str = "Data read successfully"):
        super().__init__(data=data, status_code=HTTP_200_OK, success=True, message=message)

class OkListResponse(AppBaseResponse):
    def __init__(self, data: dict = None, message: str = "Data read successfully"):
        super().__init__(data=data, status_code=HTTP_200_OK, success=True,is_list=True, message=message)

class CreatedResponse(AppBaseResponse):
    def __init__(self, data: dict = None, message: str = "Resource created successfully"):
        super().__init__(data=data, status_code=HTTP_201_CREATED, success=True, message=message)

class NoContentResponse(AppBaseResponse):
    def __init__(self, data: dict = None, message: str = ""):
        super().__init__(data=data, status_code=HTTP_204_NO_CONTENT, success=True, message=message)

class AppBaseException(Exception):
    def __init__(self, message: str, logger_name: str = None):
        if not logger_name:
            frame = inspect.stack()[1]
            logger_name = frame.frame.f_globals["__name__"]
        self.message = message
        self.logger_name = logger_name
        super().__init__(self.message)

class UnauthorizedException(AppBaseException):
    pass

class ForbiddenException(AppBaseException):
    pass

class InvalidCredentialsException(AppBaseException):
    def __init__(self, message: str = "Invalid username or password"):
        super().__init__(message)


class ResourceNotFoundException(AppBaseException):
    pass 

class BadRequestException(AppBaseException):
    pass

async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    logger = logging.getLogger(exc.logger_name)
    logger.warning(f"[{request.method}] {request.url} -> {exc.message}")
    return JSONResponse(status_code=401, content={"detail": exc.message})
 
async def resource_not_found_exception_handler(request: Request, exc: ResourceNotFoundException):
    logger = logging.getLogger(exc.logger_name)
    logger.info(f"[{request.method}] {request.url} -> {exc.message}")
    return JSONResponse(
        status_code=HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    logger = logging.getLogger(exc.logger_name)
    logger.warning(f"[{request.method}] {request.url} -> {exc.message}")
    return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"detail": exc.message})

async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    logger = logging.getLogger(exc.logger_name)
    logger.warning(f"[{request.method}] {request.url} -> {exc.message}")
    return JSONResponse(status_code=HTTP_403_FORBIDDEN, content={"detail": exc.message})
    
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    logger = logging.getLogger(exc.logger_name)
    logger.warning(f"[{request.method}] {request.url} -> {exc.message}")
    return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"detail": exc.message})


async def generic_exception_handler(request: Request, exc: AppBaseException):
    logger = logging.getLogger(exc.logger_name)
    logger.error(f"Unhandled error on {request.method} {request.url} -> {repr(exc)}", exc_info=True)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )
import logging
import os
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter() 

FILES_DIR = "static/files"

@router.get("/{file_name}")
def get_file(file_name: str):
    """
    Serve a DAG image by file name.
    """
    file_path = os.path.join(FILES_DIR, file_name)

    # Security check: ensure file is inside the allowed folder
    if not os.path.abspath(file_path).startswith(os.path.abspath(FILES_DIR)):
        raise HTTPException(status_code=403, detail="Access denied")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)



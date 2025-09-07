import logging
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.infra.database import get_db
from app.schemas.dag_schemas import DAGBase, DAGOut, DAGEdgeBase, DAGEdgeOut
from app.services.dag_service import DAGService
from app.infra.response_handlers import BadRequestException, ResourceNotFoundException

logger = logging.getLogger(__name__)
router = APIRouter()


# DAG CRUD
@router.post(
    "/",
    summary="Create a new DAG",
    response_model=DAGOut,
)
def create_dag(dag_data: DAGBase = Body(...), db: Session = Depends(get_db)):
    try:
        return DAGService.create_dag(dag_data, db, logger)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/{dag_id}",
    summary="Get DAG by ID",
    response_model=DAGOut,
)
def get_dag(dag_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    try:
        return DAGService.get_dag(dag_id, db, logger)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{dag_id}",
    summary="Update DAG by ID",
    response_model=DAGOut,
)
def update_dag(dag_id: int = Path(..., gt=0), dag_data: DAGBase = Body(...), db: Session = Depends(get_db)):
    try:
        return DAGService.update_dag(dag_id, dag_data, db, logger)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{dag_id}",
    summary="Delete DAG by ID",
)
def delete_dag(dag_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    try:
        return DAGService.delete_dag(dag_id, db, logger)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/",
    summary="List all DAGs",
)
def list_dags(db: Session = Depends(get_db)):
    return DAGService.list_dags(db, logger)


# DAG Edge CRUD
@router.post(
    "/edges/",
    summary="Add a DAG edge",
    response_model=DAGEdgeOut,
)
def add_edge(edge_data: DAGEdgeBase = Body(...), db: Session = Depends(get_db)):
    try:
        return DAGService.add_edge(edge_data, db, logger)
    except (BadRequestException, ResourceNotFoundException) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/edges/{edge_id}",
    summary="Remove DAG edge by ID",
)
def remove_edge(edge_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    try:
        return DAGService.remove_edge(edge_id, db, logger)
    except ResourceNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))



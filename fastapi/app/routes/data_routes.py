import base64
import json
import logging
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.models import model_registry  # dict: { 'users': UserModel, 'posts': PostModel }


from app.infra.database import get_db
from app.schemas.dag_schemas import DAGBase, DAGOut, DAGEdgeBase, DAGEdgeOut
from app.services.dag_service import DAGService
from app.infra.response_handlers import BadRequestException, ResourceNotFoundException
from app.services.dispatcher import Dispatcher

logger = logging.getLogger(__name__)
router = APIRouter()

def decode_base64_json(data_b64: str) -> dict:
    try:
        decoded = base64.b64decode(data_b64).decode("utf-8")
        return json.loads(decoded)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid base64 JSON: {str(e)}")


@router.get("/getone/{slug}/{id}")
def get_one(slug: str, id: int, db: Session = Depends(get_db)) -> Any:
    Model = model_registry.get(slug)
    if not Model:
        raise HTTPException(status_code=404, detail="Unknown slug")
    item = db.query(Model).get(id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return {
        "success": True,
        "data": item
    }


@router.get("/getall/{slug}")
def get_all(slug: str, db: Session = Depends(get_db)) -> Any:
    Model = model_registry.get(slug)
    if not Model:
        raise HTTPException(status_code=404, detail="Unknown slug")
    items= db.query(Model).all()
    return {
        "success": True,
        "data": items
    }


@router.get("/getmany/{slug}")
def get_many(slug: str, Data: str, db: Session = Depends(get_db)):
    Model = model_registry.get(slug)
    if not Model:
        raise HTTPException(status_code=404, detail="Unknown slug")
    filters = decode_base64_json(Data)
    query = db.query(Model)
    for key, value in filters.items():
        if hasattr(Model, key):
            query = query.filter(getattr(Model, key) == value) 
    items= query.all()
    return {
        "success": True,
        "data": items
    }


@router.post("/save/{slug}")
def save(slug: str, payload: dict, db: Session = Depends(get_db)):
    Model = model_registry.get(slug)
    if not Model:
        raise HTTPException(status_code=404, detail="Unknown slug")

    data = decode_base64_json(payload["Data"])
    if "id" in data and data["id"]:
        obj = db.query(Model).get(data["id"])
        if not obj:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in data.items():
            setattr(obj, key, value)
    else:
        obj = Model(**data)
        db.add(obj)

    db.commit()
    db.refresh(obj)
    return {
        "success": True,
        "data": obj
    }


@router.post("/remove/{slug}/{id}")
def remove(slug: str, id: int, payload: dict, db: Session = Depends(get_db)):
    Model = model_registry.get(slug)
    if not Model:
        raise HTTPException(status_code=404, detail="Unknown slug")
    obj = db.query(Model).get(id)
    if not obj:
        raise HTTPException(status_code=404, detail="Item not found")

    data = decode_base64_json(payload["Data"])
    success=False

    if(obj.id==id):
        db.delete(obj)
        db.commit()
        success=True
    # if "status" in data:
    #     obj.status = data["status"]
    # else:
    #     db.delete(obj)

    # db.commit()
    return {"success": success}


@router.post("/process/{slug}")
def process(slug: str, payload: dict, db: Session = Depends(get_db)): 
    data = decode_base64_json(payload["Data"]) 
    obj=Dispatcher.dispatch(data,slug,db)
    return {
        "success": True,
        "data": obj
    }

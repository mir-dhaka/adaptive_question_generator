from typing import TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session

Entity = TypeVar("Entity")
Schema = TypeVar("Schema")

class SqlAlchemyGenericRepository:
    def __init__(self, session: Session, db_model: Type[Entity], schema_model: Type[Schema]):
        self.session = session
        self.db_model = db_model
        self.schema_model = schema_model

    def get_by_id(self, entity_id: int) -> Optional[Schema]:
        entity_db = self.session.get(self.db_model, entity_id)
        return self.schema_model.from_orm(entity_db) if entity_db else None

    def add(self, entity: Schema, commit: bool = True) -> Schema:
        entity_db = self.db_model(**entity.dict())
        self.session.add(entity_db)
        if commit and self.session.is_active:
            self.session.commit()
            self.session.refresh(entity_db)
        return self.schema_model.from_orm(entity_db)

    def list_all(self) -> List[Schema]:
        entities_db = self.session.query(self.db_model).all()
        return [self.schema_model.from_orm(e) for e in entities_db]

    def list_paginated(self, skip: int = 0, limit: int = 10) -> List[Schema]:
        query = self.session.query(self.db_model).offset(skip).limit(limit)
        return [self.schema_model.from_orm(e) for e in query]

    def filter(self, filters: Dict[str, Any]) -> List[Schema]:
        query = self.session.query(self.db_model)
        for attr, value in filters.items():
            if hasattr(self.db_model, attr):
                query = query.filter(getattr(self.db_model, attr) == value)
        entities_db = query.all()
        return [self.schema_model.from_orm(e) for e in entities_db]

    def update(self, entity: Schema, commit: bool = True) -> Optional[Schema]:
        entity_db = self.session.get(self.db_model, entity.id)
        if not entity_db:
            return None
        for key, value in entity.dict().items():
            setattr(entity_db, key, value)
        if commit and self.session.is_active:
            self.session.commit()
            self.session.refresh(entity_db)
        return self.schema_model.from_orm(entity_db)

    def delete(self, entity_id: int, commit: bool = True) -> bool:
        entity_db = self.session.get(self.db_model, entity_id)
        if not entity_db:
            return False
        self.session.delete(entity_db)
        if commit and self.session.is_active:
            self.session.commit()
        return True

    def count(self) -> int:
        return self.session.query(self.db_model).count()

    def get_repo(self, db_model: Type[Entity], schema_model: Type[Schema]) -> "SqlAlchemyGenericRepository":
        return SqlAlchemyGenericRepository(self.session, db_model=db_model, schema_model=schema_model)

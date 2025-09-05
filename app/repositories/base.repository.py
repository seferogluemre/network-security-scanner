from typing import List, Optional, Dict, Any, Type, TypeVar
from sqlalchemy.orm import Query
from app.config.database import db
from app.models.base import BaseModel

ModelType = TypeVar('ModelType', bound=BaseModel)

class BaseRepository:
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.session = db.session
    
    def create(self, **kwargs) -> ModelType:
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            self.session.commit()
            return instance
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_by_id(self, record_id: int) -> Optional[ModelType]:
        return self.session.query(self.model).filter(
            self.model.id == record_id,
            self.model.is_active == True
        ).first()
    
    def get_all(self, active_only: bool = True) -> List[ModelType]:
        """Get all records"""
        query = self.session.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.all()
    
    def get_by_filter(self, **filters) -> List[ModelType]:
        """Get records by filters"""
        query = self.session.query(self.model).filter(self.model.is_active == True)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.all()
    
    def get_one_by_filter(self, **filters) -> Optional[ModelType]:
        """Get one record by filters"""
        query = self.session.query(self.model).filter(self.model.is_active == True)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first()
    
    def update(self, record_id: int, **updates) -> Optional[ModelType]:
        try:
            instance = self.get_by_id(record_id)
            if not instance:
                return None
            
            for key, value in updates.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            self.session.commit()
            return instance
        except Exception as e:
            self.session.rollback()
            raise e
    
    def delete(self, record_id: int, soft_delete: bool = True) -> bool:
        try:
            instance = self.get_by_id(record_id)
            if not instance:
                return False
            
            if soft_delete:
                instance.is_active = False
            else:
                self.session.delete(instance)
            
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e
    
    def count(self, active_only: bool = True) -> int:
        query = self.session.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        return query.count()
    
    def paginate(self, page: int = 1, per_page: int = 10, active_only: bool = True) -> Dict[str, Any]:
        query = self.session.query(self.model)
        if active_only:
            query = query.filter(self.model.is_active == True)
        
        total = query.count()
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1
        }
    
    def bulk_create(self, data_list: List[Dict[str, Any]]) -> List[ModelType]:
        try:
            instances = [self.model(**data) for data in data_list]
            self.session.add_all(instances)
            self.session.commit()
            return instances
        except Exception as e:
            self.session.rollback()
            raise e
    
    def exists(self, **filters) -> bool:
        query = self.session.query(self.model).filter(self.model.is_active == True)
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None
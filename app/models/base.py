from ast import Return
from datetime import datetime
from app.config.database import db


class BaseModel(db.Model):
    __abstract__=True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            return False

    
    def delete(self):
        self.is_active=False
        return self.save()


    def hard_delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"
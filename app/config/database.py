from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db=SQLAlchemy()
migrate = Migrate()

def init_database(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.models.base import BaseModel
    from app.models.host import Host
    from app.models.scan import Scan
    from app.models.user import User
    
    with app.app_context():
        try:
            db.create_all()
            print("🗄️  Database tables created successfully!")
        except Exception as e:
            print(f"❌ Database creation error: {e}")


class DatabaseManager:
    """Database operations manager"""
    
    @staticmethod
    def create_all():
        """Create all database tables"""
        db.create_all()
    
    @staticmethod
    def drop_all():
        """Drop all database tables"""
        db.drop_all()
    
    @staticmethod
    def reset_database():
        """Reset database (drop + create)"""
        DatabaseManager.drop_all()
        DatabaseManager.create_all()
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db=SQLAlchemy()
migrate = Migrate()

def init_database(app):
    db.init_app(app)
    migrate.init_app(app,db)


    "Create tables development"
    with app.app_context():
        if app.config.get('ENV')=='DEVELOPMENT':
            db.create_all()
            print("Database tables created successfully...")


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
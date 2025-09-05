from flask_bcrypt import generate_password_hash, check_password_hash
from app.models.base import BaseModel
from app.config.database import db

class User(BaseModel):
    """User model for authentication"""
    
    __tablename__ = 'users'
    
    # User bilgileri
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Profile
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    
    # Permissions
    is_admin = db.Column(db.Boolean, default=False)
    can_scan = db.Column(db.Boolean, default=True)
    can_view_reports = db.Column(db.Boolean, default=True)
    
    # Login tracking
    last_login = db.Column(db.DateTime, nullable=True)
    login_count = db.Column(db.Integer, default=0)
    
    def __init__(self, username, email, password, first_name=None, last_name=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def to_dict(self, include_sensitive=False):
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'is_admin': self.is_admin,
            'can_scan': self.can_scan,
            'can_view_reports': self.can_view_reports,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'login_count': self.login_count
        })
        
        if include_sensitive:
            base_dict['password_hash'] = self.password_hash
            
        return base_dict
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        return User.query.filter_by(username=username, is_active=True).first()
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return User.query.filter_by(email=email, is_active=True).first()
    
    @staticmethod
    def create_admin_user(username, email, password):
        """Create admin user"""
        admin = User(username=username, email=email, password=password)
        admin.is_admin = True
        admin.can_scan = True
        admin.can_view_reports = True
        return admin.save()
    
    def update_login(self):
        """Update login information"""
        from datetime import datetime
        self.last_login = datetime.utcnow()
        self.login_count += 1
        return self.save()
    
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"
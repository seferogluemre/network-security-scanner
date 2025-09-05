from app.models.base import BaseModel
from app.config.database import db

class Host(BaseModel):
    """Network host model"""
    
    __tablename__ = 'hosts'
    
    # Host bilgileri
    ip_address = db.Column(db.String(45), nullable=False, unique=True)  # IPv4/IPv6
    hostname = db.Column(db.String(255), nullable=True)
    mac_address = db.Column(db.String(17), nullable=True)  # MAC address
    
    # Network bilgileri
    network_range = db.Column(db.String(18), nullable=True)  # 192.168.1.0/24
    is_alive = db.Column(db.Boolean, default=True)
    last_seen = db.Column(db.DateTime, nullable=True)
    
    # OS Detection
    os_type = db.Column(db.String(50), nullable=True)  # Windows, Linux, macOS
    os_version = db.Column(db.String(100), nullable=True)
    
    # Relations
    scans = db.relationship('Scan', backref='target_host', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, ip_address, hostname=None, mac_address=None):
        self.ip_address = ip_address
        self.hostname = hostname
        self.mac_address = mac_address
    
    def to_dict(self):
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'ip_address': self.ip_address,
            'hostname': self.hostname,
            'mac_address': self.mac_address,
            'network_range': self.network_range,
            'is_alive': self.is_alive,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'os_type': self.os_type,
            'os_version': self.os_version,
            'total_scans': len(self.scans) if self.scans else 0
        })
        return base_dict
    
    @staticmethod
    def find_by_ip(ip_address):
        """Find host by IP address"""
        return Host.query.filter_by(ip_address=ip_address, is_active=True).first()
    
    @staticmethod
    def get_alive_hosts():
        """Get all alive hosts"""
        return Host.query.filter_by(is_alive=True, is_active=True).all()
    
    def __repr__(self):
        return f"<Host(ip={self.ip_address}, hostname={self.hostname})>"
from datetime import datetime
from app.models.base import BaseModel
from app.config.database import db
import json

class Scan(BaseModel):
    """Port scan model"""
    
    __tablename__ = 'scans'
    
    # Scan bilgileri
    target_ip = db.Column(db.String(45), nullable=False)
    scan_type = db.Column(db.String(20), nullable=False)  # 'port', 'fast', 'network'
    status = db.Column(db.String(20), default='running')  # 'running', 'completed', 'failed'
    
    # Tarama parametreleri
    ports_scanned = db.Column(db.Text, nullable=True)  # JSON string
    start_port = db.Column(db.Integer, nullable=True)
    end_port = db.Column(db.Integer, nullable=True)
    threads_used = db.Column(db.Integer, default=1)
    
    # Sonuçlar
    open_ports = db.Column(db.Text, nullable=True)  # JSON string
    closed_ports_count = db.Column(db.Integer, default=0)
    total_ports_scanned = db.Column(db.Integer, default=0)
    
    # Timing
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    duration_seconds = db.Column(db.Float, nullable=True)
    
    # Relations
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'), nullable=True)
    
    def __init__(self, target_ip, scan_type, ports_scanned=None):
        self.target_ip = target_ip
        self.scan_type = scan_type
        self.ports_scanned = json.dumps(ports_scanned) if ports_scanned else None
        self.start_time = datetime.utcnow()
    
    def set_open_ports(self, ports_list):
        """Set open ports as JSON"""
        self.open_ports = json.dumps(ports_list) if ports_list else None
    
    def get_open_ports(self):
        """Get open ports as list"""
        if self.open_ports:
            return json.loads(self.open_ports)
        return []
    
    def set_scanned_ports(self, ports_list):
        """Set scanned ports as JSON"""
        self.ports_scanned = json.dumps(ports_list) if ports_list else None
    
    def get_scanned_ports(self):
        """Get scanned ports as list"""
        if self.ports_scanned:
            return json.loads(self.ports_scanned)
        return []
    
    def complete_scan(self, open_ports, total_scanned=0):
        """Mark scan as completed"""
        self.end_time = datetime.utcnow()
        self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        self.set_open_ports(open_ports)
        self.total_ports_scanned = total_scanned
        self.closed_ports_count = total_scanned - len(open_ports)
        self.status = 'completed'
        return self.save()
    
    def fail_scan(self, error_message=None):
        """Mark scan as failed"""
        self.end_time = datetime.utcnow()
        self.duration_seconds = (self.end_time - self.start_time).total_seconds()
        self.status = 'failed'
        return self.save()
    
    def to_dict(self):
        """Convert to dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'target_ip': self.target_ip,
            'scan_type': self.scan_type,
            'status': self.status,
            'ports_scanned': self.get_scanned_ports(),
            'start_port': self.start_port,
            'end_port': self.end_port,
            'threads_used': self.threads_used,
            'open_ports': self.get_open_ports(),
            'closed_ports_count': self.closed_ports_count,
            'total_ports_scanned': self.total_ports_scanned,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.duration_seconds,
            'host_id': self.host_id
        })
        return base_dict
    
    @staticmethod
    def get_recent_scans(limit=10):
        """Get recent scans"""
        return Scan.query.filter_by(is_active=True).order_by(Scan.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_scans_by_ip(ip_address):
        """Get scans by IP address"""
        return Scan.query.filter_by(target_ip=ip_address, is_active=True).order_by(Scan.created_at.desc()).all()
    
    def __repr__(self):
        return f"<Scan(target={self.target_ip}, type={self.scan_type}, status={self.status})>"
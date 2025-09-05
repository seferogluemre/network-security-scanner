from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime

class PortScanRequest(BaseModel):
    target: str = Field(..., description="Target IP address or hostname")
    ports: List[int] = Field(..., description="List of ports to scan")
    timeout: Optional[int] = Field(3, ge=1, le=30, description="Timeout in seconds")
    
    @validator('target')
    def validate_target(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Target cannot be empty')
        return v.strip()
    
    @validator('ports')
    def validate_ports(cls, v):
        if not v:
            raise ValueError('Ports list cannot be empty')
        for port in v:
            if not (1 <= port <= 65535):
                raise ValueError(f'Port {port} must be between 1 and 65535')
        return v

class FastScanRequest(BaseModel):
    target: str = Field(..., description="Target IP address")
    start_port: int = Field(1, ge=1, le=65535, description="Start port")
    end_port: int = Field(1000, ge=1, le=65535, description="End port")
    threads: Optional[int] = Field(100, ge=1, le=500, description="Number of threads")
    timeout: Optional[int] = Field(1, ge=1, le=10, description="Timeout per port")
    
    @validator('end_port')
    def validate_port_range(cls, v, values):
        if 'start_port' in values and v <= values['start_port']:
            raise ValueError('End port must be greater than start port')
        return v

class NetworkDiscoveryRequest(BaseModel):
    network: Optional[str] = Field(None, description="Network range (e.g., 192.168.1.0/24)")
    timeout: Optional[int] = Field(1, ge=1, le=10, description="Ping timeout")
    threads: Optional[int] = Field(50, ge=1, le=200, description="Number of threads")

class ScanResponse(BaseModel):
    scan_id: int
    target: str
    scan_type: str
    status: str
    open_ports: List[Dict[str, Any]]
    total_ports_scanned: int
    duration_seconds: Optional[float]
    start_time: datetime
    end_time: Optional[datetime]
    
    class Config:
        from_attributes = True  

class PortInfo(BaseModel):
    port: int
    service: str
    status: str = "open"
    banner: Optional[str] = None

class ScanResultResponse(BaseModel):
    scan_id: int
    target_ip: str
    scan_type: str
    status: str
    open_ports: List[PortInfo]
    closed_ports_count: int
    total_ports: int
    duration: float
    threads_used: int
    timestamp: datetime

class ScanHistoryResponse(BaseModel):
    scans: List[ScanResponse]
    total_scans: int
    page: int
    per_page: int
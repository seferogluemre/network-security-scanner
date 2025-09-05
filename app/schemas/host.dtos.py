from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
import re

class HostCreateRequest(BaseModel):
    """Host creation request schema"""
    ip_address: str = Field(..., description="IP address")
    hostname: Optional[str] = Field(None, description="Hostname")
    mac_address: Optional[str] = Field(None, description="MAC address")
    network_range: Optional[str] = Field(None, description="Network range")
    
    @validator('ip_address')
    def validate_ip(cls, v):
        # Basic IP validation
        ip_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        if not re.match(ip_pattern, v):
            raise ValueError('Invalid IP address format')
        return v
    
    @validator('mac_address')
    def validate_mac(cls, v):
        if v is None:
            return v
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(mac_pattern, v):
            raise ValueError('Invalid MAC address format')
        return v.upper()

class HostUpdateRequest(BaseModel):
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    os_type: Optional[str] = None
    os_version: Optional[str] = None
    is_alive: Optional[bool] = None

class HostResponse(BaseModel):
    id: int
    ip_address: str
    hostname: Optional[str]
    mac_address: Optional[str]
    network_range: Optional[str]
    is_alive: bool
    last_seen: Optional[datetime]
    os_type: Optional[str]
    os_version: Optional[str]
    total_scans: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class NetworkDiscoveryResponse(BaseModel):
    network_range: str
    total_hosts_found: int
    alive_hosts: List[HostResponse]
    scan_duration: float
    discovery_method: str = "ping_sweep"
    timestamp: datetime

class HostStatsResponse(BaseModel):
    total_hosts: int
    alive_hosts: int
    dead_hosts: int
    hosts_with_open_ports: int
    most_scanned_host: Optional[str]
    latest_discovery: Optional[datetime]

class HostDetailResponse(BaseModel):
    host: HostResponse
    recent_scans: List[Dict[str, Any]]
    open_ports_summary: List[int]
    services_detected: List[str]
    vulnerability_count: int = 0
    risk_level: str = "low"
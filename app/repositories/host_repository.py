from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import desc, func, or_
from app.repositories.base_repository import BaseRepository
from app.models.host import Host
from app.models.scan import Scan

class HostRepository(BaseRepository):
    def __init__(self):
        super().__init__(Host)
    
    def find_by_ip(self, ip_address: str) -> Optional[Host]:
        return self.get_one_by_filter(ip_address=ip_address)
    
    def find_or_create_host(self, ip_address: str, **kwargs) -> Host:
        host = self.find_by_ip(ip_address)
        if host:
            # Update last seen
            host.last_seen = datetime.utcnow()
            self.session.commit()
            return host
        
        # Create new host
        host_data = {
            'ip_address': ip_address,
            'last_seen': datetime.utcnow(),
            'is_alive': True,
            **kwargs
        }
        return self.create(**host_data)
    
    def get_alive_hosts(self) -> List[Host]:
        return self.get_by_filter(is_alive=True)
    
    def get_dead_hosts(self) -> List[Host]:
        return self.get_by_filter(is_alive=False)
    
    def get_hosts_by_network(self, network_range: str) -> List[Host]:
        return self.get_by_filter(network_range=network_range)
    
    def update_host_status(self, ip_address: str, is_alive: bool) -> Optional[Host]:
        host = self.find_by_ip(ip_address)
        if host:
            updates = {
                'is_alive': is_alive,
                'last_seen': datetime.utcnow()
            }
            return self.update(host.id, **updates)
        return None
    
    def get_hosts_with_open_ports(self) -> List[Dict[str, Any]]:
        results = self.session.query(Host).join(Scan).filter(
            Host.is_active == True,
            Scan.is_active == True,
            Scan.status == 'completed',
            Scan.open_ports.isnot(None)
        ).distinct().all()
        
        return [host.to_dict() for host in results]
    
    def get_host_scan_history(self, ip_address: str) -> List[Scan]:
        host = self.find_by_ip(ip_address)
        if not host:
            return []
        
        return self.session.query(Scan).filter(
            Scan.target_ip == ip_address,
            Scan.is_active == True
        ).order_by(desc(Scan.created_at)).all()
    
    def get_network_statistics(self) -> Dict[str, Any]:
        total_hosts = self.count()
        alive_hosts = len(self.get_alive_hosts())
        dead_hosts = len(self.get_dead_hosts())
        hosts_with_scans = len(self.get_hosts_with_open_ports())
        
        # Most scanned host
        most_scanned = self.session.query(
            Host.ip_address,
            func.count(Scan.id).label('scan_count')
        ).join(Scan).filter(
            Host.is_active == True,
            Scan.is_active == True
        ).group_by(Host.ip_address).order_by(
            desc(func.count(Scan.id))
        ).first()
        
        return {
            'total_hosts': total_hosts,
            'alive_hosts': alive_hosts,
            'dead_hosts': dead_hosts,
            'hosts_with_scans': hosts_with_scans,
            'most_scanned_host': most_scanned.ip_address if most_scanned else None,
            'most_scan_count': most_scanned.scan_count if most_scanned else 0
        }
    
    def search_hosts(self, search_term: str) -> List[Host]:
        return self.session.query(Host).filter(
            Host.is_active == True,
            or_(
                Host.ip_address.like(f'%{search_term}%'),
                Host.hostname.like(f'%{search_term}%')
            )
        ).all()
    
    def get_recently_discovered_hosts(self, hours: int = 24) -> List[Host]:
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return self.session.query(Host).filter(
            Host.created_at >= cutoff_time,
            Host.is_active == True
        ).order_by(desc(Host.created_at)).all()
    
    def mark_hosts_offline(self, max_age_hours: int = 48) -> int:
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        offline_hosts = self.session.query(Host).filter(
            Host.last_seen < cutoff_time,
            Host.is_alive == True,
            Host.is_active == True
        ).all()
        
        count = 0
        for host in offline_hosts:
            host.is_alive = False
            count += 1
        
        self.session.commit()
        return count
    
    def get_host_details_with_stats(self, ip_address: str) -> Optional[Dict[str, Any]]:
        host = self.find_by_ip(ip_address)
        if not host:
            return None
        
        # Get scan statistics
        scans = self.get_host_scan_history(ip_address)
        completed_scans = [s for s in scans if s.status == 'completed']
        
        # Get unique open ports from all scans
        all_open_ports = set()
        for scan in completed_scans:
            all_open_ports.update(scan.get_open_ports())
        
        return {
            'host': host.to_dict(),
            'total_scans': len(scans),
            'completed_scans': len(completed_scans),
            'unique_open_ports': list(all_open_ports),
            'recent_scans': [s.to_dict() for s in scans[:5]],  # Last 5 scans
            'first_seen': host.created_at,
            'last_activity': max([s.created_at for s in scans]) if scans else host.created_at
        }
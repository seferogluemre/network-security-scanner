from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import desc, func
from app.repositories.base_repository import BaseRepository
from app.models.scan import Scan

class ScanRepository(BaseRepository):
    def __init__(self):
        super().__init__(Scan)
    
    def create_scan(self, target_ip: str, scan_type: str, **kwargs) -> Scan:
        scan_data = {
            'target_ip': target_ip,
            'scan_type': scan_type,
            'status': 'running',
            'start_time': datetime.utcnow(),
            **kwargs
        }
        return self.create(**scan_data)
    
    def get_recent_scans(self, limit: int = 10) -> List[Scan]:
        return self.session.query(Scan).filter(
            Scan.is_active == True
        ).order_by(desc(Scan.created_at)).limit(limit).all()
    
    def get_scans_by_target(self, target_ip: str) -> List[Scan]:
        return self.session.query(Scan).filter(
            Scan.target_ip == target_ip,
            Scan.is_active == True
        ).order_by(desc(Scan.created_at)).all()
    
    def get_scans_by_status(self, status: str) -> List[Scan]:
        return self.get_by_filter(status=status)
    
    def get_running_scans(self) -> List[Scan]:
        return self.get_scans_by_status('running')
    
    def get_completed_scans(self) -> List[Scan]:
        return self.get_scans_by_status('completed')
    
    def get_failed_scans(self) -> List[Scan]:
        return self.get_scans_by_status('failed')
    
    def complete_scan(self, scan_id: int, open_ports: List[int], total_scanned: int = 0) -> Optional[Scan]:
        scan = self.get_by_id(scan_id)
        if not scan:
            return None
        
        end_time = datetime.utcnow()
        duration = (end_time - scan.start_time).total_seconds()
        
        updates = {
            'status': 'completed',
            'end_time': end_time,
            'duration_seconds': duration,
            'total_ports_scanned': total_scanned,
            'closed_ports_count': total_scanned - len(open_ports)
        }
        
        # Set open ports as JSON
        scan.set_open_ports(open_ports)
        
        return self.update(scan_id, **updates)
    
    def fail_scan(self, scan_id: int, error_message: str = None) -> Optional[Scan]:
        """Mark scan as failed"""
        scan = self.get_by_id(scan_id)
        if not scan:
            return None
        
        end_time = datetime.utcnow()
        duration = (end_time - scan.start_time).total_seconds()
        
        updates = {
            'status': 'failed',
            'end_time': end_time,
            'duration_seconds': duration
        }
        
        return self.update(scan_id, **updates)
    
    def get_scan_statistics(self) -> Dict[str, Any]:
        """Get scan statistics"""
        total_scans = self.count()
        completed_scans = len(self.get_completed_scans())
        running_scans = len(self.get_running_scans())
        failed_scans = len(self.get_failed_scans())
        
        # Average scan duration for completed scans
        avg_duration_query = self.session.query(func.avg(Scan.duration_seconds)).filter(
            Scan.status == 'completed',
            Scan.is_active == True
        ).scalar()
        
        avg_duration = float(avg_duration_query) if avg_duration_query else 0.0
        
        return {
            'total_scans': total_scans,
            'completed_scans': completed_scans,
            'running_scans': running_scans,
            'failed_scans': failed_scans,
            'success_rate': (completed_scans / total_scans * 100) if total_scans > 0 else 0,
            'average_duration_seconds': avg_duration
        }
    
    def get_scans_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Scan]:
        return self.session.query(Scan).filter(
            Scan.created_at >= start_date,
            Scan.created_at <= end_date,
            Scan.is_active == True
        ).order_by(desc(Scan.created_at)).all()
    
    def get_top_scanned_targets(self, limit: int = 10) -> List[Dict[str, Any]]:
        results = self.session.query(
            Scan.target_ip,
            func.count(Scan.id).label('scan_count')
        ).filter(
            Scan.is_active == True
        ).group_by(Scan.target_ip).order_by(
            desc(func.count(Scan.id))
        ).limit(limit).all()
        
        return [
            {'target_ip': result.target_ip, 'scan_count': result.scan_count}
            for result in results
        ]
    
    def cleanup_old_scans(self, days_old: int = 30) -> int:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        old_scans = self.session.query(Scan).filter(
            Scan.created_at < cutoff_date,
            Scan.is_active == True
        ).all()
        
        count = 0
        for scan in old_scans:
            scan.is_active = False
            count += 1
        
        self.session.commit()
        return count
    
    def get_scan_with_details(self, scan_id: int) -> Optional[Dict[str, Any]]:
        scan = self.get_by_id(scan_id)
        if not scan:
            return None
        
        return {
            'scan': scan.to_dict(),
            'open_ports': scan.get_open_ports(),
            'scanned_ports': scan.get_scanned_ports(),
            'success_rate': (len(scan.get_open_ports()) / scan.total_ports_scanned * 100) 
                          if scan.total_ports_scanned > 0 else 0
        }
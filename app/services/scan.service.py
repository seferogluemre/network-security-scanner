from typing import List, Optional, Dict, Any
from app.repositories.scan_repository import ScanRepository
from app.repositories.host_repository import HostRepository
from app.schemas.scan_dto import PortScanRequest, FastScanRequest
from app.utils.logger import service_logger, log_function_entry, log_function_exit
from core.port_scanner import PortScanner
from core.threaded_scanner import FastPortScanner

class ScanService:
    def __init__(self):
        self.scan_repo = ScanRepository()
        self.host_repo = HostRepository()
        service_logger.info("🔧 ScanService initialized")
    
    def create_port_scan(self, request: PortScanRequest) -> Dict[str, Any]:
        log_function_entry(service_logger, "create_port_scan", 
                          target=request.target, ports=len(request.ports))
        
        try:
            service_logger.info(f"📝 Creating scan record for {request.target}")
            scan = self.scan_repo.create_scan(
                target_ip=request.target,
                scan_type='port',
                total_ports_scanned=len(request.ports)
            )
            service_logger.info(f"✅ Scan record created with ID: {scan.id}")
            
            # 2. Find or create host
            service_logger.info(f"🔍 Finding/creating host for {request.target}")
            host = self.host_repo.find_or_create_host(request.target)
            service_logger.info(f"🏠 Host ready: {host.ip_address} (ID: {host.id})")
            
            # 3. Execute scan
            service_logger.info(f"⚡ Starting port scan...")
            scanner = PortScanner(timeout=request.timeout)
            results = scanner.scan_ports(request.target, request.ports)
            service_logger.info(f"🎯 Scan completed: {len(results['open_ports'])} open ports found")
            
            # 4. Update scan with results
            service_logger.info(f"💾 Saving scan results...")
            open_ports = [port['port'] for port in results['open_ports']]
            self.scan_repo.complete_scan(scan.id, open_ports, len(request.ports))
            service_logger.info(f"✅ Scan results saved")
            
            # 5. Update host status
            service_logger.info(f"🔄 Updating host status...")
            self.host_repo.update_host_status(request.target, True)
            
            response = {
                'scan_id': scan.id,
                'target': request.target,
                'scan_type': 'port',
                'status': 'completed',
                'open_ports': results['open_ports'],
                'total_ports_scanned': len(request.ports),
                'host_id': host.id
            }
            
            log_function_exit(service_logger, "create_port_scan", response)
            return response
            
        except Exception as e:
            service_logger.error(f"❌ Port scan failed: {str(e)}")
            if 'scan' in locals():
                self.scan_repo.fail_scan(scan.id, str(e))
            raise e
    
    def create_fast_scan(self, request: FastScanRequest) -> Dict[str, Any]:
        log_function_entry(service_logger, "create_fast_scan",
                          target=request.target, 
                          port_range=f"{request.start_port}-{request.end_port}",
                          threads=request.threads)
        
        try:
            # 1. Create scan record
            service_logger.info(f"📝 Creating fast scan record...")
            scan = self.scan_repo.create_scan(
                target_ip=request.target,
                scan_type='fast',
                start_port=request.start_port,
                end_port=request.end_port,
                threads_used=request.threads
            )
            service_logger.info(f"✅ Fast scan record created: {scan.id}")
            
            # 2. Find or create host
            host = self.host_repo.find_or_create_host(request.target)
            service_logger.info(f"🏠 Host ready: {host.ip_address}")
            
            # 3. Execute fast scan
            service_logger.info(f"⚡ Starting fast scan with {request.threads} threads...")
            scanner = FastPortScanner(max_threads=request.threads)
            open_ports = scanner.scan_port_range_threaded(
                request.target, 
                request.start_port, 
                request.end_port
            )
            
            total_scanned = request.end_port - request.start_port + 1
            service_logger.info(f"🎯 Fast scan completed: {len(open_ports)}/{total_scanned} ports open")
            
            # 4. Update scan results
            service_logger.info(f"💾 Saving fast scan results...")
            self.scan_repo.complete_scan(scan.id, open_ports, total_scanned)
            
            # 5. Update host
            self.host_repo.update_host_status(request.target, True)
            
            response = {
                'scan_id': scan.id,
                'target': request.target,
                'scan_type': 'fast',
                'status': 'completed',
                'open_ports': open_ports,
                'total_ports_scanned': total_scanned,
                'threads_used': request.threads,
                'host_id': host.id
            }
            
            log_function_exit(service_logger, "create_fast_scan", response)
            return response
            
        except Exception as e:
            service_logger.error(f"❌ Fast scan failed: {str(e)}")
            if 'scan' in locals():
                self.scan_repo.fail_scan(scan.id, str(e))
            raise e
    
    def get_scan_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        log_function_entry(service_logger, "get_scan_history", limit=limit)
        
        service_logger.info(f"📊 Fetching {limit} recent scans...")
        scans = self.scan_repo.get_recent_scans(limit)
        service_logger.info(f"✅ Found {len(scans)} scans")
        
        results = [scan.to_dict() for scan in scans]
        log_function_exit(service_logger, "get_scan_history", results)
        return results
    
    def get_scan_by_id(self, scan_id: int) -> Optional[Dict[str, Any]]:
        log_function_entry(service_logger, "get_scan_by_id", scan_id=scan_id)
        
        service_logger.info(f"🔍 Looking for scan ID: {scan_id}")
        result = self.scan_repo.get_scan_with_details(scan_id)
        
        if result:
            service_logger.info(f"✅ Scan found: {result['scan']['target_ip']}")
        else:
            service_logger.warning(f"⚠️  Scan not found: {scan_id}")
        
        log_function_exit(service_logger, "get_scan_by_id", result)
        return result
    
    def get_scan_statistics(self) -> Dict[str, Any]:
        log_function_entry(service_logger, "get_scan_statistics")
        
        service_logger.info(f"📈 Calculating scan statistics...")
        stats = self.scan_repo.get_scan_statistics()
        service_logger.info(f"✅ Statistics calculated: {stats['total_scans']} total scans")
        
        log_function_exit(service_logger, "get_scan_statistics", stats)
        return stats
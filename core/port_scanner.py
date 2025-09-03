import socket
from datetime import datetime
from typing import List, Dict, Optional

class PortScanner:
    def __init__(self, timeout: int = 3):
        self.timeout = timeout
        
    def scan_port(self, target_ip: str, port: int) -> bool:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((target_ip, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def get_service_name(self, port: int) -> str:
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 443: "HTTPS", 3000: "Node.js",
            3306: "MySQL", 5432: "PostgreSQL"
        }
        return services.get(port, "Unknown")
    
    def scan_ports(self, target_ip: str, ports: List[int]) -> Dict:
        results = {
            'target': target_ip,
            'scan_time': datetime.now().isoformat(),
            'open_ports': [],
            'closed_ports': []
        }
        
        for port in ports:
            if self.scan_port(target_ip, port):
                results['open_ports'].append({
                    'port': port,
                    'service': self.get_service_name(port)
                })
            else:
                results['closed_ports'].append(port)
                
        return results
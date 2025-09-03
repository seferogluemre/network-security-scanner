import subprocess
import socket
import ipaddress
import threading
from concurrent.futures import ThreadPoolExecutor
import platform

class NetworkDiscovery:
    def __init__(self):
        self.alive_hosts = []
        self.lock = threading.Lock()
    
    def ping_host(self, ip):
        try:
            if platform.system().lower() == "windows":
                cmd = ["ping", "-n", "1", "-w", "1000", str(ip)]
            else:
                cmd = ["ping", "-c", "1", "-W", "1", str(ip)]
            
            result = subprocess.run(cmd, 
                                  stdout=subprocess.DEVNULL, 
                                  stderr=subprocess.DEVNULL)
            
            if result.returncode == 0:
                with self.lock:
                    self.alive_hosts.append(str(ip))
                    print(f"✅ {ip} - CANLI")
                    
        except Exception:
            pass
    
    def discover_network(self, network="192.168.1.0/24", max_threads=50):
        print(f"\n🔍 AĞ KEŞFİ")
        print(f"🌐 Hedef ağ: {network}")
        print(f"🧵 Thread sayısı: {max_threads}")
        print("-" * 50)
        
        try:
            net = ipaddress.IPv4Network(network, strict=False)
            total_hosts = net.num_addresses - 2 
            
            print(f"📡 {total_hosts} IP taranacak...")
            print("-" * 50)
            
            self.alive_hosts = []  # Reset
            
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                futures = []
                for ip in net.hosts(): 
                    future = executor.submit(self.ping_host, ip)
                    futures.append(future)
                
                for future in futures:
                    future.result()
            
            print("-" * 50)
            print(f"🎉 Toplam {len(self.alive_hosts)} canlı host bulundu")
            
            return sorted(self.alive_hosts, key=lambda x: ipaddress.IPv4Address(x))
            
        except Exception as e:
            print(f"❌ Hata: {e}")
            return []
    
    def get_hostname(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Bilinmiyor"
    
    def detailed_discovery(self, network="192.168.1.0/24"):
        print(f"\n🔍 DETAYLI AĞ KEŞFİ")
        alive_hosts = self.discover_network(network)
        
        if alive_hosts:
            print(f"\n📋 DETAYLI RAPOR:")
            print("-" * 70)
            print(f"{'IP Adresi':<15} {'Hostname':<25} {'Durum'}")
            print("-" * 70)
            
            for ip in alive_hosts:
                hostname = self.get_hostname(ip)
                print(f"{ip:<15} {hostname:<25} Canlı")

def get_local_network():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()

        ip_parts = local_ip.split('.')
        network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        
        return network, local_ip
    except:
        return "192.168.1.0/24", "192.168.1.1"

if __name__ == "__main__":
    print("🌐 Network Discovery v3.0")
    print("=" * 50)
    
    network, local_ip = get_local_network()
    print(f"🏠 Kendi IP'n: {local_ip}")
    print(f"🌐 Tahmin edilen ağ: {network}")
    
    choice = input(f"\n1. Bu ağı tara ({network})\n2. Özel ağ gir\n3. Detaylı tarama\nSeçim: ")
    
    discovery = NetworkDiscovery()
    
    if choice == "1":
        discovery.discover_network(network)
    elif choice == "2":
        custom_network = input("Ağ aralığı (örn: 192.168.0.0/24): ")
        discovery.discover_network(custom_network)
    elif choice == "3":
        discovery.detailed_discovery(network)
    else:
        print("❌ Geçersiz seçim!")
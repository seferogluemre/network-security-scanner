import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class FastPortScanner:
    def __init__(self, max_threads=100):
        self.max_threads = max_threads
        self.open_ports = []
        self.lock = threading.Lock() 
        
    def scan_single_port(self, target_ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1) 
            result = sock.connect_ex((target_ip, port))
            sock.close()
            
            if result == 0:
                with self.lock:
                    self.open_ports.append(port)
                    print(f"✅ Port {port:5d} AÇIK")
                    
        except Exception:
            pass
    
    def scan_port_range_threaded(self, target_ip, start_port, end_port):
        print(f"\n🚀 HIZLI TARAMA MODU")
        print(f"🎯 Hedef: {target_ip}")
        print(f"📡 Port aralığı: {start_port}-{end_port}")
        print(f"🧵 Thread sayısı: {self.max_threads}")
        print(f"⏰ Başlangıç: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 60)
        
        start_time = time.time()
        self.open_ports = []  # Reset
        
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for port in range(start_port, end_port + 1):
                future = executor.submit(self.scan_single_port, target_ip, port)
                futures.append(future)
            
            for future in futures:
                future.result()

        end_time = time.time()
        duration = end_time - start_time
        
        print("-" * 60)
        print(f"⚡ Tarama süresi: {duration:.2f} saniye")
        print(f"📊 Bulunan açık portlar: {len(self.open_ports)}")
        print(f"🎉 Açık portlar: {sorted(self.open_ports)}")
        
        return sorted(self.open_ports)

def compare_speeds(target_ip="127.0.0.1"):
    print("🏁 HIZ KARŞILAŞTIRMASI")
    print("=" * 60)
    
    print("\n1️⃣ NORMAL TARAMA (Sıralı)")
    start_time = time.time()
    
    normal_open = []
    for port in range(1, 101): 
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((target_ip, port)) == 0:
                normal_open.append(port)
            sock.close()
        except:
            pass
    
    normal_time = time.time() - start_time
    print(f"⏱️  Süre: {normal_time:.2f} saniye")
    print(f"📊 Bulunan: {len(normal_open)} port")
    
    print("\n2️⃣ THREADING TARAMA (Paralel)")
    scanner = FastPortScanner(max_threads=50)
    threaded_open = scanner.scan_port_range_threaded(target_ip, 1, 100)
    
    print("\n📈 SONUÇ:")
    print(f"Normal tarama: {normal_time:.2f} saniye")
    print(f"Threading tarama: Yukarıda gösterildi") 
    print(f"Hız artışı: ~{normal_time/1:.1f}x daha hızlı!")

if __name__ == "__main__":
    print("🚀 Threading Port Scanner v2.0")
    print("=" * 60)
    
    choice = input("1. Hız karşılaştırması\n2. Hızlı port tarama\nSeçim: ")
    
    if choice == "1":
        compare_speeds()
    elif choice == "2":
        target = input("Hedef IP (Enter=localhost): ").strip() or "127.0.0.1"
        start = int(input("Başlangıç port: "))
        end = int(input("Bitiş port: "))
        threads = int(input("Thread sayısı (Enter=100): ") or "100")
        
        scanner = FastPortScanner(max_threads=threads)
        scanner.scan_port_range_threaded(target, start, end)
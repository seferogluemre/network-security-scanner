import requests
import json
import time
from datetime import datetime

class NetScoutAPIClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'NetScout-TestClient/1.0'
        })
    
    def test_connection(self):
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=5)
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, str(e)
    
    def scan_ports(self, target="127.0.0.1", ports=None):
        if ports is None:
            ports = [21, 22, 80, 443, 3000, 3306, 5432]
        
        payload = {
            "target": target,
            "ports": ports
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/scan/ports",
                json=payload,
                timeout=30
            )
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, str(e)
    
    def fast_scan(self, target="127.0.0.1", start=1, end=100, threads=50):
        """Hızlı tarama testi"""
        payload = {
            "target": target,
            "start_port": start,
            "end_port": end,
            "threads": threads
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/scan/fast",
                json=payload,
                timeout=60
            )
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, str(e)
    
    def discover_network(self, network=None):
        """Ağ keşfi testi"""
        payload = {}
        if network:
            payload["network"] = network
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/network/discover",
                json=payload,
                timeout=60
            )
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, str(e)
    
    def simple_scan(self, target="127.0.0.1"):
        """Basit GET tarama testi"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/scan/simple",
                params={"target": target},
                timeout=30
            )
            return response.status_code == 200, response.json()
        except Exception as e:
            return False, str(e)

def print_result(test_name, success, result):
    """Test sonucunu yazdır"""
    status = "✅ BAŞARILI" if success else "❌ BAŞARISIZ"
    print(f"\n{status} - {test_name}")
    print("-" * 50)
    
    if success and isinstance(result, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Hata: {result}")

def run_all_tests():
    """Tüm testleri çalıştır"""
    print("🧪 NetScout API Test Suite")
    print("=" * 60)
    print(f"⏰ Test zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    client = NetScoutAPIClient()
    
    # 1. Bağlantı Testi
    print("\n1️⃣ API Bağlantı Testi")
    success, result = client.test_connection()
    print_result("Health Check", success, result)
    
    if not success:
        print("\n❌ API server çalışmıyor! Önce 'python api/server.py' çalıştırın")
        return
    
    # 2. Basit Tarama
    print("\n2️⃣ Basit Port Tarama (GET)")
    success, result = client.simple_scan("127.0.0.1")
    print_result("Simple Scan", success, result)
    
    # 3. Detaylı Port Tarama
    print("\n3️⃣ Detaylı Port Tarama (POST)")
    success, result = client.scan_ports("127.0.0.1", [80, 443, 3000, 22, 21])
    print_result("Port Scan", success, result)
    
    # 4. Hızlı Tarama
    print("\n4️⃣ Hızlı Port Tarama (Threading)")
    success, result = client.fast_scan("127.0.0.1", 1, 200, 30)
    print_result("Fast Scan", success, result)
    
    # 5. Ağ Keşfi (Opsiyonel - yavaş olabilir)
    print("\n5️⃣ Ağ Keşfi (Otomatik)")
    print("⚠️  Bu test biraz uzun sürebilir...")
    success, result = client.discover_network()
    print_result("Network Discovery", success, result)
    
    print("\n🎉 Tüm testler tamamlandı!")
    print("=" * 60)

def interactive_test():
    """Etkileşimli test modu"""
    client = NetScoutAPIClient()
    
    # Bağlantı kontrolü
    success, _ = client.test_connection()
    if not success:
        print("❌ API server bağlantısı kurulamadı!")
        print("Önce 'python api/server.py' komutunu çalıştırın")
        return
    
    print("✅ API server bağlantısı başarılı!")
    
    while True:
        print("\n🧪 NetScout API Test Menüsü")
        print("-" * 40)
        print("1. 🎯 Port Tarama")
        print("2. ⚡ Hızlı Tarama")
        print("3. 🌐 Ağ Keşfi")
        print("4. 🔍 Basit Tarama")
        print("5. 🩺 Sağlık Kontrolü")
        print("6. 🚀 Tüm Testleri Çalıştır")
        print("0. ❌ Çıkış")
        
        choice = input("\nSeçiminiz: ").strip()
        
        if choice == "1":
            target = input("Hedef IP (Enter=localhost): ").strip() or "127.0.0.1"
            success, result = client.scan_ports(target)
            print_result("Port Tarama", success, result)
            
        elif choice == "2":
            target = input("Hedef IP (Enter=localhost): ").strip() or "127.0.0.1"
            start = int(input("Başlangıç port (Enter=1): ") or "1")
            end = int(input("Bitiş port (Enter=100): ") or "100")
            success, result = client.fast_scan(target, start, end)
            print_result("Hızlı Tarama", success, result)
            
        elif choice == "3":
            network = input("Ağ aralığı (Enter=otomatik): ").strip() or None
            success, result = client.discover_network(network)
            print_result("Ağ Keşfi", success, result)
            
        elif choice == "4":
            target = input("Hedef IP (Enter=localhost): ").strip() or "127.0.0.1"
            success, result = client.simple_scan(target)
            print_result("Basit Tarama", success, result)
            
        elif choice == "5":
            success, result = client.test_connection()
            print_result("Sağlık Kontrolü", success, result)
            
        elif choice == "6":
            run_all_tests()
            
        elif choice == "0":
            print("👋 Test client kapatılıyor...")
            break
            
        else:
            print("❌ Geçersiz seçim!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_all_tests()
    else:
        interactive_test()

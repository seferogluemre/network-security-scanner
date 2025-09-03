import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.port_scanner import PortScanner
from core.network_discovery import NetworkDiscovery
from core.threaded_scanner import FastPortScanner

def show_banner():
    print("""
╔══════════════════════════════════════╗
║           🛡️  NetScout v1.0          ║
║     Network Security Scanner         ║
║                                      ║
║  Güvenli ve yasal kullanım için!     ║
╚══════════════════════════════════════╝
    """)

def main_menu():
    while True:
        print("\n🔍 ANA MENÜ")
        print("-" * 40)
        print("1. 🎯 Port Tarama")
        print("2. 🌐 Ağ Keşfi")
        print("3. ⚡ Hızlı Tarama (Threading)")
        print("4. 📊 Detaylı Rapor")
        print("0. ❌ Çıkış")
        
        choice = input("\nSeçiminiz: ").strip()
        
        if choice == "1":
            port_scan_menu()
        elif choice == "2":
            network_discovery_menu()
        elif choice == "3":
            fast_scan_menu()
        elif choice == "4":
            detailed_report_menu()
        elif choice == "0":
            print("👋 Güle güle!")
            break
        else:
            print("❌ Geçersiz seçim!")

def port_scan_menu():
    scanner = PortScanner()
    target = input("🎯 Hedef IP: ").strip() or "127.0.0.1"
    
    print("\n📡 Tarama türü:")
    print("1. Yaygın portlar")
    print("2. Port aralığı")
    print("3. Özel port listesi")
    
    scan_type = input("Seçim: ").strip()
    
    if scan_type == "1":
        ports = [21, 22, 23, 25, 53, 80, 443, 3000, 3306, 5432]
    elif scan_type == "2":
        start = int(input("Başlangıç: "))
        end = int(input("Bitiş: "))
        ports = list(range(start, end + 1))
    elif scan_type == "3":
        port_input = input("Portlar (virgülle ayır): ")
        ports = [int(p.strip()) for p in port_input.split(",")]
    else:
        return
    
    print(f"\n🚀 {target} taranıyor...")
    results = scanner.scan_ports(target, ports)
    
    print(f"\n📊 SONUÇLAR:")
    print(f"Açık portlar: {len(results['open_ports'])}")
    for port_info in results['open_ports']:
        print(f"✅ {port_info['port']} - {port_info['service']}")

def network_discovery_menu():
    from core.network_discovery import NetworkDiscovery, get_local_network
    
    discovery = NetworkDiscovery()
    network, local_ip = get_local_network()
    
    print(f"\n🏠 Kendi IP'n: {local_ip}")
    print(f"🌐 Tahmin edilen ağ: {network}")
    
    choice = input(f"\n1. Bu ağı tara ({network})\n2. Özel ağ gir\nSeçim: ")
    
    if choice == "1":
        discovery.discover_network(network)
    elif choice == "2":
        custom_network = input("Ağ aralığı (örn: 192.168.0.0/24): ")
        discovery.discover_network(custom_network)

def fast_scan_menu():
    from core.threaded_scanner import FastPortScanner
    
    target = input("🎯 Hedef IP: ").strip() or "127.0.0.1"
    start = int(input("Başlangıç port: "))
    end = int(input("Bitiş port: "))
    threads = int(input("Thread sayısı (Enter=100): ") or "100")
    
    scanner = FastPortScanner(max_threads=threads)
    scanner.scan_port_range_threaded(target, start, end)

def detailed_report_menu():
    print("🚧 Bu özellik yakında gelecek!")

if __name__ == "__main__":
    show_banner()
    main_menu()
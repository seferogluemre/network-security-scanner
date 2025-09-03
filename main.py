import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from netscout.core.port_scanner import PortScanner
from netscout.core.network_discovery import NetworkDiscovery
from netscout.core.threaded_scanner import FastPortScanner

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

if __name__ == "__main__":
    show_banner()
    main_menu()
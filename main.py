import socket
import sys
from datetime import datetime

def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        return result == 0
    except Exception as e:
        return False

def get_port_service(port):
    services = {
        21: "FTP",
        22: "SSH", 
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        443: "HTTPS",
        993: "IMAPS",
        995: "POP3S",
        3000: "Node.js Dev",
        3001: "React Dev",
        4000: "GraphQL",
        5000: "Flask Dev",
        5432: "PostgreSQL",
        3306: "MySQL",
        3389: "RDP",
        8000: "HTTP Alt",
        8080: "HTTP Proxy",
        9000: "Various",
        6379: "Redis"
    }
    return services.get(port, "Unknown")

def scan_port_range(target_ip, start_port, end_port):
    print(f"\n🎯 Hedef: {target_ip}")
    print(f"📡 Port aralığı: {start_port}-{end_port}")
    print(f"⏰ Tarama başladı: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)
    
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        if scan_port(target_ip, port):
            service = get_port_service(port)
            print(f"✅ Port {port:5d} AÇIK    [{service}]")
            open_ports.append(port)
        else:
            pass
    
    print("-" * 60)
    print(f"📊 Sonuç: {len(open_ports)} açık port bulundu")
    return open_ports

def scan_common_ports(target_ip):
    common_ports = [
        21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 3389,
        3306, 5432, 1433, 27017,
        3000, 3001, 4000, 5000, 8000, 8080, 9000,
        6379, 11211, 5672
    ]
    
    print(f"\n🎯 Hedef: {target_ip}")
    print(f"📡 Yaygın portları taranıyor...")
    print(f"⏰ Tarama başladı: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)
    
    open_ports = []
    
    for port in common_ports:
        if scan_port(target_ip, port):
            service = get_port_service(port)
            print(f"✅ Port {port:5d} AÇIK    [{service}]")
            open_ports.append(port)
    
    print("-" * 60)
    print(f"📊 Sonuç: {len(open_ports)} açık port bulundu")
    return open_ports


if __name__ == "__main__":
    target = "127.0.0.1"  # localhost
    
    print("🔍 Basit Port Scanner v1.5")
    print("=" * 60)
    print("1. Yaygın portları tara")
    print("2. Port aralığı tara (örn: 1-1000)")
    print("3. Tek port tara")
    
    choice = input("\nSeçiminiz (1-3): ").strip()
    
    if choice == "1":
        open_ports = scan_common_ports(target)
        
    elif choice == "2":
        start = int(input("Başlangıç portu: "))
        end = int(input("Bitiş portu: "))
        open_ports = scan_port_range(target, start, end)
        
    elif choice == "3":
        port = int(input("Port numarası: "))
        if scan_port(target, port):
            service = get_port_service(port)
            print(f"✅ Port {port} AÇIK [{service}]")
        else:
            print(f"❌ Port {port} kapalı")
        open_ports = []
    
    else:
        print("❌ Geçersiz seçim!")
        sys.exit(1)
    
    if open_ports:
        print(f"\n🎉 Açık portlar: {open_ports}")
    
    print("\n✨ Tarama tamamlandı!")
import socket
import sys
from datetime import datetime

def scan_port(target_ip,port):
    "Tek bir portu tarar args:target:ip(str) tarancak İP adresi, port(int):tarancak port numarası"

    try:
        socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        socket.settimeout(3)

        result=socket.connect_ex((target_ip,port))

        socket.close()

        return result==0
    except Exception as e:
        return False
        

def scan_common_ports(target_ip):
    "common ports"
    common_ports=[21,22,23,25,53,80,110,443,3000,4000,5000,6379,5432,3306]

    print(f"Target: {target_ip}")
    print(f"Scanning Started.... {datetime.now().strftime('%H:%M:%S')}")
    print("-",* 50)

    open_ports=[]

    for port in common_ports:
        if scan_port(target_ip,port):
            print(f"✅ Port {port} AÇIK")
            open_ports.append(port)
        else:
            print(f"❌ Port {port} kapalı")
    print("-" * 50)
    print(f"📊 Sonuç: {len(open_ports)} açık port bulundu")
    return open_ports

# main program
if __name__ == "__main__":
    # local test
    target = "127.0.0.1"  # localhost
    
    print("🔍 Basit Port Scanner v1.0")
    print("=" * 50)
    
    open_ports = scan_common_ports(target)
    
    if open_ports:
        print(f"\n🎉 Açık portlar: {open_ports}")
    else:
        print("\n Hiç açık port bulunamadı")
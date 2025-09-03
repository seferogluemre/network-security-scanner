# 🛡️ NetScout - Network Security Scanner

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Educational-red.svg)](#-legal-disclaimer)

**NetScout**, ağ güvenliği profesyonelleri ve sistem yöneticileri için geliştirilmiş **Python tabanlı** network tarama ve keşif aracıdır. **Multi-threading** desteği ve **REST API** ile hızlı ve etkili ağ analizi sağlar.

## 🚀 Özellikler

### 🎯 **Core Tarama Modülleri**
- **Port Scanner**: TCP port tarama ve servis tespiti
- **Network Discovery**: Ağdaki aktif cihazları bulma (Ping Sweep)
- **Fast Scanner**: Multi-threading ile hızlandırılmış tarama (10x-50x hızlı)
- **Service Detection**: Açık portlardaki servisleri tanımlama

### 🌐 **REST API Server**
- **Flask** tabanlı RESTful API
- **CORS** desteği ile cross-origin erişim
- **JSON** formatında sonuçlar
- **Health check** ve monitoring endpoint'leri

### 💻 **Kullanıcı Arayüzleri**
- **İnteraktif CLI** menü sistemi
- **API Test Client** (otomatik ve manuel test)
- **Programatik** kullanım için Python modülleri

## 📦 Teknoloji Stack

| Kategori | Teknoloji | Versiyon | Açıklama |
|----------|-----------|----------|----------|
| **Core** | Python | 3.7+ | Ana programlama dili |
| **Network** | socket | built-in | TCP/IP bağlantıları |
| **Threading** | concurrent.futures | built-in | Paralel işlemler |
| **API** | Flask | 2.2+ | REST API server |
| **CORS** | flask-cors | 3.0+ | Cross-origin requests |
| **HTTP** | requests | 2.28+ | API test client |
| **Network Utils** | subprocess | built-in | Ping operations |
| **Data** | ipaddress | built-in | IP/subnet hesaplamaları |

## 🛠️ Kurulum

### **Gereksinimler**
- Python 3.7 veya üzeri
- pip (Python package manager)
- Unix/Linux/macOS (Windows kısmen desteklenir)

### **Hızlı Kurulum**
```bash
# Repo'yu klonla
git clone https://github.com/seferogluemre/network-security-scanner.git
cd netscout-py

# Gereksinimleri kur
pip3 install -r requirements.txt

# Ana programı çalıştır
python3 main.py
```

### **Gereksinimler Detay**
```bash
# Core dependencies
pip3 install flask flask-cors requests

# Optional (development)
pip3 install pytest black flake8
```

## 🎮 Kullanım Rehberi

### **1. 🖥️ CLI (Command Line Interface)**

#### Temel Kullanım
```bash
# Ana menüyü başlat
python3 main.py

# Menü seçenekleri:
# 1. 🎯 Port Tarama - Belirli portları tara
# 2. 🌐 Ağ Keşfi - Ağdaki cihazları bul  
# 3. ⚡ Hızlı Tarama - Multi-threading ile hızlı tarama
# 4. 📊 Detaylı Rapor - Gelişmiş analiz (yakında)
```

#### Port Tarama Örnekleri
```bash
# Yaygın portları tara
Hedef IP: 192.168.1.1
Tarama türü: 1 (Yaygın portlar)

# Özel port aralığı
Hedef IP: 10.0.0.1  
Tarama türü: 2 (Port aralığı)
Başlangıç: 1
Bitiş: 1000

# Manuel port listesi
Hedef IP: example.com
Tarama türü: 3 (Özel portlar)
Portlar: 80,443,22,21,3000
```

### **2. 🌐 REST API Server**

#### API Server'ı Başlat
```bash
python3 api/server.py

# Output:
# 🚀 NetScout API Server Başlatılıyor...
# 🌐 URL: http://localhost:8080
# ✨ Ctrl+C ile durdurun
```

#### API Endpoint'leri

| Method | Endpoint | Açıklama | Parametreler |
|--------|----------|----------|--------------|
| `GET` | `/` | Ana sayfa ve endpoint listesi | - |
| `GET` | `/api/health` | Sağlık kontrolü | - |
| `POST` | `/api/scan/ports` | Port tarama | `target`, `ports` |
| `POST` | `/api/scan/fast` | Hızlı tarama | `target`, `start_port`, `end_port`, `threads` |
| `POST` | `/api/network/discover` | Ağ keşfi | `network` (opsiyonel) |
| `GET` | `/api/scan/simple` | Basit tarama | `target` (query param) |

#### API Kullanım Örnekleri

**Port Tarama (POST)**
```bash
curl -X POST http://localhost:8080/api/scan/ports \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.1",
    "ports": [80, 443, 22, 21, 3000]
  }'
```

**Hızlı Tarama (POST)**
```bash
curl -X POST http://localhost:8080/api/scan/fast \
  -H "Content-Type: application/json" \
  -d '{
    "target": "127.0.0.1",
    "start_port": 1,
    "end_port": 1000,
    "threads": 100
  }'
```

**Basit Tarama (GET)**
```bash
curl "http://localhost:8080/api/scan/simple?target=google.com"
```

### **3. 🧪 API Test Client**

#### Otomatik Test Suite
```bash
# Tüm endpoint'leri test et
python3 api/test_client.py --auto
```

#### İnteraktif Test
```bash
# Manuel test menüsü
python3 api/test_client.py

# Test menüsü:
# 1. 🎯 Port Tarama
# 2. ⚡ Hızlı Tarama  
# 3. 🌐 Ağ Keşfi
# 4. 🔍 Basit Tarama
# 5. 🩺 Sağlık Kontrolü
```

### **4. 📚 Programatik Kullanım**

#### Python Modül Olarak
```python
# Port scanner
from core.port_scanner import PortScanner

scanner = PortScanner()
results = scanner.scan_ports("192.168.1.1", [80, 443, 22])
print(f"Açık portlar: {results['open_ports']}")

# Hızlı tarama
from core.threaded_scanner import FastPortScanner

fast_scanner = FastPortScanner(max_threads=100)
open_ports = fast_scanner.scan_port_range_threaded("10.0.0.1", 1, 1000)
print(f"Bulunan portlar: {open_ports}")

# Ağ keşfi
from core.network_discovery import NetworkDiscovery

discovery = NetworkDiscovery()
alive_hosts = discovery.discover_network("192.168.1.0/24")
print(f"Canlı hostlar: {alive_hosts}")
```

## 👥 Kimler Kullanabilir?

### ✅ **Uygun Kullanıcılar**
- **Siber Güvenlik Uzmanları** - Penetration testing ve vulnerability assessment
- **Sistem Yöneticileri** - Network monitoring ve troubleshooting
- **DevOps Engineers** - Infrastructure monitoring ve health checks
- **Öğrenciler** - Cybersecurity ve network programming öğrenimi
- **Araştırmacılar** - Network security research ve analiz
- **IT Profesyonelleri** - Network inventory ve documentation

### 🎓 **Eğitim Amaçlı**
- Network programming öğrenimi
- Python socket programming
- Multi-threading concepts
- REST API development
- Cybersecurity fundamentals

### 💼 **Profesyonel Kullanım**
- **Internal network auditing**
- **Service discovery** ve inventory
- **Network troubleshooting**
- **Automated monitoring** entegrasyonu
- **CI/CD pipeline** health checks

## 📊 Performans

### **Hız Karşılaştırması**
| Tarama Türü | 100 Port | 1000 Port | 10000 Port |
|--------------|----------|-----------|------------|
| **Sıralı** | ~100 saniye | ~1000 saniye | ~10000 saniye |
| **Threading** | ~3-5 saniye | ~10-15 saniye | ~30-60 saniye |
| **Hız Artışı** | **20x-30x** | **60x-100x** | **150x-300x** |

### **Kaynak Kullanımı**
- **CPU**: Orta (multi-threading)
- **Memory**: Düşük (~50-100MB)
- **Network**: Orta (paralel bağlantılar)
- **Disk**: Minimal (log files)

## 🏗️ Proje Yapısı

```
netscout-py/
├── 📄 main.py                    # Ana CLI menü
├── 📄 requirements.txt           # Python gereksinimleri
├── 📁 core/                      # Temel tarama modülleri
│   ├── port_scanner.py           # Port tarama motoru
│   ├── network_discovery.py      # Ağ keşif modülü
│   └── threaded_scanner.py       # Multi-thread tarama
├── 📁 api/                       # REST API modülleri
│   ├── server.py                 # Flask API server
│   └── test_client.py            # API test client
├── 📁 utils/                     # Yardımcı fonksiyonlar
│   ├── logger.py                 # Logging utilities
│   └── network_utils.py          # Network helper functions
├── 📁 config/                    # Konfigürasyon
│   └── settings.py               # Uygulama ayarları
└── 📁 tests/                     # Test dosyaları
    └── test_scanner.py           # Unit testler
```

## 🔧 Gelişmiş Konfigürasyon

### **Environment Variables**
```bash
export NETSCOUT_API_PORT=8080
export NETSCOUT_LOG_LEVEL=INFO
export NETSCOUT_MAX_THREADS=100
export NETSCOUT_TIMEOUT=5
```

### **Custom Settings**
```python
# config/settings.py dosyasını düzenle
DEFAULT_TIMEOUT = 3
MAX_THREADS = 100
API_PORT = 8080
LOG_LEVEL = "INFO"
```

## 🧪 Test Etme

### **Unit Tests**
```bash
# Test suite'i çalıştır
python -m pytest tests/

# Coverage report
python -m pytest --cov=core tests/
```

### **API Tests**
```bash
# API server'ı başlat (terminal 1)
python3 api/server.py

# Test client'ı çalıştır (terminal 2)  
python3 api/test_client.py --auto
```

## 🚨 Legal Disclaimer

### ⚠️ **ÖNEMLİ UYARILAR**

Bu araç **sadece aşağıdaki durumlarda** kullanılmalıdır:

✅ **İzin Verilen Kullanımlar:**
- **Kendi ağınızda** test ve monitoring
- **Yetkiniz olan sistemlerde** güvenlik testi
- **Eğitim amaçlı** öğrenme ve araştırma
- **Kurumsal ortamda** network auditing (izin ile)
- **Penetration testing** (resmi sözleşme ile)

❌ **Yasak Kullanımlar:**
- **İzinsiz ağ tarama** (illegal)
- **Başkalarının sistemlerine** saldırı
- **DDoS** veya **DoS** saldırıları
- **Kötü niyetli** aktiviteler
- **Gizlilik ihlali** amaçlı kullanım

### 📜 **Yasal Sorumluluk**

- Bu aracı kullanarak **tüm yasal sorumluluk** kullanıcıya aittir
- Yerel ve uluslararası **cybersecurity yasalarına** uyun
- **Etik hacking** prensiplerini benimseyin
- Şüpheli durumlarda **hukuki danışmanlık** alın

### 🛡️ **Güvenlik İlkeleri**

1. **Responsible Disclosure** - Bulduğunuz güvenlik açıklarını sorumlu şekilde bildirin
2. **No Harm Principle** - Sistemlere zarar vermeyin
3. **Permission First** - Önce izin alın, sonra test edin
4. **Educational Purpose** - Öğrenme amaçlı kullanın

## 🤝 Katkıda Bulunma

### **Geliştirme Süreci**
```bash
# Fork & clone
git clone https://github.com/yourusername/netscout-py.git
cd netscout-py

# Development branch oluştur
git checkout -b feature/new-feature

# Değişiklikleri commit et
git add .
git commit -m "feat: add new scanning feature"

# Pull request gönder
git push origin feature/new-feature
```

### **Code Style**
```bash
# Code formatting
black *.py core/*.py api/*.py

# Linting
flake8 --max-line-length=88 .

# Type checking (optional)
mypy core/ api/
```

## 📞 Destek ve İletişim

### **Sorun Bildirimi**
- 🐛 **Bug Reports**: GitHub Issues
- 💡 **Feature Requests**: GitHub Discussions  
- 📖 **Documentation**: Wiki sayfaları

### **Topluluk**
- 💬 **Discord**: [NetScout Community](#)
- 📧 **Email**: security@netscout.dev
- 🐦 **Twitter**: [@NetScoutTool](#)

## 📈 Roadmap

### **v1.1.0 (Yakında)**
- [ ] **Web Dashboard** - Modern web arayüzü
- [ ] **Database Integration** - Scan history
- [ ] **Scheduled Scans** - Otomatik tarama
- [ ] **Email Notifications** - Alert sistemi

### **v1.2.0 (Gelecek)**
- [ ] **Docker Support** - Containerization
- [ ] **Kubernetes Integration** - Cloud-native deployment
- [ ] **Advanced Reporting** - PDF/HTML raporlar
- [ ] **Plugin System** - Genişletilebilir mimari

### **v2.0.0 (Uzun Vadeli)**
- [ ] **Machine Learning** - Anomaly detection
- [ ] **Distributed Scanning** - Multi-node support
- [ ] **Real-time Monitoring** - WebSocket streaming
- [ ] **Mobile App** - iOS/Android client

## 📄 License

Bu proje **MIT License** altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

```
MIT License - Özgürce kullanabilir, değiştirebilir ve dağıtabilirsiniz.
Tek şart: Telif hakkı bildirimini korumanız.
```

## 🙏 Teşekkürler

### **Katkıda Bulunanlar**
- [@emreseferoglu](https://github.com/emreseferoglu) - Proje kurucusu
- **Python Community** - Güçlü ecosystem
- **Flask Team** - Mükemmel web framework
- **Open Source Community** - İlham ve destek

### **Kullanılan Teknolojiler**
- **Python** - Güçlü ve esnek programlama dili
- **Flask** - Minimal ve etkili web framework
- **Socket Programming** - Network communication
- **Threading** - Paralel işlem desteği

---

<div align="center">

**🛡️ NetScout ile ağlarınızı güvenle keşfedin!**

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/netscout-py?style=social)](https://github.com/yourusername/netscout-py/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/yourusername/netscout-py?style=social)](https://github.com/yourusername/netscout-py/network/members)

**Made with ❤️ by [Emre Seferoğlu](https://github.com/emreseferoglu)**

</div>

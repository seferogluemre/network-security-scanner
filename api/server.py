from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.port_scanner import PortScanner
from core.network_discovery import NetworkDiscovery, get_local_network
from core.threaded_scanner import FastPortScanner

app = Flask(__name__)
CORS(app)  

API_VERSION = "1.0.0"
SERVICE_NAME = "NetScout API"

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'service': SERVICE_NAME,
        'version': API_VERSION,
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'port_scan': '/api/scan/ports (POST)',
            'fast_scan': '/api/scan/fast (POST)',
            'network_discovery': '/api/network/discover (POST)'
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': SERVICE_NAME,
        'version': API_VERSION,
        'uptime': 'running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/scan/ports', methods=['POST'])
def scan_ports_api():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'JSON body gerekli'
            }), 400
        
        target_ip = data.get('target', '127.0.0.1')
        ports = data.get('ports', [80, 443, 22, 21, 3000])
        
        print(f"🎯 Port tarama: {target_ip} -> {ports}")
        
        scanner = PortScanner()
        results = scanner.scan_ports(target_ip, ports)
        
        return jsonify({
            'success': True,
            'data': results,
            'message': f'{len(results["open_ports"])} açık port bulundu',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Port tarama hatası: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scan/fast', methods=['POST'])
def fast_scan_api():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'JSON body gerekli'
            }), 400
        
        target_ip = data.get('target', '127.0.0.1')
        start_port = data.get('start_port', 1)
        end_port = data.get('end_port', 100)
        max_threads = data.get('threads', 50)
        
        print(f"⚡ Hızlı tarama: {target_ip} -> {start_port}-{end_port} ({max_threads} threads)")
        
        scanner = FastPortScanner(max_threads=max_threads)
        open_ports = scanner.scan_port_range_threaded(target_ip, start_port, end_port)
        
        return jsonify({
            'success': True,
            'data': {
                'target': target_ip,
                'port_range': f'{start_port}-{end_port}',
                'open_ports': open_ports,
                'total_found': len(open_ports),
                'threads_used': max_threads
            },
            'message': f'{len(open_ports)} açık port bulundu',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Hızlı tarama hatası: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/network/discover', methods=['POST'])
def network_discovery_api():
    try:
        data = request.get_json() or {}
        network = data.get('network', None)
        
        if not network:
            network, local_ip = get_local_network()
            print(f"🏠 Otomatik ağ tespiti: {network}")
        else:
            print(f"🌐 Manuel ağ tarama: {network}")
        
        discovery = NetworkDiscovery()
        alive_hosts = discovery.discover_network(network)
        
        return jsonify({
            'success': True,
            'data': {
                'network': network,
                'alive_hosts': alive_hosts,
                'total_hosts': len(alive_hosts)
            },
            'message': f'{len(alive_hosts)} canlı host bulundu',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ Ağ keşfi hatası: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scan/simple', methods=['GET'])
def simple_scan():
    target = request.args.get('target', '127.0.0.1')
    
    try:
        scanner = PortScanner()
        common_ports = [21, 22, 23, 80, 443, 3000]
        results = scanner.scan_ports(target, common_ports)
        
        return jsonify({
            'success': True,
            'target': target,
            'open_ports': [p['port'] for p in results['open_ports']],
            'total': len(results['open_ports'])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 NetScout API Server Başlatılıyor...")
    print("=" * 50)
    print(f"📡 Servis: {SERVICE_NAME}")
    print(f"🔢 Versiyon: {API_VERSION}")
    print(f"🌐 URL: http://localhost:5000")
    print("\n📋 Endpoint'ler:")
    print("   GET  /                    - Ana sayfa")
    print("   GET  /api/health          - Sağlık kontrolü")
    print("   POST /api/scan/ports      - Port tarama")
    print("   POST /api/scan/fast       - Hızlı tarama")  
    print("   POST /api/network/discover - Ağ keşfi")
    print("   GET  /api/scan/simple     - Basit tarama")
    print("\n✨ Ctrl+C ile durdurun")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

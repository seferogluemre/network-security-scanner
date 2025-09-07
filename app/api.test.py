#!/usr/bin/env python3
"""
NetScout Enterprise API Test Script
Tüm akışı log'larla görmek için
"""

import requests
import json
import time
from datetime import datetime

class EnterpriseAPITester:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
    
    def print_separator(self, title):
        print("\n" + "="*60)
        print(f"🧪 {title}")
        print("="*60)
    
    def print_response(self, response, title="Response"):
        print(f"\n📊 {title}:")
        print(f"Status: {response.status_code}")
        try:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(response.text)
    
    def test_health_check(self):
        """Test health endpoint"""
        self.print_separator("HEALTH CHECK")
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            self.print_response(response, "Health Check")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False
    
    def test_api_info(self):
        """Test API info"""
        self.print_separator("API INFO")
        
        try:
            response = self.session.get(f"{self.base_url}/api/info")
            self.print_response(response, "API Info")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ API info failed: {e}")
            return False
    
    def test_port_scan(self):
        """Test port scanning with logs"""
        self.print_separator("PORT SCAN TEST")
        
        payload = {
            "target": "127.0.0.1",
            "ports": [22, 80, 443, 3000, 8080],
            "timeout": 2
        }
        
        print(f"📨 Sending request: {json.dumps(payload, indent=2)}")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v2/scan/ports",
                json=payload
            )
            self.print_response(response, "Port Scan Result")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Port scan failed: {e}")
            return False
    
    def test_fast_scan(self):
        """Test fast scanning"""
        self.print_separator("FAST SCAN TEST")
        
        payload = {
            "target": "127.0.0.1",
            "start_port": 8070,
            "end_port": 8090,
            "threads": 10,
            "timeout": 1
        }
        
        print(f"📨 Fast scan request: {json.dumps(payload, indent=2)}")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/v2/scan/fast",
                json=payload
            )
            self.print_response(response, "Fast Scan Result")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Fast scan failed: {e}")
            return False
    
    def test_scan_history(self):
        """Test scan history"""
        self.print_separator("SCAN HISTORY")
        
        try:
            response = self.session.get(f"{self.base_url}/api/v2/scan/history?limit=5")
            self.print_response(response, "Scan History")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Scan history failed: {e}")
            return False
    
    def test_scan_stats(self):
        """Test scan statistics"""
        self.print_separator("SCAN STATISTICS")
        
        try:
            response = self.session.get(f"{self.base_url}/api/v2/scan/stats")
            self.print_response(response, "Scan Statistics")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Scan stats failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run all tests and show flow"""
        print("🚀 NetScout Enterprise API Test Suite")
        print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("API Info", self.test_api_info),
            ("Port Scan", self.test_port_scan),
            ("Fast Scan", self.test_fast_scan),
            ("Scan History", self.test_scan_history),
            ("Scan Statistics", self.test_scan_stats)
        ]
        
        results = []
        for test_name, test_func in tests:
            print(f"\n🔄 Running: {test_name}")
            success = test_func()
            results.append((test_name, success))
            time.sleep(1)  # Logs'ları görebilmek için
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        passed = 0
        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status} - {test_name}")
            if success:
                passed += 1
        
        print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
        print(f"⏰ Completed at: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    tester = EnterpriseAPITester()
    tester.run_all_tests()
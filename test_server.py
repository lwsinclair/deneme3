"""
Test the weather server
"""

import json
from urllib.request import urlopen
from urllib.error import URLError

def test_weather_api():
    """Test the weather API"""
    try:
        print("Testing weather server...")

        # Test server info
        print("\n1. Testing server info:")
        with urlopen("http://localhost:8080/", timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(json.dumps(data, ensure_ascii=False, indent=2))

        # Test weather endpoint
        print("\n2. Testing weather for Istanbul:")
        with urlopen("http://localhost:8080/weather?city=Istanbul", timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(json.dumps(data, ensure_ascii=False, indent=2))

        # Test MCP endpoint
        print("\n3. Testing MCP tools/list:")
        import urllib.request

        mcp_request = {
            "method": "tools/list",
            "params": {}
        }

        req = urllib.request.Request(
            "http://localhost:8080/mcp",
            data=json.dumps(mcp_request).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(json.dumps(data, ensure_ascii=False, indent=2))

        # Test MCP get_weather tool
        print("\n4. Testing MCP get_weather tool:")
        mcp_request = {
            "method": "tools/call",
            "params": {
                "name": "get_weather",
                "arguments": {
                    "city": "İstanbul"
                }
            }
        }

        req = urllib.request.Request(
            "http://localhost:8080/mcp",
            data=json.dumps(mcp_request).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        with urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(json.dumps(data, ensure_ascii=False, indent=2))

        print("\n✅ Tüm testler başarılı!")

    except URLError as e:
        print(f"❌ Bağlantı hatası: {e}")
        print("Sunucunun çalıştığından emin olun: python simple_weather.py")
    except Exception as e:
        print(f"❌ Test hatası: {e}")

if __name__ == "__main__":
    test_weather_api()

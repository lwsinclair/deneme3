"""
Simple Weather MCP Server - Minimal implementation
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from urllib.error import URLError
import threading
import time

class WeatherHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        print(f"GET request: {self.path} -> parsed path: {parsed_path.path}")

        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "name": "Weather MCP Server",
                "version": "1.0.0",
                "description": "Simple weather server using wttr.in",
                "endpoints": [
                    "GET / - Server info",
                    "GET /weather?city=<city> - Get weather",
                    "POST /mcp - MCP protocol endpoint"
                ]
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

        elif parsed_path.path == '/weather':
            query_params = parse_qs(parsed_path.query)
            city = query_params.get('city', [''])[0]

            if not city:
                self.send_error(400, "City parameter required")
                return

            weather_data = self.get_weather(city)

            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(weather_data, ensure_ascii=False).encode('utf-8'))

        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/mcp':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                request_data = json.loads(post_data.decode('utf-8'))
                response = self.handle_mcp_request(request_data)

                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))

            except Exception as e:
                self.send_error(500, f"Error processing request: {str(e)}")
        else:
            self.send_error(404, "Not found")

    def get_weather(self, city):
        """Get weather data from wttr.in"""
        try:
            url = f"https://wttr.in/{city}?format=j1"

            with urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            current = data.get('current_condition', [{}])[0]
            location = data.get('nearest_area', [{}])[0]

            result = {
                "city": city,
                "location": {
                    "area_name": location.get('areaName', [{}])[0].get('value', city),
                    "country": location.get('country', [{}])[0].get('value', 'Unknown'),
                    "region": location.get('region', [{}])[0].get('value', 'Unknown')
                },
                "current_weather": {
                    "temperature_c": current.get('temp_C', 'N/A'),
                    "temperature_f": current.get('temp_F', 'N/A'),
                    "feels_like_c": current.get('FeelsLikeC', 'N/A'),
                    "humidity": current.get('humidity', 'N/A'),
                    "description": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                    "wind_speed_kmh": current.get('windspeedKmph', 'N/A'),
                    "pressure": current.get('pressure', 'N/A')
                },
                "status": "success"
            }

            return result

        except URLError as e:
            return {
                "city": city,
                "error": f"Hava durumu alınamadı: Bağlantı hatası - {str(e)}",
                "status": "error"
            }
        except Exception as e:
            return {
                "city": city,
                "error": f"Hava durumu alınamadı: {str(e)}",
                "status": "error"
            }

    def handle_mcp_request(self, request_data):
        """Handle MCP protocol requests"""
        method = request_data.get('method', '')
        params = request_data.get('params', {})

        if method == 'initialize':
            return {
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "weather",
                        "version": "1.0.0"
                    }
                }
            }

        elif method == 'tools/list':
            return {
                "result": {
                    "tools": [{
                        "name": "get_weather",
                        "description": "Get current weather information for a specified city",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "city": {
                                    "type": "string",
                                    "description": "Name of the city to get weather for"
                                }
                            },
                            "required": ["city"]
                        }
                    }]
                }
            }

        elif method == 'tools/call':
            tool_name = params.get('name')
            arguments = params.get('arguments', {})

            if tool_name == 'get_weather':
                city = arguments.get('city')
                if not city:
                    return {
                        "error": {
                            "code": -32602,
                            "message": "Invalid parameters: city is required"
                        }
                    }

                weather_data = self.get_weather(city)
                return {
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": json.dumps(weather_data, ensure_ascii=False, indent=2)
                        }]
                    }
                }
            else:
                return {
                    "error": {
                        "code": -32601,
                        "message": f"Unknown tool: {tool_name}"
                    }
                }

        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Unknown method: {method}"
                }
            }

def run_server(port=8080):
    """Run the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, WeatherHandler)
    print(f"Weather MCP Server başlatıldı: http://localhost:{port}")
    print("Kullanım örnekleri:")
    print(f"  GET  http://localhost:{port}/weather?city=İstanbul")
    print(f"  POST http://localhost:{port}/mcp")
    print("\nSunucuyu durdurmak için Ctrl+C tuşlayın")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruluyor...")
        httpd.shutdown()

if __name__ == "__main__":
    run_server()

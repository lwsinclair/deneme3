"""
MCP Configuration for Weather Application
"""

from typing import Dict, Any, List
import requests
import json


class WeatherTool:
    """Weather tool implementation for MCP"""
    
    @staticmethod
    def get_weather(city: str) -> Dict[str, Any]:
        """
        Get weather information for a given city using wttr.in service
        
        Args:
            city (str): Name of the city
            
        Returns:
            Dict[str, Any]: Weather information or error message
        """
        try:
            # wttr.in API endpoint with JSON format
            url = f"https://wttr.in/{city}?format=j1"
            
            # Make request with timeout
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse JSON response
            weather_data = response.json()
            
            # Extract relevant information
            current = weather_data.get('current_condition', [{}])[0]
            location = weather_data.get('nearest_area', [{}])[0]
            
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
                    "feels_like_f": current.get('FeelsLikeF', 'N/A'),
                    "humidity": current.get('humidity', 'N/A'),
                    "description": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                    "wind_speed_kmh": current.get('windspeedKmph', 'N/A'),
                    "wind_direction": current.get('winddir16Point', 'N/A'),
                    "pressure": current.get('pressure', 'N/A'),
                    "visibility": current.get('visibility', 'N/A')
                },
                "status": "success"
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            return {
                "city": city,
                "error": f"Hava durumu alınamadı: Bağlantı hatası - {str(e)}",
                "status": "error"
            }
        except json.JSONDecodeError as e:
            return {
                "city": city,
                "error": f"Hava durumu alınamadı: Veri formatı hatası - {str(e)}",
                "status": "error"
            }
        except Exception as e:
            return {
                "city": city,
                "error": f"Hava durumu alınamadı: Beklenmeyen hata - {str(e)}",
                "status": "error"
            }


# MCP Tool definitions
MCP_TOOLS = [
    {
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
    }
]

# MCP Server configuration
MCP_CONFIG = {
    "name": "weather",
    "version": "1.0.0",
    "description": "Weather information service using wttr.in API",
    "tools": MCP_TOOLS
}

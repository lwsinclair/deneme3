"""
Simple test for weather functionality
"""

import requests
import json

def test_weather(city="İstanbul"):
    """Test weather API directly"""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        print(f"Testing weather for: {city}")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            current = data.get('current_condition', [{}])[0]
            location = data.get('nearest_area', [{}])[0]
            
            result = {
                "city": city,
                "location": location.get('areaName', [{}])[0].get('value', city),
                "temperature": current.get('temp_C', 'N/A'),
                "description": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                "humidity": current.get('humidity', 'N/A')
            }
            
            print("Weather data:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return result
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("=== Weather API Test ===")
    test_weather("İstanbul")
    print("\n=== Test Complete ===")

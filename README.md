[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/iremaltunay55-deneme3-badge.png)](https://mseep.ai/app/iremaltunay55-deneme3)

# Weather MCP Server

Bu proje, Model Context Protocol (MCP) kullanarak hava durumu bilgisi sağlayan bir FastAPI uygulamasıdır.

## Özellikler

- **MCP Protokolü**: Model Context Protocol standardına uygun
- **FastAPI**: Modern, hızlı web framework
- **Hava Durumu API**: wttr.in servisini kullanarak gerçek zamanlı hava durumu
- **Hata Yönetimi**: Kapsamlı hata yakalama ve kullanıcı dostu mesajlar

## Kurulum

1. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

2. **Sunucuyu başlatın:**
```bash
python main.py
```

Sunucu `http://localhost:8000` adresinde çalışmaya başlayacaktır.

## Kullanım

### MCP Protokolü ile

MCP protokolü üzerinden `/mcp` endpoint'ini kullanın:

```json
POST /mcp
{
    "method": "tools/call",
    "params": {
        "name": "get_weather",
        "arguments": {
            "city": "İstanbul"
        }
    }
}
```

### Direkt API Kullanımı

Test amaçlı direkt endpoint'ler:

```bash
# GET isteği
curl http://localhost:8000/weather/İstanbul

# POST isteği
curl -X POST http://localhost:8000/weather \
  -H "Content-Type: application/json" \
  -d '{"name": "get_weather", "arguments": {"city": "İstanbul"}}'
```

## API Endpoints

- `GET /` - Sunucu bilgileri
- `GET /health` - Sağlık kontrolü
- `POST /mcp` - Ana MCP protokol handler
- `GET /weather/{city}` - Basit hava durumu sorgusu
- `POST /weather` - Detaylı hava durumu sorgusu

## Yanıt Formatı

Başarılı yanıt örneği:
```json
{
    "city": "İstanbul",
    "location": {
        "area_name": "Istanbul",
        "country": "Turkey",
        "region": "Istanbul"
    },
    "current_weather": {
        "temperature_c": "15",
        "temperature_f": "59",
        "feels_like_c": "14",
        "feels_like_f": "57",
        "humidity": "72",
        "description": "Partly cloudy",
        "wind_speed_kmh": "11",
        "wind_direction": "NW",
        "pressure": "1013",
        "visibility": "10"
    },
    "status": "success"
}
```

Hata yanıtı örneği:
```json
{
    "city": "GeçersizŞehir",
    "error": "Hava durumu alınamadı: Bağlantı hatası - 404 Client Error",
    "status": "error"
}
```

## Geliştirme

Sunucuyu geliştirme modunda çalıştırmak için:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Dosya Yapısı

- `main.py` - Ana FastAPI uygulaması ve MCP sunucu
- `mcp_config.py` - MCP konfigürasyonu ve weather tool implementasyonu
- `requirements.txt` - Python bağımlılıkları
- `README.md` - Bu dosya

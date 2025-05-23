"""
Weather MCP Server
A Model Context Protocol server that provides weather information using wttr.in API
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from mcp_config import WeatherTool, MCP_CONFIG, MCP_TOOLS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Weather MCP Server",
    description="Model Context Protocol server for weather information",
    version="1.0.0"
)

# Pydantic models for request/response
class MCPRequest(BaseModel):
    method: str
    params: Optional[Dict[str, Any]] = None

class MCPResponse(BaseModel):
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class ToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

# Weather tool instance
weather_tool = WeatherTool()

@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "name": "Weather MCP Server",
        "version": "1.0.0",
        "description": "Model Context Protocol server for weather information",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": asyncio.get_event_loop().time()}

@app.post("/mcp")
async def mcp_handler(request: MCPRequest):
    """Main MCP protocol handler"""
    try:
        method = request.method
        params = request.params or {}
        
        if method == "initialize":
            return MCPResponse(result={
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": MCP_CONFIG["name"],
                    "version": MCP_CONFIG["version"]
                }
            })
        
        elif method == "tools/list":
            return MCPResponse(result={"tools": MCP_TOOLS})
        
        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if tool_name == "get_weather":
                city = arguments.get("city")
                if not city:
                    return MCPResponse(error={
                        "code": -32602,
                        "message": "Invalid parameters: city is required"
                    })
                
                result = weather_tool.get_weather(city)
                return MCPResponse(result={
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                })
            else:
                return MCPResponse(error={
                    "code": -32601,
                    "message": f"Unknown tool: {tool_name}"
                })
        
        else:
            return MCPResponse(error={
                "code": -32601,
                "message": f"Unknown method: {method}"
            })
    
    except Exception as e:
        logger.error(f"Error handling MCP request: {e}")
        return MCPResponse(error={
            "code": -32603,
            "message": f"Internal error: {str(e)}"
        })

@app.post("/weather")
async def get_weather_direct(request: ToolCallRequest):
    """Direct weather endpoint for testing"""
    try:
        if request.name != "get_weather":
            raise HTTPException(status_code=400, detail="Invalid tool name")
        
        city = request.arguments.get("city")
        if not city:
            raise HTTPException(status_code=400, detail="City parameter is required")
        
        result = weather_tool.get_weather(city)
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error in direct weather endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/weather/{city}")
async def get_weather_simple(city: str):
    """Simple GET endpoint for weather"""
    try:
        result = weather_tool.get_weather(city)
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Error in simple weather endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

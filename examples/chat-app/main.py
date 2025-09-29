"""
AI Chat Application Example
Demonstrates multi-cloud AI deployment with RAG and MCP
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging
import os
from datetime import datetime

# Import our AI services
import sys
sys.path.append('../../src')

from rag.system import RAGSystem, create_chroma_rag
from mcp.server import MCPClient
from common.config import Settings

logger = logging.getLogger(__name__)

app = FastAPI(title="AI Chat Application", version="1.0.0")

# Pydantic models
class ChatMessage(BaseModel):
    id: str
    message: str
    timestamp: datetime
    is_user: bool
    sources: Optional[List[str]] = None

class ChatRequest(BaseModel):
    message: str
    use_rag: bool = True
    use_agents: bool = False

class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []
    processing_time: float
    model_used: str

# Global services
rag_system: Optional[RAGSystem] = None
mcp_client: Optional[MCPClient] = None
chat_sessions: Dict[str, List[ChatMessage]] = {}

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Connection closed, remove it
                self.active_connections.remove(connection)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    """Initialize AI services on startup"""
    global rag_system, mcp_client
    
    logger.info("Initializing AI Chat Application...")
    
    try:
        # Initialize RAG system
        rag_system = await create_chroma_rag("chat_documents")
        
        # Initialize MCP client
        mcp_client = MCPClient("http://localhost:8080/mcp")
        await mcp_client.connect()
        
        # Add some sample documents to RAG system
        sample_docs = [
            {
                "content": "Full-Stack AI Apps is a comprehensive framework for deploying AI applications across multiple cloud platforms including AWS, GCP, Azure, and Vercel.",
                "metadata": {"source": "project_overview.txt", "type": "documentation"}
            },
            {
                "content": "The system supports RAG (Retrieval Augmented Generation) which combines vector search with language models for enhanced AI responses.",
                "metadata": {"source": "rag_info.txt", "type": "technical"}
            },
            {
                "content": "Model Context Protocol (MCP) is a standardized way for AI models to interact with various data sources and tools.",
                "metadata": {"source": "mcp_explanation.txt", "type": "technical"}
            }
        ]
        
        await rag_system.add_documents(sample_docs)
        
        logger.info("AI services initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize AI services: {e}")

@app.get("/")
async def get_chat_interface():
    """Serve the chat interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Full-Stack AI Chat</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .chat-container {
                width: 800px;
                height: 600px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
            }
            .chat-header {
                background: #4A90E2;
                color: white;
                padding: 20px;
                border-radius: 10px 10px 0 0;
                text-align: center;
            }
            .chat-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f8f9fa;
            }
            .message {
                margin: 10px 0;
                padding: 10px 15px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .user-message {
                background: #007bff;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            .ai-message {
                background: #e9ecef;
                color: #333;
                margin-right: auto;
            }
            .chat-input-container {
                padding: 20px;
                background: white;
                border-radius: 0 0 10px 10px;
                border-top: 1px solid #dee2e6;
            }
            .chat-input {
                width: 100%;
                padding: 12px;
                border: 2px solid #dee2e6;
                border-radius: 25px;
                outline: none;
                font-size: 14px;
            }
            .chat-input:focus {
                border-color: #007bff;
            }
            .send-button {
                background: #007bff;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 25px;
                margin-left: 10px;
                cursor: pointer;
            }
            .send-button:hover {
                background: #0056b3;
            }
            .options {
                display: flex;
                gap: 15px;
                margin-bottom: 10px;
                align-items: center;
            }
            .checkbox-container {
                display: flex;
                align-items: center;
                gap: 5px;
            }
            .sources {
                font-size: 12px;
                color: #666;
                margin-top: 5px;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h1>🤖 Full-Stack AI Chat</h1>
                <p>Powered by Multi-Cloud AI • RAG • MCP • Agents</p>
            </div>
            <div class="chat-messages" id="messages"></div>
            <div class="chat-input-container">
                <div class="options">
                    <div class="checkbox-container">
                        <input type="checkbox" id="useRag" checked>
                        <label for="useRag">Use RAG</label>
                    </div>
                    <div class="checkbox-container">
                        <input type="checkbox" id="useAgents">
                        <label for="useAgents">Use Agents</label>
                    </div>
                </div>
                <div style="display: flex;">
                    <input type="text" class="chat-input" id="messageInput" placeholder="Ask me anything about Full-Stack AI...">
                    <button class="send-button" onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>

        <script>
            const ws = new WebSocket(`ws://localhost:8000/ws`);
            const messages = document.getElementById('messages');
            const messageInput = document.getElementById('messageInput');

            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                addMessage(data.message, false, data.sources);
            };

            function addMessage(message, isUser, sources = []) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
                messageDiv.innerHTML = message;
                
                if (sources && sources.length > 0) {
                    const sourcesDiv = document.createElement('div');
                    sourcesDiv.className = 'sources';
                    sourcesDiv.innerHTML = `Sources: ${sources.join(', ')}`;
                    messageDiv.appendChild(sourcesDiv);
                }
                
                messages.appendChild(messageDiv);
                messages.scrollTop = messages.scrollHeight;
            }

            function sendMessage() {
                const message = messageInput.value.trim();
                if (message) {
                    addMessage(message, true);
                    
                    const request = {
                        message: message,
                        use_rag: document.getElementById('useRag').checked,
                        use_agents: document.getElementById('useAgents').checked
                    };
                    
                    ws.send(JSON.stringify(request));
                    messageInput.value = '';
                }
            }

            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            // Add welcome message
            addMessage('Welcome to Full-Stack AI Chat! I can help you with questions about multi-cloud AI deployment, RAG systems, MCP, and more. Try asking me something!', false);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            request = json.loads(data)
            
            # Process the chat request
            chat_request = ChatRequest(**request)
            response = await process_chat_message(chat_request)
            
            # Send response back to client
            await manager.send_personal_message(
                json.dumps({
                    "message": response.response,
                    "sources": response.sources,
                    "processing_time": response.processing_time,
                    "model_used": response.model_used
                }),
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_api(request: ChatRequest):
    """REST API endpoint for chat"""
    return await process_chat_message(request)

async def process_chat_message(request: ChatRequest) -> ChatResponse:
    """Process incoming chat message with AI services"""
    start_time = asyncio.get_event_loop().time()
    
    try:
        response_text = ""
        sources = []
        model_used = "default"
        
        if request.use_rag and rag_system:
            # Use RAG system for enhanced responses
            rag_result = await rag_system.query(request.message, top_k=3)
            response_text = rag_result.generated_response
            sources = rag_result.sources
            model_used = "RAG + LLM"
            
        elif request.use_agents and mcp_client:
            # Use MCP agents
            agent_result = await mcp_client.execute_agent(request.message)
            response_text = agent_result.get("result", "Agent execution completed.")
            model_used = "MCP Agent"
            
        else:
            # Simple response without RAG or agents
            response_text = f"I received your message: '{request.message}'. This is a simple response without RAG or agent capabilities enabled."
            model_used = "Simple Response"
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return ChatResponse(
            response=response_text,
            sources=sources,
            processing_time=processing_time,
            model_used=model_used
        )
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return ChatResponse(
            response=f"I apologize, but I encountered an error processing your request: {str(e)}",
            sources=[],
            processing_time=processing_time,
            model_used="Error Handler"
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    rag_healthy = False
    mcp_healthy = False
    
    if rag_system:
        rag_health = await rag_system.health_check()
        rag_healthy = rag_health.get("status") == "healthy"
    
    if mcp_client:
        # mcp_health = await mcp_client.health_check()
        mcp_healthy = True  # Simplified for demo
    
    return {
        "status": "healthy" if (rag_healthy or mcp_healthy) else "degraded",
        "services": {
            "rag": "healthy" if rag_healthy else "unavailable",
            "mcp": "healthy" if mcp_healthy else "unavailable"
        }
    }

@app.get("/api/stats")
async def get_stats():
    """Get chat application statistics"""
    return {
        "total_sessions": len(chat_sessions),
        "active_connections": len(manager.active_connections),
        "services": {
            "rag_available": rag_system is not None,
            "mcp_available": mcp_client is not None
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )
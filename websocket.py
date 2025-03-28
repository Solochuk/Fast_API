from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Chat</title>
</head>
<body>
    <h2>WebSocket Chat</h2>
    <input id="messageInput" type="text" placeholder="Type a message..."/>
    <button onclick="sendMessage()">Send</button>
    <ul id="messages"></ul>
    <script>
        let ws = new WebSocket("ws://localhost:8000/ws");

        ws.onmessage = function(event) {
            let messages = document.getElementById('messages');
            let message = document.createElement('li');
            message.textContent = event.data;
            messages.appendChild(message);
        };

        function sendMessage() {
            let input = document.getElementById("messageInput");
            ws.send(input.value);
            input.value = '';
        }
    </script>
</body>
</html>
"""

connections = []

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(data)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connections.remove(websocket)

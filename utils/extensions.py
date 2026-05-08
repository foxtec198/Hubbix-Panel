from flask_socketio import SocketIO

# Cria o servidor de WebSockets
ws = SocketIO(cors_allowed_origins="*", async_mode="gevent")
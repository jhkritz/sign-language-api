from socket import socket
from application import init_app
from flask_socketio import SocketIO

app = init_app()
socketio = SocketIO(app)
if __name__ == "__main__":
    socketio.run(app)
    # app.run(host='0.0.0.0')
from socket import socket
from application import init_app
from flask_socketio import SocketIO
from application import socketio

app = init_app()



#okta_client = UsersClient("dev-9239130.okta.com", "00--WuaKx41U62Dk4a7ugEz-cHRR20bbqUhWcI91uz")


#socketio = SocketIO(app)
if __name__ == "__main__":
    socketio.run(app, log_output=True)
    # app.run(host='0.0.0.0')

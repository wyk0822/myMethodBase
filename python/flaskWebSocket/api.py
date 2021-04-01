from flask import Flask, render_template, request
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.websocket import WebSocket

app = Flask(__name__)
user_socket_list = []


@app.route('/ws')
def ws():
    user_socket: WebSocket = request.environ.get("wsgi.websocket")
    if user_socket:
        user_socket_list.append(user_socket)
    print(user_socket_list)
    while 1:
        try:
            msg = user_socket.receive()
        except:
            user_socket_list.remove(user_socket)
            return "断开连接"
        print(msg)
        for u_socket in user_socket_list:
            if u_socket == user_socket:
                continue
            else:
                u_socket.send(msg)


@app.route("/")
def index():
    return render_template("ws.html")


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('127.0.0.1', 666), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()

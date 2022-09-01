from contextlib import closing
from flask import Flask
import socket

app = Flask(__name__)
HOST = "localhost"
PORT = [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089]


@app.route("/home")
def home():

    port_list = []
    for port in PORT:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex((HOST, port)) == 0:
                port_list.append(f"<li>Service at port {str(port)} is up </li><br>")
            else:
                port_list.append(f"<li>Service at port {str(port)} is down </li><br>")
    return "".join(port_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)

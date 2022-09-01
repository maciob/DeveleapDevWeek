#!/usr/bin/env python3
from contextlib import closing
from flask import Flask, render_template
import socket
from flaskext.mysql import MySQL

import requests



app = Flask(__name__)
HOST = "localhost"
PORT = [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089]


# hostname = socket.gethostname()
# IPAddr = socket.gethostbyname(hostname)
# temp_list = IPAddr.split(".")
# last_digit = int(temp_list[3]) + 1
# temp_list[3] = str(last_digit)
# new_IP = ".".join(temp_list)
mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "app"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass"
app.config["MYSQL_DATABASE_DB"] = "billdb"
app.config["MYSQL_DATABASE_HOST"] = f"18.170.241.119"

dependiences = {"Database": "Unknown"}


@app.route("/health-mysql", methods=["GET", "POST"])
def add_provider():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(f"SELECT 1;")
    data = cur.fetchall()
    return f"{data}"



# 8080-Weight app
# 8081-mysql weight
# 8082-Billing app
# 8083-mysql Billing
# 8084-Weight app testing
# 8085-mysql weight testing
# 8086-Billing app testing
# 8087-mysql Billing testing
# 8088-health
# 8089-github api (edited) 


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


@app.route("/health-post")
def health_post():

    post_ports = [8080, 8082, 8084, 8086, 8088, 8089]
    response_codes = []
    msg = "Hello"
    for p in post_ports:
        try:
            requests.post(f"http://18.170.241.119:{p}/monitor", msg)
            response_codes.append(f"Port {p} is running.")
        except:
            response_codes.append(f"Port {p} is not running.")
    return render_template('monitor.html', response_codes=response_codes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)
    

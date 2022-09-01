from flask import Flask, jsonify, request
import json
import os
import threading
import time

app = Flask(__name__)

lista = []
lock = threading.Lock()

testingflag = False

@app.route("/monitor",methods=["POST"])
def health():
    r = request.data.decode('utf-8')
    return jsonify(success=True)


@app.route("/api", methods=["POST"])
def list():
    global testingflag
    r = request.json
    before = r["before"]
    after = r["after"]
    branch = r["ref"]
    #lista.append(before)
    #lista.append(after)
    #lista.append(branch)
    lock.acquire()
    #os.system("git clone https://github.com/maciob/DeveleapDevWeek git")
    lista.append(before)
    lista.append(after)
    lista.append(branch)
    os.system("docker rm -f mysql-flask-app-container python-flask-app-container")
    os.system("docker build -t mysql_db:1.0  db/.")
    os.system("docker build -t billing_server:1.0 app/.")
    os.system("command docker-compose --env-file ./config/.env.prod up --detach")
    #docker rm -f mysql-flask-app-container python-flask-app-container
    lock.release()
    return jsonify(success=True)


@app.route("/home")
def home():

    return lista


if __name__ == "__main__":
    testingflag = False
    app.run(host="0.0.0.0", port=8089)

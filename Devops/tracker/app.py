from flask import Flask, jsonify
from datetime import datetime
import requests
from flask import request
import json
import time
import os
import threading


app = Flask(__name__)

lista = []
lock = threading.Lock()

testingflag = False


@app.route("/api", methods=["POST"])
def list():
    global testingflag
    r = request.json
    before = r["before"]
    after = r["after"]
    lista.append(before)
    lista.append(after)
    lock.acquire()
    #os.system("git clone https://github.com/maciob/DeveleapDevWeek git")
    os.system("docker -H tcp://0.0.0.0:9000 ps -a")
    #time.sleep(20)  # testingphase
    lock.release()
    return jsonify(success=True)


@app.route("/home")
def home():

    return lista


if __name__ == "__main__":
    testingflag = False
    app.run(host="0.0.0.0", port=8089)

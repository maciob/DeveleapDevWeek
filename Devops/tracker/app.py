from flask import Flask, jsonify, request
import json
import os
import threading
import time
import re

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

    lock.acquire()
    os.system("git clone https://github.com/maciob/DeveleapDevWeek git")
    lista.append(before)
    lista.append(after)
    lista.append(branch)
    br = re.search(r'/[a-zA-Z]+g',branch)
    os.system('echo "git checkout to dir git"')
    os.system(f"git -C git/ checkout {after}")
    os.system('echo "docker rm"')
    os.system("docker rm -f mysql-flask-app-container python-flask-app-container")
    os.system('echo "docker build db"')
    os.system("docker build . -t mysql_db:1.0  -f git/Billing/db/Dockerfile")
    os.system('echo "docker build billing"')
    os.system("docker build . -t billing_server:1.0 -f git/Billing/app/Dockerfile")
    os.system('echo "docker compose up"')
    os.system("docker-compose --env-file ./git/Billing/config/.env.dev up --detach")
    os.system('echo "run the tests"')
    os.system("./git/Billing/test_batch.sh")
    os.system('echo "docker rm"')
    os.system("docker rm -f mysql-flask-app-container python-flask-app-container")
#    os.system("rm -r git")
#    os.system("mkdir git")
    lock.release()

    return jsonify(success=True)


@app.route("/home")
def home():

    return lista


if __name__ == "__main__":
    testingflag = False
    app.run(host="0.0.0.0", port=8089)

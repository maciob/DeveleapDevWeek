from flask import Flask, jsonify
from datetime import datetime
import requests
from flask import request

app = Flask(__name__)
logs = []

@app.route("/api", methods=["POST"])
def list():
    r = request.data.decode('utf-8')
    logs.append(r)
    return jsonify(success=True)

@app.route("/home")
def home():
    #now = datetime.now()
    #r = requests.get("http://172.18.0.2:5000")
    #logs.append(r.text)

    #    y = requests.args.get()
    return "\n".join(logs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8089)
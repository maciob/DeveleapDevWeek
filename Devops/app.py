from flask import Flask, jsonify
from datetime import datetime
import requests
from flask import request
import json
import time
import os
app = Flask(__name__)

lista = []

testingflag=False

@app.route("/api", methods=["POST"])
def list():
	global testingflag
	r = request.json
	before = r['before']
	after = r['after']
	os.system("docker ps -a")
	lista.append(before)
	lista.append(after)
	#lock acquire
	while(True):
		if testingflag==False:
			testingflag=True
			time.sleep(20)
			testingflag=False
			break
	#lock release
	return jsonify(success=True)

@app.route("/home")
def home():

	return lista
if __name__ == "__main__":
	testingflag=False
	app.run(host='0.0.0.0', port=8089)

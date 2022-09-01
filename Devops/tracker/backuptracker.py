from flask import Flask, jsonify
from datetime import datetime
import requests
from flask import request
import json
import time
import os
app = Flask(__name__)


commit_list=[]

@app.route("/api", methods=["POST"])
def list():
    
    r = request.json
    
    if type(r) == list:
        for res in r:
            commit_list.append({'before': res['before'], 'after': res['after'], 'head': res['ref']})
    else:
    	commit_list.append({'before': r['before'], 'after': r['after'], 'head': r['ref']})





@app.route("/home")
def home():

	return commit_list
if __name__ == "__main__":
	testingflag=False
	app.run(host='0.0.0.0', port=8089)

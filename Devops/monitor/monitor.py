from flask import Flask, jsonify
from datetime import datetime
import requests
from flask import request
import json
import socket
import os

app = Flask(__name__)

lista = []

testingflag = False


@app.route("/home")
def home():
	HOST = "localhost"
	PORT = 8080

	# Creates a new socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Try to connect to the given host and port
	if sock.connect_ex((HOST, PORT)) == 0:
		lista.append("Port " + str(PORT) + " is open") # Connected successfully
	else:
		lista.append("Port " + str(PORT) + " is closed") # Failed to connect because port is in use (or bad host)

	# Close the connection
	sock.close()

	return lista


if __name__ == "__main__":
	testingflag = False
	app.run(host="0.0.0.0", port=8088)

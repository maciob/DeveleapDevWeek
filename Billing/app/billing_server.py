#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

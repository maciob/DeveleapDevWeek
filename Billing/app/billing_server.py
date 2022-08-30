#!/usr/bin/env python3
from flask import Flask, render_template

app = Flask(__name__)


def run():
    app.run(host="0.0.0.0")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    # here we should add checking connection to database
    return "OK"


@app.route("/provider", methods=["POST"])
def add_provider():
    # here we should add creating new provider
    # it should return a unique provider id as json: { "id":<str>}
    return 0


@app.route("/provider/<id>", methods=["PUT"])
def update_provider(id):
    # here we should add updating provider
    return 0


if __name__ == "__main__":
    run()

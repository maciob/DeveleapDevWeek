#!/usr/bin/env python3
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "app"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass"
app.config["MYSQL_DATABASE_DB"] = "billdb"
app.config["MYSQL_DATABASE_HOST"] = "172.17.0.3"
mysql.init_app(app)


def run():
    app.run(host="0.0.0.0")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    # here we should add checking connection to database
    return "OK"


# Temporarily changed to GET for testing -- later change to POST method!!!
@app.route("/provider", methods=["GET"])
def add_provider():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM Provider")
    data = cur.fetchall()
    return f"{data}"
    


@app.route("/provider/<id>", methods=["GET"])
def update_provider(id):
    # here we should add updating provider
    return f"{id}"


if __name__ == "__main__":
    run()

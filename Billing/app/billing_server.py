#!/usr/bin/env python3
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "password"
app.config["MYSQL_DATABASE_DB"] = "billdb"
app.config["MYSQL_DATABASE_HOST"] = "db_server"
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
    connector = mysql.connect()
    cursor = connector.cursor()
    cursor.execute(f"SELECT * FROM Providers")
    data = cursor.fetchall()
    return "data"
    # here we should add creating new provider
    # it should return a unique provider id as json: { "id":<str>}
    # return 0


@app.route("/provider/<id>", methods=["PUT"])
def update_provider(id):
    # here we should add updating provider
    return 0


if __name__ == "__main__":
    run()

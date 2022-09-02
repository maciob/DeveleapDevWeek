#!/usr/bin/env python3
from flask import Flask, render_template
from flaskext.mysql import MySQL


app = Flask(__name__)


mysql = MySQL(app)
app.config["MYSQL_DATABASE_HOST"] = "172.18.0.3"
app.config["MYSQL_DATABASE_USER"] = "root"


@app.route("/", methods=["GET", "POST"])
def add_provider():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(f"SELECT 1;")
    data = cur.fetchall()
    print(f"{data}")
    return f"{data}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



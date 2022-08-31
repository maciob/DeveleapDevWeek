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

independiences = {"Database": "Unknown"}


def run():
    app.run(host="0.0.0.0")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Provider")
        data = cur.fetchone()
        if data:
            independiences["Database"] = "OK"
            return independiences
    except:
        independiences["Database"] = "DOWN"
        return independiences
    # DO NOT DELETE COMMENTS BELOW  - ITS ANOTHER VERSION, MAYBE FOR FUTURE USAGE :)
    # if data:
    #     independiences["Database"] = "OK"
    #     return independiences
    # else:
    #     independiences["Database"] = "DOWN"
    #     return independiences


# Temporarily changed to GET for testing -- later change to POST method!!!
@app.route("/provider", methods=["GET","POST"])
def add_provider():
    if request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Provider")
        data = cur.fetchall()
        return f"{data}"
    else:
        name=request.form["username"]
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO Provider (`name`) VALUES ('{name}');")
        conn.commit()
        
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM Provider WHERE name = '{name}';")
        data = cur.fetchone()
        return str(data)


@app.route("/provider/<id>", methods=["PUT"])
def update_provider(id):
    name=request.form["username"]
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(f"UPDATE Provider SET name = '{name}' WHERE id = '{id}';")
    conn.commit()
    
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(f"SELECT id,name FROM Provider WHERE id = '{id}';")
    data = cur.fetchone()
    return str(data)

@app.route("/ip", methods=["GET"])
def ip():
    resp = [str(f"{f}: {request.environ[f]}") for f in request.environ]
    return "</br>".join(resp)
    
@app.route("/truck", methods=["POST", "PUT"])
def truck():
    if request.method == 'POST':
        truck_id=request.form["truck_id"]
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO Trucks (`id`) VALUES ('{truck_id}');")
        conn.commit()
        cur2 = conn.cursor()
        cur.execute(f"SELECT id,provider_id FROM Trucks WHERE id = '{truck_id}';")
        trucks = cur.fetchall()
        return str(trucks)

if __name__ == "__main__":
    run()

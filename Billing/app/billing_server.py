#!/usr/bin/env python3
from flask import Flask, render_template, request
from flaskext.mysql import MySQL
import pandas as pd
from openpyxl import load_workbook
import socket
from flask import send_file


hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
temp_list = IPAddr.split(".")
last_digit = int(temp_list[3]) + 1
temp_list[3] = str(last_digit)
new_IP = ".".join(temp_list)

app = Flask(__name__)

mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "app"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass"
app.config["MYSQL_DATABASE_DB"] = "billdb"
app.config["MYSQL_DATABASE_HOST"] = f"{new_IP}"
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
@app.route("/provider", methods=["GET", "POST"])
def add_provider():
    if request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Provider")
        data = cur.fetchall()
        return f"{data}"
    else:
        name = request.form["username"]
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
    name = request.form["username"]
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
    # resp = [str(f"{f}: {request.environ[f]}") for f in request.environ]
    # return "</br>".join(resp)
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    temp_list = IPAddr.split(".")
    last_digit = int(temp_list[3]) + 1
    temp_list[3] = str(last_digit)
    new_IP = ".".join(temp_list)
    return (
        f"Your flask app IP address is {IPAddr}, and DB server IP address is {new_IP}"
    )


@app.route("/truck", methods=["POST", "GET"])  # GET added for testing
def add_truck():
    if request.method == "POST":
        truck_id = request.form["truck_id"]
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO Trucks (`id`) VALUES ('{truck_id}');")
        conn.commit()
        cur.execute(f"SELECT id,provider_id FROM Trucks WHERE id = '{truck_id}';")
        trucks = cur.fetchall()
        return str(trucks)
    elif request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Trucks;")
        conn.commit()
        trucks = cur.fetchall()
        return str(trucks)


@app.route("/truck/<id>", methods=["PUT"])
def updadate_(id):
    provider_id = request.form["provider_id"]
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(f"UPDATE Trucks SET provider_id = '{provider_id}' WHERE id = '{id}';")
    conn.commit()
    return "OK"


@app.route("/rates", methods=["POST", "GET"])
def rates():
    if request.method == "GET":
        # book = load_workbook("in/rates.xlsx")
        # sheet = book.active
        # return render_template("s3_excel_table.html", sheet=sheet)
        path = "in/rates.xlsx"
        return send_file(path, as_attachment=True)

        
    elif request.method == "POST":
        excel_data = pd.read_excel('in/rates.xlsx')
        # Read the values of the file in the dataframe
        data = pd.DataFrame(excel_data, columns=['Product', 'Rate', 'Scope'])
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM Rates;")
        conn.commit()

        for i in range(len(data.index)):
            conn = mysql.connect()
            cur = conn.cursor()
            
            cur.execute(f"INSERT INTO Rates (product_id, rate, scope) VALUES ('{data.iloc[i,0]}','{data.iloc[i,1]}','{data.iloc[i,2]}');")
            conn.commit()

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Rates;")
        data = cur.fetchall()
        return str(data)
        


if __name__ == "__main__":
    run()

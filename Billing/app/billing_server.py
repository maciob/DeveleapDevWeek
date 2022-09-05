#!/usr/bin/env python3
from asyncio import proactor_events
from crypt import methods
from flask import Flask, render_template, request, jsonify
from flaskext.mysql import MySQL
import pandas as pd
import socket
from flask import send_file
from datetime import datetime
import requests
import os


def get_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    temp_list = IPAddr.split(".")
    last_digit = int(temp_list[3]) + 1
    temp_list[3] = str(last_digit)
    new_IP = ".".join(temp_list)
    return (IPAddr, new_IP)


app = Flask(__name__)

mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "app"
app.config["MYSQL_DATABASE_PASSWORD"] = "pass"
app.config["MYSQL_DATABASE_DB"] = "billdb"
app.config["MYSQL_DATABASE_HOST"] = f"{get_ip()[1]}"
mysql.init_app(app)

dependiences = {"Database": "Unknown"}


def run():
    app.run(host="0.0.0.0")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/env")
def env():
    resp = [str(f"{f}: {request.environ[f]}") for f in request.environ]
    odp = " \t ".join(resp)
    return render_template("env.html", env=str(odp), title="ENV data for debug")


@app.route("/monitor", methods=["GET", "POST"])
def monitor():
    if request.method == "POST":
        return jsonify(status=200)
    elif request.method == "GET":
        return "<h1>U can POST this /monitor to get server status</h1></br>For example: </br> curl -X POST localhost:8086/monitor </br>"


@app.route("/health", methods=["GET"])
def health():
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT 1;")
        data = cur.fetchone()
        if data:
            dependiences["Database"] = "OK"
            cur.close()
            conn.close()
            return render_template(
                "health.html", status=dependiences, title="Health status"
            )
    except:
        dependiences["Database"] = "DOWN"
        return render_template(
            "health.html", status=dependiences, title="Health status"
        )


# Temporarily changed to GET for testing -- later change to POST method!!!
@app.route("/provider", methods=["GET", "POST"])
def add_provider():
    if request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Provider ORDER BY 'id';")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("provider.html", providers=data, title="Add provider")

    elif request.method == "POST":
        name = request.form["username"]
        conn = mysql.connect()
        cur = conn.cursor()
        if cur.execute(f"SELECT * FROM Provider WHERE name = '{name}';"):
            cur.close()
            conn.close()
            return "Name already in database. Try again.\n"
        else:
            cur.execute(f"INSERT INTO Provider (`name`) VALUES ('{name}');")
            conn.commit()
            cur.close()
            conn.close()
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(f"SELECT id FROM Provider WHERE name = '{name}';")
            data = cur.fetchone()
            cur.close()
            conn.close()
            return jsonify(id=data)


@app.route("/provider/<id>", methods=["PUT", "GET", "POST"])
def update_provider(id):
    if request.method == "PUT":
        name = request.form["username"]
        conn = mysql.connect()
        cur = conn.cursor()
        if not cur.execute(f"SELECT * FROM Provider WHERE id = '{id}';"):
            cur.close()
            conn.close()
            return "No provider with this ID in database.\n"
        else:
            cur.execute(f"UPDATE Provider SET name = '{name}' WHERE id = '{id}';")
            conn.commit()
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute(f"SELECT id,name FROM Provider WHERE id = '{id}';")
            data = cur.fetchone()
            cur.close()
            conn.close()
            return jsonify(data)

    elif request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Provider ORDER BY 'id';")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template(
            "update_provider.html", providers=data, title="Update provider name", ids=id
        )

    elif request.method == "POST":
        name = request.form["username"]
        response = requests.put(
            f"http://{request.environ['HTTP_HOST']}/provider/{id}",
            data={"username": f"{name}"},
        )
        # return inf
        return response.content


@app.route("/ip", methods=["GET"])
def ip():
    resp = f"Your flask app IP address is {get_ip()[0]}, and DB server IP address is {get_ip()[1]}"
    # return f"Your flask app IP address is {get_ip()[0]}, and DB server IP address is {get_ip()[1]}"
    return render_template("ip.html", ip=resp, title="IP")


@app.route("/ipdb", methods=["GET"])
def ipdb():
    data = get_ip()[1]
    return jsonify(data)


@app.route("/truck", methods=["POST", "GET"])  # GET added for testing
def add_truck():
    if request.method == "POST":
        truck_id = request.form["id"]
        provider_id = request.form["provider"]
        conn = mysql.connect()
        cur = conn.cursor()
        if len(truck_id) > 11:
            return "Truck ID too long. Try again.\n"
        elif cur.execute(f"SELECT * FROM Trucks WHERE id = '{truck_id}';"):
            return "Truck's ID already in the database. Try again.\n"
        elif not cur.execute(f"SELECT * FROM Provider WHERE id = '{provider_id}';"):
            return "Provider's ID not in the database. Try again. \n"
        cur.execute(
            f"INSERT INTO Trucks (id, provider_id) VALUES ('{truck_id}', '{provider_id}');"
        )
        conn.commit()
        cur.execute(f"SELECT id,provider_id FROM Trucks WHERE id = '{truck_id}';")
        trucks = cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(trucks)

    elif request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Trucks;")
        conn.commit()
        trucks = cur.fetchall()
        cur.close()
        conn.close()
        # data = jsonify(trucks)
        return render_template("trucks.html", status=trucks, title="Add truck")

def getBaseHost(url):
    list = url.split(":")
    host = list[0]
    port = list[1]
    if port == '8086':
        new_port = '8084'
    else:
        new_port = '8080'
    return host,new_port

def getCurrentTime():
    now = datetime.now()
    month = now.strftime("%m")
    year = now.strftime("%Y")
    current_time = now.strftime("%Y%m%d%H%M%S")
    return month,year,current_time

@app.route("/truck/<id>", methods=["PUT", "GET"])
def updadate_(id):
    if request.method == "PUT":
        provider_id = request.form["provider"]
        conn = mysql.connect()
        cur = conn.cursor()
        if not cur.execute(f"SELECT * FROM Provider WHERE id = '{provider_id}';"):
            return "No provider with this ID in database.\n"
        elif not cur.execute(f"SELECT * FROM Trucks WHERE id = '{id}';"):
            return "No truck with this ID in database.\n"
        cur.execute(
            f"UPDATE Trucks SET provider_id = '{provider_id}' WHERE id = '{id}';"
        )
        conn.commit()
        cur.close()
        conn.close()
        return "OK"
    if request.method == "GET":
        month,year,current_time = getCurrentTime()
        truck_id = str(id)
        t1 = request.form.get("t1", f"{year}01{month}000000")
        t2 = request.form.get("t2", current_time)
        host, new_port = getBaseHost(request.environ['HTTP_HOST'])
        url_for_request = host + ':' + new_port
        weight_response = requests.get(f"http://{url_for_request}/item/{truck_id}?from={t1}&to={t2}")
        #weight_response = {"id": truck_id, "t1": t1, "t2": t2}
        return weight_response.content
    

@app.route("/trucks/<id>", methods=["GET", "POST"])
def update_truck_html(id):
    if request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Trucks;")
        conn.commit()
        trucks = cur.fetchall()
        cur.close()
        conn.close()
        return render_template(
            "update_truck.html", status=trucks, ids=id, title="Update Trucks data"
        )
    if request.method == "POST":
        name = request.form["provider"]
        response = requests.put(
            f"http://{request.environ['HTTP_HOST']}/truck/{id}",
            data={"provider": f"{name}"},
        )
        # return inf
        return response.content


@app.route("/rates", methods=["POST", "GET"])
def rates():
    if request.method == "GET":
        # book = load_workbook("in/rates.xlsx")
        # sheet = book.active
        # return render_template("s3_excel_table.html", sheet=sheet)
        path = r"/app/in/rates.xlsx"
        return send_file(path, as_attachment=True)
    #
    elif request.method == "POST":
        excel_data = pd.read_excel(r"/app/in/rates.xlsx")
        # Read the values of the file in the dataframe
        data = pd.DataFrame(excel_data, columns=["Product", "Rate", "Scope"])
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM Rates;")
        conn.commit()
        cur.close()
        conn.close()
        #
        conn = mysql.connect()
        cur = conn.cursor()
        for i in range(len(data.index)):

            cur.execute(
                f"INSERT INTO Rates (product_id, rate, scope) VALUES ('{data.iloc[i,0]}','{data.iloc[i,1]}','{data.iloc[i,2]}');"
            )
            conn.commit()
        cur.close()
        conn.close()

        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Rates;")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return "Inserted into DB successfully"

@app.route("/bill/<id>", methods=['GET'])
def get_bill(id):
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute(f"SELECT name from Provider WHERE id = {id};")
    conn.commit()
    provider_name = cur.fetchall()
    cur.execute(f"SELECT COUNT(id) FROM Trucks WHERE provider_id={id};")
    truck_count = cur.fetchall()
    cur.execute(f"SELECT id FROM Trucks WHERE provider_id={id};")
    truck_ids = cur.fetchall()
    truck_ids_list = list(map(lambda x: x[0], truck_ids))
    cur.close()
    conn.close()
    session_count = 0
    total = 0
    products = []
    single_product = {}
    month,year,current_time = getCurrentTime()
    t1 = request.form.get("t1", f"{year}01{month}000000")
    t2 = request.form.get("t2", current_time)
    for truck_id in truck_ids_list:
        weight_item = requests.get(f"http://18.170.241.119:8084/item/{truck_id}?from={t1}&to={t2}")
        #GET SESSIONS LIST FOR THAT TRUCK, return lenght, add lenght to session_count
        #GET with ID of ever session of this truck > /GET sessions, parse 'neto'
        #get product name from GET /weight ???
   
    #trucks_ids for testing only
    bill={"id": id, "name": provider_name[0], "from": t1, "to": t2, "truckCount": truck_count[0], "trucks_ids": truck_ids_list, "products": products, "total": total}
    

    return jsonify(bill)

#
@app.route("/prates", methods=["POST", "GET"])
def prates():
    if request.method == "GET":
        return render_template("rates.html", title="Post rates")
    if request.method == "POST":
        response = requests.post(f"http://{request.environ['HTTP_HOST']}/rates")
        return response.content


if __name__ == "__main__":
    run()

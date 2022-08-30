from locale import format_string
from logging import root
from flask import Flask,render_template, request
from datetime import datetime
from flasktext.mysql import MySQL
from datetime import datetime
import csv
import json
import mysql.connector

app = Flask(__name__)
# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'app'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
# app.config['MYSQL_DATABASE_DB'] = 'mydb'
# app.config['MYSQL_DATABASE_HOST'] = '172.17.0.3'
# mysql.init_app(app)


@app.route("/weight ",methods=["POST"])
def weight(): 
	# POST /weight
    return None
 

@app.route("/batch-weight ",methods=["POST"])
def batch_weight(): 
	# POST /batch-weight
    return None




@app.route("/unknown",methods=["GET"])
def unknown(): 
    # GET /unknown
    return None

@app.route("/item/<id>",methods=["GET"])
def item(id): 
    # GET /item/<id>
    return None
    
@app.route("/session/<id>",methods=["GET"])
def session(id): 
    # GET /session/<id>
    return None
    
@app.route("/health",methods=["GET"])
def testdb():
    if request.method == "GET":
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("Select VERSION()")
        results = cur.fetchone()
        ver = results[0]
        if (ver is None):
            return render_template("health.html", content="no")
        else: 
            return render_template("health.html", content="OK")
    

 
db =  mysql.connector.connect(user='root', host='172.17.0.3', port='3306', password='password', database='weight')
cur = db.cursor()

input = "container2.json"
index = input.index(".")
extension = input[index:index+5]

def json_parsing():
    f = open(input)
    data = json.load(f)
    for element in data:
        id = element["id"]
        weight = element["weight"]
        unit = element["unit"]
        cur.execute("INSERT INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s)", (id,weight,unit))
       


















if __name__ == "__main__":
	app.run()
 

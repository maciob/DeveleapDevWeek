from locale import format_string
from logging import root
from flask import Flask,render_template, request, jsonify
from datetime import datetime
from flaskext.mysql import MySQL
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

@app.route("/",methods=["GET"])
def home():
    return "<h1>Hello!<h1> This is the main page of the weight team app!"
    
@app.route("/weight ",methods=["POST"])
def weight(): 
	# POST /weight
    return None
 

@app.route("/batch-weight",methods=["GET","POST"])
def batch_weight(): 
    if request.method == "POST":
        details = request.form
        file = details['file']
        handling_files(file)
    return render_template("batch.html")





@app.route("/unknown",methods=["GET"])
def unknown(): 
    
    if request.method == "GET":
        users = []
        conn = mysql.connect()
        cursor = conn.cursor()
        query = 'SELECT UserId from <table_name>'
        cursor.execute(query)

        for  row in cursor:
            users.append(row['UserId'])

        conn.close()

        return jsonpickle.encode(users)

@app.route("/item/<id>",methods=["GET"])
def item(id,t1,t2): 
    
    if request.method == "GET":
        # users = user list from /unknown page
        if id in users:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT id,tara,sessions from <table_name> WHERE UserId = 'id' "
            cursor.execute(query)            
            the_user = cur.fetchall()
            conn.close()
            
            x = datetime.datetime.now()
            t_1 = datetime.datetime(x.year,x.month,1).strftime("%Y%m%d%H%M%S")
            t_2 = x.strftime("%Y%m%d%H%M%S") # current time
            
            t1 = request.args.get('t1', t_1)
            t2 = request.args.get('t2', t_2)
            
            return jsonpickle.encode(the_user)

    else:
        # return render_template('404.html')
        return None

@app.route("/weight",methods=["GET"])
def weight(t1,t2, f): 
    if request.method == "GET":
        
        x = datetime.datetime.now()
        t_1 = datetime.datetime(x.year,x.month,x.day).strftime("%Y%m%d%H%M%S") # server time
        t_2 = x.strftime("%Y%m%d%H%M%S") # current time
        
        filter = request.args.get('filter', default = "in,out,none", type = str)
        t1 = request.args.get('t1', default = t_1, type = int)
        t2 = request.args.get('t2', default = t_2, type = int)
        
        
        conn = mysql.connect()
        cursor = conn.cursor()
        query = "SELECT * from <table_name> WHERE direction = 'the_filter' "
        cursor.execute(query)            
        the_object = cur.fetchone()
        conn.close()  
            
        return jsonpickle.encode(the_object)
    
    else:
        # return render_template(index.html) 
        return None
    
    
@app.route("/session/<id>",methods=["GET"])
def sessionid(id):
    s1 = mysql.connect()
    cur = s1.cursor()
    query = """select * from containers_registered where container_id = %s"""
    tuple1 = id
    cur.execute(query, tuple1)
    sessions = cur.fetchall()
    return render_template("session.html", content = sessions)
    
@app.route("/health",methods=["GET"])
def testdb():
    
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("select * from containers_registered")
        results = cur.fetchall()
        if results:
            thisdict = {"Connection": "OK"}
            return thisdict
    except:
        thisdict = {"Connection": "No"}
        return thisdict
    
def handling_files(file):
    conn = mysql.connect()
    cur = conn.cursor()
    input = file
    index = input.index(".")
    extension = input[index:index+5]

    def json_parsing():    #Handling json_files
        f = open(f"in/{input}")
        data = json.load(f)
        for element in data:
            id = element["id"]
            weight = element["weight"]
            unit = element["unit"]
            cur.execute("INSERT INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s)", (id,weight,unit))

    def csv_parsing():      #Handling csv files
        with open(f"in/{input}") as file:
            content = file.readlines()
            unit = content[0].split(",")[1][1:3]
            for num in range (1,len(content) -1):
                row = content[num].split(",")
                print(row[0])
                print(row[1])
                cur.execute("INSERT INTO containers_registered(container_id,weight,unit) VALUES (%s, %s, %s)", (row[0],row[1],unit))
                


#Logic of function
    def extract_data():
        if extension == ".json":
            json_parsing()
        elif extension == ".csv":
            csv_parsing()
        else:
            print("File with bad extension")

#Execution of logic
    extract_data()
    

@app.route("/monitor", methods=["GET","POST"])
def monitor():
    if request.method == "POST":
        return jsonify(status=200)
    else:
        return "<h1>U can POST this /monitor to get server status</h1></br>For example: </br> curl -X POST localhost:8080/monitor"



if __name__ == "__main__":
	app.run()
 

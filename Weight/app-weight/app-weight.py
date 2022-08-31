from locale import format_string
from logging import root
from flask import Flask,render_template, request
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
    # Returns a list of all recorded containers that have unknown weight:
    # ["id1","id2",...]
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
def item(id): 
    # GET /item/<id>
    # GET /item/<id>?from=t1&to=t2
    # - id is for an item (truck or container). 404 will be returned if non-existent
    # - t1,t2 - date-time stamps, formatted as yyyymmddhhmmss. server time is assumed.
    # default t1 is "1st of month at 000000". default t2 is "now". 

    if request.method == "GET":
        # users = user list from /unknown page
        if id in users:
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "SELECT * from <table_name> WHERE UserId = 'id' "
            cursor.execute(query)            
            the_user = cur.fetchone()
            conn.close()
            
            return jsonpickle.encode(the_user)


        # Returns a json:
        # { "id": <str>,
        #   "tara": <int> OR "na", // for a truck this is the "last known tara"
        #   "sessions": [ <id1>,...] 
        # }
    else:
        # return render_template('404.html')
        
        # @main.app_errorhandler(404) def page_not_found(e):
        # if request.accept_mimetypes.accept_json and \ not request.accept_mimetypes.accept_html:
        # response = jsonify({'error': 'not found'}) response.status_code = 404
        # return response
        # return render_template('404.html'), 404

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
    
















if __name__ == "__main__":
	app.run()
 

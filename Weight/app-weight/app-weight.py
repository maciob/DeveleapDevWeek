from locale import format_string
from logging import root
from flask import Flask,render_template, request, jsonify
from datetime import datetime
from flaskext.mysql import MySQL
from datetime import datetime
import csv
import json
import socket
from werkzeug.utils import secure_filename  
import os
from dotenv import load_dotenv 
from functions import handle_out,handle_in,handle_none,handle_files

# import mysql.connector


load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    UPLOAD_FOLDER = os.path.join(basedir, './in')
    ALLOWED_EXTENSIONS = {'csv','json'}
    SESSION_TYPE = 'session'


app = Flask(__name__)
app.config.from_object(Config)  #1
app.secret_key = "@#dsfs$!!fsgsg342424"

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
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "password"
app.config["MYSQL_DATABASE_DB"] = "weight"
app.config["MYSQL_DATABASE_HOST"] = f"{get_ip()[1]}"
mysql.init_app(app)

def getMysqlConnection():
    return mysql.connector.connect(user='root', host=f"{get_ip()[1]}", port='3306', password='password', database='weight',auth_plugin='mysql_native_password')



@app.route("/weight", methods=["GET","POST"])
def weight():
    if request.method == "POST":
        details = request.form                      
        id = details["id"]
        direction = details["direction"]
        truck_license = details["truck_license"]
        containers = details["containers"]
        type_product = details["type_product"]
        if type_product == "":
            type_product = "na"
        if truck_license == "":
            truck_license = "na"
        date_created = details["date_created"]
        weight = details["weight"]
        force = details["force"]
        conn = getMysqlConnection()
        cur = conn.cursor()
        
        if force == "True":
            cur.execute(f"SELECT direction FROM transactions WHERE id='{id}'")
            result = cur.fetchall()
            result = result[0][0]
            if result == direction and result == "in":   
                cur.execute(f"UPDATE transactions SET bruto = '{weight}', datetime = '{date_created}' WHERE id = '{id}'")
                return f'New gross weight - {weight}'

            elif result == direction and result == "out":
                json = handle_out(id,weight,direction,date_created)
                return f"New data {json}"

            else:
                return render_template('error.html')
        
        elif direction == "in":
            try:
                json = handle_in(id,date_created,direction,truck_license,containers,weight,type_product)
                return json
            except:
                return render_template('error.html')
        
        elif direction == "out":
            try:
                cur.execute(f"SELECT direction FROM transactions WHERE id='{id}'")
                result = cur.fetchall()
                result = result[0][0]
                if result == "out":
                    return 'You cannot overwrite existing form without force'
                json = handle_out(id,weight,direction,date_created)
                return json
            except:
               return render_template('error.html')
        elif direction == "none":
            try:
                response = handle_none(direction,containers,weight,date_created)
                return response
            except:
                return render_template('error.html')
        else:
            return render_template('error.html')
    else:
        return render_template("form.html")


def weight1(t1,t2,arg1):
    conn = mysql.connect()
    cursor = conn.cursor()
    query = f"SELECT * FROM transactions WHERE direction='{arg1}' AND datetime BETWEEN '{t1}' AND '{t2}';"
    cursor.execute(query)
    the_object = cursor.fetchall()
    the_weight_list = []
    for item in the_object:
        the_weight_dic = {}
        the_weight_dic["id"] = item[0]
        the_weight_dic["direction"] = item[2]
        the_weight_dic["neto"] = item[7]
        the_weight_dic["produce"] = item[8]
        the_weight_dic["bruto"] = item[5]
        the_weight_dic["containers"] = item[4]
        the_weight_list.append(the_weight_dic)
    conn.close()
    return json.dumps(the_weight_list)

def getitem(id, arg1, arg2):
    db = mysql.connect()
    cur1 = db.cursor()
    sidtruck = f"SELECT * FROM transactions WHERE id='{id}' and datetime BETWEEN '{arg1}' AND '{arg2}';"
    cur1.execute(sidtruck)
    back1=cur1.fetchall()
    cur1.close()
    new_records = []
    for record in back1:
        truck1 = {}
        truck1["id"] = record[0]
        truck1["tara"] = record[6]
        new_records.append(truck1)
    if back1==[]:
        db = mysql.connect()
        cur1 = db.cursor()
        sidtruck = f"SELECT * FROM containers_registered WHERE container_id='{id}';"
        cur1.execute(sidtruck)
        back1=cur1.fetchall()
        cur1.close()
        new_records = []
        for record in back1:
            container1 = {}
            container1["container_id"] = record[0]
            container1["weight"] = record[1]
            container1["unit"] = record[2]
            new_records.append(container1)
    return new_records



@app.route("/",methods=["GET"])
def home():
    db = mysql.connect()
    cur = db.cursor()
    data = cur.execute("SELECT * FROM containers_registered;")
    data = cur.fetchall()
    return f"<h1>Home page of weight team app</h1>"
    

@app.route('/batch-weight', methods = ['GET', 'POST']) 
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      f.save(os.path.join(Config.UPLOAD_FOLDER, filename))
      handle_files(filename)
      return f"You've uploaded file - {filename}"
   
   else:
        return render_template('upload.html') 


@app.route("/unknown",methods=["GET"])
def unknown(): 
    
    if request.method == "GET":
        users = []
        conn =  mysql.connect()
        cursor = conn.cursor()
        query = 'SELECT UserId from <table_name>;'
        cursor.execute(query)

        for  row in cursor:
            users.append(row['UserId'])

        conn.close()

        return jsonpickle.encode(users)

@app.route("/item/<id>",methods=["GET","POST"])
def item(id):
    arg1 = request.args.get('from', default=datetime.combine(datetime.today().replace(day=1), datetime.min.time()))
    arg2 = request.args.get('to', default=datetime.now())
    
    item_truck = getitem(id, arg1, arg2)
    return json.dumps(item_truck)

@app.route("/weight1",methods=["GET", "POST"])
def weight1():
    arg1 = request.args.get('filter', default = "in", type = str)
    t1 = request.args.get('t1', default = datetime.combine(datetime.today().replace(day=1), datetime.min.time()))
    t2 = request.args.get('t2', default = datetime.now(), type = int)
    weight11 = weight1(t1,t2,arg1)
    return json.dumps(weight11)
    
    
@app.route("/session/<id>",methods=["GET"])
def sessionid(id):
    s1 = mysql.connect()
    cur = s1.cursor()
    query = """select * from transactions where id = %s;"""
    tuple1 = id
    cur.execute(query, tuple1)
    sessions = cur.fetchall()
    return jsonify(sessions)
    
@app.route("/health",methods=["GET"])
def testdb():
    
    try:
        conn = mysql.connect()
        cur = conn.cursor()
        cur.execute("select 1;")
        results = cur.fetchone()
        if results:
            thisdict = {"Connection": "OK"}
            return jsonify(thisdict)
    except:
        thisdict = {"Connection": "No"}
        return jsonify(thisdict)
    
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
	app.run(host='0.0.0.0')
 

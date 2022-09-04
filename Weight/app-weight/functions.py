import mysql.connector
import json
import socket


def get_ip():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    temp_list = IPAddr.split(".")
    last_digit = int(temp_list[3]) + 1
    temp_list[3] = str(last_digit)
    new_IP = ".".join(temp_list)
    return (IPAddr, new_IP)

def getMysqlConnection():
     return mysql.connector.connect(user='root', host=f"{get_ip()[1]}", port='3306', password='password', database='weight')



def handle_in(id,date_created,direction,truck_license,containers,weight,type_product):
    conn = getMysqlConnection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM transactions ORDER BY id desc LIMIT 1")  #Creating unique id, based on last record, altough if no result - create a id with number 1
    result = cur.fetchall()
    if not result:
        id = 1
    else:
        id = result[0][0] + 1
    cur.execute("INSERT INTO transactions(id,datetime,direction,truck,containers,bruto,produce) VALUES (%s, %s, %s,%s, %s, %s,%s)", (id,date_created,direction,truck_license,containers,weight,type_product))
    data = {}
    data['id'] = id         #Creating a json output
    data['truck'] = truck_license
    data['bruto'] = weight
    data['unit'] = "kg"
    json_data = json.dumps(data)
    return json_data

def handle_out(id,weight,direction,date_created):
    conn = getMysqlConnection()
    cur = conn.cursor()
    truckTara = weight
    cur.execute("SELECT * FROM containers_registered")
    containers_database = cur.fetchall()
    cur.execute(f"SELECT containers FROM transactions WHERE id='{id}'")
    containers_declared = cur.fetchall()
    containers_declared = list(containers_declared[0])
    containers_declared= containers_declared[0].split(",")  #Change format of data to simplify extracting needed information
    sum = 0
    for container in containers_declared:                   #Loop through results from database in order to find matched containers from declaration
        for container_db in containers_database:
            if container == container_db[0]:
                if container_db[2] == "lbs":
                    container_db[1] * 0,45359237            #Convert lbs to kg
                    sum += int(container_db[1])
                else:
                    sum += container_db[1]
    cur.execute(f"SELECT bruto FROM transactions WHERE id='{id}'")
    brutto = cur.fetchall()
    brutto = brutto[0][0]
    netto = int(brutto) - int(weight) - int(sum)       # Compute weight of products, based on given data
    cur.execute(f"UPDATE transactions SET direction = '{direction}', truckTara = '{truckTara}', neto = '{netto}', datetime = '{date_created}' WHERE id = '{id}'")
    cur.execute(f"SELECT id,truck,bruto,truckTara FROM transactions WHERE id={id}")
    result = cur.fetchall()
    result = result[0]
    data = {}
    data['id'] = result[0]
    data['truck'] = result[1]
    data['bruto'] = result[2]         #Return data in json format
    data['truckTara'] = truckTara
    data['neto'] = netto
    json_data = json.dumps(data)
    return json_data

def handle_none(direction,container,weight,date_created):
    conn = getMysqlConnection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM transactions ORDER BY id desc LIMIT 1")
    result = cur.fetchall()
    if not result:
        id = 1
    else:
        id = result[0][0] + 1
    conn = getMysqlConnection()
    cur = conn.cursor()
    cur.execute("INSERT INTO transactions(id,direction,containers,bruto,datetime) VALUES (%s, %s, %s,%s,%s)", (id,direction,container,weight,date_created))
    return "Container was succesfully registered to database"


def handle_files(file):
    conn = getMysqlConnection()
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
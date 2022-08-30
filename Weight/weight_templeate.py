from locale import format_string
from logging import root
from flask import Flask,render_template, request
from datetime import datetime
from flaskext.mysql import MySQL
from datetime import datetime

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
 

@app.route("/batch-weight ",methods=["POST"])
def batch_weight(): 
	# POST /batch-weight




@app.route("/unknown",methods=["GET"])
def unknown(): 
    # GET /unknown

@app.route("/item/<id>",methods=["GET"])
def item(id): 
    # GET /item/<id>
    
@app.route("/session/<id>",methods=["GET"])
def session(id): 
    # GET /session/<id>
    
@app.route("/health",methods=["GET"])
def health(): 
    # GET /health
    

 
if __name__ == "__main__":
	app.run()
 
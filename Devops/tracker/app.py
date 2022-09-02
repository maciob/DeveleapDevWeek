import smtplib
from email.mime.text import MIMEText
from flask import Flask, jsonify, request
import json
import os
import threading
import time
import re

app = Flask(__name__)

lista = []
lock = threading.Lock()
mailing_list = ['dawidtomczynski@gmail.com', 'bekasmaciej@gmail.com', 'adamkobus11@gmail.com',
                'dominikborkowski89@gmail.com', 'adam.stegienko1@gmail.com']
testingflag = False


def send_email(subject, message, receiver_mail):

    #  sends an email with feedback to committer, team leaders and devops team

    msg = MIMEText(message, 'plain')
    msg['Subject'] = subject
    port = 587
    my_mail = 'blueteamdevops@outlook.com'
    my_password = 'G00gleit'
    with smtplib.SMTP('smtp-mail.outlook.com', port) as server:
        server.starttls()
        server.login(my_mail, my_password)
        for mail in mailing_list:
            server.sendmail(my_mail, mail, f"CC: {msg.as_string()}")
        if receiver_mail not in mailing_list:
            server.sendmail(my_mail, receiver_mail, msg.as_string())
        server.quit()


@app.route("/monitor", methods=["POST"])
def health():
    r = request.data.decode('utf-8')
    return jsonify(success=True)


@app.route("/api", methods=["POST"])
def continuous_integration():
    global testingflag
    r = request.json
    before = r["before"]
    after = r["after"]
    branch = r["ref"]
    commits = r['commits']
    for commit in commits:
        committer_mail = commit['author']['email']
    lock.acquire()
    os.system("git clone https://github.com/maciob/DeveleapDevWeek git")
    lista.append(before)
    lista.append(after)
    lista.append(branch)
    br = re.search(r'/[a-zA-Z]+g', branch)
    os.system('echo "git checkout to dir git"')
    os.system(f"git -C git/ checkout {after}")
    os.system('echo "docker rm"')
    os.system("docker rm -f mysql-flask-app-container python-flask-app-container")
    os.system('echo "docker build db"')
    os.system("docker build . -t mysql_db:1.0  -f git/Billing/db/Dockerfile")
    os.system('echo "docker build billing"')
    os.system("docker build . -t billing_server:1.0 -f git/Billing/app/Dockerfile")
    os.system('echo "docker compose up"')
    os.system("docker compose -f git/Billing/docker-compose.yml --env-file ./git/Billing/config/.env.dev up --detach")
    os.system('echo "run the tests"')
    os.system("./git/Billing/test_batch.sh")
    os.system('echo "docker rm"')
#    os.system("docker rm -f mysql-flask-app-container python-flask-app-container")
#    os.system("rm -r git")
#    os.system("mkdir git")
#     if test_result == True:
#         send_email(f"Commit on branch {branch} - tests passed.", f"Bravo {committer_mail}! Tests results:", committer_mail)
#     else:
#         send_email(f"Commit on branch {branch} - tests not passed.", f"Sorry {committer_mail}, Tests results:", committer_mail)
    lock.release()

    return jsonify(success=True)


@app.route("/home")
def home():

    return lista


if __name__ == "__main__":
    testingflag = False
    app.run(host="0.0.0.0", port=8089)

import smtplib
from email.mime.text import MIMEText
from flask import Flask, jsonify, request
import json
import os
import threading
import time
import re
import subprocess

app = Flask(__name__)

lista = []
lock = threading.Lock()
mailing_list = ['dawidtomczynski@gmail.com', 'bekasmaciej@gmail.com', 'adamkobus11@gmail.com',
                'dominikborkowski89@gmail.com', 'adam.stegienko1@gmail.com']

testingflag = False


@app.route("/monitor", methods=["POST"])
def health():
    r = request.data.decode('utf-8')
    return jsonify(success=True)


#asd
@app.route("/api", methods=["POST"])
def continuous_integration():
    r = request.json
    before = r["before"]
    after = r["after"]
    branch = r["ref"]
    commits = r['commits']
    for commit in commits:
        committer_mail = commit['author']['email']
    lock.acquire()
    os.system("docker rm -f MYSQL-Billing-app-testing Billing-app-testing Weight-app-testing MYSQL-Weight-app-testing")
    os.system("rm -r git")
    os.system("mkdir git")
    os.system("git clone https://github.com/maciob/DeveleapDevWeek git")
    lista.append(before)
    lista.append(after)
    lista.append(branch)
    #branch_name = re.search(r'/[a-zA-Z]+g', branch)
    os.system('echo "git checkout to dir git"')
    os.system(f"git -C git/ checkout {after}")
    os.system('echo "docker build db"')
    os.system("docker build . -t mysql_db:1.0  -f git/Billing/db/Dockerfile")
    os.system('echo "docker build billing"')
    os.system("docker build . -t billing_server:1.0 -f git/Billing/app/Dockerfile")
    os.system('echo "docker build weight"')
    os.system("docker build . -t weight_server:1.0 -f git/Weight/app-weight/Dockerfile")
    os.system('echo "docker compose up"')
    os.system("docker-compose -f git/Billing/docker-compose.yml --env-file ./git/Billing/config/.env.dev up --detach")
    os.system('echo "docker compose up"')
    os.system("docker-compose -f git/Weight/docker-compose.yml --env-file ./git/Weight/config/.env.dev up --detach")

    time.sleep(20)

    os.system('echo "run the tests"')

    result = subprocess.Popen("./git/Billing/test_batch.sh")
    text = result.communicate()[0]
    return_code = result.returncode

    os.system('echo "docker rm"')

    subject_pass = f"Commit on branch {branch} - tests passed."
    subject_fail = f"Commit on branch {branch} - tests failed."
    message_pass = f"Congrats! Your commit {after} passed all the tests."
    message_fail = f"Sorry! Your commit {after} passed only {return_code} tests."
    if return_code == 100 and "master" in branch:
        # os.system(f"git checkout {br}")
        # os.system(f"git merge {after}")
        # os.system(f"git push origin {branch}")
        os.system('echo "stawiamy nowa wersja z mastera"')
        os.system("docker build . -t mysql_db:1.1  -f git/Billing/db/Dockerfile")
        os.system("docker build . -t billing_server:1.1  -f git/Billing/app/Dockerfile")
        os.system("docker build . -t weight_server:1.1  -f git/Weight/app-weight/Dockerfile")
        os.system("docker rm -f MYSQL-Billing-app Billing-app Weight-app MYSQL-Weight-app")
        os.system('echo "docker compose up"')
        os.system("docker-compose -f git/Billing/prod.yml --env-file ./git/Billing/config/.env.prod up --detach")
        os.system('echo "docker compose up"')
        os.system("docker-compose -f git/Weight/prod.yml --env-file ./git/Weight/config/.env.prod up --detach")
    elif return_code == 100 and "master" not in branch:
        os.system('echo "success"')
        #send_email(subject_pass, message_pass, committer_mail)
    else:
        os.system('echo "fail"')
        #send_email(subject_fail, message_fail, committer_mail)
    lock.release()

    return jsonify(success=True)


def send_email(subject, message, receiver_mail):
    global mailing_list
    #  sends an email with feedback to committer, team leaders and devops team
    os.system('echo "tu tez bylem"')
    msg = MIMEText(message, 'plain')
    msg['Subject'] = subject
    port = 587
    my_mail = 'blueteamdevops@outlook.com'
    my_password = 'G00gleit'
    with smtplib.SMTP('smtp-mail.outlook.com', port) as server:
        server.starttls()
        server.login(my_mail, my_password)
        for mail in mailing_list:
            os.system(f'echo "{mail}"')
            server.sendmail(my_mail, mail, f"CC: {msg.as_string()}")
        if receiver_mail not in mailing_list:
            server.sendmail(my_mail, receiver_mail, msg.as_string())
        server.quit()


@app.route("/home")
def home():

    return lista


if __name__ == "__main__":
    testingflag = False
    app.run(host="0.0.0.0", port=8089)

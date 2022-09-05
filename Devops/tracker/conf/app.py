import smtplib
from email.message import EmailMessage
import os
import yaml

conf = yaml.load(open('app.yml'),Loader=yaml.Loader)
email = conf['user']['email']
pwd = str(conf['user']['password'])

branch = "XD"
after = "XD"
return_code = "XD"
print(pwd)
print(email)
print(type(email))
subject_pass = f"Commit on branch {branch} - tests passed."
subject_fail = f"Commit on branch {branch} - tests failed."
message_pass = f"Congrats! Your commit {after} passed all the tests."
message_fail = f"Sorry! Your commit {after} passed only {return_code} tests."

msg = EmailMessage()


msg['Subject'] = subject_pass
#msg['To'] = ['bekasmaciej@gmail.com']
msg['To'] = ['dawidtomczynski@gmail.com', 'bekasmaciej@gmail.com', 'adamkobus11@gmail.com', 'dominikborkowski89@gmail.com', 'adam.stegienko1@gmail.com']

msg.set_content(message_pass)
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, pwd)
        smtp.send_message(msg)
except:
    print("Failure in sending mail")
    pass

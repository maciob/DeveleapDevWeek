#!/usr/bin/env python3
from contextlib import closing
from flask import Flask, render_template
import socket
import os
import requests



app = Flask(__name__)

@app.route("/health-post",methods=["GET"])
def health_post():
    post_ports = [8080, 8081, 8082, 8083, 8084, 8085, 8086, 8087, 8088, 8089]
    response_codes = []
    msg = "Hello"
    for p in post_ports:
        if p==8081 or p==8083 or p==8085 or p==8087:
            output = os.system(f"curl http://18.170.241.119:{p}")
            if str(output) != "256":
                match str(p):
                    case "8081":
                        response_codes.append(f"Service at port {str(p)} is DOWN. Service is MYSQL Weight DB.")

                    case "8083":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is MYSQL Billing DB.')

                    case "8085":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is MYSQL Weight DB Testing.')

                    case "8087":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is MYSQL Billing DB Testing.')
            else:
                match str(p):
                    case "8081":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is MYSQL Weight DB.')

                    case "8083":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is MYSQL Billing DB.')

                    case "8085":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is MYSQL Weight DB Testing.')

                    case "8087":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is MYSQL Billing DB Testing.')

        else:
            try:
                requests.post(f"http://18.170.241.119:{p}/monitor", msg)
                match str(p):
                    case "8080":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is Weight App.')

                    case "8082":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is Billing App.')

                    case "8084":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is Weight App Testing.')

                    case "8086":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is Billing App Testing.')

                    case "8088":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is Monitor.')

                    case "8089":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is Github Tracker/CI.')

            except:
                match str(p):
                    case "8080":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is Weight App.')

                    case "8082":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is Billing App.')

                    case "8084":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is Weight App Testing.')

                    case "8086":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is Billing App Testing.')

                    case "8088":
                        response_codes.append(f'Service at port {str(p)} is DOWN. Service is Monitor.')

                    case "8089":
                        response_codes.append(f'Service at port {str(p)} is UP. Service is GithubTracker/CI.')


    return render_template('monitor.html', response_codes=response_codes)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)

FROM python:slim
WORKDIR app/
COPY git/Billing/app/. .
COPY git/Billing/app/in/rates.xlsx in/.
RUN pip install -r requirements.txt
ENTRYPOINT ["./billing_server.py"]

FROM python:slim
WORKDIR app/
COPY git/Billing/app/. .
RUN pip install -r requirements.txt
ENTRYPOINT ["./billing_server.py"]

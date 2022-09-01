FROM python:slim
COPY Billing/app/ /app/
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["./billing_server.py"]

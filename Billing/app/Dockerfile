FROM python:slim
COPY ./git/Billing/app/ /app/
WORKDIR /app
RUN mkdir in
RUN pip install -r requirements.txt
ENTRYPOINT ["./billing_server.py"]

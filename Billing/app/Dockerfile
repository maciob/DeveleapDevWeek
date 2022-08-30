FROM python:3.11.0rc1-alpine3.16
COPY . /app/
WORKDIR /app
RUN pip install flask
RUN pip install flask-mysql
ENTRYPOINT ["./billing_server.py"]
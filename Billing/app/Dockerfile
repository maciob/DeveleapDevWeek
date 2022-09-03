FROM python:slim
COPY ./git/Billing/app/billing_server.py /app/billing_server.py
COPY ./git/Billing/app/requirements.txt /app/requirements.txt
COPY ./git/Billing/app/templates /app/templates
WORKDIR /app
RUN mkdir in
RUN pip install -r requirements.txt
ENTRYPOINT ["./billing_server.py"]

FROM python:3.11-rc
RUN FLASK_APP=app-weight
WORKDIR /flask/app
COPY ./git/Weight/app-weight/. /flask/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app-weight.py"]

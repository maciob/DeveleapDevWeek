FROM python:3.11-rc
RUN FLASK_APP=app-weight
WORKDIR /flask/app
WORKDIR /flask/app
COPY . /flask/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app-weight.py"]
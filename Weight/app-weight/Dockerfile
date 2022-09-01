FROM python:3.7
RUN python -m venv /opt/venv \
    FLASK_APP=flaskapp
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /flask/app
COPY . /flask/app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app-weight.py"]
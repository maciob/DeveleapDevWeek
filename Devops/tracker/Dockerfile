FROM python:3.8
WORKDIR app/
COPY requirements.txt requirements.txt
COPY app.py app.py
RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install apt-transport-https ca-certificates curl software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
RUN apt-get -y update
RUN apt-get -y install docker-ce
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "-m" , "flask", "--app", "app.py", "run", "--host=0.0.0.0"]


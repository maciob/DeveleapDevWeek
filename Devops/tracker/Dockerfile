FROM python:3.8-slim-buster
WORKDIR app/
COPY requirements.txt requirements.txt
COPY app.py app.py
RUN apt-get -y update
RUN apt-get -y install git
RUN apt-get -y install apt-transport-https ca-certificates curl software-properties-common
RUN pip3 install -r requirements.txt
#RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
RUN apt-cache policy docker-ce
#RUN apt install docker-ce
ENTRYPOINT ["python3", "-m" , "flask", "--app", "app.py", "run", "--host=0.0.0.0"]


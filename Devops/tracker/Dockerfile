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
RUN mkdir -p ~/.docker/cli-plugins/
RUN curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
RUN chmod +x ~/.docker/cli-plugins/docker-compose
ENTRYPOINT ["python3", "-m" , "flask", "--app", "app.py", "run", "--host=0.0.0.0"]


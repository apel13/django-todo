FROM ubuntu:16.04

RUN apt-get update && \
    apt-get upgrade -y && \ 	
    apt-get install -y \
    git \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    nginx \
    supervisor \
    sqlite3 && \
    pip3 install -U pip setuptools && \
      rm -rf /var/lib/apt/lists/*

RUN pip3 install uwsgi

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY service-nginx.conf /etc/nginx/sites-available/default
COPY service-supervisor.conf /etc/supervisor/conf.d/

COPY requirements.txt /home/docker/code/
RUN pip3 install -r /home/docker/code/requirements.txt

COPY . /home/docker/code/
WORKDIR /home/docker/code/
RUN python3 ./manage.py makemigrations && python3 ./manage.py migrate
RUN python3 ./manage.py collectstatic

EXPOSE 80
# CMD python3 ./manage.py runserver 0.0.0.0:80

CMD ["supervisord", "-n"]

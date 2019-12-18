FROM python:buster
ENV PYTHONUNBUFFERED 1

RUN pip3 install uwsgi
COPY requirements.txt /home/docker/code/
RUN pip3 install -r /home/docker/code/requirements.txt
COPY . /home/docker/code/
WORKDIR /home/docker/code/

RUN python3 ./manage.py makemigrations && python3 ./manage.py migrate
# RUN python3 ./manage.py collectstatic

EXPOSE 80
# CMD python3 ./manage.py runserver 0.0.0.0:80
# CMD uwsgi --ini uwsgi.ini

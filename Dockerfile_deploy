FROM tiangolo/meinheld-gunicorn-flask:python3.6-alpine3.8

ADD . .


RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt
RUN pip install sqlalchemy_utils

#ENV GUNICORN_PATH ./gunicorn_conf.py
ENV MODULE_NAME "app"
ENV VARIABLE_NAME "app"

RUN flask db init
RUN flask db migrate -m "first migration"
#RUN mv migrate.mako ./migrations/script.py.mako  

#RUN flask db upgrade

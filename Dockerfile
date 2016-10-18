FROM ubuntu:trusty

ENV LANG en_US.UTF-8

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y supervisor python3-pip python3 python3-dev libmysqlclient-dev mysql-client git

RUN mkdir /code
COPY /weather_snowpack_website /code
WORKDIR /code

RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8
RUN locale

RUN echo "[mysqld]\nexplicit_defaults_for_timestamp = 1" >> /etc/mysql/my.cnf

ADD /weather_snowpack_website/requirements.txt /code/
RUN pip3 install -r /code/requirements.txt

ADD runserver.sh /code/
RUN chmod +x runserver.sh
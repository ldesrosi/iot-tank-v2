FROM flask-base
MAINTAINER Luc Desrosiers "ldesrosi73@gmail.com"

COPY . /app
WORKDIR /app

EXPOSE 5000
ENTRYPOINT ["/usr/local/bin/gunicorn", "trevor:app", "--workers", "1", "-b", "0.0.0.0:5000", "--worker-class", "eventlet"]

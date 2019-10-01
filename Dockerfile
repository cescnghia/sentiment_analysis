FROM python:3-onbuild

ADD flask-app /opt/flask-app
WORKDIR /opt/flask-app

EXPOSE 8080

CMD ["python", "./app.py"]
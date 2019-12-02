FROM python:3

ADD not-a-hello-world-app.py /not-a-hello-world-app.py

CMD [ "python", "./not-a-hello-world-app.py" ]

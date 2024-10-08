FROM python:3.9.19-slim

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "--app=main", "run", "--host=0.0.0.0", "--port=8080"]
FROM python:3.8-slim-buster
COPY requirements.txt requirements.txt
RUN apt update && apt install -y python3-dev gcc libc-dev
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
COPY . .
CMD ["python3", "web.py"]
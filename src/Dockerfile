FROM python:3.8-slim-buster
COPY . .
RUN apt update && apt install -y python3-dev gcc libc-dev ffmpeg libsm6 libxext6
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
RUN python3 install.py 
CMD ["python3", "web.py"]
FROM python:3.11-slim
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev libc-dev libgl1 libglib2.0-0 && apt-get clean
RUN pip install -r requirements.txt
RUN cp __init__.py /usr/local/lib/python3.11/site-packages/ultralytics/cfg/__init__.py
CMD ["python", "web.py"]
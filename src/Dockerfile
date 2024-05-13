FROM python:3.11-slim
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends libgl1 libglib2.0-0 && apt-get clean
RUN pip install -r requirements.txt
CMD ["python", "web.py"]
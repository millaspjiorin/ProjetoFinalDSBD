FROM apache/spark-py:latest

USER root
WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["/opt/spark/bin/spark-submit", "/app/run.py"]

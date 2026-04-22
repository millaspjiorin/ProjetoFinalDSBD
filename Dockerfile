FROM apache/spark-py:latest

USER root
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /opt/spark/jars && \
    curl -L -o /opt/spark/jars/iceberg-spark-runtime.jar \
    https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.10.1/iceberg-spark-runtime-3.5_2.12-1.10.1.jar

COPY . .

CMD ["/opt/spark/bin/spark-submit", "/app/run.py"]
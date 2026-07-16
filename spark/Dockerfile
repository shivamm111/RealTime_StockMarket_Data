FROM apache/spark:3.5.1

COPY deps/*.jar /opt/spark/jars/

USER root
RUN pip install delta-spark==3.2.0
USER spark
FROM ubuntu:22.04

# Install Python, Java, and git
RUN apt-get update && \
    apt-get install -y python3 python3-pip openjdk-17-jdk git g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

EXPOSE 5001

CMD ["python3", "server.py"]
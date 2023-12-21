FROM python:3.9-slim AS chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user

RUN apt update && \
    apt install socat -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/user

COPY main.py .
COPY flag.txt .

RUN chmod 005 main.py && \
    chmod 004 flag.txt

CMD socat \
      -T60 \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"/usr/local/bin/python3 main.py"

FROM python:3.9-slim AS chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user

RUN apt update && \
    apt install socat -y && \
    rm -rf /var/lib/apt/lists/*
    
RUN pip install --no-cache-dir pandas random2

WORKDIR /home/user

COPY main.py .

USER user

CMD socat \
      -T60 \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"python3 /usr/local/bin/python3 main.py"

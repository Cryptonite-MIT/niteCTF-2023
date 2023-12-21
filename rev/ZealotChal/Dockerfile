FROM ubuntu:22.04 AS chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user

RUN apt-get update && \
    apt-get install -y socat

WORKDIR /home/user/

COPY Zealot flag.txt .

RUN chmod 001 chal
RUN chmod 004 flag.txt

USER user

CMD socat \
      -T60 \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"chal"

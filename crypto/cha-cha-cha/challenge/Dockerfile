FROM ubuntu:20.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt update && apt install -y build-essential python3 python3-pip
RUN pip3 install cryptography

COPY secret.py /home/user/
COPY server.py /home/user/

CMD socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"python3 server.py"

FROM ubuntu:20.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
RUN apt update && apt install -y build-essential python3 python3-pip
RUN pip3 install ecdsa
RUN pip3 install pycryptodome

COPY secret.py /home/user/
COPY server.py /home/user/
COPY public.pem /home/user/
COPY users.json /home/user/

CMD socat \
      TCP-LISTEN:8080,reuseaddr,fork \
      EXEC:"python3 server.py"

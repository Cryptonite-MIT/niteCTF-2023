FROM python:3.9-slim AS chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user

RUN apt update && \
    apt install socat -y

COPY main.py /usr/bin/gpgparsemail
COPY flag.txt /var/quantumLava/

RUN chmod 005 /usr/bin/gpgparsemail && \
     chmod 004 /var/quantumLava/flag.txt

USER user

CMD socat \
      -T60 \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"/usr/bin/gpgparsemail"

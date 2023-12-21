FROM python:3.9-slim AS chroot

RUN apt update && \
    apt install cowsay -y && \
    apt purge at -y

RUN mv /usr/games/cowsay /usr/bin/cowsay

COPY flag.txt /etc/cowsay/falg.txt
RUN chmod 444 /etc/cowsay/falg.txt

WORKDIR /home/user

COPY src/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ADD src .

CMD ["run.sh", "1337"]


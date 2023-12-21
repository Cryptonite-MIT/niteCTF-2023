FROM node:slim AS chroot

RUN /usr/sbin/useradd --no-create-home -u 2000 user

WORKDIR /home/user

COPY package.json package-lock.json .

RUN npm install

ADD src .

RUN node initDb.js

CMD ["/usr/local/bin/node", "main.js", "1337"]
    
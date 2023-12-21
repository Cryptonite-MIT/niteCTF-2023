FROM ubuntu:22.04 AS chroot

ENV NODE_MAJOR 20

RUN apt update && apt install -y ca-certificates curl gnupg coreutils wget && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt update && \
    apt install -y nodejs

WORKDIR /home/user

COPY src/package*.json .

RUN npm install

ADD src .

CMD ["/usr/bin/node", "index.js", "1337"]

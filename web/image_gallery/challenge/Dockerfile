FROM python:3.9-slim AS chroot

WORKDIR /home/user

COPY src/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ADD src .

CMD run.sh

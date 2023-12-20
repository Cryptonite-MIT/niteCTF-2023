FROM ubuntu:22.04 AS chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user

RUN apt update && \
    apt install -y socat

COPY the_road_not_taken /home/user/

RUN chmod +x /home/user/the_road_not_taken

USER user

CMD socat \
      -T60 \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"the_road_not_taken"

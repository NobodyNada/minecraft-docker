FROM alpine
RUN apk add openjdk11-jre-headless python3
RUN python3 -m ensurepip && pip3 install --upgrade pip requests
ENV PYTHONUNBUFFERED=1
EXPOSE 25565
RUN mkdir -p /minecraft
WORKDIR /minecraft
COPY ./scripts ./scripts
ENTRYPOINT ["/minecraft/scripts/run.sh"]

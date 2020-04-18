FROM python:3.7

RUN pip install twitch-python \
 && pip install slackclient

COPY reevefresh/__main__.py /bin/reevefresh
RUN chmod a+x /bin/reevefresh

LABEL "my.docker.cmd"="docker run --restart=unless-stopped --name reevefresh --detach --network=host --env SLACK_API_KEY=$SLACK_API_KEY --env TWITCH_API_KEY=$TWITCH_API_KEY localhost:5000/reevefresh:latest -u arhont_tv,blackufa,squirrel"

ENTRYPOINT ["/bin/reevefresh"]

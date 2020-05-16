FROM python:3.7

RUN pip install twitch-python \
 && pip install slackclient

COPY reevefresh/__main__.py /bin/reevefresh
RUN chmod a+x /bin/reevefresh

LABEL "my.docker.cmd"="docker run --restart=unless-stopped --name reevefresh --detach --network=host --env SLACK_API_KEY=$SLACK_API_KEY --env TWITCH_CLIENT_ID=$TWITCH_CLIENT_ID --env TWITCH_CLIENT_SECRET=$TWITCH_CLIENT_SECRET --env TWITCH_REDIRECT_URI=$TWITCH_REDIRECT_URI --env TWITCH_RESPONCE_TYPE=$TWITCH_RESPONCE_TYPE --env TWITCH_SCOPE=$TWITCH_SCOPE localhost:5000/reevefresh:latest -u arhont_tv,blackufa,squirrel"

ENTRYPOINT ["/bin/reevefresh"]

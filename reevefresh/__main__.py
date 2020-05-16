#!/usr/bin/env python

import argparse
import time
import os
import http.client
import json
from twitch import Helix
from slack import WebClient

def main():
    parser = argparse.ArgumentParser(description="Twitch notifications")
    parser.add_argument("-c", "--channel", default="#video", help="Slack channel")
    parser.add_argument("-n", "--notifications", default="#ci",
                        help="Slack channel notifications for errors or warnings")
    parser.add_argument("-i", "--interval", default=30, help="Update interval in seconds", type=int)
    parser.add_argument("-u", "--users", default="", help="Twitch users")
    args = parser.parse_args()

    remember_online_users = []

    TWITCH_CLIENT_ID=os.environ["TWITCH_CLIENT_ID"]
    TWITCH_CLIENT_SECRET=os.environ["TWITCH_CLIENT_SECRET"]
    TWITCH_REDIRECT_URI=os.environ["TWITCH_REDIRECT_URI"]
    TWITCH_RESPONCE_TYPE=os.environ["TWITCH_RESPONCE_TYPE"]
    TWITCH_SCOPE=os.environ["TWITCH_SCOPE"]
    def bearer():
        connection = http.client.HTTPSConnection("id.twitch.tv")
        connection.request("POST", "/oauth2/token?client_id=" + TWITCH_CLIENT_ID
                           + "&client_secret=" + TWITCH_CLIENT_SECRET
                           + "&grant_type=client_credentials")
        response = connection.getresponse()
        return json.loads(response.read().decode('utf8'))['access_token']

    while(True):
        twitch = Helix(client_id=TWITCH_CLIENT_ID,
                       client_secret=TWITCH_CLIENT_SECRET,
                       bearer_token=bearer())
        slack = WebClient(token=os.environ["SLACK_API_KEY"])
        try:
            for user in args.users.split(","):
                if twitch.user(user).is_live:
                    print("TWITCH_LIVE: {}".format(user))
                    if user not in remember_online_users:
                        remember_online_users.append(user)
                        slack.chat_postMessage(channel=args.channel,
                                               attachments=[{"text": "TWITCH_LIVE: https://www.twitch.tv/{}".format(user),
                                                             "color": "#ff0000"}])
                else:
                    if user in remember_online_users:
                        remember_online_users.remove(user)
        except error.HTTPError as exception:
            print("ERROR: {}".format(exception))
            slack.chat_postMessage(channel=args.notifications,
                                   attachments=[{"text": "ERROR: Failed to receive Twitch user status: {}".format(exception),
                                                 "color": "#ff0000"}])
        print("Online users: {}\n".format(",".join(remember_online_users)))
        time.sleep(args.interval)

if __name__ == "__main__":
    main()

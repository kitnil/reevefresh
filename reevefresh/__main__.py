#!/usr/bin/env python

import argparse
import time
import os
from twitch import Helix
from slack import WebClient

def main():
    parser = argparse.ArgumentParser(description="Twitch notifications")
    parser.add_argument("-c", "--channel", default="#video", help="Slack channel")
    parser.add_argument("-i", "--interval", default=30, help="Update interval in seconds", type=int)
    parser.add_argument("-u", "--users", default="", help="Twitch users")
    args = parser.parse_args()
    remember_online_users = []
    while(True):
        twitch = Helix(os.environ["TWITCH_API_KEY"])
        slack = WebClient(token=os.environ["SLACK_API_KEY"])
        for user in args.users.split(","):
            if twitch.user(user).is_live:
                print("TWITCH_LIVE: {}".format(user))
                if user not in remember_online_users:
                    remember_online_users.append(user)
                    slack.chat_postMessage(channel=args.channel, text="TWITCH_LIVE: https://www.twitch.tv/{}".format(user))
            else:
                if user in remember_online_users:
                    remember_online_users.remove(user)
        print("Online users: {}\n".format(",".join(remember_online_users)))
        time.sleep(args.interval)

if __name__ == "__main__":
    main()

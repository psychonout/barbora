from config import slack_settings
from slack import WebClient


SETTINGS = slack_settings()

CLIENT = WebClient(token=SETTINGS["token"])


'''
    TODO:
        function to get channels
        find out if possible to make calls
        push it to github and make pull process for all the other locations
'''


def send_message(message, channel="general"):
    CLIENT.chat_postMessage(
        channel=SETTINGS[channel],
        text=message)

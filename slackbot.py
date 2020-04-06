from config import slack_settings
from slack import WebClient


SETTINGS = slack_settings()

CLIENT = WebClient(token=SETTINGS["token"])


'''
    TODO:
        function to get channels
        find out if possible to make calls
'''


def send_message(message, channel="general"):
    CLIENT.chat_postMessage(
        channel=SETTINGS[channel],
        text=message)

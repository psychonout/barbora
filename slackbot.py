from config import bot_token
from slack import WebClient


CLIENT = WebClient(token=bot_token())

CHANNELS = {
    "barbora": "C0113NV7JG2"
}

'''
    TODO:
        function to get channels
        find out if possible to make calls
        push it to github and make pull process for all the other locations
'''


def send_message(message, channel="C84RDUGQZ"):
    CLIENT.chat_postMessage(
        channel=channel,
        text=message)


def call_somebody(user="D85B580RG"):
    pass

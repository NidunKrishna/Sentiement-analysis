import urllib.request as request
from urllib.error import HTTPError
from http.client import HTTPResponse
from typing import Dict, Union
import json
from datetime import datetime
import signal
import os

signal.signal(signal.SIGINT, signal.SIG_DFL)


class TelegramEcho:
    def __init__(self, TG_KEY: str):
        self.TG_URL = "https://api.telegram.org/bot{}/{}"
        self.TG_KEY = TG_KEY

        self.__last = None
        self.__last_time = None

    def run(self):
        while True:
            try:
                incoming = self.__handle_incoming()

                if not incoming:
                    continue

                if self.__last == incoming["message"]["message_id"]:
                    continue
                else:
                    self.__last = incoming["message"]["message_id"]

                if not self.__last_time:
                    self.__last_time = incoming["message"]["date"]
                    continue
                elif self.__last_time < incoming["message"]["date"]:
                    self.__last_time = incoming["message"]["date"]
                else:
                    continue

                self.__print_incoming(incoming)

                # Specify the chat ID here
                chat_id = 1407068016

                outgoing = self.__handle_outgoing(
                    chat_id,
                    incoming["message"]["text"])

                self.__print_outgoing(outgoing)

            except (HTTPError, IndexError):
                continue

    def __handle_outgoing(self, chat_id: int,
                      message_txt: str) -> Dict[str, Union[int, str]]:
        try:
            outgoing_text = f"You sent me: {message_txt}"

            _data: Dict[str, Union[int, str]] = {
                "chat_id": chat_id,
                "text": outgoing_text
            }

            _request: request.Request = request.Request(
                self.TG_URL.format(self.TG_KEY, "sendMessage"),
                data=json.dumps(_data).encode('utf8'),
                headers={"Content-Type": "application/json"})

            sendMessage: HTTPResponse = request.urlopen(_request)
            response_data: Dict[str, Union[int, str]] = json.loads(
                sendMessage.read().decode())

            if "ok" in response_data and response_data["ok"]:
                return response_data
            else:
                print(f"Failed to send message. Response: {response_data}")
                return {}

        except HTTPError as e:
            print(f"HTTPError in __handle_outgoing: {e.code} - {e.reason}")
            print(f"Response content: {e.read().decode()}")
            return {}
        except Exception as e:
            print(f"An error occurred in __handle_outgoing: {e}")
            return {}


    def __print_outgoing(self, outgoing):
        print("[>>>] Message Sent")

        # Check if 'text' key is present
        if 'text' in outgoing:
            print("\tText: %s" % outgoing["text"])
        else:
            print("\tText not available")

        # Check if 'from' key is present
        if 'from' in outgoing and 'first_name' in outgoing['from']:
            print("\tFrom: %s" % outgoing["from"]["first_name"])
        else:
            print("\tSender information not available")

        # Check if 'message_id' key is present
        if 'message_id' in outgoing:
            print("\tMessage ID: %d" % outgoing["message_id"])
        else:
            print("\tMessage ID not available")

        # Check if 'chat' key is present and has 'id' key
        if 'chat' in outgoing and 'id' in outgoing['chat']:
            print("\tChat ID: %d" % outgoing["chat"]["id"])
        else:
            print("\tChat ID not available")

        print("-" * os.get_terminal_size().columns)


if __name__ == "__main__":
    tg = TelegramEcho("6599628479:AAEH5OFwkEmjuMopAAMuC8JeRiak5htjItE")
    tg.run()

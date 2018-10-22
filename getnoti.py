# getnoti.py
#
# Simple repeat macro for noti_parser
#
import time
import os
import noti_parser

url = "http://elogbook.cern.ch/eLogbook/eLogbook.jsp?lgbk=60"
# To get a telegram bot token, check this url: https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
chat_id = ""
token = ""

while(1):
    if(noti_parser.get_latest(url,chat_id,token) == 0):
        print("No change")
    time.sleep(30)

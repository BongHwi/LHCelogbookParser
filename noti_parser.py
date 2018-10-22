# noti_parser.py
import sys
import requests
from bs4 import BeautifulSoup
import os

if len(sys.argv) != 2:
    print("WARNING: it'd be better run with url \neg) python3 noti_parser.py http://elogbook.cern.ch/eLogbook/eLogbook.jsp?lgbk=60")
    url = "http://elogbook.cern.ch/eLogbook/eLogbook.jsp?lgbk=60"

def get_latest(url,chat_id,token):
    # Check the latest title of the notificiation website, and compare it with old one. If it's different with the old one, send telegram massage
    # To get a telegram bot token, check this url: https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token
    # Input: url
    #        chat_id: ex) "123456789"
    #        token: ex) "123456789:ABCDEFGHijklmopqrhblhablah"
    # if there is update, return updated post
    # if no update, return 0
    
    # Base URL of file
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    link_phrase = soup.find("table",id="events_table").find("tbody")
    latest = link_phrase.contents[-2].text.replace("\n","").replace("  ","").replace("\r","-").replace("\t","").replace("Comment","").replace("New","").replace("--","").split("created")[0]
    
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        if before != latest:
            print("new post: ", latest)
        f_read.close()
    
    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
        f_write.write(latest)
        f_write.close()

    data = {'chat_id': chat_id, 'text':latest}

    if before != latest:
        requests.post('https://api.telegram.org/bot'+token+'/sendMessage', data=data)
        return latest
    else:
        return 0

if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) == 2:
        url = sys.argv[1]
    get_latest(url)

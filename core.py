import requests
from twilio.rest import Client
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime
import random
import configparser

#Sites of Interest
sites = ['https://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/6364255.p?skuId=6364255',
         'https://www.bestbuy.com/site/nintendo-switch-32gb-console-gray-joy-con/6364253.p?skuId=6364253',
         'https://www.bestbuy.com/site/nintendo-switch-animal-crossing-new-horizons-edition-32gb-console-multi/6401728.p?skuId=6401728',
         'https://www.bestbuy.com/site/combo/nintendo-switch-consoles/8cfdae25-e006-446b-9433-1e7496c3dc75',
         'https://www.bestbuy.com/site/combo/nintendo-switch-consoles/9a9bf66d-e475-47bc-8860-7c44535f323e'
         ]

#Init stuff
headers = {'User-Agent': 'Mozilla/5.0'}
session = requests.Session()

def open_site(site, headers, session):
    time.sleep(2)
    r = session.get(site, headers=headers)
    if r.status_code == 200:
        content = r.text
        check_site(content, site)
    else:
        print(f"Connection Failed. Status Code: {r.status_code}")

def check_site(content, site):
    soup = BeautifulSoup(content, 'html.parser')
    search_result = soup.find_all(string="Add to Cart")
    config = configparser.ConfigParser()
    config.read('config.cfg')
    account_sid_num = config.get('SWITCH TRACKER', 'ACCOUNT_SID')
    auth_token_num = config.get('SWITCH TRACKER', 'AUTH_TOKEN')
    from_num = config.get('SWITCH TRACKER', 'FROM')
    to_num = config.get('SWITCH TRACKER', 'TO')
    if search_result:

        account_sid = account_sid_num
        auth_token = auth_token_num
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body="Switch in stock!",
            from_=from_num,
            to=to_num
            )
        print(message.sid)
        print(datetime.now())
        print("Switch Found!")
        print(site)
        print(soup.prettify())
        raise SystemExit(0)
    else:
        print("Not here")
        print(datetime.now())

def find_switch(websites, headers, session):
    for website in websites:
        open_site(website, headers, session)

schedule.every(random.randint(17, 27)).seconds.do(find_switch, sites, headers, session)

while True:
    schedule.run_pending()
    time.sleep(1)



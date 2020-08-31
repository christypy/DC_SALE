import requests
from bs4 import BeautifulSoup
from time import sleep
import time

url="https://www.ptt.cc/bbs/DC_SALE/index.html"
def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec
second = sleeptime(1,0,0)

def get_price(url1):
    r = requests.get(url1)
    soup = BeautifulSoup(r.text,"html.parser")
    description = soup.find("meta",  property="og:description")
    get_price=[i.split()[1] for i in description["content"].split('\n') if '價格' in i ][0]
    return str(get_price)
def get_all_href(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.select("div.title")    
    for item in results:
        try:
            item_href = item.select_one("a")
            if '售'in item_href.text  and '富士'in item_href.text  and '35' in item_href.text:
                get_url='https://www.ptt.cc'+item_href.get("href")
                price=get_price(get_url)
                return [item_href.text,price,get_url]
        except:
            pass
while 1==1:
    post_txt=[]
    for page in range(1,3):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        btn = soup.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url = next_page_url
        post_txt.append(get_all_href(url = url))
    post=[i for i in post_txt if i is not None]
    headers = {"Authorization": "Bearer " + "WYTJLyezlYkbDhJhVo85YOkI3HmW5dWrWOTmb2nQXSf","Content-Type": "application/x-www-form-urlencoded"}
    params = {"message": post[0][0]+post[0][1]+post[0][2]}
    r = requests.post("https://notify-api.line.me/api/notify",headers=headers, params=params)
    print(r.status_code)  #200
    time.sleep(second)
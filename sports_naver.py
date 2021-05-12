import json, requests
import sys
from bs4 import BeautifulSoup
headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36', 'Accept':'application/json, text/plain, */*','Accept-Language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'}
def get_channel_url(var):
    link=requests.get("https://apis.naver.com/pcLive/livePlatform/sUrl?ch="+var+"&q=5000&p=hls&cc=KR&env=pc", headers=headers)
    soup=BeautifulSoup(link.text, 'html.parser')
    json_code=json.loads(str(soup))
    object=json_code['secUrl']
    return object
def main_code():
    code=sys.argv[1]
    video=get_channel_url(code)
    print(video)
main_code()

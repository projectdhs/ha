from flask import Flask, escape, request
import re, os, sys
import requests
from bs4 import BeautifulSoup
import json
from json import JSONDecodeError
import time
#fileLocation='C:/bin/'
fileLocation='/var/www/ha/radio/'
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'
@app.route('/sav_sbs/<string:var>')    
def sav_sbs(var):
    sbs_ch={'sbs' : 'S01', 'sbspowerfm' : 'S07', 'sbslovefm': 'S08', 'sbsplus' : 'S03', 'sbsgolf' : 'S05', 'sbsfune' : 'S04', 'sbsmtv' : 'S09', 'sbsbiz': 'S06' }
    s=requests.session()
    html=s.get("http://apis.sbs.co.kr/play-api/1.0/onair/channel/"+sbs_ch[var]+"?v_type=2&platform=pcweb&protocol=hls&jwt-token=")
    soup=BeautifulSoup(html.text, 'html.parser')
    jsons=json.loads(str(soup))
    j=jsons['onair']['source']["mediasourcelist"][0]['mediaurl']
    #print(j)
    s1=j[:250]
    s2=j[250:]
    p={'link1' : s1, 'link2' : s2}
    p=json.dumps(p)
    #f=open('/var/www/ha/radio/sbs.txt', 'w', encoding='utf-8')
    f=open(fileLocation + var + '.txt', 'w', encoding='utf-8')
    f.write(p)
    f.close()
    return j
@app.route('/pr_sbs/<string:var>')
def print_sbs(var):
    f=open(fileLocation + var + '.txt', 'r', encoding='utf-8')
    return f.read()
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

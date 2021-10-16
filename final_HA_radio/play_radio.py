import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, redirect

#21-10-16 추가, 파일 경로 지정
direc='/home/radios/'

app = Flask(__name__)

def play_media(urls, infor):
    payload = {
        "entity_id": "[플레이어 엔티티 아이디]",
        "media_content_id": urls,
        "media_content_type": "music",
        "extra": 
            {"metadata" : 
                {"metadataType" : 3 ,
                "title" :  infor, 
                "images" :[
                {"url" : "https://tilos.hu/images/kockalogo.png"}]

                }
                    }
    }
    h={"Authorization" : "Bearer [장기토큰]", "content-type": "application/json"}
    re = requests.post('[HA URL : https://ip:port]/api/services/media_player/play_media', headers=h, data = json.dumps(payload))
    print(re.status_code)


@app.route('/play_mbc')
def sav_mbc():
    hh={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'Referer' : 'http://mini.imbc.com/', 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding' : 'gzip, deflate'}
    ch=request.args.get("ch")
    mbc_ch={'mbcfm4u' : 'mfm', 'mbcfm' : 'sfm', 'allthat': 'chm'}
    mbc_ch_param={'mbcfm4u' : 'mbc FM4U', 'mbcfm' : 'MBC 표준 FM', 'allthat' : 'MBC all that'}
    html=requests.get('http://miniplay.imbc.com/WebHLS.ashx?channel='+mbc_ch[ch]+'&protocol=M3U8&agent=ios&nocash=0.3996827673840577&callback=jarvis.miniInfo.loadOnAirComplete', headers=hh)
    text=str(html.text)
    text='http://'+text.split('"http://')[1].split('"')[0]
    html2=str(requests.get(text, headers=hh).text)
    text2=html2.split('m3u8?')[1].strip()
    #print(text2)
    urls='http://175.158.10.83/s'+mbc_ch[ch]+'/_definst_/'+mbc_ch[ch]+'.stream/playlist.m3u8?'+text2
    play_media(urls, mbc_ch_param[ch])
    return 'success'


#21-10-16 sbs 라디오 패치 (miumida님 소스 참고)
@app.route('/play_sbs')
def sav_sbs():

    ch=request.args.get("ch")
    sbs_ch={'powerfm' : 'powerpc', 'lovefm': 'lovepc'}
    SBS_URL='https://apis.sbs.co.kr/play-api/1.0/livestream/{}/{}?protocol=hls&ssl=Y'
    
    sbsheader = {
        'Host': 'apis.sbs.co.kr',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) GOREALRA/1.2.1 Chrome/85.0.4183.121 Electron/10.1.3 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://gorealraplayer.radio.sbs.co.kr',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://gorealraplayer.radio.sbs.co.kr/main.html?v=1.2.1',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko',
        'If-None-Match': 'W/"134-0OoLHiGF4IrBKYLjJQzxNs0/11M"'
    }
    html = requests.get(SBS_URL.format(sbs_ch[ch], ch), headers=sbsheader)
    j=html.text
    

    play_media(j, sbs_ch_param[ch])
    print(j)
    return 'success'

@app.route('/play_kbs')
def sav_kbs():
    ch=request.args.get("ch")
    kbs_ch={'kbscoolfm' : 'url', 
            'kbshappyfm': 'url',
            'kbs1radio' : 'url',
            'kbsclassicfm' : 'url',
            'kbs3radio' : 'url'}
    kbs_ch_param={'kbscoolfm' : 'kbs 쿨 FM',
                  'kbshappyfm' : 'kbs 해피 FM',
                  'kbs1radio' : 'kbs 1 라디오',
                  'kbsclassicfm' : 'kbs 클래식 FM',
                  'kbs3radio' : 'kbs 3 라디오'}
    play_media(kbs_ch[ch], kbs_ch_param[ch])
    return 'success'



@app.route('/play_kbs1')
def kbs():
    ch=request.args.get("ch")
    kbs_ch={'kbs1radio' : '21', 'kbs2radio' : '22', 'kbs3radio': '23', 'kbs1fm' : '24', 'kbs2fm' : '25' }
    hh={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36', 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7', 'Accept-Encoding' : 'gzip, deflate'}
    sour=requests.get("https://onair.kbs.co.kr/index.html?sname=onair&stype=live&ch_code="+kbs_ch[ch], headers=hh)
    soup=str(BeautifulSoup(sour.text, 'html.parser'))
    lines=soup.split("\n")
    for each_line in lines:
        if(each_line.find("Key-Pair-Id")>0):
            line = each_line
            break
    line=line.replace('\\', '')
    stream=line.split('"service_url":"')[1].split('"')[0]
    return redirect(stream, code=302)

#21-10-16 추가
@app.route('/return_cbs_music')
def return_cbs_music():
    f=open(direc+'cbs_music.txt', 'r')
    get_url=f.read()
    f.close()
    return redirect(get_url, code=302)
    
@app.route('/return_cbs_fm')
def return_cbs_fm():
    f=open(direc+'cbs_fm.txt', 'r')
    get_url=f.read()
    f.close()
    return redirect(get_url, code=302)
    
@app.route('/return_ifm')
def return_ifm():
    f=open(direc+'ifm.txt', 'r')
    get_url=f.read()
    f.close()
    return redirect(get_url, code=302)
    
@app.route('/return_tbnfm')
def return_tbnfm():
    f=open(direc+'tbnfm.txt', 'r')
    get_url=f.read()
    f.close()
    return redirect(get_url, code=302)
    
@app.route('/return_tbsfm')
def return_tbsfm():
    f=open(direc+'tbsfm.txt', 'r')
    get_url=f.read()
    f.close()
    return redirect(get_url, code=302)

@app.route('/return_ytn')
def return_ytn( ):
    f=open(direc+'ytn.txt', 'r')
    get_url=f.read()
    f.close()
    return redirect(get_url, code=302)
#21-10-16 추가 끝


@app.route('/play_tbs')
def sav_tbs():
    j='url'
    play_media(j, 'tbs 라디오')
    return 'success'

@app.route('/play_tbn')
def sav_tbn():
    j='url'
    play_media(j, 'tbn 라디오')
    return 'success'

@app.route('/play_ifm')
def sav_ifm():
    j='url'
    play_media(j, '경인방송 라디오')
    return 'success'

@app.route('/play_ytn')
def sav_ytn():
    j='url'
    play_media(j, 'ytn 라디오')
    return 'success'

@app.route('/play_cbs_music')
def sav_cbs_m():
    j='url'
    play_media(j, 'cbs 음악 FM')
    return 'success'

@app.route('/play_cbs_fm')
def sav_cbs():
    j='url'
    play_media(j, 'cbs FM')
    return 'success'

#21-10-16 방식 변경
@app.route('/play_ebs')
def sav_ebs():
    f=open(direc+'ebs.txt', 'r')
    play_media(f.read(), 'ebs 라디오')
    f.close()
    return 'success'

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8989)

import requests
import json
import time
import os

def web_request(method_name, url, timeout_seconds=3):
    """Web GET or POST request를 호출 후 그 결과를 dict형으로 반환 """
    method_name = method_name.upper() # 메소드이름을 대문자로 바꾼다 
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')
        
    if method_name == 'GET': # GET방식인 경우
        response = requests.get(url=url, timeout=timeout_seconds)
    elif method_name == 'POST': # POST방식인 경우
        if is_urlencoded is True:
            response = requests.post(url=url, data=dict_data, \
                                     timeout=timeout_seconds, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), \
                                     timeout=timeout_seconds, headers={'Content-Type': 'application/json'})
    
    dict_meta = {'status_code':response.status_code, 'ok':response.ok, 'encoding':response.encoding, 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']): # JSON 형태인 경우
        return {**dict_meta, **response.json()}
    else: # 문자열 형태인 경우
        return {**dict_meta, **{'text':response.text}}
    
def web_request_retry(num_retry=3, sleep_seconds=1, **kwargs):
    """timeout발생 시 sleep_seconds쉬고 num_retyrp번 재시도 한다"""
    for n in range(num_retry):
        try:
            return web_request(**kwargs)
        except requests.exceptions.Timeout:
            print(str(n+1) + ' Timeout')
            time.sleep(sleep_seconds)
            continue
    return None
fail = 0
while True:
    try:
       url  = '웹서버url' # IP주소는 접속할 사이트주소 또는 IP주소를 입력한다          # 요청할 데이터
       response = web_request_retry(method_name='GET', url=url, num_retry=2)
       if response is not None: 
           print(response)
           if response['ok'] == True:
               print('Good')
               if fail >= 1:
                   fail = 0
        # 성공 응답 시 액션
    except requests.exceptions.ConnectionError:
        print("Connection refused")
        fail = fail + 1
    if fail >= 1:
        print("fail = ", fail)
        web_request_retry(method_name='GET', url="텔레그램 RPI Server", num_retry=2)
        os.system('mosquitto_pub -m "" -t "plug/off"')
        time.sleep(15)
        os.system('mosquitto_pub -m "" -t "plug/on"')   
    if fail >= 4:
        web_request_retry(method_name='GET', url="텔레그램 Python stoped", num_retry=2) 
        break
    time.sleep(600)

import sys
import requests

def write_file(a1, a2):
	f = open(direc+'/'+a1, 'w')
	f.write(a2)
	f.close()
    
#파일 저장 경로 지정
direc='/home/radios/'

arg1 = sys.argv[1]
if(arg1 == 'update'):
	r1 = requests.get('https://raw.githubusercontent.com/projectdhs/kor_radio/main/cbs_music.txt')
	write_file('cbs_music.txt', r1.text.replace('\r','').replace('\n',''))
	r1 = requests.get('https://raw.githubusercontent.com/projectdhs/kor_radio/main/cbs_fm.txt')
	write_file('cbs_fm.txt', r1.text.replace('\r','').replace('\n',''))
	r1 = requests.get('https://raw.githubusercontent.com/projectdhs/kor_radio/main/ifm.txt')
	write_file('ifm.txt', r1.text.replace('\r','').replace('\n',''))
	r1 = requests.get('https://raw.githubusercontent.com/projectdhs/kor_radio/main/tbnfm.txt')
	write_file('tbnfm.txt', r1.text.replace('\r','').replace('\n',''))
	r1 = requests.get('https://raw.githubusercontent.com/projectdhs/kor_radio/main/tbsfm.txt')
	write_file('tbsfm.txt', r1.text.replace('\r','').replace('\n',''))
	r1 = requests.get('https://raw.githubusercontent.com/projectdhs/kor_radio/main/ytn.txt')
	write_file('ytn.txt', r1.text.replace('\r','').replace('\n',''))


   

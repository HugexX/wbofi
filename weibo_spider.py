#-*- coding: utf-8 -*-
import re, requests, signal, sys, shutil
from lxml import etree
from os.path import expanduser

def handleTimeOut(signum, frame):
	print "超时 请检查防火墙设置或更改超时时间"
	sys.exit(1)

def cheTimeOut(handler, sec):
	signal.signal(signal.SIGALRM, handleTimeOut)
	signal.setitimer(signal.ITIMER_REAL, sec)

def getContent(userId):
	try:
		userId = "http://weibo.com/"+str(userId)
		userAgent = {'User-agent': 'Googlebot'}
		return requests.get(userId, headers=userAgent)
	except requests.exceptions.ConnectionError:
		print "请检查您的网络连接"
		sys.exit(1)

def getName(pageContent):
	try:
		return re.findall(r"CONFIG\['onick'\]='(.*?)'", pageContent.text)[0].encode('utf-8')
	except IndexError:
		print "没有找到这个用户"
		sys.exit(1)

def getOid(pageContent):
	try:
		return re.findall(r"CONFIG\['oid'\]='(.*?)'", pageContent.text)[0].encode('utf-8')
	except IndexError:
		print "没有找到这个用户"
		sys.exit(1)

def getHeadPic(userName, pageContent):
	path = expanduser("~")+'/'+userName+'.jpg'
	xhtml = etree.HTML(pageContent.text)
	imgLis = xhtml.xpath('//div[@class="pf_head_pic"]/img/@src')
	loadedImg = requests.get(imgLis[0], stream=True)
	if loadedImg.status_code == 200:
		with open(path, 'wb') as f:
			loadedImg.raw.decode_content = True
			shutil.copyfileobj(loadedImg.raw, f)   
			print "头像已下载到: "+path

def getFerList(userName, pageContent):
	pass

if __name__ == "__main__":
	cheTimeOut(handleTimeOut, 8)
	userId = 'hanhan'
	content = getContent(userId)
	userName = getName(content)
	userOid = getOid(content)
	getHeadPic(userName, content)
	print "用户名: "+userName

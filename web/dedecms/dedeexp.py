#!/usr/bin/env python
#search the dedecms version at the zoomeye,get the host url and test the exp.
#joey:joeyxy83@gmail.com create at 20131125

from threading import Thread
from Queue import Queue
from termcolor import colored
import urllib
import re
import sys
import httplib
from termcolor import colored


url_queue = Queue()


def showinfo():
	print "#########################################################"
	print "###                 search result                     ###"
	print "###  usage: python geturl.py keyword pagenumber       ###"
	print "###        ex: python geturl.py dedecms:5.1 5         ###"
	print "#########################################################"

def test():
	print "<h4><a href=\"(.*)\" target=\"_blank\""

def gethtml(url):
	page=urllib.urlopen(url)
	html=page.read()
	return html

def geturl(html):
	a="<h4><a href=\"(.*)\" target=\"_blank\""
	resp=re.findall(a,html)
	return resp

def check_url(i,url_q):
	#print "the thread:%s" % i	
	while True:
		host=url_q.get().split('//')[1]
		resource = '/plus/download.php'
		resource2 = '/plus/search.php'
		try:
			conn = httplib.HTTPConnection(host,80)
			#print 'http connection created success'
			#make request
			req = conn.request('GET',resource)
			#print 'request for :%s at host: %s' % (resource,host)
			#get response
			response = conn.getresponse()
			#print 'response status:%s' % response.status
                        if response.status in [200,301]:
				print colored("Url:%s%s can access" % (host,resource),'green')
		except httplib.HTTPException,e:
			print 'HTTP connection failed:%s' % e
			url_q.task_done()
		except :
			print 'other error.' 
			url_q.task_done()
		url_q.task_done()

def main(keywords,pagenum):
	num=0
	for x in range(1,int(pagenum)+1):
		html=gethtml('http://zoomeye.scanv.com/search?q=' + keywords + '&p=' + pagenum)
		url=geturl(html)
		num+=len(url)
		for y in url:
			print y
			url_queue.put(y)
	print "total"+str(num)+"urls!"

	url_threads = 50
        if url_queue.qsize() < url_threads :
		url_threads = url_queue.qsize()

	for i in range(url_threads):
		worker = Thread(target=check_url,args=(i,url_queue))
		worker.setDaemon(True)
		worker.start()

	print "Main Thread waiting"
	url_queue.join()
	print "Done"

if __name__ == "__main__":
	if len(sys.argv) == 3:
		keywords=sys.argv[1]
		pagenum=sys.argv[2]
		main(keywords,pagenum)
	elif len(sys.argv) == 2:
		if sys.argv[1]=="-h" or sys.argv[1]=="--help":
			showinfo()
		else:
			keywords=sys.argv[1]
			pagenum=3
			main(keywords,pagenum)
	else:
		showinfo()


from bs4 import BeautifulSoup
import urllib3
import json
import re

urllib3.disable_warnings()

url ="https://www.homefacts.com/offenders.html"
http=urllib3.PoolManager()
response=http.request('GET', url)

soup=BeautifulSoup(response.data)


states=soup.find_all(href=re.compile("/offenders/"))
for s in states:
    http2 = urllib3.PoolManager()
    response2=http2.request('GET', 'https://www.homefacts.com'+s.get('href'))
    soup2=BeautifulSoup(response2.data)
    county=soup2.find_all(href=re.compile('%s/' % s.get('href').strip('.html')))
    for c in county:
        http3=urllib3.PoolManager()
        response3=http3.request('GET', 'https://www.homefacts.com'+c.get('href'))
        soup3=BeautifulSoup(response3.data)
        print("https://homefacts.com"+c.get('href'))
        offenders=soup3.find_all(href=re.compile("/offender-detail/"))
        print(offenders)
        n=1
        cmp_str = "https://homefacts.com"+c.get('href').strip(".html")+str(n)+(".html")
        #while():
        #url_str == "https://homefacts.com"+c.get('href').strip(".html")+str(n)+(".html")):
        #offenders=soup3.find_all(href=re.compile("/offender-detail/"))
        #for o in offenders:
        #    print("true")
        #    http4=urllib3.PoolManager()
        #    response4=http4.request('GET', "https://www.homefacts.com"+o.get('href'))
        #    soup4=BeautifulSoup(response4.data)
        #    offender=soup4.find_all(href=re.compile("/offender-detail/"))
        #    print(offender)

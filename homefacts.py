from bs4 import BeautifulSoup
import urllib3
import json
import re

urllib3.disable_warnings()

file = open('output.txt', 'wb')

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
        #print(offenders)
        #cmp_str = "https://homefacts.com"+c.get('href').strip(".html")+"-"+str(n)+(".html")
        #print(cmp_str)
        max_pg = int(re.search(r'\d+', (soup3.find("a", {"class", "last"}).get('href'))).group())
        while(max_pg>=1):
            url_str = "https://homefacts.com"+c.get('href').strip(".html")+'-'+str(max_pg)+(".html")
            print(url_str)
            response4=http3.request('GET', url_str)
            soup4=BeautifulSoup(response4.data)
            offender=soup4.find_all(href=re.compile("/offender-detail/"))
            print(offender)
            for link in offender:
                file.write(link.encode())
            max_pg-=1
file.close()

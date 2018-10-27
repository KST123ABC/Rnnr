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
        max_pg = int(re.search(r'\d+', (soup3.find("a", {"class", "last"}).get('href'))).group())
        while(max_pg>=1):
            url_str = "https://homefacts.com"+c.get('href').strip(".html")+'-'+str(max_pg)+(".html")
            response4=http3.request('GET', url_str)
            soup4=BeautifulSoup(response4.data)
            offender=soup4.find_all(href=re.compile("/offender-detail/"))
            for link in offender:
                offender_profile=("http:"+link.get('href'))
                print(offender_profile)
                http4=urllib3.PoolManager()
                response4=http3.request('GET', offender_profile)
                soup4=BeautifulSoup(response4.data)
                print(soup4.find_all('dd'))
            max_pg-=1
file.close()

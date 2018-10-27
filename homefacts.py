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
duplicate = []
deduplicate = []

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
                http4=urllib3.PoolManager()
                response4=http3.request('GET', offender_profile)
                soup4=BeautifulSoup(response4.data)
                name = soup4.find("span", {"itemprop" : "name"}).find_all(text=True)
                description = soup4.find_all("span", {"itemprop" : "description"})
                address = soup4.find("span", {"itemprop" : "streetAddress"}).find_all(text=True)
                locality = soup4.find("span", {"itemprop" : "addressLocality"}).find_all(text=True)
                region = soup4.find("span", {"itemprop" : "addressRegion"}).find_all(text=True)
                birth = soup4.find("span", {"itemprop" : "birthDate"}).find_all(text=True)
                race = description[0].find_all(text=True)
                gender = soup4.find("span", {"itemprop" : "gender"}).find_all(text=True)
                eye = description[1].find_all(text=True)
                height = soup4.find("span", {"itemprop" : "height"}).find_all(text=True)
                hair = description[2].find_all(text=True)
                weight = soup4.find("span", {"itemprop" : "weight"}).find_all(text=True)
                offense = description[3].find_all(text=True)
                content = list(zip(name, address, locality, region, birth, race, gender, eye, height, hair, weight, offense))
                print(content)
                duplicate.append(content)
            max_pg-=1
for idx in range(len(duplicate)-1):
    if duplicate[idx] != duplicate[idx+1]:
        deduplicate.append(duplicate[idx])
print(deduplicate)
file.close()

from bs4 import BeautifulSoup
import urllib3
import json
import sqlite3 as sql
import re

urllib3.disable_warnings()

table_name = 'offenders'
conn = sql.connect('Rnnr.db.sqlite')
con = conn.cursor()

# con.execute("DROP TABLE {tn}".format(tn=table_name))
# con.execute("CREATE TABLE {tn} ("
#             "id INTEGER NOT NULL PRIMARY KEY,"
#             "name CHAR(64) NOT NULL, "
#             "address CHAR(64) NOT NULL, "
#             "city TEXT NOT NULL, "
#             "state TEXT NOT NULL, "
#             "DOB TEXT NOT NULL, "
#             "race TEXT NOT NULL, "
#             "gender TEXT NOT NULL, "
#             "eye TEXT NOT NULL, "
#             "height TEXT NOT NULL, "
#             "hair TEXT NOT NULL, "
#             "weight TEXT NOT NULL, "
#             "offense CHAR(64) NOT NULL)".format(tn=table_name))

url ="https://www.homefacts.com/offenders.html"
http=urllib3.PoolManager()
response=http.request('GET', url)

soup=BeautifulSoup(response.data)
off_list = []
response_json = {}
states=soup.find_all(href=re.compile("/offenders/"))
for s in states:
    if s.get('href') == '/offenders/New-York.html':
        http2 = urllib3.PoolManager()
        response2=http2.request('GET', 'https://www.homefacts.com'+s.get('href'))
        soup2=BeautifulSoup(response2.data)
        county=soup2.find_all(href=re.compile('%s/' % s.get('href').strip('.html')))
        for c in county:
            if c.get('href') == '/offenders/New-York/Monroe-County.html':
                off_list = []
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
                        description = soup4.find_all("span", {"itemprop" : "description"})
                        if len(description) < 4:
                            offense = "Not Reported"
                        else:
                            offense = description[3].find_all(text=True)
                        if soup4.find("span", {"itemprop" : "birthDate"}):
                            birth = soup4.find("span", {"itemprop" : "birthDate"}).find_all(text=True)
                        else:
                            birth = "Not Reported"
                        content = [ soup4.find("span", {"itemprop" : "name"}).find_all(text=True),            # name
                                    soup4.find("span", {"itemprop" : "streetAddress"}).find_all(text=True),   # streetAddress
                                    soup4.find("span", {"itemprop" : "addressLocality"}).find_all(text=True), # addressLocality
                                    soup4.find("span", {"itemprop" : "addressRegion"}).find_all(text=True),
                                    birth,         #birthDate
                                    description[0].find_all(text=True),
                                    soup4.find("span", {"itemprop" : "gender"}).find_all(text=True),            #gender
                                    description[1].find_all(text=True),
                                    soup4.find("span", {"itemprop" : "height"}).find_all(text=True),           #height
                                    description[2].find_all(text=True),
                                    soup4.find("span", {"itemprop" : "weight"}).find_all(text=True),
                                    offense

                                    ]                                         #
                        if content not in off_list:
                            item = [(content[0][0], content[1][0], content[2][0], content[3][0], content[4][0], content[5][0],
                                     content[6][0], content[7][0], content[8][0], content[9][0], content[10][0],
                                     content[11][0])]
                            off_list.append(content)
                            for i in item:
                                con.execute("INSERT INTO offenders VALUES ((SELECT MAX(id) + 1 FROM offenders), ?,?,?,?,?,?,?,?,?,?,?,?)", i)
                                conn.commit()
                    max_pg-=1

conn.close()

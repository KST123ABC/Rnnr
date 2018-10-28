import ssl
import certifi
import sqlite3 as sql
import geopy
from geopy.geocoders import Nominatim

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context=ctx

table_name='offenders'
conn=sql.connect('Rnnr.db.sqlite')
con=conn.cursor()
con.execute("SELECT * FROM offenders;")
rows = con.fetchall()
for r in rows:
    geolocator = Nominatim(user_agent="Rnnr")
    location = geolocator.geocode(r[2] + " " + r[3]+" "+r[4])
    if location != None:
        print((location.latitude, location.longitude))


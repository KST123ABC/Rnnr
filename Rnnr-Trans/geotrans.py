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

#con.execute("ALTER TABLE offenders ADD lon DOUBLE;")
con.execute("SELECT * FROM offenders;")
rows = con.fetchall()
for r in rows:
    if r[13] == None:
      geolocator = Nominatim(user_agent="rnnr-app")
      location = geolocator.geocode(r[2] + " " + r[3]+" "+r[4])
      if location != None:
        print((location.latitude, location.longitude))
        con.execute("UPDATE offenders SET lat = (?) WHERE id LIKE ?", [location.latitude, r[0]])
        con.execute("UPDATE offenders SET lon = (?) WHERE id LIKE ?", [location.longitude, r[0]])
        conn.commit()
conn.close()

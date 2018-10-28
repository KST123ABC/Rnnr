import sqlite3 as sql
from geopy.geocoders import Nominatim

table_name='offenders'
conn=sql.connect('Rnnr.db.sqlite')
con=conn.cursor()
print(con.execute("SELECT * FROM offenders;"))
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("175 5th Avenue NYC")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)

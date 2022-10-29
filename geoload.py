#WITH THIS SOFTWARE WE JUST CREATE A TABLE, CONNECT THE TABLE WITH THE...
#... THE PYTHON FILE, AND DOWNLOAD THE INFO IN THE TABLE. FIND, OPEN AND...
#...READ AND STORE THE FILE.

#APPARENTLY THE DATABASE ALLOW US STORE INFORMATION AND ALSO TO NOT LOSE...
#...THE INFO GATHERED PREVIOUSLY. THEREFORE, IF THEE SYSTEM BLOW UP WE...
#...WILL BE COVER BY THE DATABASE.

import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys

api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

#Extra 0.1= This part is very important, because in some way decide the...
#... if the data proceed from "Chuck´s web page" or from "Google Maps".

if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#Extra 1: If there is less of 200 lines of data, the code will no print...
#..."Retrieved 200 locations, restart to retrieve more".

#Extra 1.1: I am not sure of the format  of the "where.data" because it is...
#...appanrently easy to modify. To be precise I delete almost all the...
#...addresses that belong to this file and just leave one and also add...
#..one address.

fh = open("where.data")
count = 0
for line in fh:
    if count > 200 :
        print('Retrieved 200 locations, restart to retrieve more')
        break

#Extra 2: In this part the every line of data is stripped.

#Extra 2.1: in this part of the code, we also are saying that the...
#...database we receive in the column address, the address encode.

    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))

#Extra 3: This is when we are going to fetch (i.e."Buscar") one record
#...from the "Cursor". Usually there is only one record retrieved...
#...because is is unique.

#Extra 4: This comment apply also fot he other "cur.fetchone"

#Extra 5: The zero (0) in the "cur.fetchone" means that there is more...
#than one thing in thata row and I am selecting only the first thing...
#that row.

#Extra 6: We will try to find the "address" in the database. If the "database"...
#... is found, then the code will print "Found in database".
    try:
        data = cur.fetchone()[0]
        print("Found in database ",address)
        continue
    except:
        pass
    
#Extra 7: We will try to find the "address" in the database. If the "database"...
#... is not found, then the code will create a dictionary. With this...
#...dctionary we will add every new address. Then we will use the "API Key"...
#...(i.e. whenever I have the API Key) to find this address in the web...
#...(i.e. we will encode the info and then send it to the web). I think that...
#...we send it to the web to find more data (geodata and son forth).
    parms = dict()
    parms["address"] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)

#Extra 8: We recieve from the web the data (geodata and son forth). We open...
#...read and decode the data that wwe recieve from the web. Then we will...
#...print the URL (print('Retrieving', url) and print more info of the...
#...data (('Retrieved', len(data), 'characters', data[:20].replace('\n', ' ')...

#Extra 9: I am no sure what is the meaning of what this code does...
#...(data[:20].replace('\n', ' '))) because we cannot see its effect on...
#...the print.
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

#Extra 10: I use JSON because allow us to intechange data and also, because...
#...JSON is built in structures like lists and dictionaries. JSON will allow..
#...us to communicate with the file "where.html" and in consequence will...
#:..allow to see our "where.data" (i.e. the addresses) in Google Maps.

#Extra 11: The red pins in the Google Mpas (i.e. the pins that allow us..
#... to identify easily a place) are thank to the file "where.js"
    try:
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break

    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
    
#Extra 1:Python time method sleep() suspends execution for the given...
#...number of seconds. The argument may be a floating point number to...
#...indicate a more precise sleep time.

#Extra 2: The actual suspension time may be less than that requested...
#...because any caught signal will terminate the sleep() following...
#execution of that signal's catching routin.

#Extra 3: If we use "Ctrl + Z" we will stop de running code.

    conn.commit()
    if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")

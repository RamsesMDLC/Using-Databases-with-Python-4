import sqlite3
import json

#Extra 1: This module defines base classes for standard Python codecs (encoders and...
#...decoders) and provides access to the internal Python codec registry,...
#...which manages the codec and error handling lookup process. Most standard...
#...codecs are text encodings, which encode text to bytes, but there are...
#...also codecs provided that encode text to text, and bytes to bytes. 

import codecs

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')

#Extra 2: codecs.open(filename, mode='r', encoding=None, errors='strict',...
#...buffering=-1)

#Extra 3: Open an encoded file using the given mode and return an instance...
#...of StreamReaderWriter, providing transparent encoding/decoding. The...
#...default file mode is 'r', meaning to open the file in read mode.

#Extra 4: The underlying encoded files are always opened in binary mode....
#...No automatic conversion of '\n' is done on reading and writing.

#Extra 5: encoding specifies the encoding which is to be used for the file...
#...Any encoding that encodes to and decodes from bytes is allowed, and...
#...the data types supported by the file methods depend on the codec used.

fhand = codecs.open('where.js', 'w', "utf-8")

#Extra 6: "\n" It is a special character sequence. This sequences are called...
#...escape characters The '\n' sequence is a popular one found in many...
#...languages that support escape sequences. It is used to indicate a new...
#...line in a string.

#Extra 7: Python file method write() writes a string str to the file. There...
#...is no return value. 

fhand.write("myData = [\n")
count = 0
for row in cur :
    data = str(row[1].decode())
    try: js = json.loads(str(data))
    except: continue

    if not('status' in js and js['status'] == 'OK') : continue

    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'", "")
    try :
        print(where, lat, lng)

        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")


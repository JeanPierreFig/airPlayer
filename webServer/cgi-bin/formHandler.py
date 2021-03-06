#!/usr/bin/python
import cgi, cgitb
import json
import requests
cgitb.enable()

formData = cgi.FieldStorage()
accessToken = formData['token'].value


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
          if line[0:6]=='Serial':
            cpuserial = line[10:26]
        f.close()
    except:
      cpuserial = "ERROR000000000"

    return cpuserial


with open('/home/pi/airPlayer/Plist.json', 'r') as json_data:
    d = json.load(json_data)
    d['Access_token'] = accessToken
    d['Device_Serial'] = getserial()


#Write to the file the new values
with open('/home/pi/airPlayer/Plist.json', 'w') as outfile:
    outfile.write(json.dumps(d))



print ("Content-type: text/html\n\n")

html = """

<!DOCTYPE html>
<html>
<head>
   <!-- HTML meta refresh URL redirection -->
   <meta http-equiv="refresh"
   content="0; url=http://localhost:8000/cgi-bin/Wifi.py">
</head>
<body>
   <p>The page has moved to:
   <a href="http://www.mydomain.com/new-page.html">this page</a></p>
</body>
</html>

"""



print(html)

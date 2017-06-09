#!/usr/bin/python3
import cgi, cgitb
import json

cgitb.enable()


formData = cgi.FieldStorage()
password = formData['password'].value
ssid = formData['ssid'].value




#Get the json file and store it in d
with open('/home/pi/airPlayer/Plist.json', 'r') as json_data:
    d = json.load(json_data)


#set the new vaules
d['ssid'] = ssid
d['password'] = password
d['isTryingToConnectToWifi'] = True

#Write to the file the new values
with open('/home/pi/airPlayer/Plist.json', 'w') as outfile:
    outfile.write(json.dumps(d))



print ("Content-type: text/html\n\n")

html = """

<!DOCTYPE html>
<html>

<head>

</head>
<style media="screen">

      h2{
      text-align: center;
      font-family: 'Open Sans', sans-serif;
      color: #929292


      }
      h1{
      text-align: center;
      font-family: 'Open Sans', sans-serif;
      color: #7e8b8c
      }

      #logo {
      text-align: center;
      margin-top: 100px;


      }
      </style>


<body>

<div id="logo" >
  <img src="/logo.png" alt="HTML5 Icon" style="max-width: 20%; max-height: 20%;" class="center">
</div>

<h1>The player will try to connect to wifi.<h1>
<h2>Follow the player on screen instructions.</h2>

</body>



</html>


"""



print(html)

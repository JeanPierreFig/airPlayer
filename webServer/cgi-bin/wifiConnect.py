#!/usr/bin/python3
import wifiHandler
import cgi, cgitb;


cgitb.enable()


formData = cgi.FieldStorage()
password = formData['password'].value
ssid = formData['ssid'].value



d['ssid'] = ssid
d['password'] = password
d['isTryingToConnectToWifi'] = True
with open('/home/pi/airplayer/Plist.json', 'w') as outfile:
    outfile.write(json.dumps(d))



print "Content-type: text/html";

html = """

<!DOCTYPE html>
<html>

<head>

</head>
<style media="screen">


.center {
max-width: 65%;
max-height: 65%;
bottom: 0;
left: 0;
margin: auto;
overflow: auto;
position: fixed;
right: 0;
top: 0;

}

h1{
text-align: center;
font-family: 'Open Sans', sans-serif;
color: #7e8b8c
}

</style>

<body>

<img src="http://localhost/logo.png"   alt="HTML5 Icon" class="center">
<h1>Trying to connect..<h1>

</body>



</html>


"""



print(html)

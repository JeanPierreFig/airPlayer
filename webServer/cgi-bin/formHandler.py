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


data = {'Access_token':accessToken,'data-type':'0'}

url = 'http://192.168.1.117/deviceActivation.php'
headers = {'content-type': 'application/json'}





response = requests.post(url, data=json.dumps(data), headers=headers)
j = json.loads(response.text)



device = (j['header'][0]['Device'])
isActivated = (j['header'][0]['isActivated'])

with open('/home/pi/Plist.json') as json_data:
    d = json.load(json_data)




print "Content-type: text/html\n\n";


if device == 'yes' and isActivated == '0':


           d['Access_token'] = accessToken
           d['isSetup'] = True
           with open('/home/pi/Plist.json', 'w') as outfile:
               outfile.write(json.dumps(d))

           #Raspberry pi only
           post = {'serial-number':getserial(),'data-type':'1'}
           response = requests.post(url, data=json.dumps(post), headers=headers)




           print """

           <!DOCTYPE html>
           <html>

           <head>
           <link href="https://fonts.googleapis.com/css?family=Open+Sans:600" rel="stylesheet"></head>
           <style media="screen">

           h3{
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
           <img src="http://localhost:8000/greenCheck.png" alt="HTML5 Icon" style="max-width: 20%; max-height: 20%;" class="center">

           </div>

           <h1>All Done, Your content will start Showing in a few minutes.<h1>


           </body>



           </html>





           """
else:
   print """

       <!DOCTYPE html>
       <html>

       <head>
       <script src='https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'></script>

       <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css'>

       <link href='https://fonts.googleapis.com/css?family=Open+Sans:600' rel='stylesheet'>

       </head>

       <style media='screen'>

       h3{
       text-align: center;
       font-family: 'Open Sans', sans-serif;
       color: #929292


       }
       h1{
       text-align: center;
       font-family: 'Open Sans', sans-serif;
       color: #7e8b8c
       }
       form {
       text-align: center;
       }
       input[type=text] {
       margin-top: 20px;
       margin-bottom: 25px;
       width: 35%;
       border: 1px solid #ccc;
       padding: 8px 15px;
       border-radius: 6px;
       font-size: 20px;
       outline:none;



       }
       input{
       text-align:center;

       }

       input[type="submit"] {

       background-color: #3498db;
       width: 190px;
       height: 55px;
       margin-top: 25px;
       border-radius: 10px;
       border: none;
       font-family: 'Open Sans', sans-serif;
       font-size: 15px;
       color: white;
       margin-left: auto ;
       margin-right: auto ;
       outline: none;
       }


       #logo {
       text-align: center;
       margin-top: 100px;


       }




       </style>





       <body>

       <div id="logo" >
       <img src="http://localhost:8000/logo.png" alt="HTML5 Icon" style="max-width: 15%; max-height: 15%;" class="center">
       <h1>Try again, The access token was incorect.
       </div>


       <form method='POST' id='form' action='/cgi-bin/formHandler.py'>
       <input type='text' id='text-Input' placeholder="Device token" name='token'>
       <br>
       <input type='submit' value='Activate Device'>
       </form>


       </body>


       <script>

       $('#form').submit(function( event ) {

       var text = $('#form').find('input[name="token"]').val();

       if(text != ''){

         console.log("submit");
        $(body).off("submit", "form");
        $('#form').submit();
       }
       else{

       $('input[name="token"]').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
          function() {
          $(this).removeClass('animated shake');

       });


       }

       event.preventDefault();
       });

       $('input[name="token"]').addClass('animated shake').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend',
       function() {
       $(this).removeClass('animated shake');

       });

       </script>


       </html>





       """

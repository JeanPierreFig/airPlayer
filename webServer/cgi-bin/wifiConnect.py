#!/usr/bin/python3
import wifiHandler
import cgi, cgitb;


cgitb.enable()


formData = cgi.FieldStorage()
password = formData['password'].value
ssid = formData['ssid'].value



isConnect = wifiHandler.Connect(ssid,password)


print "Content-type: text/html\n\n";

if isConnect == False:


    htmlString """

    <!DOCTYPE html>
    <html>

    <head>
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:600" rel="stylesheet">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" >
    <script src='https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js'></script>

    </head>

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



    </style>

    <body>

    <div id="logo" >
    <img src="http://localhost:8000/logo.png" alt="HTML5 Icon" style="max-width: 20%; max-height: 20%;" class="center">
    </div>

    <h1>incrorect Password. If no password type none</h1>

    <h1>Password for "{0}"</h1>
    <form method='POST' id='form'action='/cgi-bin/wifiConnect.py'>
    <input type='text' id='text-Input' placeholder='Password' name='password'>

    <br>
    <input type='submit' value='Connect'>
    </form>


    </div>






    </body>
    <script>


    </script>


    </html>


    """.format(htmlList)

    print(htmlString)





else:

   print(isConnect)

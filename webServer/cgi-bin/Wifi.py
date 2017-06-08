#!/usr/bin/python3

import cgi, cgitb, os
import WifiHandler
cgitb.enable()

#Get a list of wifi networks available
wifiList = wifiHandler.Search()

global htmlList

htmlList = " "

for wifi in wifiList:

    htmlList += "<tr><td>{0}</td></tr>".format(wifi.ssid)



print ("Content-type: text/html\n\n")

htmlString = """

<!DOCTYPE html>
<html>

<head>
<link href="https://fonts.googleapis.com/css?family=Open+Sans:600" rel="stylesheet">
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
table{

font-family: arial, sans-serif;
border-collapse: collapse;
margin: 0 auto;
margin-top: 20px;


}


td, th {
border: 1px solid #dddddd;
text-align: center;;
padding: 8px;
min-width: 200px;

}

tr:nth-child(even) {
background-color: #dddddd;
}

#logo {
text-align: center;
margin-top: 100px;


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

<div id="wifiList">
<h1>Select your wifi network.</h1>


<div class="tableview">
<table id="table">
 {}

</table>
</div>

</div>

<div id="wifiPassword">


</div>






</body>
<script>

$("#table tr").click(function(){
$(this).addClass('selected').siblings().removeClass('selected');
var value=$(this).find('td:first').html();

$("#wifiList").remove();
    $("#wifiPassword").append("<h1>Password for "+value+"</h1><form method='POST' id='form'action='/cgi-bin/wifiConnect.py'><input type='text' id='text-Input' placeholder='Password' name='password' value=''> <input type='hidden' name='ssid' value='"+value+"'><br> <input type='submit' value='Connect'></form>")

});

 $('.ok').on('click', function(e){
alert($("#table tr.selected td:first").html());
});

</script>


</html>

"""



print(htmlString.format(htmlList)

import requests
import json
import time
import time, threading
import urllib.request
import os

#from omxplayer import OMXPlayer
from pathlib import Path



def createHtml(data,type):


    print(data)

    if type == "content":

        html = """

        <!DOCTYPE html>
        <html>

        <head>

        </head>
        <style media="screen">

        body{
        background-color: black;

        }

        .center {
        max-width: 100%;
        max-height: 100%;
        bottom: 0;
        left: 0;
        margin: auto;
        overflow: auto;
        position: fixed;
        right: 0;
        top: 0;

        }
        </style>

        <body>

        <img src="/data/" alt="HTML5 Icon" class="center">

        </body>



        </html>


        """.replace('/data/', data)

    if type == "blank":
            html = """

            <!DOCTYPE html>
            <html>

            <head>

            </head>
            <style media="screen">

            body{
            background-color: black;

            }

            .center {
            max-width: 100%;
            max-height: 100%;
            bottom: 0;
            left: 0;
            margin: auto;
            overflow: auto;
            position: fixed;
            right: 0;
            top: 0;

            }
            </style>

            <body>


            </body>



            </html>


            """

    if type == "logo":

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
            </style>

            <body>

            <img src="http://localhost/logo.png"   alt="HTML5 Icon" class="center">

            </body>



            </html>


            """




    if type == "Access_token":

            html = """

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
            <img src="http://localhost:8000/logo.png" alt="HTML5 Icon" style="max-width: 20%; max-height: 20%;" class="center">
            </div>
            <h3>Go to your computor make sure it's connected to the same network and type the address on your web browser<h3>
            <h1>/ip/:8000</h1>


            </body>



            </html>""".replace('/ip/', data)



    if type == "network":

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
            </style>

            <body>

            <img src="http://localhost:8000/logo.png"   alt="HTML5 Icon" class="center">

            <h3>You are connected to network that is not connected to the internet.</h3>



            </body>



            </html>


            """

    return html

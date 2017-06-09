import requests
import json
import time, threading
import urllib.request
import os
import webview
import socket
import fcntl
import subprocess
import webServer
import WifiHandler
from datetime import datetime
from createHtml import createHtml
#from omxplayer import OMXPlayer
from pathlib import Path



url = 'http://10.0.0.69/updateContent.php'
#need to change this to look for saved access_token
headers = {'content-type': 'application/json'}

content_list = None
json_count = 0

def CheckServerForContent():

    with open('/home/pi/airPlayer/Plist.json') as json_data:
          global Plist
          Plist = json.load(json_data)

    data = {'Access_token':Plist['Access_token']}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    j = json.loads(response.text)


    update = (j['header'][0]['update'])
    storeurl = ''
    if update == 'yes' and is_connected():

       count = (j['header'][0]['count'])
       index = 0
       for i in range(count):

          index = i + 1
          link = j['data'][i]['link']
          linkArray = link.split("/")
          imageURl = "{0}".format(link)


          savePathWithName = "/home/pi/airPlayer/webServer/content/{0}".format(linkArray[-1])

          imageFile = Path(savePathWithName)


          #Check if we have the file on the unit if not download it again
          if imageFile.is_file():
              print("have file")

          else:
          #look for the file on the s3 server and save it to the local forder
               urllib.request.urlretrieve(imageURl,savePathWithName)
               imageFile = Path(savePathWithName)
               print(imageFile)
               #check if the file download and it's in the folder
               if imageFile.is_file():
                  print('good panda')
               else:
                    break

            #This check if there are files in the dir that do not need to be there



       if index == count:
          print('all good')

          with open('/home/pi/airPlayer/data.json', 'w') as outfile:
              outfile.write(json.dumps(j))

          create_content_list()
          #send downlod confermation
          threading.Timer(120, CheckServerForContent).start()
          print("Done checking server.")

          DeleteFiles(j)






       else:
          print('nope nope nope')
          #send error messesge




#Not checking if the firs time it downloaded content.
    else:
       threading.Timer(120, CheckServerForContent).start()
       print("Checking Server.")




class contentObject(object):


    def __init__(self,*args,**kwargs):

        self.index = 0
        self.contentPath = None

    def get_next_content_index(self):

        #check for amount of itmes on the json list
        self.index += 1

        if self.index > json_count-1:
           self.index = 0



        return self.index






def create_content_list():

    with open('/home/pi/data.json') as json_data:
        d = json.load(json_data)
        global content_list,json_count
        content_list = d['data']
        json_count = d['header'][0]['count']



## main loop to display the content
def content_loop(contentObject):


    index = contentObject.get_next_content_index()

    link = content_list[index]['link']
    linkArray = link.split("/")
    itemName = linkArray[-1]


    if content_list[index]['type'] == 'image':

        if isShowed(contentObject,index):

           webview.load_html(createHtml("http://localhost:8000/content/{0}".format(itemName),"content"))
           time.sleep(5)

        else:
            print("Will not display content because content schedule.")
            time.sleep(5)

    if content_list[index]['type'] == 'video':
        #display video
        print("video")
        webview.load_html(createHtml("","blank"))
        #player = OMXPlayer("file:///home/pi/simuMall.mov").format(content_list[index]['link']))
        #player.play()
        #time.sleep(player.duration())








def DeleteFiles(j):

    # if mac test on /Users/jeanpierre/Desktop/images/

    listOfFiles = os.listdir("/home/pi/airPlayer/webServer/content/")

    count = (j['header'][0]['count'])
    print(listOfFiles)

    #Check for the file on my json object and remove is from the list of files stored on the dir
    for i in range(count):

        link = j['data'][i]['link']
        linkArray = link.split("/")

        # -1 is = to the last number item on the array -1 start from the back
        if linkArray[-1] in listOfFiles:
            print("good file")
            listOfFiles.remove(linkArray[-1])


    #now remove the file from the dir
    for file in listOfFiles:

        # if mac test on /Users/jeanpierre/Desktop/images/
        #os.remove("/home/pi/webServer/content/{0}".format(file))
        print("delete")






#This function will check if the content can be display
def isShowed(contentObject,index):

    #Format date string
    sDate = content_list[index]['sDate'].split("/")
    eDate = content_list[index]['eDate'].split("/")
    sTime = content_list[index]['sTime'].split("/")
    eTime = content_list[index]['eTime'].split("/")

    #Get Current date
    day = datetime.today().day
    year = datetime.today().year
    month = datetime.today().month

    #Check that the year month and day rang is correct
    if day >= int(sDate[1]) and day <= int(eDate[1]) and month >= int(sDate[0]) and month <= int(eDate[0]) and  year >= int(sDate[2]) and year <= int(eDate[2]):
        return True
    else:
        return False


#I might remove this
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname("www.google.com")
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
    pass
  return False



def get_ip():
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.connect(('8.8.8.8', 1))  # connect() for UDP doesn't send packets
      local_ip_address = s.getsockname()[0]
      return local_ip_address
    except OSError:
      return False


def StartContentServer():
    # if mac test on /Users/jeanpierre/Desktop/webServer
    os.chdir("/home/pi/airPlayer/webServer")
    webServer.start()


def ConnectToWifi(ssid,password):

     isConnected = False
     numTry = 0

     while True:
         #call WifiHandler function
         isConnected = WifiHandler.Connect(ssid,password)

         if isConnected != False:
             return True

         if numTry > 5:
            return False
        #number of trys to connect wifi
         numTry += 1




def StartHotSpot():

   numTry = 0

   while True:

         try:
            subprocess.call("sudo hotspotd start",shell=True)

         except OSError:
            #There was an error try again
            numTry += 1
            #Return false if the number of trys are more then 5
            if numTry > 5:
                return False

         else:
             #The hotspotd was started
             return True

def StopHotSpot():

   numTry = 0

   while True:

         try:
            subprocess.call("sudo hotspotd stop",shell=True)

         except OSError:
            #There was an error try again
            numTry += 1
            #Return false if the number of trys are more then 5
            if numTry > 5:
                return False

         else:
             #The hotspotd was stoped
             return True


def Get_Plist():

    with open('/home/pi/airPlayer/Plist.json') as json_data:
          Plist = json.load(json_data)

    return Plist

def Set_Plist(ssid,password,isTryingWifi,isSetup):


    Plist = Get_Plist()

    Plist['ssid'] = ssid
    Plist['password'] = password
    Plist['isSetup'] = isSetup
    Plist['isTryingToConnectToWifi'] = isTryingWifi

    with open('/home/pi/airPlayer/Plist.json', 'w') as outfile:
        outfile.write(json.dumps(Plist))


def main():

    #Get device settings
    Plist = Get_Plist()


    if Plist["isSetup"]:



            CheckServerForContent()
            contentObj = contentObject()
            create_content_list()
            webview.load_html(createHtml("","logo"))

            #Main content loop
            while True:

                  content_loop(contentObj)


    else:


        if StartHotSpot() != False:
            webview.load_html(createHtml("169.254.9.20","Access_token"))
        else:
            webview.load_html(createHtml("There was a problem creating the Wi-Fi hotspot.","Message"))



        #Check every 10 sec if the the user has added the wifi credential
        while Plist["isTryingToConnectToWifi"] == False:
            Plist = Get_Plist()
            time.sleep(10)

        else:
            webview.load_html(createHtml("Trying to connect...","Message"))

            StopHotSpot()
            Plist = Get_Plist()
            if ConnectToWifi(Plist["ssid"],Plist["password"]) != False:

                #Set_Plist("","",False,True)

                #!!!! still need to make the user set the access token!!!!

                #Run the program
                #CheckServerForContent()
                #contentObj = contentObject()
                #create_content_list()
                webview.load_html(createHtml("Staring Player","logo"))

                #Main content loop
                while True:

                      content_loop(contentObj)
            else:
                Set_Plist("","",False,False)
                webview.load_html(createHtml("There was a problem connecting to the WiFI network. Lets try again.","Message"))
                time.sleep(10)
                #Call main again to restart the steup process
                main()





if __name__ == "__main__":

    try:

       #start server.
       s = threading.Thread(target=StartContentServer)
       s.start()
       #start main Program.
       t = threading.Thread(target=main)
       t.start()
       #start webview to display content.
       webview.create_window("","",fullscreen=False)
       webview.load_html(createHtml("Staring Player","logo"))


    except:

        raise

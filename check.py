 
import requests
import json
import time
import time, threading
import urllib.request
import os
import webview
import threading
import socket
#import import wifihan
import webServer
from datetime import datetime
from createHtml import createHtml
#from omxplayer import OMXPlayer
from pathlib import Path


#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options

url = 'http://10.0.0.69/updateContent.php'
#need to change this to look for saved access_token 
headers = {'content-type': 'application/json'}



content_list = None
json_count = 0






def CheckServerForContent():

    with open('/home/pi/airplayer/Plist.json') as json_data:
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
          
          savePathWithName = "/home/pi/airplayer/webServer/content/{0}".format(linkArray[-1])
          imageFile = Path(savePathWithName)
          
          
          #Check if we have the file on the unit to not dowload it again
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

          with open('/home/pi/airplayer/data.json', 'w') as outfile:
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
           print("yes")
        
           time.sleep(5)
               
        else:
            print("Date not right")
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
    listOfFiles = os.listdir("/home/pi/airplayer/webServer/content/")
    
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




def isShowed(contentObject,index):
    
    
    
    sDate = content_list[index]['sDate'].split("/")
    eDate = content_list[index]['eDate'].split("/")
    sTime = content_list[index]['sTime'].split("/")
    eTime = content_list[index]['eTime'].split("/")
    
    day = datetime.today().day
    year = datetime.today().year
    month = datetime.today().month
    
    
    
    #Check that the year month and day rang is correct
    if day >= int(sDate[1]) and day <= int(eDate[1]) and month >= int(sDate[0]) and month <= int(eDate[0]) and  year >= int(sDate[2]) and year <= int(eDate[2]):
        
        return True
    

    else:
        return False


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
    os.chdir("/home/pi/airplayer/webServer")
    webServer.start()


def main():


    
    
    """
    #print(get_ip())

    #wifihan.Connect("Claro425EE1","0C77A3FADB")

    #print(isConnected)
   
    with open('/home/pi/airplayer/Plist.json') as json_data:
          global Plist
          Plist = json.load(json_data)
    
    s = threading.Thread(target=StartContentServer)
    #s.start()

    print(get_ip())
    
    if Plist["isSetup"]:
            print("yes")

            CheckServerForContent()
            contentObj = contentObject()
            create_content_list()
            webview.load_html(createHtml("","logo"))


            while True:

                  content_loop(contentObj)

    else:
        print("no")



        if get_ip() == False:
        
             webview.load_html(createHtml(get_ip(),"network"))
             print('no ip')
        
        elif is_connected == False:
        
             webview.load_html(createHtml(get_ip(),"network"))
             print("connected to a network but not the internet")
        
        else:
        
            webview.load_html(createHtml(get_ip(),"Access_token"))
        

        while Plist["isSetup"] == False:

              with open('/home/pi/airplayer/Plist.json') as json_data:
                    Plist = json.load(json_data)
                    time.sleep(15)

        else:

            CheckServerForContent()
            contentObj = contentObject()
            create_content_list()
            #webview.load_html(createHtml("","logo"))
            
            
            while True:
                
                content_loop(contentObj)




"""




        
if __name__ == "__main__":

    try:

       t = threading.Thread(target=main)
       t.start()
        
       webview.create_window("","",fullscreen=False)
                

    except:

        raise

        





    



     

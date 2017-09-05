from bs4 import BeautifulSoup
import urllib.request
import time
import os
import subprocess
import time
import pycurl, json
from io import BytesIO

playerName = "Hernandez" #Change players name

#Instapush Setup
appID = "KEY REMOVED"
appSecret = "KEY REMOVED"
pushEvent = "PriceAlert"
pushMessage = playerName + "'s price is high enough"
buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://api.instapush.im/v1/post')
c.setopt(c.HTTPHEADER, ['x-instapush-appid: ' + appID,
'x-instapush-appsecret: ' + appSecret,
'Content-Type: application/json'])
json_fields = {}
json_fields['event']=pushEvent
json_fields['trackers'] = {}
json_fields['trackers']['message']=pushMessage
postfields = json.dumps(json_fields)
c.setopt(c.POSTFIELDS, postfields)
c.setopt(c.WRITEFUNCTION, buffer.write)

#BeautifulSoup Setup and price checking
user_agent = user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}
url = "https://www.futbin.com/17/player/94/hern%C3%A1ndez"	#Futbin URL for player
request = urllib.request.Request(url,None,headers) 
response = urllib.request.urlopen(request)
data = response.read()
soup = BeautifulSoup(data, "lxml")
previousValue = "";
running = True
notificationValue = 240000	#Notification price, change to value wanted
notified = True

while running:
	request=urllib.request.Request(url,None,headers)
	response = urllib.request.urlopen(request)
	data = response.read()
	soup = BeautifulSoup(data, "lxml")
	result = soup.find("span", {"id": "xboxlbin"})
	output = result.text

	if previousValue != output:
		print("The Price has changed")

	previousValue = result.text
	print(playerName + " cheapest BIN = " + output)
	result2 = soup.find("tr", {"class": "lowest_bin_updated_tr_xb1"})
	output2 = result2.text
	print("Futbin was " + output2.strip())
	print(time.ctime())
	print("")

	intValue = output
	intValue = intValue.replace(',','')
	intValue = int(intValue)

	if notificationValue <= intValue:	#Change < or > for buying/selling player
		if notified is True:
			c.perform()
			notified = False

	time.sleep(60)

# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 12:46:40 2022

@author: mosiah
"""

import requests
from bs4 import BeautifulSoup

# currently not implemented yet, may do buildable urls to be requested
    # Base url
url = "https://trimet.org/ride/stop_schedule.html?stop_id="

    # sort by destinations
arg = "&sort=destination"



# Make a request
page = requests.get(
    "https://trimet.org/ride/stop_schedule.html?stop_id=3051&sort=destination")
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup.prettify())

'''
<div class="scheduletimes">
<ul class="sortbytime">
'''
# Create top_items as empty list
bus_lines = {}  # List of dictionaries for the buses passing through this stop
info = {}   # The dictionary of an individual bus

info2 = {}  # Temporary dictionary to store id number and text for alerts
alertList = [] # List of dictionaries for alerts - mimicing buslines

# Extract and store in top_items according to instructions on the left
schedules = soup.select('div.scheduletimes')
for elem in schedules:
    description = elem.select('h3')[0].text
    # format description to be more readable by removing long spaces, tabs, and newlines
    description = description.replace("\t", "").replace("\r", "").replace("\n", "")
    description = description.replace("                ", "").replace("Next arrivals", "")
    
    # Separate the line number away from the description
    descriptionParts = description.partition("-")
    info["ID"] = descriptionParts[0]
    info["Description"] = descriptionParts[2]
    
    buses = elem.select('ul.sortbydestination')
    arrivalTimes = [] # List to contain arrival times for this bus
    for bus in buses:
        arrivalTime = bus.select('span')
        for time in arrivalTime:
            arrivalTimes.append(time.text.strip())
        
    
    info["Arrivals"] = arrivalTimes[:]
    bus_lines[descriptionParts[0]] = info
    

# Get the alerts from the website as well
alertTextBlock = soup.select_one("div#alerts").text
#print(alertTextBlock)
alerts = alertTextBlock.split("\n\n")
for alert in alerts:
    if len(alert) == 0:
        pass
    else:
        alert.replace("\n", "")
        #print(alert)
        #print("******")
        
        alertParts = alert.partition(":  ")
        busID = alertParts[0]   # list of bus ids which have this alert
        busID = busID.replace("\n", "")
        alertInfo = alertParts[2] # text containing the actual alert
        alertList.append(alertInfo)
        #print(alert)
        
        info2["IDs"] = busID
        info2["alert"] = alertInfo
        #print(info2)
        #print("------\n")
       
        if busID in bus_lines:
            if "Alerts" not in bus_lines[busID]:
                bus_lines[busID]["Alerts"] = []
                bus_lines[busID]["Alerts"] += alertList[-1]
            else:
                bus_lines[busID]["Alerts"] += alertList[-1]
        #alertList.append(info2)
    

#print(alertList)



# Alternate method to get alerts (not done)
alerts2 = soup.select("img[src='//trimet.org/global/img/icon-alert.png']")
for alert in alerts:
    '''
    busID = elem.select('b')
    alert = elem.text.strip()
    print(alert)
    print(busID)
    print("******")
    '''
# psuedocode which adds the alert to a bus's info dictionary if the bus id matches those listed in the alert
#   if busID in info2:
#        info2["alert"] = alert    

'''
for i in bus_lines["6"]["Alerts"]:
    print(i)
    print()
'''
for i in alertList:
    print(i)
    print()

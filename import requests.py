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
bus_lines = []

# Extract and store in top_items according to instructions on the left
schedules = soup.select('div.scheduletimes')
for elem in schedules:
    busName = elem.select('h3')[0].text
    buses = elem.select('ul.sortbydestination')
    
    arrivalTimes = []
    for bus in buses:
        arrivalTime = bus.select('span')
        for time in arrivalTime:
            arrivalTimes.append(time.text.strip())
        
    
    info = {
        "name": busName.strip(),
        "arrivals": arrivalTimes
    }
    bus_lines.append(info)
    info2 = info
# Get the alerts from the website as well
alerts = soup.select('img')
for elem in alerts:
    busID = elem.select('b')

    alert = elem.text.strip()
    print(alert)
# psuedocode which adds the alert to a bus's info dictionary if the bus id matches those listed in the alert
#   if busID in info2:
#        info2["alert"] = alert    

print(bus_lines)

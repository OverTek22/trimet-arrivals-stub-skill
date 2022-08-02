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


'''
<div class="scheduletimes">
<ul class="sortbytime">
'''
# Create top_items as empty list
bus_lines = []

# Extract and store in top_items according to instructions on the left
schedules = soup.select('div.scheduletimes')
for elem in schedules:
    busName = elem.select('h3')[0]
    buses = schedules.select('ul.sortbydestination')
    
    arrivalTimes = []
    for bus in buses:
        arrivalTime = bus.select('span')[0].text
        arrivalTimes.append(arrivalTime.strip())
    
    
    info = {
        "name": busName.strip(),
        "arrivals": arrivalTimes
    }
    bus_lines.append(info)

print(bus_lines)
from mycroft import MycroftSkill, intent_handler
import requests
import re
from bs4 import BeautifulSoup
class TrimetArrivalsStub(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    @intent_handler('stub.arrivals.trimet.intent')
    def handle_stub_arrivals_trimet(self, message):
        stopid = self.get_response('which.stop')
        #utterance = message.data.get('stopid_message')
        #num = re.findall('[0-9]+', utterance)
        self.log.info(stopid)
        #self.speak("I heard:")
        #self.speak(stopid)
        
        # Base url
        url = "https://trimet.org/ride/stop_schedule.html"
        # Using the stop ID passed in, get schedules sorted by destinations
        stop_url = "{}?stop_id={}&sort=destination".format(url, stopid)
        self.log.info("requesting url")
        # Make a request
        page = requests.get(stop_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        self.log.info("good request")
        # Create top_items as empty list
        bus_lines = {}  # List of dictionaries for the buses passing through this stop
        # Extract and store in top_items according to instructions on the left
        schedules = soup.select('div.scheduletimes')
        for elem in schedules:
            info = {}   # The dictionary of an individual bus
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
            self.log.info("Getting times")
            for bus in buses:
                arrivalTime = bus.select('span')
                for time in arrivalTime:
                    arrivalTimes.append(time.text.strip())
            info["Arrivals"] = arrivalTimes[:]
            bus_lines[descriptionParts[0]] = info
        
        
        BusID = list(bus_lines.keys())[0]
        # Example of user asking for line 47
        self.speak(bus_lines[BusID]["ID"], wait=True)
        self.log.info(bus_lines[BusID]["ID"])
        self.speak(bus_lines[BusID]["Description"],wait=True)
        self.log.info(bus_lines[BusID]["Description"])
        self.speak_dialog('speak.string', {'intro': "The bus arrives at these times", 'stuff': bus_lines[BusID]["Arrivals"]}, wait=True)
        self.log.info(bus_lines[BusID]["Arrivals"])
        '''
        self.log.info("Getting alerts")# Get the alerts from the website as well
        try:
            alertTextBlock = soup.select_one("div#alerts").text
            # print(alertTextBlock)
            alerts = alertTextBlock.split("\n\n")
            for alert in alerts:
                info2 = {}  # Temporary dictionary to store id number and text for alerts
                if len(alert) == 0:
                    pass
                else:
                    alert.replace("\n", "")
                    alertParts = alert.partition(":  ")
                    busID = alertParts[0]   # list of bus ids which have this alert
                    busID = busID.replace("\n", "")
                    alertInfo = alertParts[2] # text containing the actual alert
                   # split the string of ids into a list of ids
                    busIDS = busID.split(", ")
                    for ID in busIDS:
                        #print("--" + ID)
                        if ID in bus_lines: # add the alert if the bus goes to the stop
                            if "Alerts" not in bus_lines[ID]:
                                bus_lines[ID]["Alerts"] = []
                                bus_lines[ID]["Alerts"].append(alertInfo)
                            else:
                                bus_lines[ID]["Alerts"].append(alertInfo)
        finally:
            BusID = list(bus_lines.keys())[0]
            # Example of user asking for line 47
            self.speak_dialog('speak.string', {'intro': "The next bus arrives at", 'stuff': bus_lines[BusID]["Arrivals"][0]})
            # self.speak_dialog('stop.11771')
        '''
    '''
    @intent_handler('stop.3051.intent')
    def handle_stop_3051(self, message):
        self.log.info(message.data.keys())
        utterance = message.data.get('utterance')
        num = re.findall('[0-9]+', utterance)
        self.log.info(num[0])

        self.speak("I heard")
        self.speak(num[0])

        # Base url
        url = "https://trimet.org/ride/stop_schedule.html"
        # Using the stop ID passed in, get schedules sorted by destinations
        stop_url = "{}?stop_id={}&sort=destination".format(url, 3051)
        self.log.info("requesting url")
        # Make a request
        page = requests.get(stop_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        self.log.info("good request")
        # Create top_items as empty list
        bus_lines = {}  # List of dictionaries for the buses passing through this stop
        # Extract and store in top_items according to instructions on the left
        schedules = soup.select('div.scheduletimes')
        for elem in schedules:
            info = {}   # The dictionary of an individual bus
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
            self.log.info("Getting times")
            for bus in buses:
                arrivalTime = bus.select('span')
                for time in arrivalTime:
                    arrivalTimes.append(time.text.strip())
            info["Arrivals"] = arrivalTimes[:]
            bus_lines[descriptionParts[0]] = info
        self.log.info("Getting alerts")
        # Get the alerts from the website as well
        alertTextBlock = soup.select_one("div#alerts").text
        # print(alertTextBlock)
        alerts = alertTextBlock.split("\n\n")
        for alert in alerts:
            info2 = {}  # Temporary dictionary to store id number and text for alerts
            if len(alert) == 0:
                pass
            else:
                alert.replace("\n", "")
                alertParts = alert.partition(":  ")
                busID = alertParts[0]   # list of bus ids which have this alert
                busID = busID.replace("\n", "")
                alertInfo = alertParts[2] # text containing the actual alert
               # split the string of ids into a list of ids
                busIDS = busID.split(", ")
                for ID in busIDS:
                    #print("--" + ID)
                    if ID in bus_lines: # add the alert if the bus goes to the stop
                        if "Alerts" not in bus_lines[ID]:
                            bus_lines[ID]["Alerts"] = []
                            bus_lines[ID]["Alerts"].append(alertInfo)
                        else:
                            bus_lines[ID]["Alerts"].append(alertInfo)
        # Example of user asking for line 45
        self.speak_dialog('speak.string', {'intro': "Here is the schedule for the line 45 bus", 'stuff': bus_lines["45"]["Arrivals"]})
        # self.speak_dialog('stop.3051')
    
    @intent_handler('stop.11771.intent')
    def handle_stop_11771(self, message):
        # Base url
        url = "https://trimet.org/ride/stop_schedule.html"
        # Using the stop ID passed in, get schedules sorted by destinations
        stop_url = "{}?stop_id={}&sort=destination".format(url, 11771)
        # stop_url = "{}?stop_id={}&sort=destination".format(url, 10764)
        # Make a request
        page = requests.get(stop_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        #print(soup.prettify())
        # Create top_items as empty list
        bus_lines = {}  # List of dictionaries for the buses passing through this stop
        # Extract and store in top_items according to instructions on the left
        schedules = soup.select('div.scheduletimes')
        for elem in schedules:
            info = {}   # The dictionary of an individual bus
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
        try:
            alertTextBlock = soup.select_one("div#alerts").text
            # print(alertTextBlock)
            alerts = alertTextBlock.split("\n\n")
            for alert in alerts:
                info2 = {}  # Temporary dictionary to store id number and text for alerts
                if len(alert) == 0:
                    pass
                else:
                    alert.replace("\n", "")
                    alertParts = alert.partition(":  ")
                    busID = alertParts[0]   # list of bus ids which have this alert
                    busID = busID.replace("\n", "")
                    alertInfo = alertParts[2] # text containing the actual alert
                   # split the string of ids into a list of ids
                    busIDS = busID.split(", ")
                    for ID in busIDS:
                        #print("--" + ID)
                        if ID in bus_lines: # add the alert if the bus goes to the stop
                            if "Alerts" not in bus_lines[ID]:
                                bus_lines[ID]["Alerts"] = []
                                bus_lines[ID]["Alerts"].append(alertInfo)
                            else:
                                bus_lines[ID]["Alerts"].append(alertInfo)
        finally:
            BusID = list(bus_lines.keys())[0]
            # Example of user asking for line 47
            self.speak_dialog('speak.string', {'intro': "The next bus arrives at", 'stuff': bus_lines[BusID]["Arrivals"][0]})
            # self.speak_dialog('stop.11771')
'''
def create_skill():
    return TrimetArrivalsStub()

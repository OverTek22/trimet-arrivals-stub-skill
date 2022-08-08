from mycroft import MycroftSkill, intent_handler
from adapt.intent import IntentBuilder
import requests
from bs4 import BeautifulSoup

class TrimetArrivalsStub(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    
    @intent_handler(IntentBuilder('next.arrivals').require('get.arrivals').one_of('stop.3051', 'stop.11771'))
    def handle_get_arrivals(self, message):
	    self.log.info("next arrivals adept intent")
        utterance = message.data.get('utterance')
        num = int(extract_number(utterance))
        self.speak_dialog('speak.string', {'intro': "I heard stop", 'stuff': num})
    
    
    @intent_handler('stub.arrivals.trimet.intent')
    def handle_stub_arrivals_trimet(self, message):
        self.log.info("Stub intent handler used")
        self.speak_dialog('which.stop')
    
    @intent_handler('stop.3051.intent')
    def handle_stop_3051(self, message):
        self.log.info("Stop 3051 intent handler used")
        self.log.info(message.data.keys())
        
        utterance = message.data.get('utterance')
	    num = int(extract_number(utterance))
        self.log.info(num)
        
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

            # Once the arrivals list is done, add that to the dictionary
            info["Arrivals"] = arrivalTimes[:]
            bus_lines[descriptionParts[0]] = info # Add this bus's dictionary to the bus line dictionary with its ID as the key 

        # After all of the buses have been added to the bus line dictionary
        # Example of user asking for line 45
        self.speak_dialog('speak.string', {'intro': "Here is the schedule for the line 45 bus", 'stuff': bus_lines["45"]["Arrivals"]})
        # self.speak_dialog('stop.3051')
        
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
        self.speak_dialog('speak.string', {'intro': "The alerts for the 45 bus are", 'stuff': bus_lines["45"]["Arrivals"]})
        # self.speak_dialog('stop.3051')
    
    @intent_handler('stop.11771.intent')
    def handle_stop_11771(self, message):
        self.log.info("Stop 11771 intent handler used")
        
        # Base url
        url = "https://trimet.org/ride/stop_schedule.html"
        # Using the stop ID passed in, get schedules sorted by destinations
        stop_url = "{}?stop_id={}&sort=destination".format(url, 10764)

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

        BusID = list(bus_lines.keys())[0]
        # Example of user asking for line 47
        self.speak_dialog('speak.string', {'intro': "The next bus arrives at", 'stuff': bus_lines[BusID]["Arrivals"][0]})
        # self.speak_dialog('stop.11771')
        
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
            self.speak_dialog('speak.string', {'intro': "The alerts for this bus are", 'stuff': bus_lines[BusID]["Arrivals"][0]})
            # self.speak_dialog('stop.11771')
    

def create_skill():
    return TrimetArrivalsStub()


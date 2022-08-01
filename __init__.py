from mycroft import MycroftSkill, intent_file_handler


class TrimetArrivalsStub(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('stub.arrivals.trimet.intent')
    def handle_stub_arrivals_trimet(self, message):
        self.speak_dialog('which.stop')
    
    @intent_handler('stop.3051.intent')
    def handle_stop_3051(self, message):
        # stub file for stop 3051
        self.speak_dialog('stop.3051')
    
    @intent_handler('stop.11771.intent')
    def handle_stop_11771(self, message):
        # stub file for stop 11771
        self.speak_dialog('stop.11771')


def create_skill():
    return TrimetArrivalsStub()


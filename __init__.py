from mycroft import MycroftSkill, intent_file_handler


class TrimetArrivalsStub(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('stub.arrivals.trimet.intent')
    def handle_stub_arrivals_trimet(self, message):
        self.speak_dialog('stub.arrivals.trimet')


def create_skill():
    return TrimetArrivalsStub()


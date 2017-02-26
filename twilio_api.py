from twilio_credentials import *
from twilio.rest import TwilioRestClient

class UrlGrabber():    
    def __init__(self, sid, num):
        self.sid = sid
        self.num = num

    def get_url(self):
        try:
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.get(self.sid)
            medias = message.media_list.list()
            imageUrl = medias[0].uri
            return imageUrl
        except ValueError:
            return None

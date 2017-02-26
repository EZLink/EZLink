from twilio_credentials import *
from twilio.rest import TwilioRestClient

class UrlGrabber():    
    def __init__(self, sid):
        self.sid = sid

    # returns image from url
    def get_url(self):
        #print(self.sid)
        try:
            client = TwilioRestClient(account_sid, auth_token)
            message = client.messages.get(self.sid)
            medias = message.media_list.list()
            imageUrl = medias[0].uri
            print(imageUrl)
            return imageUrl
        except ValueError:
            return ""

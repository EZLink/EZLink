from flask import Flask, request, url_for, session, redirect, send_from_directory
from twilio_api import UrlGrabber
from name_card_processing import ImageProcessor, TextExtract
from contact_maker import make_vcf
from smscomm import respondToUser, handleText
import urllib

app = Flask(__name__, static_url_path='')


IMAGE_ROOT_DIR = '/home/bobby/tempImg/'
EZLINK_FILE_NAME = 'EZLink.vcf'

@app.route('/vcf/<path:path>')
def vcf(path):
    """ 
    This is the endpoint intended to serve twilio. 
    NOT intended for the user to use
    """

    return send_from_directory('/vcf/', path)


@app.route('/input', methods = ['GET', 'POST']))
def input():
    """ 
    Cues input processing and response. Called by twilio.
    NOT intended for the user to use
    """
    if 'From' in request.args and 'SmsMessageSid' in request.args:
        phone_number = request.args["From"]
        sid = request.args["SmsMessageSid"]

        # Get the url of twilio stored image
        grabber = UrlGrabber(sid)
        url = grabber.get_url()

        if contains_image(url):
            user_uploaded_file_path = download_image(url, phone_number)

            image_processor = ImageProcessor(user_uploaded_file_path)
            result = image_processor.image_to_string()

            extracter = TextExtract(result)
            user_info = extracter.extract()

            vcf_file_name = make_vcf(*user_info)
            
            respondToUser(vcf_file_name, phone_number, EZLINK_FILE_NAME)
        else:
            handleText(request.args["Body"], phone_number)

        return "The message is successfully processed"

def contains_image(url):
    return len(url) > 0

def download_image(url, phone_number):
    """
    helper method to download the image passed through by twilio
    """
    user_uploaded_file_path = '{}{}.jpeg'.format(IMAGE_ROOT_DIR, phone_number)
    req = urllib.request.Request(url, headers={'User-Agent' : 'Magic Browser'})
    response = urllib.request.urlopen(req)
    with open(user_uploaded_file_path, 'wb') as f:
        f.write(response.read())
    return user_uploaded_file_path
    


@app.route('/')
def index():
    return "<h1>You have reached the EZ link project server, please refer to documentation for usage</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)

from flask import Flask, request, url_for, session, redirect, send_from_directory
from twilio_api import UrlGrabber
from name_card_processing import ImageProcessor, TextExtract
from contact_maker import make_vcf
from smscomm import respondToUser #, handleText
import urllib

import cv2

app = Flask(__name__, static_url_path='')



""" This is the endpoint intended to serve twilio. 
NOT intended for the user to use
"""
@app.route('/vcf/<path:path>')
def vcf(path):
    return send_from_directory('/vcf/', path)


""" Cues input processing and response. Called by twilio.
NOT intended for the user to use
"""
@app.route('/input', methods = ['GET', 'POST'])#)
def input():
    if(('From' in request.args) and ('SmsMessageSid' in request.args)):
        num = request.args["From"]
        sid = request.args["SmsMessageSid"]

        grabber = UrlGrabber(sid)
        url = grabber.get_url()

        if(len(url) > 0): #there is image associated with message
            # TODO change naming holly molly what is all these hodgepodge BULLSHIT
            temp_file_name = '/home/bobby/tempImg/{}.jpeg'.format(num)
            req = urllib.request.Request(url, headers={'User-Agent' : 'Magic Browser'})
            response = urllib.request.urlopen(req)
            with open(temp_file_name, 'wb') as f:
                f.write(response.read())
                
            ori_img = cv2.imread(temp_file_name, cv2.IMREAD_GRAYSCALE)
            image_processor = ImageProcessor(ori_img)
            result = image_processor.image_to_string()
            extracter = TextExtract(result)
            args = extracter.extract()
                
            file_name = make_vcf(*args)

            respondToUser(file_name, num, 'EZLink.vcf')

        if(len(request.args["Body"]) > 0): #there is text in body
            handleText(request.args["Body"], num)

        return "End of the Input"


# For testing purposes
@app.route('/')
def index():
    return "<h1>hello World</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False)

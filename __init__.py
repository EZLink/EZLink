from flask import Flask, request, url_for, session, redirect, send_from_directory
from twilio_api import UrlGrabber
from name_card_processing import ImageProcessor
from contact_maker import make_vcf
from smscomm import respondToUser


import cv2

app = Flask(__name__, static_url_path='')


# This is the endpoint intended to serve twilio. 
# NOT intended for the user to use
@app.route('/vcf/<path:path>')
def vcf(path):
    return send_from_directory('/vcf/', path)

# Testing purpose
@app.route('/')
def index():
    return "<h1>hello World</h1>"

@app.route('/input', methods = ['GET', 'POST'])#)
def input():
    if(('From' in request.args) and ('SmsMessageSid' in request.args)):
        print("hi")
        num = request.args["From"]
        sid = request.args["SmsMessageSid"]

        grabber = UrlGrabber(sid, num)
        # TODO change name
        url = grabber.get_image()

        ori_img = cv2.imread('nc6.jpeg', cv2.IMREAD_GRAYSCALE)
        image_processor = ImageProcessor(ori_img)
        result = image_processor.image_to_string()
            
        file_name = make_vcf(*result)

        # TODO delete
        print(file_name)

        respondToUser(file_name, num, 'EZLink.vcf')
        return "End of the Input"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

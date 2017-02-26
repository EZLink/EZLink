# EZLink

An SMS-messaging tool for automatically creating a phone contact using a physical business card. Never lose a potential connection again!
  * Takes a picture of a business card (sent to Twilio) and returns a digital contact card.
  * Uses python to perform image recognition in order to extract a name and phone number from a physical object.
  * Uses Flask back-end to serve .vcf files (phone contact file) to the Twilio API to be sent back to the user.

## USAGE
  * Get a business card at a career fair.
  * Take a picture of the card so you don't lose it.
  * Text it to EZLink's easy to reach phone number -- (872) 240-5571

## BUILD/INSTALLATION INSTRUCTIONS
  * Mac/OS
    * Make a twilio/AWS account (for free!)
    * Provide the respective API keys in files called `twilio_credentials.py` and `aws_credentials.py`
    * `pip install requirements.txt`
    * A set up script for a server will be available soon. Until then, our server will be up (for at least four months).

## INTERFACES
  * Everything is done by sending a text message.

## OTHER SOURCES OF DOCUMENTATION
  * [Video demonstration of use](https://vimeo.com/205741775)

## Contributor Guide
  * [LINK TO CONTRIBUTING.md]

## License
  * This project is on the MIT License

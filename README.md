# EZLink

_Ever gotten a really important person's business card, intended to contact them, and lost it? This will fix that._
  * An SMS-messaging tool for automatically creating a phone contact using a physical business card.
  * Utilizes image recognition to extract a name and phone number from a physical object.
  * Creates a virtual contact card using processed data. 
  * Uses Flask back-end to serve .vcf files (phone contact file) to the Twilio API to be sent back to the user.

## USAGE
  * Get a business card at a career fair.
  * Take a picture of the card so you don't lose it.
  * Text it to EZLink's easy to reach phone number -- (872) 240-5571
  * EZLink will respond with a contact card, allowing you to easily store the contact
## BUILD/INSTALLATION INSTRUCTIONS
  * Mac/OS
    * Make a Twilio/AWS account (for free!)
    * Provide the respective API keys in files called `twilio_credentials.py` and `aws_credentials.py`
    * `pip install -r requirements.txt`
    * A set up script for a server will be available soon. Until then, our server will be up (for at least four months).

## INTERFACES
  * Everything is done by sending a text message. 
  * No installation, no registration, access from any phone.

## OTHER SOURCES OF DOCUMENTATION
  * [Video demonstration of use](https://vimeo.com/205743684)

## Contributor Guide
  * [CONTRIBUTERS.md](https://github.com/EZLink/EZLink/blob/master/CONTRIBUTORS.md)

## License
  * This project is under the MIT License

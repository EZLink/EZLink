# EZLink

_Ever gotten a really important person's business card, intended to contact them, and lost it? This will fix that._

EZLink utilizes image recognition to extract a name and phone number from a physical object, such as a business card. It then creates a virtual contact card using processed data, and finally uses Flask back-end to serve .vcf files (phone contact file) to the Twilio API to be sent back to the user.

## USAGE
  * Get a business card at a career fair or by other means. 
  * Take a picture of the card and text it to EZLink's easy to reach phone number: __(872) 240-5571__ .
  * EZLink will respond with a contact card, allowing you to easily store the contact.

## BUILD/INSTALLATION INSTRUCTIONS
  * Unix:
    * Make free Twilio and AWS accounts.
    * Provide the respective API keys in files called `twilio_credentials.py` and `aws_credentials.py`
    * `pip install -r requirements.txt` to install all dependencies.

## INTERFACES
  * Everything is done by sending a text message. 
  * No installation, no registration, access from any phone.

## OTHER SOURCES OF DOCUMENTATION
  * [Video demonstration of use](https://vimeo.com/205743684)

## Contributor Guide
  * [CONTRIBUTING.md](https://github.com/EZLink/EZLink/blob/master/CONTRIBUTING.md)

## License
  * This project is under the MIT License

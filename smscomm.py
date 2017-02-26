from twilio.rest import TwilioRestClient
import twilio_credentials as Twilio_Credentials
import boto3
import aws_credentials as AWS_Credentials
import os
from botocore.exceptions import ClientError

def putFileInS3(client, fileName):
    """stores vcf file in amazon S3 bucket"""
    client.upload_file(fileName, "easylink-users", fileName)

def deleteFileFromS3(client, fileName):
    """deletes the object with the filename from the S3 bucket"""
    client.delete_object(Bucket = "easylink-users", Key = fileName)

def checkIfFirstTimeUser(phoneNumber):
    """checks if the phone number is in the S3 database,
    returns false if the user exists. if not, creates the
     file in the database for the user and returns true.
    """
    firstTimeUser = False
    if ".txt" not in phoneNumber:
        phoneNumber += ".txt"
    s3Client = boto3.client('s3', aws_access_key_id = AWS_Credentials.AWS_ACCESS_KEY, aws_secret_access_key = AWS_Credentials.AWS_SECERET_KEY)
    try:
        numberInBucket = s3Client.download_file("easylink-users", phoneNumber, phoneNumber)
        os.remove(phoneNumber)
        return firstTimeUser

    except ClientError as e:
        if e.response["ResponseMetadata"]["HTTPStatusCode"] == 404:
            firstTimeUser = True

        if firstTimeUser:
            fileName = phoneNumber
            with open(fileName, "w"):
                s3Client.upload_file(fileName, "easylink-users", fileName)
            os.remove(fileName)

    return firstTimeUser

def respondToUser(vcfFileName, phoneNumber, easyCardFileName):
    """sends the response card corresponding to the user's input.
    Send the name prompt and standard EasyLink card if the user
    is a first time user
    """
    sendResponseCard(vcfFileName, phoneNumber)
    sendShareInfoPrompt(phoneNumber)

    addPotentialCardExchange(phoneNumber)

    # get EZLink registered in their phone as a contact
    if checkIfFirstTimeUser(phoneNumber):
        sendEasyLinkCard(easyCardFileName, phoneNumber)
        registationMessage = "Send us your name for a more personalized experience at any time! "
                                + " (In the format \"name: first last\")"
        sendTextPrompt(phoneNumber, registationMessage)

def sendTextPrompt(toNumber, message):
    """Sends the name prompt message to the phone number passed as a parameter"""
    client = TwilioRestClient(Twilio_Credentials.accountName, Twilio_Credentials.accountPassword)
    fromNumber = Twilio_Credentials.twilioNumber
    client.messages.create(to = toNumber, from_ = fromNumber, body = message)

def sendEasyLinkCard(easyCardFileName, toNumber):
    """Sends the default EasyLink card to the phone number passed as a parameter"""
    sendResponseCard(easyCardFileName, toNumber)

def sendResponseCard(vcfFileName, toNumber):
    """Sends the response card to the phone number passed as a parameter"""
    vcfURL = "http://104.131.28.198:8000/vcf/" + vcfFileName

    client = TwilioRestClient(Twilio_Credentials.accountName, Twilio_Credentials.accountPassword)
    fromNumber = Twilio_Credentials.twilioNumber
    client.messages.create(to = toNumber, from_ = fromNumber, media_url = vcfURL)

def hasNameInDatabase(phoneNumber):
    """Returns true if the user has a name in the database, false if the file is empty"""
    if os.path.getsize(phoneNumber) == 0:
        return False
    else:
        return True

def addPotentialCardExchange(phoneNumber):
    """adds the card exchange identifier to the current phone number"""
    try:
        phoneNumber += ".txt"
        s3Client = boto3.client('s3', aws_access_key_id = AWS_Credentials.AWS_ACCESS_KEY, aws_secret_access_key = AWS_Credentials.AWS_SECERET_KEY)
        s3Client.download_file("easylink-users", phoneNumber, phoneNumber)
        with open(phoneNumber, "a") as file:
            file.write("\nexchanging information")
        putFileInS3(s3Client, phoneNumber)
        os.remove(phoneNumber)
    except ClientError as e:
        return

def associateNameWithNumber(name, phoneNumber):
    """Downloads the phone number file from the S3 database, and writes the users
    name to the file, and uploads it to the database
    """
    checkIfFirstTimeUser(phoneNumber)
    if ".txt" not in phoneNumber:
        phoneNumber += ".txt"
    s3Client = boto3.client('s3', aws_access_key_id = AWS_Credentials.AWS_ACCESS_KEY, aws_secret_access_key = AWS_Credentials.AWS_SECERET_KEY)
    s3Client.download_file("easylink-users", phoneNumber, phoneNumber)
    with open(phoneNumber, "w") as file:
        file.write(name)
    putFileInS3(s3Client, phoneNumber)
    os.remove(phoneNumber)

def changeName(name, phoneNumber):
    """Changes the name of the user in the database"""
    try:
        if ".txt" not in phoneNumber:
            phoneNumber += ".txt"
        s3Client = boto3.client('s3', aws_access_key_id = AWS_Credentials.AWS_ACCESS_KEY, aws_secret_access_key = AWS_Credentials.AWS_SECERET_KEY)
        s3Client.download_file("easylink-users", phoneNumber, phoneNumber)
        with open(phoneNumber, "w") as file:
            file.write(name)
        putFileInS3(s3Client, phoneNumber)
        os.remove(phoneNumber)
    except ClientError as e:
        associateNameWithNumber(name, phoneNumber)

def exchangingCard(phoneNumber):
    """Checks to see if the user has a \"pending card exchange\" tag associated with them"""
    try:
        if ".txt" not in phoneNumber:
            phoneNumber += ".txt"
        s3Client = boto3.client('s3', aws_access_key_id = AWS_Credentials.AWS_ACCESS_KEY, aws_secret_access_key = AWS_Credentials.AWS_SECERET_KEY)
        s3Client.download_file("easylink-users", phoneNumber, phoneNumber)
        with open(phoneNumber, "r") as file:
            exchangingCard = False
            lines = file.read().split("\n")
            for line in lines:
                if line == "exchanging information":
                    exchangingCard = True
                    break
            return exchangingCard
    except ClientError as e:
        return False

def handleText(text, phoneNumber):
    """mother method for handling incoming messages with text"""
    lowerText = text.lower()
    textParts = text.split(" ")

    if len(textParts) > 1 and textParts[0] == "name:":
        textParts.remove("name:")
        name = " ".join(textParts)
        changeName(name, phoneNumber)
    elif text == "yes" or text == "yeah" or text == "yup":
        if exchangingCard(text, phoneNumber):
            userName = getName(phoneNumber)
            exchangeCard(userName, phoneNumber)

def getName(phoneNumber):
    """Returns the name of the user which matches the phone number"""
    try:
        if ".txt" not in phoneNumber:
            phoneNumber += ".txt"
        s3Client = boto3.client('s3', aws_access_key_id = AWS_Credentials.AWS_ACCESS_KEY, aws_secret_access_key = AWS_Credentials.AWS_SECERET_KEY)
        s3Client.download_file("easylink-users", phoneNumber, phoneNumber)
        with open(phoneNumber, "r") as file:
            lines = file.read()
            return lines[0]
    except ClientError as e:
        return ""


def sendShareInfoPrompt(phoneNumber):
    """Sends text to the user prompting them to share their information with their new contact"""
    message = "Would you like to share your contact information with your new contact?"
    sendTextPrompt(phoneNumber, message)

def sendCardExchange(cardURL, recipientPhoneNumber):
    """Sends the users contact information to their new contact"""
    message = "A new contact of yours shared their information with you!"
    client = TwilioRestClient(Twilio_Credentials.accountName, Twilio_Credentials.accountPassword)
    fromNumber = Twilio_Credentials.twilioNumber
    client.messages.create(to = recipientPhoneNumber, from_ = fromNumber, body = message, media_url = cardURL)

def exchangeCard(name, phoneNumber, recipientPhoneNumber):
    """Exchanges the users contact card with their new contact"""
    try:
        nameParts = name.split(" ")
        formattedName = "_".join(nameParts)
        cardURL = "http://104.131.28.198:8000/vcf/" + formattedName + ".vcf"
        sendCardExchange(cardURL, recipientPhoneNumber)
    except ClientError as e:
        failMessage = "Unable to send your information."
        sendTextPrompt(phoneNumber, failMessage)

if __name__ == "__main__":
    pass
    #handleText("name: aaron green", "5024243665")
    #handleText("billy joel", "5024243665")

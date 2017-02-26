from twilio.rest import TwilioRestClient
import twilio_credentials as Twilio_Credentials
import boto3
import aws_credentials as AWS_Credentials
import os
from botocore.exceptions import ClientError

# @param: vcf file to be stored in amazon S3 bucket
def putFileInS3(client, fileName):
    client.upload_file(fileName, "easylink-users", fileName)

# @param: delete the object with the filename from the S3 bucket
def deleteFileFromS3(client, fileName):
    client.delete_object(Bucket = "easylink-users", Key = fileName)

# @param: phone number of user as string
# @return: true if first time user, false otherwise
def checkIfFirstTimeUser(phoneNumber):
    firstTimeUser = False
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

# @param: vcfURL url of the card which is the response to the user's image
# @param: phoneNumber phone number of the user who is going to recieve the message
# @param: ezCardURL url of the default EZLink card for user's to have
def respondToUser(vcfFileName, phoneNumber, easyCardFileName):
    sendResponseCard(vcfFileName, phoneNumber)

    # get EZLink registered in their phone as a contact
    if checkIfFirstTimeUser(phoneNumber):
        sendEZLinkCard(easyCardFileName, phoneNumber)
        sendNamePrompt(phoneNumber)


# @param toNumber phone number of user who is going to receive the message
def sendNamePrompt(toNumber):
    registrationMessage = "Send us your name for a more personalized experience at any time!"
    client = TwilioRestClient(Twilio_Credentials.accountName, Twilio_Credentials.accountPassword)
    fromNumber = Twilio_Credentials.twilioNumber
    client.messages.create(to = toNumber, from_ = fromNumber, body = registrationMessage)

# @param: ezCardURL default url of the EZLink
# @param: toNumber phone number of user receiving message
def sendEZLinkCard(easyCardFileName, toNumber):
    sendResponseCard(easyCardFileName, toNumber)

# @param: url of the vCard on the server
# Send the text message with the vCard to the user
def sendResponseCard(vcfFileName, toNumber):
    vcfURL = "http://104.131.28.198:8000/vcf/" + vcfFileName

    client = TwilioRestClient(Twilio_Credentials.accountName, Twilio_Credentials.accountPassword)
    fromNumber = Twilio_Credentials.twilioNumber
    client.messages.create(to = toNumber, from_ = fromNumber, media_url = vcfURL)


# @param: name user's to be asssociated with the phone number
# @param: phone number to have the name associated with it
def associateNameWithNumber(name, phoneNumber):
    checkIfFirstTimeUser(phoneNumber)
    phoneNumber += ".txt"
    s3Client = boto3.client('s3', aws_access_key_id = AWS_Credentials.AWS_ACCESS_KEY, aws_secret_access_key = AWS_Credentials.AWS_SECERET_KEY)
    s3Client.download_file("easylink-users", phoneNumber, phoneNumber)
    with open(phoneNumber, "w") as file:
        file.write(name)
    putFileInS3(s3Client, phoneNumber)
    os.remove(phoneNumber)

if __name__ == "__main__":
    pass
    # associateNameWithNumber("Aaron Green", "5024243665")
    # print (checkIfFirstTimeUser("5024243665"))
    # print (checkIfFirstTimeUser("3613941111"))
    # print (checkIfFirstTimeUser("2413651212"))
    # print (checkIfFirstTimeUser("5024243665"))

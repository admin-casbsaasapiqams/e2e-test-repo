import boto3
import json

# The name of the profile you'd like to use
profile_name = 'sso_engineer'

# Create a session using the specified profile
session = boto3.Session(profile_name=profile_name,region_name="us-west-2")

# Create SQS client using the session
sqs = session.client('sqs')
# URL of the SQS queue
queue_url = 'https://sqs.us-west-2.amazonaws.com/495547762392/stg3_1ddadf999c04c7d7ab5cb32ef25cbadd_email'

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=10,  # Adjust the number of messages to retrieve
    WaitTimeSeconds=10  # Long polling (optional)
)

# Check if we received any messages
if 'Messages' in response:
    for message in response['Messages']:
        print("Message ID:", message['MessageId'])
        print("Receipt Handle:", message['ReceiptHandle'])
        print("Message Body:", message['Body'])
        print("Attributes:", message.get('Attributes', {}))
        print("Message Attributes:", message.get('MessageAttributes', {}))
        print("----")
        # Optional: Delete the message after processing
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
else:
    print("No messages available")
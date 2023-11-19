import os
from twilio.rest import Client

def send_notification(body, from_, to_):
  account_sid = os.environ['TWILIO_ACCOUNT_SID']
  auth_token = os.environ['TWILIO_AUTH_TOKEN']
  client = Client(account_sid, auth_token)
  
  message = client.messages \
    .create( body=body, from_=from_, to=to_ )
    
  return message.sid
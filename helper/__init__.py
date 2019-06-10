from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from database import EmailDb 

db = EmailDb()

SCOPES = 'https://www.googleapis.com/auth/gmail'

def store_email():
  store = file.Storage('token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
  service = build('gmail', 'v1', http=creds.authorize(Http()))
  # Call the Gmail API to fetch INBOX
  results = service.users().messages().list(userId='me').execute()
  messages = results.get('messages', [])
  senders = []
  msg_details = []
  for index in range(0, 32):
    message = messages[index]
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    msg_headers=msg["payload"]["headers"]
    message = msg['snippet']
    subject = [i['value'] for i in msg_headers if i["name"]=="Subject"]
    sender = [i['value'] for i in msg_headers if i["name"]=="From"]
    date = [i['value'] for i in msg_headers if i["name"]=="Date"]
    db.store(sender[0], date[0], subject[0], message)
    msg_details.append({
      'sender' : sender[0],
      'date' : date[0],
      'subject' : subject[0],
      'message' : message
      })
  return msg_details

def filter_all(email_id, contains):
  response = []
  subjects = db.get_subject(email_id)
  for subject in subjects:
    words = subject[0].split(' ')
    for word in words:
      if word == contains:
        response.append({
          "sender" : email_id,
          "subject" : subject[0]
        })
  return response

def filter_any(email_id, contains):
  response = []
  email_subjects = db.get_subject(email_id)
  for email_subject in email_subjects:
    response.append({
      "sender" : email_id,
      "subject" : email_subject[0]
    })
  subjects = db.get_all_subject()
  for subject in subjects:
    words = subject[0].split(' ')
    sender = db.get_email(subject[0])
    for word in words:
      if word == contains:
        response.append({
          "sender" : sender[0],
          "subject" : subject[0]
        })
  result = [index for length, index in enumerate(response) if index not in response[length + 1:]] 
  return (result)
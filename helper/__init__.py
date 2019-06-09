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
  for index in range(0, 10):
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

def filter_emailid(email_id):
  if db.email_exist(email_id):
    email_details = db.get_details(email_id)
    return email_details
  return {
    'message' : 'Email id not found'
  }
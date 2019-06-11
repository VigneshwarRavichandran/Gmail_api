from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from database import EmailDb 
from datetime import datetime, timedelta
from time import strptime

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
  for index in range(0, 38):
    message = messages[index]
    message_id = message['id']
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    msg_headers=msg["payload"]["headers"]
    message = msg['snippet']
    subject = [i['value'] for i in msg_headers if i["name"]=="Subject"]
    sender = [i['value'] for i in msg_headers if i["name"]=="From"]
    date = [i['value'] for i in msg_headers if i["name"]=="Date"]
    db.store(sender[0], date[0], subject[0], message, message_id)
    msg_details.append({
      'sender' : sender[0],
      'date' : date[0],
      'subject' : subject[0],
      'message' : message
      })
  return msg_details

def filter_all(email_id, contains, days):
  response = []
  contents = db.get_content(email_id)
  for content in contents:
    mail_date = content[0]
    mail_subject = content[1]
    words = mail_subject.split(' ')
    for word in words:
      if word == contains:
        temp_arr = mail_date.split(', ')
        date_string = temp_arr[len(temp_arr)-1]
        date_arr = date_string.split(' ')
        if date_arr[0] == '':
          date_arr.pop(0)
        day = int(date_arr[0])
        month = int(strptime(date_arr[1],'%b').tm_mon)
        year = int(date_arr[2])
        date = datetime(year, month, day)
        limit = datetime.now() - timedelta(days=int(days)+1)
        if date > limit:
          response.append({
            "sender" : email_id,
            "subject" : mail_subject,
            "date" : mail_date
          })
  return response

def filter_any(email_id, contains, days):
  response = []
  contents = db.get_all_content()
  for content in contents:
    mail_sender = content[0]
    mail_date = content[1]
    mail_subject = content[2]
    temp_arr = mail_date.split(', ')
    date_string = temp_arr[len(temp_arr)-1]
    date_arr = date_string.split(' ')
    if date_arr[0] == '':
      date_arr.pop(0)
    day = int(date_arr[0])
    month = int(strptime(date_arr[1],'%b').tm_mon)
    year = int(date_arr[2])
    date = datetime(year, month, day)
    limit = datetime.now() - timedelta(days=int(days)+1)
    words = mail_subject.split(' ')
    word_contain = False
    for word in words:
      if word == contains:
        word_contain = True
    if mail_sender == email_id or date > limit or word_contain == True:
      response.append({
        "sender" : mail_sender,
        "subject" : mail_subject,
        "date" : mail_date
      })
  return response

def mail_action():
  store = file.Storage('token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
  service = build('gmail', 'v1', http=creds.authorize(Http()))
  service.users().messages().modify(userId='me', id='16b47f24f4beb842', body={'addLabelIds': ['INBOX'],'removeLabelIds': ['UNREAD']}).execute()
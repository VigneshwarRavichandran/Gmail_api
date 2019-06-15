from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from database import EmailDb 
from datetime import datetime, timedelta
from time import strptime

db = EmailDb()

SCOPES = 'https://www.googleapis.com/auth/gmail'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
  creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

def store_email():
  results = service.users().messages().list(userId='me').execute()
  messages = results.get('messages', [])
  for message in messages:
    message_id = message['id']
    msg = service.users().messages().get(userId='me', id=message['id']).execute()
    msg_headers=msg["payload"]["headers"]
    mail_subject = [i['value'] for i in msg_headers if i["name"]=="Subject"]
    mail_sender = [i['value'] for i in msg_headers if i["name"]=="From"]
    message_date = [i['value'] for i in msg_headers if i["name"]=="Date"]
    # Date formatting for storage
    mail_date = message_date[0]
    temp_date_arr = mail_date.split(', ')
    date_string = temp_date_arr[len(temp_date_arr)-1]
    date_arr = date_string.split(' ')
    if date_arr[0] == '':
      date_arr.pop(0)
    day = int(date_arr[0])
    month = int(strptime(date_arr[1],'%b').tm_mon)
    year = int(date_arr[2])
    date = "{}-{:02d}-{:02d}".format(year, month, day)
    # Extracting email id from the sender data
    sender = mail_sender[0]
    sender = sender.split('<')
    sender = sender[len(sender)-1]
    email_id = sender[0:len(sender)-1]
    # Store message_id, email_id, date, mail_subject in the database
    try:
      db.store(message_id, email_id, date, mail_subject[0])
    except:
      pass
    return "INBOX messages stored successfully!"

def filter_all(email_id, contains, days, action):
  # Get the appropriate date for the condition
  date_limit = datetime.now() - timedelta(days=int(days)+1)
  day = date_limit.day
  month = date_limit.month
  year = date_limit.year
  date = "{}-{:02d}-{:02d}".format(year, month, day)
  mail_ids = db.contain_all(email_id, date, contains)
  message_ids = []
  for mail_id in mail_ids:
    message_ids.append(mail_id[0])
  # Check whether there is a mail on given conditions
  if message_ids == []:
    return 'No messages with the specified conditions!'
  else:
    # Mark as UNREAD for all the mails that satisfy the conditions
    if action == "UNREAD":
      service.users().messages().batchModify(userId='me', body={'addLabelIds': ['UNREAD'], 'ids': message_ids}).execute()
    # Mark as UNREAD for all the mails that satisfy the conditions
    elif action == "READ":
      service.users().messages().batchModify(userId='me', body={'removeLabelIds': ['UNREAD'], 'ids': message_ids}).execute()
    return 'Action is done successfully!'


def filter_any(email_id, contains, days, action):
  # Get the appropriate date for the condition
  date_limit = datetime.now() - timedelta(days=int(days)+1)
  day = date_limit.day
  month = date_limit.month
  year = date_limit.year
  date = "{}-{:02d}-{:02d}".format(year, month, day)
  mail_ids = db.contain_any(email_id, date, contains)
  message_ids = []
  for mail_id in mail_ids:
    message_ids.append(mail_id[0])
  # Check whether there is a mail on given conditions
  if message_ids == []:
    return 'No messages with the specified conditions!'
  else:
    if action == "UNREAD":
      # Mark as UNREAD for all the mails that satisfy the conditions
      service.users().messages().batchModify(userId='me', body={'addLabelIds': ['UNREAD'], 'ids': message_ids}).execute()
    elif action == "READ":
      # Mark as READ for all the mails that satisfy the conditions
      service.users().messages().batchModify(userId='me', body={'removeLabelIds': ['UNREAD'], 'ids': message_ids}).execute()
    return 'Action is done successfully!'
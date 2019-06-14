from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build


store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))
results = service.users().messages().list(userId='me').execute()
messages = results.get('messages', [])
message = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
print('Message snippet: %s' % message['snippet'])
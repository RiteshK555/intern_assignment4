import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

#load env
load_dotenv()

EMAIL = os.getenv('EMAIL')

def send_email():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart()
    message['to'] = EMAIL
    message['subject'] = 'CSV Attachment'
    message.attach(MIMEText('Please see the attached CSV file'))

    filename = 'output.csv'
    with open(filename, 'r') as f:
        csv_data = f.read()
    csv_part = MIMEBase('application', 'octet-stream')
    csv_part.set_payload(csv_data)
    encoders.encode_base64(csv_part)
    csv_part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    message.attach(csv_part)

    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(F'sent message to {message["to"]} Message Id: {send_message["id"]}')




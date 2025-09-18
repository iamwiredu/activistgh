import smtplib
from email.mime.text import MIMEText  # fix import and class name

sender = 'hello@outhinck.agency'
recipient = 'kwakuwiredu0@gmail.com'

# build the message
msg = MIMEText('This is the body of the email.')
msg['Subject'] = 'This is the subject of Email'  # header names are case-sensitive
msg['From'] = sender
msg['To'] = recipient

# send via Zoho SMTP over SSL
with smtplib.SMTP_SSL('smtppro.zoho.in', 465) as server:
    server.login(sender, 'j29y fUPF KxuG')       # fix method name: login, not ogin
    server.sendmail(sender, recipient, msg.as_string())

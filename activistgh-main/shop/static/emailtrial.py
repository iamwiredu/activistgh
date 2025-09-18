import smtplib
from email.mime.text import MIMEText  # fix import and class name

sender = 'hello@outhinck.agency'
recipient = 'kwakuwiredu0@gmail.com'

# build the message
msg = MIMEText('This is the body of the email.')
msg['Subject'] = 'This is the subject of Email'  # header names are case-sensitive
msg['From'] = sender
msg['To'] = recipient

with smtplib.SMTP_SSL('smtppro.zoho.in', 465) as server:
    server.set_debuglevel(1)                      # <-- prints SMTP traffic
    server.login(sender, 'j29yfUPFKxuG')            # use your app-specific pwd
    server.sendmail(sender, recipient, msg.as_string())

import smtplib
from email.mime.multipart import MIMEMultipart as mtp
from email.mime.text import MIMEText as mt
from config import gmail_smtp


def send_email(recipients, subject, body, filepaths=[]):
    '''
    uses mailgun SMTP credentials and smtplib
    Expects:
      recipients as list
      subject as string
      email body as string
      file paths as list (optional)
    '''
    creds = gmail_smtp()
    msg = mtp()
    msg['Subject'] = subject
    msg['From'] = creds["from"]
    msg['To'] = ", ".join(recipients)
    msg.attach(mt(body, "plain"))
    for file in filepaths:
        with open(file, 'rb') as fp:
            body = mt(fp.read())
        body.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(body)

    s = smtplib.SMTP(creds["hostname"], creds["port"])
    s.ehlo()
    s.starttls()
    s.login(creds["username"], creds["password"])
    s.sendmail(msg['From'], recipients, msg.as_string())
    s.quit()
    return True

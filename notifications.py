import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import os
  
def emailMe():
    port = 465 
    smtp_server = "mail.delgaudiomike.com"
    sender_email = os.environ.get("EMAIL_USER") 
    receiver_email = "delgaudiomike@gmail.com" 
    password = os.environ.get("EMAIL_PASS")
    message = MIMEMultipart("alternative")
    message["Subject"] = "[POPULAR TICKERS] {}".format(date.today().strftime("%m/%d/%y"))
    message["From"] = sender_email
    message["To"] = receiver_email

    html = """\
    <html>
    <body>
        <h1>Today's most popular trade: ''</h1>
        <h2>Most frequent for this week: ''</h2>
        <h2>Here are new tickers that first appeared today: ''</h2>
    </body>
    </html>
    """
    part2 = MIMEText(html, "html")
    message.attach(part2)
    try:
        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_bytes())
    except Exception as err:
        print(err)
    finally:
        server.quit()
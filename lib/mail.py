import smtplib
from email.message import EmailMessage
import imghdr

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)

    user = "robotic.arm.delpozzo@gmail.com"
    password = "lwoahwsncgwjocgp"

    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = user
    server = smtplib.SMTP("smtp.gmail.com")
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

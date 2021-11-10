#! /usr/local/bin/python
# import argparse
import sys
import os
import json
from smtplib import SMTP_SSL, SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.mime.text import MIMEText
from os.path import expanduser
home = expanduser("~")
default_path=os.path.join(home,".mail")
#! /usr/local/bin/python
# from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP_SSL, SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.mime.text import MIMEText

def send(**kwargs):
    with open(default_path, "r") as f:
        params = json.load(f)
    SMTPserver = params['SMTPserver']
    USERNAME = params['USERNAME']
    if('PASSWORD' in params): 
        PASSWORD = params['PASSWORD']
    else:
        print("[Warning!] No password specified!")
        PASSWORD = None
    #fail sender to username if not provided
    if('sender' in params): sender = params['sender']
    else: sender = params['USERNAME']
    if('type' in kwargs):
        text_subtype = kwargs['type']
    else:
        text_subtype = 'plain'

    #compose message
    if('destination' in kwargs):
        destination =kwargs['destination']
    elif('to' in kwargs):
        destination = kwargs['to']
    elif('destination' in params):
        print("Trying to load destination from file")
        destination = params['destination']
    elif('to' in params):
        print("Trying to load destination from file")
        destination = params['to']
    else:
        print("No destination specified. Using sender address")
        destination = sender
    if('subject' in kwargs):
        subject=kwargs['subject']
    else:
        subject = "Message from: "+sender
    if(len(subject)<2): subject="Message from "+sender
    if('message' in kwargs):
        content=kwargs['message']
    else:
        content = subject
    msg = MIMEText(content, text_subtype)
    msg['Subject']= subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all
    print("Sending message: "+subject)
    if(PASSWORD):
        try:
            conn = SMTP_SSL(SMTPserver)
            # conn.set_debuglevel(False)
            conn.login(USERNAME, PASSWORD)
        except:
            print("Unable to authenticate with secure SMTP with SSL. Trying SMTP.")
            try:
                conn = SMTP(SMTPserver)
                conn.login(USERNAME, PASSWORD)
            except:
                conn = SMTP(SMTPserver)
    else:
        print("Trying without authenticating.")
        conn = SMTP(SMTPserver)
    try:
        print("[Sending email message]")
        print("Sender: "+sender)
        print("To: "+destination)
        print("Subject: "+subject)
        print("Message: "+msg.as_string())
        conn.sendmail(sender, destination, msg.as_string())
    except Exception as e:
        print("Oh no! Encountered an error sending this message!")
        print(e)
        raise Exception("[Error] Unable to send message")
    finally:
        conn.quit()
    return True

if(__name__=='__main__'):
    #load args and kwargs and pass them through
    args = []
    kwargs = {}
    for arg in sys.argv[1:]:
        print(arg)
        if("=" in arg):
            k = arg.split("=")
            kwargs[k[0]] = k[1]
        else:
            args.append(arg)
    #pass through
    send(**kwargs)
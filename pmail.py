#! /usr/local/bin/python
# import argparse
import sys
import json
from smtplib import SMTP_SSL, SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from email.mime.text import MIMEText

def send(**kwargs):
    print("Sending email")
    print(kwargs)
    if('file' in kwargs): #load params from file
        with open(kwargs['file'],"r") as f:
            params = json.load(f)
    elif('auth' in kwargs): #if auth specified as json text
        params = json.loads(kwargs['auth'])
    else:
        try:
            print("Loading parameters from default file")
            with open("email.json","r") as f:
                params = json.load(f)
        except:
            print("No parameters specified. Exiting")
            exit(1)
    if('SMTPserver' in params):
        SMTPserver = params['SMTPserver']
    elif('server' in params):
        SMTPserver = params['server']
    else:
        print("No server specified")
        exit(1)
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
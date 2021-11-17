# psmtp
Python SMTP client.
- compatible with Linux mail command, without the headaches of system configuration.
- Behaves like the mail command and supports standard commandline options for mail
- Requires .mail config file in user's home directory (~/.mail)
- Syntax: 
    'echo "test message"| pmail -s "test subject" -c cc@example.com to@example.com'
# .mail example:
- Place this content in: ~/.mail
- Note that optional default params in this file are overwritten by commandline arguments
```
{
    "SMTPserver" : "[smtp.mail.yahoo.com]",
    "sender" :     "[user]@yahoo.com",
    "USERNAME" : "[user]",
    "PASSWORD" : "[password]",
    "to":"[optional... destination@example.com]"
}
```

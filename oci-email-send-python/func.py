#
# oci-email-send-python version 1.0.
#
# Copyright (c) 2020 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import io
import json
import smtplib 
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fdk import response


def handler(ctx, data: io.BytesIO=None):
    smtp_username = smtp_password = smtp_host = ""
    smtp_port = 0
    sender_email = sender_name = recipient = subject = body = ""
    try:
        cfg = ctx.Config()
        smtp_username = cfg["smtp-username"]
        smtp_password = cfg["smtp-password"]
        smtp_host = cfg["smtp-host"]
        smtp_port = cfg["smtp-port"]
    except Exception as ex:
        print('ERROR: Missing configuration key', ex, flush=True)
        raise
    try:
        payload_bytes = data.getvalue()
        if payload_bytes==b'':
            raise KeyError('No keys in payload')
        payload = json.loads(payload_bytes)
        sender_email = payload["sender-email"]
        sender_name = payload["sender-name"]
        recipient = payload["recipient"]
        subject = payload["subject"]
        body = payload["body"]
    except Exception as ex:
        print('ERROR: Missing key in payload', ex, flush=True)
        raise
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((sender_name, sender_email))
    msg['To'] = recipient
    msg.attach(MIMEText(body, 'plain'))

    try: 
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.close()
    except Exception as ex:
        print("ERROR: ", ex, flush=True)
        raise
    else:
        print ("INFO: Email successfully sent!", flush=True)

    return response.Response(
        ctx, 
        response_data="Email successfully sent!",
        headers={"Content-Type": "application/json"}
    )

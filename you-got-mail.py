import datetime
import email
import imaplib
import mailbox
import subprocess
import schedule
import time

LAST_UID = 0

def job():
    global LAST_UID

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login("example@example.com", "EMAIL_PASSWORD")
    mail.list()
    mail.select('inbox')


    result, data = mail.uid('search', None, "ALL")
    latest_email_uid = data[0].split()[-1]
    if LAST_UID != latest_email_uid:
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')

        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))


        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                subprocess.Popen(['mpg123', '-q', 'you-got-mail.mp3']).wait()
                print("from: " + email_from)
            else:
                continue
    LAST_UID = latest_email_uid


schedule.every(1).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)

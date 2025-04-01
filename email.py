import imaplib
import email

def save_emails(username, password, output_dir):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select('inbox')
    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    os.makedirs(output_dir, exist_ok=True)
    for e_id in email_ids:
        result, data = mail.fetch(e_id, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)
        filename = f"email_{e_id.decode()}.eml"
        with open(os.path.join(output_dir, filename), 'wb') as f:
            f.write(raw_email)

import smtplib, os, json
from email.message import EmailMessage

def notification(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = os.environ.get("GEMAIL_ADDRESS")
        sender_password = os.environ.get("GEMAIL_PASSWORD")
        receiver_address = message['usernme']

        msg = EmailMessage()
        msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_address
        
        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_password)
        session.send_message(msg)
        session.quit()
        print("Mail Sent!")
    except Exception as err:
        print(err)
        return err
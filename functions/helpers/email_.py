import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication

class Email():
    def __init__(self,email,password):
        self.email= email
        self.password = password
    
    def send_email(self,reciver,subject,content,files=None,):
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = reciver
        message['Bb'] = ['chavanomkar245@gmail.com','ankitkotharkar99@gmail.com',self.email]
        message['Subject'] =  subject #The subject line
        #The body and the attachments for the mail
        message.attach(MIMEText(content, 'plain'))
        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            message.attach(part)
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(self.email, self.password) #login with mail_id and password
        text = message.as_string()
        session.sendmail(self.password, reciver, text)
        session.quit()
        print('Mail Sent')

# subject='A test mail sent by Python. It has an attachment.' 
# em=Email('g15sigce2021@gmail.com','g15Deforestration')
# mail_content = '''Hello,
# This is a simple mail. There is one attachments,The mail is sent using Python SMTP library.
# Thank You'''

# em.send_email('ankitkotharkar99@gmail.com',subject,content=mail_content,files=['requirements1.txt'])
# em.send_email('chavanomkar245@gmail.com',subject,content=mail_content,files=['requirements1.txt'])
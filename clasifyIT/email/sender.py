import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendMail:
   def __init__(self):
       self.username = 'clasifyit2@gmail.com'
       self.password = 'E^Utad3c9+Ny,CV-'
       self.message = MIMEMultipart()

   def prepare_base_email(self,toaddrs,sub,mesg,base = True):
        self. message["From"] = self.username
        self.message["To"] = toaddrs
        self.message["Subject"] = sub
        html = """\
      <html>
        <body>
          <p>Hi!,<br>
            How are you today?<br>
            <p> {}<p>
          <p> Have a poor and dark day, ClassifyIT!<p>
        </body>
      </html>
      """.format(mesg)
        self.message.attach(MIMEText(html, "html"))
        if base:
            self.__send

   @property
   def __send(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.username, self.password)
            server.sendmail(self.username, self.message["To"], self.message.as_string())

   def  preapare_attatched_mail(self,toaddrs,sub,mesg,text):

        self.prepare_base_email(toaddrs=toaddrs,sub=sub,mesg=mesg,base =False)

        attachment = MIMEText(text)
        attachment.add_header('Content-Disposition', 'attachment', filename='result.txt')
        self.message.attach(attachment)
        self.__send



sender= SendMail()
#sender.prepare_base_email(toaddrs  = 'liorrezn@gmail.com', sub = "We are all fucked up", mesg = "lucifer save are souls!")
sender.preapare_attatched_mail(toaddrs  = 'liorrezn@gmail.com', sub = "We are all fucked up", mesg = "lucifer save are souls!",text="oh my")

#os.environ.get('EMAIL_USER')
#os.environ.get('EMAIL_PASSWORD')


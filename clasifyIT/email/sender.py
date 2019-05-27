import smtplib, ssl , os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SendMail:
   """""
   mail sender
   """""
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
          <h1>Hi!,<br>
            How are you today?<h1>
            <p> {}<p>
          <table width="351" cellspacing="0" cellpadding="0" border="0"> 
          <tr> <td style="vertical-align: top; text-align:left;color:#000000;font-size:12px;font-family:helvetica, arial;; text-align:left">
           <span><span style="margin-right:5px;color:#000000;font-size:15px;font-family:helvetica, arial">Classify IT! ,
            Have a poor ,dark and
            crappy day</span> </span> <br><br> 
            <table cellpadding="0" cellpadding="0" border="0"><tr></tr>
            </table> </td> </tr> </table> 
            <table width="351" cellspacing="0" cellpadding="0" border="0" style="margin-top:10px"> <tr>
             <td style="text-align:left;color:#aaaaaa;font-size:10px;font-family:helvetica, arial">
          <p>Do not use our services even not as a joke</p></td> </tr> </table>
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





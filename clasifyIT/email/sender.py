import smtplib, ssl , os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..singelton import singleton

@singleton
class SendMail:
   """""
   mail sender
   """""
   def __init__(self):
       self.username = 'clasifyit2@gmail.com'
       self.password = 'E^Utad3c9+Ny,CV-'
       self.message = MIMEMultipart()

   def prepare_base_email(self,toaddrs,sub,mesg,base = True):
        """
        base email (text without attachment) in a form of html
        :param toaddrs:
        :param sub:
        :param mesg:
        :param base:
        :return:
        """
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
            self.__send #sending the message

   @property
   def __send(self):
        """
        method to send the email
        :return:
        """
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:#openning an ssl connection to our gmail account
            server.login(self.username, self.password)# logging in
            server.sendmail(self.username, self.message["To"], self.message.as_string()) #sending the message

   def  preapare_attatched_mail(self,toaddrs,sub,mesg,text):
        """
        method to send a message with an txt attachment used for sending th result or the 3-rd auth code
        :param toaddrs:
        :param sub:
        :param mesg:
        :param text:
        :return:
        """
        self.prepare_base_email(toaddrs=toaddrs,sub=sub,mesg=mesg,base =False)

        attachment = MIMEText(text)
        attachment.add_header('Content-Disposition', 'attachment', filename='result.txt')#making the file
        self.message.attach(attachment)
        self.__send





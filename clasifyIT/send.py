import smtplib

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()

fromaddr = 'clasifyit@gmail.com'
toaddrs  = 'almoggro12@gmail.com'
username = 'clasifyIT'
password = 'clasifyit12345'

msg = "\r\n".join([
  "From: {}".format(fromaddr),
  "To: {}".format(toaddrs),
  "Subject: Just a message",
  "",
  "Why, oh why"
  ])

server.login(username, password)
server.sendmail(fromaddr, toaddrs, msg)
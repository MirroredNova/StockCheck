import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import os

# @param: to - Email address to send to
# @param: emailFrom - email address to come from
# @param: subject - Subject line for email 
# @param: body - Body text of the email
# @param: filePath - Path to the file to attach

# NEED TO PICK AND EMAIL TO HAVE THIS WORK
def sendEmail(to: str,email_from: str,subject: str,body: str='',file_path:str=None) -> None:
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = to
 
    msg.attach(MIMEText(body, 'plain'))
    
    if file_path != None:
        filename = os.path.basename(file_path)
        attachment = open(file_path, "rb") 
        p = MIMEBase('application', 'octet-stream') 
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
        # encode into base64 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p)


    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587)  
    # start TLS for security 
    s.starttls() 
    # Authentication 
    s.login(email_from, "PASSWORD") 
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    # sending the mail 
    s.sendmail(email_from, to, text) 
    # terminating the session 
    s.quit()
     


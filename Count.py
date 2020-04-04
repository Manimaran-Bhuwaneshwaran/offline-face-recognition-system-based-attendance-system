import os
import cv2
import sys
import glob
import csv
import numpy as np
import pandas
from datetime import datetime
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

#clear temp file
for i in glob.glob("Temp/*.jpg"):
    imagePath = i
    os.remove(i)

#Training data set from ./Unknown to ./Temp
out=0
for i in glob.glob("capturedImages/*.jpg"):
    imagePath = i
    cascPath = "Classifier/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
    ins=0
    for (x, y, w, h) in faces:
        ci=image[y:y+h,x:x+w]
        cv2.imwrite(f"Temp/face.{out}.{ins}.jpg",ci)
        ins+=1
    out+=1

#load and check the ./Temp with ./Known and count presented students
Present=[]
for i in glob.glob("Temp/*.jpg"):
    imagePath = i
    img_rgb = cv2.imread(i)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    for j in glob.glob("Database/Images/Known/*.jpg"):
        template = cv2.imread(j,0)
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        fname=j[22:-5]
        lname=j[-5:-4]
        name=fname+' '+lname
        if len(res)==1:
            Present.append(name)
Total=['Periyasamy M','Jeeva T','Karthikeyan M','Prasath P','Prabhakaran R','Manimaran B','Vengatesan R'
]
Total.sort()
Absent=[]
P=[]
fields=['S no','Name','Status']
sno=1
rows=[]
#Calculate absenties
for i in Total:
    e=[]
    e.append(str(sno))
    e.append(i)
    sno+=1
    if i not in Present:
        Absent.append(i)
        e.append('Absent')
    else:
        P.append(i)
        e.append('Present')
    rows.append(e)
now = datetime.now()
date_time=str(now)
filename='Database/Reports/Total/Master-Attendance.csv'
with open(filename,'w') as masterfile:
    csvwriter=csv.writer(masterfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)   
fields=['S no','Name'] 
sno=1
rows=[]
for i in P:
    e=[]
    e.append(sno)
    e.append(i)
    rows.append(e)
    sno+=1
filename='Database/Reports/Present/Master-Attendance-Present.csv'
with open(filename,'w') as masterfile:
    csvwriter=csv.writer(masterfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)     
print()
sno=1
rows=[]
for i in Absent:
    e=[]
    e.append(sno)
    e.append(i)
    rows.append(e)
    sno+=1
filename='Database/Reports/Absent/Master-Attendance-Absent.csv'
with open(filename,'w') as masterfile:
    csvwriter=csv.writer(masterfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows) 

print("Total : ",len(Total))
print("Present : ",len(Present))
print("Absent : ",len(Absent))
'''       
#send email
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Today's Attendance report"
body = "This is today's attendance report: It contaions Total,Prasent,Absent data sets"
sender_email = "manimaranbhuwaneshwaran@gmail.com"
receiver_email = ""
password = ""
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email 
message.attach(MIMEText(body, "plain"))
filename = "Database/Reports/Total/Master-Attendance.csv"  
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())  
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)
message.attach(part)
text = message.as_string()
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
print("Message sented Sucessfully")'''


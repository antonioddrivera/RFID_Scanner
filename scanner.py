import os
import requests
import pandas as pd
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

# Initialize the RFID reader
reader = SimpleMFRC522()

# Function to send an email with an image
def send_email_with_image(card_text, image_path):
    # Create an MIMEMultipart object
    msg = MIMEMultipart()
    msg['Subject'] = 'RFID Approved'
    msg['From'] = 'your_from_email@gmail.com'  # Change this to your desired "From" address
    msg['To'] = 'your_to_email@gmail.com'  # You can also change the "To" address if needed

    # Create plain text and HTML content for the email
    text = f"Hello,\nHere is a picture and ID of who scanned in.\nRFID Text: {card_text}"
    html = f"""\
    <html>
    <head>
    <p>Hello,<br>Here is a picture and ID of who scanned in.<br>RFID Text: {card_text}</p>
    <p><br></p>
    <p><b>Automated Email</b></p>
    </body>
    </html>
    """

    # Create MIMEText parts for both plain text and HTML
    part1 = MIMEText(text, 'plain')
    # part2 = MIMEText(html, 'html')

    # Attach the parts to the MIMEMultipart message
    msg.attach(part1)
    # msg.attach(part2)

    # Attach the captured image to the email
    with open(image_path, 'rb') as image_file:
        image = MIMEImage(image_file.read(), name='photo.jpg')
        msg.attach(image)

    # Send the email with the attached image
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("your_from_email@gmail.com", "your_app_specific_password")  # Use the app-specific password
        server.sendmail('your_from_email@gmail.com', 'your_to_email@gmail.com', msg.as_string())
    print("Message sent")

# Email to send when RFID tag is incorrect
def incorrect_send_email_with_image(card_text, image_path):
    # Create an MIMEMultipart object
    msg = MIMEMultipart()
    msg['Subject'] = 'RFID Rejected'
    msg['From'] = 'your_from_email@gmail.com'  # Change this to your desired "From" address
    msg['To'] = 'your_to_email@gmail.com'  # You can also change the "To" address if needed

    # Create plain text and HTML content for the email
    text = f"Hello,\nHere is a picture and ID of who scanned in.\nRejected RFID Text: {card_text}"
    html = f"""\
    <html>
    <head>
    <p>Hello,<br>Here is a picture and ID of who scanned in.<br>Rejected RFID Text: {card_text}</p>
    <p><br></p>
    <p><b>Automated Email</b></p>
    </body>
    </html>
    """

    # Create MIMEText parts for both plain text and HTML
    part1 = MIMEText(text, 'plain')
    # part2 = MIMEText(html, 'html')

    # Attach the parts to the MIMEMultipart message
    msg.attach(part1)
    # msg.attach(part2)

    # Attach the captured image to the email
    with open(image_path, 'rb') as image_file:
        image = MIMEImage(image_file.read(), name='photo.jpg')
        msg.attach(image)

    # Send the email with the attached image
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login("your_from_email@gmail.com", "your_app_specific_password")  # Use the app-specific password
        server.sendmail('your_from_email@gmail.com', 'your_to_email@gmail.com', msg.as_string())
    print("Message sent")

approved_id = [152035799932, 822695793]

try:
    print("Hold the tag near the reader")
    while True:
        card_id, card_text = reader.read()
        print("RFID Identification:", card_text)
        os.system("libcamera-still -n -o photo.jpg")
        image_path = 'photo.jpg'  # Set the desired image path
        approved = False
        for x in range(len(approved_id)):
            print(f"The current id in the list: {approved_id[x]}")
            if card_id == approved_id[x]:
                approved = True
                break
        if approved:
            send_email_with_image(card_text, image_path)
            print('RFID Accepted')
        else:
            incorrect_send_email_with_image(card_text, image_path)
            print('RFID Rejected')
        print("Rfid read wait 10 seconds")
        time.sleep(10)
        print("Hold tag near reader")

finally:
    GPIO.cleanup()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from model import RealEstateModel
import pandas as pd

class RealEstateController:
    def __init__(self, model, email_credentials):
        self.model = model
        self.email_credentials = email_credentials
        self.old_houses = self.read_existing_listings()

    def read_existing_listings(self):
        ''' Read the existing listings from a file '''
        try:
            with open('existing_listings.txt', 'r') as file:
                return set(line.strip() for line in file)
        except FileNotFoundError:
            return set()

    def update_existing_listings(self, new_listings):
        ''' Update the existing listings file with the new listings '''
        with open('existing_listings.txt', 'a') as file:
            for address in new_listings:
                file.write(f"{address}\n")

    def update_data(self):
        self.model.fetch_data()
        new_houses = self.model.get_new_houses(self.old_houses)
        if new_houses:
            self.send_email(new_houses)
            self.update_existing_listings([house['address'] for house in new_houses])
        else:
            print("No new houses found.")

    def send_email(self, new_houses):
        msg = MIMEMultipart()
        msg['From'] = self.email_credentials['from']
        msg['To'] = self.email_credentials['to']
        msg['Subject'] = 'New Houses Available'

        body = "The following new houses have been listed:\n\n"
        for house in new_houses:
            body += f"{house['address']}, {house['price']}, {house['url']}\n"
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.email_credentials['smtp_server'], self.email_credentials['smtp_port'])
        server.starttls()
        server.login(self.email_credentials['from'], self.email_credentials['password'])
        text = msg.as_string()
        server.sendmail(self.email_credentials['from'], self.email_credentials['to'], text)
        server.quit()

from controller import RealEstateController
from model import vdLindenModel, vbtModel
import yaml
import time
import sys

# Load the config.yaml file
config_path = 'config.yaml'  
secrets_path = 'secrets.yaml'  

# Extract URL and email from config
with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Extract the password from secrets.yaml
with open(secrets_path, 'r') as file:
    secrets = yaml.safe_load(file)

# Extract the URL and email credentials from the config and secrets
vdl_url = config['urls']['van der linden']
vbt_url = config['urls']['vb en t']

# Extract email credentials
email_credentials = {
    'from': config['email']['from'],
    'to': config['email']['to'],
    'smtp_server': config['email']['smtp_server'],
    'smtp_port': config['email']['smtp_port'],
    'password': secrets['email']['password'],
}

# Create the Model and run it every five minutes
try: 
    while True:
        # Update the data for Van der Linden
        vdl_houses = vdLindenModel(vdl_url)
        vdl_controller = RealEstateController(vdl_houses, email_credentials)
        vdl_controller.update_data()

        # Update the data for VB&T
        vbt_houses = vbtModel(vbt_url)
        vbt_controller = RealEstateController(vbt_houses, email_credentials)
        vbt_controller.update_data()

        # Wait for 5 minutes
        time.sleep(300)
except KeyboardInterrupt:
    print("Exiting the program...")


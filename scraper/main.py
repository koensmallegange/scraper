from controller import RealEstateController
from model import RealEstateModel
import yaml

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
url = config['url']
email_credentials = {
    'from': config['email']['from'],
    'to': config['email']['to'],
    'smtp_server': config['email']['smtp_server'],
    'smtp_port': config['email']['smtp_port'],
    'password': secrets['email']['password'],
}

# Create the Model
houses = RealEstateModel(url)
controller = RealEstateController(houses, email_credentials)
controller.update_data()

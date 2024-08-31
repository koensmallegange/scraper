from scraper.controller import RealEstateController
from scraper.model import vdLindenModel, vbtModel
import yaml
import time
import streamlit as st

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

# Extract general config
city = config['general']['city']
time_interval = config['general']['time_interval']

# Extract email credentials
email_credentials = {
    'from': config['email']['from'],
    'to': config['email']['to'],
    'smtp_server': config['email']['smtp_server'],
    'smtp_port': config['email']['smtp_port'],
    'password': secrets['email']['password'],
}

# Sidebar email config
st.sidebar.title('Email setup')
with st.sidebar.expander("Configure email settings", expanded=False):
    new_email_from = st.text_input('New From Email:', value=config['email']['from'])
    new_email_to = st.text_input('New To Email:', value=config['email']['to'])
    new_smtp_server = st.text_input('New SMTP Server:', value=config['email']['smtp_server'])
    new_smtp_port = st.number_input('New SMTP Port:', value=config['email']['smtp_port'], min_value=1, max_value=65535)
    new_email_password = st.text_input('New Email Password:', value=secrets['email']['password'], type='password')

    # Save button inside the expander
    if st.button('Save email settings'):
        # Update the config and secrets with new values
        config['email']['from'] = new_email_from
        config['email']['to'] = new_email_to
        config['email']['smtp_server'] = new_smtp_server
        config['email']['smtp_port'] = new_smtp_port
        secrets['email']['password'] = new_email_password

        # Save the updated config to the YAML files
        with open(config_path, 'w') as file:
            yaml.safe_dump(config, file)

        with open(secrets_path, 'w') as file:
            yaml.safe_dump(secrets, file)

        st.success('Settings updated successfully!')

# Sidebar scraper config
st.sidebar.title('Scraper setup')
with st.sidebar.expander("Configure scraper settings", expanded=False):
    city = st.text_input('City:', value=config['general']['city'])
    time_interval = st.number_input('Time interval (in seconds):', value=config['general']['time_interval'], min_value=1)
    vdl_url = st.text_input('Van der Linden URL:', value=config['urls']['van der linden'])
    vbt_url = st.text_input('VB&T URL:', value=config['urls']['vb en t'])

    if st.button('Save scraper settings'):
        # Update the config with the new URLs
        config['urls']['van der linden'] = vdl_url
        config['urls']['vb en t'] = vbt_url

        # Save the updated config to the YAML file
        with open(config_path, 'w') as file:
            yaml.safe_dump(config, file)

        st.success('Settings updated successfully!')

# Page title
st.title('Real Estate Scraper')
st.divider()

# display welcome message from docs/welcome.md
with open('docs/welcome.md', 'r') as file:
    welcome_message = file.read()
    st.markdown(welcome_message)

st.divider()

# Scraper status

st.header('Scraper status')

# Run the scraper
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

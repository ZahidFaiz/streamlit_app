# authenticate.py

import yaml
from yaml.loader import SafeLoader
import streamlit as st
import streamlit_authenticator as stauth

def check_password():
    hashed_passwords = stauth.Hasher(['123', '456']).generate()
    with open('credentials.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
        )

    name, authentication_status, username = authenticator.login(location = 'main')
    if authentication_status:
        authenticator.logout(location= 'sidebar')
        # st.write(f'Welcome *{name}*')
        # st.title('Some content')
        return authentication_status

    elif authentication_status == False:
        st.error('Username/password is incorrect')
        
    elif authentication_status == None:
        st.warning('Please enter your username and password')
        
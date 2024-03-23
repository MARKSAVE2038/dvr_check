import os
import sys
from dotenv import load_dotenv

from ip_discovery import find_public_ip, update_cache

import requests
import textwrap

from mailjet import Client, Recipient

# Take environment variables from .env.
load_dotenv()

class EndpointStatus:
    """ Valid endpoint statuses """
    
    OK = "Online"
    """ Endpoint is online. """

    KO = "Offline"
    """ Endpoint is offline. """

def main():
    # Get the public IP of the current router
    public_ip = find_public_ip()

    if not update_cache(public_ip):
        print("WARN: IP has not changed, retry later...")
        return True

    # Detect whether the camera service is online or not
    camera_url = f"http://{public_ip}:8081/"
    try:
        ictv_request = requests.get(camera_url, timeout=10)
        ictv_request.raise_for_status()

        endpoint_status = EndpointStatus.OK
    except:
        endpoint_status = EndpointStatus.KO



    # Check if required environment variables are set
    if None in [os.environ.get("MAILJET_API_KEY", None), os.environ.get("MAILJET_SECRET_KEY", None)]:
        print("ERROR: Make sure you have 'MAILJET_API_KEY' and 'MAILJET_SECRET_KEY' correctly set in your '.env' file.")
        return False
    
    

    # Build the email HTML body
    email_body = textwrap.dedent(f"""
        <h1>Il tuo indirizzo IP pubblico è {public_ip}</h1>

        <p>
            Puoi accedere ai tuoi servizi accedendo ai seguenti link:
            <ul>
                <li><a href="{camera_url}">Telecamera 1</a>: <span style="color: {"green" if endpoint_status == EndpointStatus.OK else "red"}">{endpoint_status}</span></li>
            </ul>
        </p>
    """)

    # Create a connection to the email SMTP server
    email_client = Client(
        os.getenv("MAILJET_API_KEY"),
        os.getenv("MAILJET_SECRET_KEY"),
    )

    # Send the email
    try:
        email_client.send(
            address_from=Recipient("marksave2038@gmail.com", "Automated email (Marco Salvarani)"),
            address_to=[
                Recipient("marksavefrogs@gmail.com", "Marco Salvarani"),
                Recipient("lucasalvarani99@gmail.com", "Luca Salvarani"),
            ],
            subject="[DVR] Notifica stato",
            body_html=email_body,
        )
    except Exception as e:
        print(f"ERROR: {e}")
        return False

    print("INFO: IP has changed, email was sent!")
    
if __name__ == '__main__':
    if not main():
        sys.exit(1)
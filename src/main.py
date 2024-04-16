import jwt
from datetime import datetime
import json
import msal
import yaml
from kombu import Queue, Connection, Consumer


def read_config(file_path):
    with open(file_path, "r") as stream:
        try:
            data = yaml.safe_load(stream)
            return data
        except yaml.YAMLError as exc:
            print(exc)


def print_token_details(token):
    # We don't care about verifying the token because we only want to print it
    options = {
        "verify_signature": False,  # Verify signature
        "verify_exp": False,  # Verify expiration
        "verify_nbf": False,  # Verify not before
        "verify_iat": False,  # Verify issued at (time token was issued)
        "verify_aud": False,  # Verify audience
        "verify_iss": False,  # Verify issuer
        "require_exp": False,  # expiration is required
        "require_iat": False,  # Issued at is optional
        "require_nbf": False,  # not before is optional
    }

    decoded_token = jwt.decode(access_token, options=options)

    print(f"Token expires @ {datetime.fromtimestamp(decoded_token['exp'])}")
    print(f"Decoded: {json.dumps(decoded_token, indent=4)}")
    print(
        "\nThe roles key in the above token describes the authorization rabbit uses.\n"
    )
    print(f"Token: {access_token}")


config = read_config("config.yaml")

with open(config["private_key_filename"], "rb") as private_key_file:
    # Credentials to get the token
    client_credential = {
        "thumbprint": config["fingerprint"],
        "private_key": private_key_file.read(),
        "passphrase": config.get("private_key_password", None),
    }

# Create the MSAL client
azure_client = msal.ConfidentialClientApplication(
    config["client_id"],
    authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
    client_credential=client_credential,
)

scopes = [f"api://{config['rabbit_server_id']}/.default"]

# Gets the token
result = azure_client.acquire_token_for_client(scopes)

# This is the token to use as password when calling RabbitMQ
access_token = result["access_token"]

print_token_details(access_token)


def process_message(body, message):
    print(f"Message: {body}")
    message.ack()

print(f'Consuming from {config["rabbit_server_url"]}:{config["rabbit_server_port"]} on virtual host {config["virtual_host"]}')
connection = Connection(
    hostname=config["rabbit_server_url"],
    virtual_host=config["virtual_host"],
    port=config["rabbit_server_port"],
    password=access_token,
    transport="amqps",
)
consumer = Consumer(
    connection,
    queues=Queue("test_external", no_declare=True),
    callbacks=[process_message],
)

consumer.consume()
# This will read one message from the queue. Wrap this call in a loop to read more messages.
connection.drain_events(timeout=1)

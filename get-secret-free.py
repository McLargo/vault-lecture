import hvac
import os

# Vault Configuration
VAULT_ADDR = "http://localhost:8200"
# Vault Configuration from Environment Variables
VAULT_ROLE_ID = os.environ.get("VAULT_ROLE_ID")
VAULT_SECRET_ID = os.environ.get("VAULT_SECRET_ID")

# Secret Path and Key to Retrieve
SECRET_PATH = "demo/API"
SECRET_KEY = "mysecret"


def init_client(role_id: str, secret_id:str) -> hvac.Client | None:
    try:
        client = hvac.Client(url=VAULT_ADDR)

        login_response = client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id
        )

        client.token = login_response["auth"]["client_token"]

        print(f"Successfully authenticated to Vault at {VAULT_ADDR}")
        return client

    except hvac.exceptions.InvalidRequest as e:
        print("Error during authentication. Check your VAULT_ROLE_ID and VAULT_SECRET_ID values.")
        print(f"Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def get_secret(client, path, key):
    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path=path.split("/")[-1],
            mount_point=path.split("/")[0],
            raise_on_deleted_version=False,
        )

        secret_value = read_response["data"]["data"][key]

        print(f"Retrieved value for {key}: {secret_value}")

    except hvac.exceptions.Forbidden as e:
        print("Access denied when retrieving secret. Check your client's permissions.")
        print(f"Details: {e}")
    except hvac.exceptions.InvalidRequest as e:
        print(f"Error retrieving secret. Ensure the path ({SECRET_PATH}) and key ({SECRET_KEY}) are correct.")
        print(f"Details: {e}")


if __name__ == "__main__":
    if not VAULT_ROLE_ID or not VAULT_SECRET_ID:
        print("Please set the VAULT_ROLE_ID and VAULT_SECRET_ID environment variables.")
        exit(1)

    client = init_client(VAULT_ROLE_ID, VAULT_SECRET_ID)
    if client:
        get_secret(client, SECRET_PATH, SECRET_KEY)

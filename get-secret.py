import hvac

# Vault Configuration
VAULT_ADDR = "http://localhost:8200"
VAULT_TOKEN = "myroot"

# Secret Path and Key to Retrieve
SECRET_PATH = "demo/API"
SECRET_KEY = "mysecret"


def init_client() -> hvac.Client | None:
    try:
        client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)

        if not client.is_authenticated():
            print("Vault client is not authenticated. Check `VAULT_TOKEN` value.")
            return None

        print(f"Successfully authenticated to Vault at {VAULT_ADDR}")
        return client

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def get_secret(client, path, key):
    try:
        read_response = client.secrets.kv.v2.read_secret_version(
            path=path.split("/")[-1],
            mount_point=path.split("/")[0],
            raise_on_deleted_version=False,
        )

        secret_value = read_response["data"]["data"][key]

        print(f"Retrieved value for {key}: {secret_value}")

    except hvac.exceptions.InvalidRequest as e:
        print(f"Error retrieving secret. Ensure the path ({SECRET_PATH}) and key ({SECRET_KEY}) are correct.")
        print(f"Details: {e}")


if __name__ == "__main__":
    client = init_client()
    if client:
        get_secret(client, SECRET_PATH, SECRET_KEY)

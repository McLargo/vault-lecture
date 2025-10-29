import hvac
import os


VAULT_ADDR = "http://localhost:8200"
# Vault Configuration from Environment Variables
VAULT_ROLE_ID = os.environ.get("VAULT_ROLE_ID")
VAULT_SECRET_ID = os.environ.get("VAULT_SECRET_ID")


def renew_token(role_id: str, secret_id: str) -> None:
    try:
        client = hvac.Client(url=VAULT_ADDR)

        login_response = client.auth.approle.login(
            role_id=role_id,
            secret_id=secret_id
        )

        client.token = login_response["auth"]["client_token"]

        print(f"Successfully authenticated to Vault at {VAULT_ADDR}")

        # renew token before it expires
        client.token = login_response['auth']['client_token']
        renewal_response = client.auth.token.renew_self()

        new_ttl = renewal_response['lease_duration']
        print(f"Token renewed successfully. New TTL: {new_ttl} seconds.")

    except hvac.exceptions.InvalidRequest as e:
        print("Error during authentication. Check your VAULT_ROLE_ID and VAULT_SECRET_ID values.")
        print(f"Details: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    if not VAULT_ROLE_ID or not VAULT_SECRET_ID:
        print("Please set the VAULT_ROLE_ID and VAULT_SECRET_ID environment variables.")
        exit(1)

    renew_token(VAULT_ROLE_ID, VAULT_SECRET_ID)

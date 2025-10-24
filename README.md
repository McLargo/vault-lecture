# Vault lecture

Security is a key aspect to consider in any application. Usually, as you develop
any application, you can find there is sensitive information to use (secret)
which cannot be exposed to the public (ej. API keys, database credentials, etc).
Any leak of this information can have serious consequences.

[Vault](https://github.com/hashicorp/vault) is a tool to securely store your
secrets. It provides an interface to store and access secrets, with access
control and audit log. It is written in Go and open source.

## Key features

- Data encryption out of the box. It happens before writing to persistent
  storage, so access to raw storage isn't enough to access your secrets.
- Leasing and renewal mechanism for secrets.
- OIDC and LDAP authentication methods.

## Installation

> To make things easier, we will use [Taskfile](https://taskfile.dev/) to manage
> our commands. You can install it following the
[instructions](https://taskfile.dev/#/installation). If you prefer not to use it,
> you can check [Taskfile.yaml](Taskfile.yaml) file and run the commands
> directly in your terminal.

Vault can be installed
[natively on your linux](https://developer.hashicorp.com/vault/docs/deploy/run-as-service),
or you can use Docker. In this lecture we will use
[Docker](https://docs.docker.com/engine/install/).

To run the Vault server in development mode, just Run the following command:

```bash
task server
```

After a few seconds, you should have a Vault server running on
[http://localhost:8200](http://localhost:8200) where you can access the UI.

## Configuration/Navigation

From the UI, you can now start configuring your Vault server (keep in mind that
UI is not the only way to interact with Vault, you can also use the CLI or API).
But for the shake of simplicity, we will use the UI.

### Secret Engines

Secret Engines are components that store, generate, or encrypt data. There are
multiple engines available, such as Key/Value, Database, AWS, Consul, etc.
Select the one that best fits your use case.

After you create your engine, you can start adding secrets to it.

### Authentication Methods

In our initial configuration, we are using Token authentication method, which is
the simplest one. But you can configure other methods such as OIDC, LDAP, github
username/password...

### ACL Policies

ACL Policies are used to define access control for your secrets. You can create
policies that allow or deny access to specific paths in your Vault server, and
assign them to users or groups.

## Usage

### Cli

You can also interact with Vault using the CLI. In our docker compose,
everything is configured to start using the `vault` cli command from inside the
container. YOu can open a shell inside the container using:

```bash
task cli
```

Then, you can use the `vault` command to interact with the server. To confirm is
working, you can run:

```bash
vault status
```

There are multiple commands available, you can do most of the operations you can
do from the UI. Run `vault --help` to see the available commands.

### API

Perhaps you now want to access secrets from your application. Vault offers an
HTTP API to interact with the server. You can use any HTTP client to make
requests to the server.

Also, there are multiple client libraries available for different programming
languages, such as:

- [Python](https://github.com/hvac/hvac)
- [Golang](https://github.com/hashicorp/vault-client-go)

In this lecture, we will use the Python client library `hvac` to interact with
the Vault server. See the [get-secret.py](get-secret.py) file for an example of
how to use the library to retrieve secrets from the Vault.

To run the example, execute:

```bash
task get-secret-python
```

> NOTE: This command will install any poetry dependencies and run the
> `get-secret.py` file.

## How to implement your app Secret-free

As we have been discussing, the best practice for your application is to not store any secret in its code or
configuration files. Instead, it should retrieve secrets from Vault at runtime,
where your app is agnostic to how authentication and secret management is done.

In the previous example, we used a root token to access the secrets. This is not
a good practice, as the root token has full access to the Vault server. Instead,
we should use a more restrictive token with limited permissions. We need to
achieve two main goals:

- Secrets to authenticate are dynamic, rotated periodically and injected at
  runtime from outside the application.
- Fine-grained access control to secrets.

By following the next steps, you can ensure that your application is secure and
that secrets are managed properly:

1. **Authenticate your application**: Use an authentication method supported by
   Vault (ej. AppRole, Kubernetes, etc) to authenticate your application and
   retrieve a token.
2. **Retrieve secrets**: Use the token to access the secrets stored in Vault.
3. **Use secrets**: Use the retrieved secrets in your application as needed.
4. **Rotate secrets**: Periodically rotate your secrets in Vault and update your
   application to use the new secrets.

Ideally, using K8s will be the best option to deploy your application, as it has
native support for Vault integration using the
[Vault Agent](https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent). But in order to keep things simple, let's use a `AppRole` authentication method.

### AppRole authentication method

What we need to do is:

- Add the AppRole authentication method to our Vault server.
- Add new policies to access the secrets.
- Create a new role with the policies assigned.
- Retrieve the Role ID and Secret ID for the role created.

You can create everything using the UI, but here are the steps to do it using
the CLI:

1. If not exist, create AppRole as Authentication method in Vault.

```bash
docker exec vault-consul vault auth enable approle
```

2. Create a policy that allows access to the secrets.

```bash
docker exec vault-consul sh -c 'vault policy write <policy-name> - <<EOF
path "demo/data/API" {
  capabilities = ["read", "list"]
}
EOF'
```

Where `<policy-name>` is the name of the policy you want to create.

3. Create a new role inside `approle` with the policy recently created.

```bash
docker exec vault-consul vault write auth/approle/role/<role-name> \
    token_policies="<policy-name>" \
    secret_id_num_uses=10 \
    token_ttl=1h
```

Where `<role-name>` is the name of the role you want to create, and
`<policy-name>` is the name of the policy you created in step 2. Also, you can
configure other parameters such as `secret_id_num_uses` and `token_ttl`
according to your needs. This configuration defines how many times the secret ID
can be used and the time-to-live of the token generated.

4. Create a secret ID for the role and export into a environment variable, that
   will be use for your application.

```bash
export VAULT_SECRET_ID=$(docker exec vault-consul vault write -f -format=json auth/approle/role/<role-name>/secret-id | jq -r '.data.secret_id')
```

Where `<role-name>` is the name of the role you created in step 3.

5. Retrieve the Role ID for the role. Export it into a environment variable,
   that will be use for your application.

```bash
export VAULT_ROLE_ID=$(docker exec vault-consul vault read -format=json auth/approle/role/<role-name>/role-id | jq -r '.data.role_id')
```

Now you have everything you need to authenticate your application using AppRole.
See the [get-secret-free.py](get-secret-free.py) file for an example of how to
use the AppRole authentication method to retrieve secrets from Vault. To run the
example, execute:

```bash
task get-secret-free-python
```

Following this steps, you can ensure that your application does not store any
secret, have access only to the secrets it needs and retrieves them securely
from Vault at runtime. Any potential secret leak from the application code or
configuration files is avoided.

## Persistence storage

So far, this lecture uses the development mode of Vault, which is not suitable
for production. In development mode, all data is stored in memory and will be
lost when the server is stopped.

For production, you should configure a persistent storage backend, such as
Consul, PostgreSQL, MySQL, etc. See the
[official documentation](https://developer.hashicorp.com/vault/docs/configuration/storage).
In our lecture, we will configure Consul as the persistence storage. Consul is a
tool (developed by the same company as Vault) that provides a distributed
key-value store, service discovery, and health checking. It uses a volume to
store your store secrets in a persistent storage (docker volumen in our
example). You can stop the server and start it again, and your secrets will
persist.

By default, when Vault uses Consul, it will be sealed. This means, every time we
start the vault server, we need to unseal it using the unseal keys provided
during the initialization. To initialize Vault with Consul as the storage
backend, you can use execute the following command:

```bash
task init-consul
```

> NOTE: Unseal is configured with only one key for simplicity. In production,
> you should use multiple keys and a threshold to unseal the vault.

After successful unsealing, you can access the Vault server using the UI and
root token provided during initialization. Keep in mind that unseal keys/token
cannot be generated again, so store it securely.

To confirm everything is working, let's add some secret. Then, let's stop and
start the Consul-based Vault server using:

```bash
task stop-start-consul
task start-consul
```

## References

- [Vault official documentation](https://developer.hashicorp.com/vault/docs)
- [Vault CLI](https://developer.hashicorp.com/vault/docs/commands)

# Vault lecture

Security is a key aspect to consider in any application. Usually, as you develop
any application, you can find there is sensitive information to use (secret)
which cannot be exposed to the public (ej. API keys, database credentials, etc).

[Vault](https://github.com/hashicorp/vault) is a tool to securely store your
secrets. It provides an interface to store and access secrets, with access
control and audit log. It is written in Go and open source.

## Key features

- Data encryption out of the box. It happens before writing to persistent
  storage, so access to raw storage isn't enough to access your secrets.
- Leasing and renewal mechanism for secrets.
- OIDC and LDAP authentication methods.

## Installation

Vault can be installed
[natively on your linux](https://developer.hashicorp.com/vault/docs/deploy/run-as-service),
or you can use Docker. In this lecture we will use Docker.

To run the Vault server, you can use the provided `Taskfile.yaml` to start the
server in development mode. Run the following command:

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

In our configuration, we used Token authentication method, which is the simplest
one. But you can configure other methods such as OIDC, LDAP, github
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
the Vault server. See the [main.py](main.py) file for an example of how to use
the library to retrieve secrets from the Vault.

To run the example, execute:

```bash
task get_secret_python
```

> NOTE: This command will install any poetry dependencies and run the `main.py`
> file.

## Persistence storage

<!-- TODO -->

## How to implement your app Secret-free

<!-- TODO -->

## References

- [Vault official documentation](https://developer.hashicorp.com/vault/docs)
- [Vault CLI](https://developer.hashicorp.com/vault/docs/commands)

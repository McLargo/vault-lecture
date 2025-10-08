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
[http://localhost:8200](http://localhost:8200).

## Configuration/Navigation

<!-- TODO -->

## Usage

<!-- TODO CLI ? -->
<!-- TODO APP (fastapi vs go) -->

## Persistence storage

<!-- TODO -->

## How to implement your app Secret-free

<!-- TODO -->

## References

- [Vault official documentation](https://developer.hashicorp.com/vault/docs)

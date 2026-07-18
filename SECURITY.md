# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | Yes |

## Reporting a Vulnerability

If you discover a security vulnerability in `azure-mcp-platform`, please **do not** open a public GitHub issue.

Instead, report it privately by emailing: **challaakkireddy@gmail.com**

Please include:
- A description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested mitigations

We aim to respond within **48 hours** and will work with you to understand and resolve the issue before any public disclosure.

## Security Design Principles

This project is designed with security-first principles:

1. **Read-only by default** — All tools only read Azure resources; no write operations are exposed.
2. **Credential isolation** — Uses `DefaultAzureCredential` (Managed Identity, env vars, or Azure CLI). No hardcoded credentials.
3. **Least privilege** — Service principals require only `Reader` role at subscription scope.
4. **No secret values exposed** — `get_key_vault_secrets` returns only secret *names*, never values.
5. **No PII leakage** — Tool responses are scoped to resource metadata, not data-plane content.
6. **Environment variable configuration** — All sensitive config is passed via env vars, never committed to code.

## Threat Model

| Threat | Mitigation |
|---|---|
| Credential leakage via logs | Tool responses never log raw credentials |
| Over-privileged service principal | Reader-only RBAC enforced |
| Secret value exposure | Key Vault tool returns names only |
| MCP prompt injection | Tool inputs are validated; no shell execution |
| Supply chain attack | Pin dependencies; run `pip audit` in CI |

## Responsible Disclosure

We follow [coordinated vulnerability disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure). Security fixes will be released as patch versions with a corresponding advisory.

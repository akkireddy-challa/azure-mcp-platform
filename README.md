# azure-mcp-platform

> MCP server for Azure resource management, AI Foundry, and Entra ID — inspect and operate Azure infrastructure through AI agents.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Azure](https://img.shields.io/badge/Azure-MCP-0078D4.svg)](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/)
[![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is this?

`azure-mcp-platform` wraps the [official Azure MCP Server](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/) with production-ready configuration, Entra ID authentication, and platform-engineering patterns for operating Azure environments safely from AI agents.

Built for platform engineers running multi-tenant Azure environments with AI Foundry, AKS, and enterprise SSO via Entra ID.

---

## Available Tools

| Tool | Description |
|---|---|
| `list_resource_groups` | List all resource groups in a subscription |
| `list_resources` | List resources in a resource group by type |
| `get_resource` | Get details of a specific Azure resource |
| `list_ai_foundry_projects` | List Azure AI Foundry projects and deployments |
| `get_aks_cluster` | Get AKS cluster status and node pool health |
| `list_entra_users` | List Entra ID users and group memberships (read-only) |
| `get_key_vault_secrets` | List secret names (not values) in Key Vault |
| `list_storage_accounts` | List storage accounts and their access tiers |

---

## Quick Start

### Prerequisites

- Python 3.11+
- Azure CLI authenticated: `az login`
- Appropriate Azure RBAC role: `Reader` minimum
- (Optional) Service principal with `Reader` + `AcrPull` for CI environments

### Run locally

```bash
git clone https://github.com/akkireddy-challa/azure-mcp-platform.git
cd azure-mcp-platform
pip install -r requirements.txt
az login
python server.py
```

### Configure with Claude Desktop

```json
{
  "mcpServers": {
    "azure": {
      "command": "python",
      "args": ["/path/to/azure-mcp-platform/server.py"],
      "env": {
        "AZURE_SUBSCRIPTION_ID": "your-subscription-id",
        "AZURE_TENANT_ID": "your-tenant-id"
      }
    }
  }
}
```

---

## Example Usage

Ask your AI agent:

- *"List all resource groups in my subscription"*
- *"What AKS clusters are running in the production resource group?"*
- *"Show me all AI Foundry projects and their model deployments"*
- *"Which storage accounts in rg-data have public access enabled?"*
- *"List all users in the platform-engineers Entra group"*

---

## Security Model

- **Read-only by default**: all tools use `GET` operations only
- **Entra ID SSO**: authenticates via Azure CLI credential chain or Managed Identity
- **No secrets exposed**: Key Vault tool lists secret names only, never values
- **Subscription-scoped**: tools operate within a single configured subscription
- **Recommended role**: `Reader` at subscription scope for full read access

```bash
# Assign Reader role to a service principal
az role assignment create \
  --assignee <service-principal-id> \
  --role Reader \
  --scope /subscriptions/<subscription-id>
```

---

## Use Cases at Telia

This pattern is used to allow AI agents to:

- Audit resource configurations across multi-tenant Azure environments
- Cross-reference AKS cluster state with AI Foundry model deployments
- Investigate Entra ID group membership for access reviews
- Inspect cost anomalies by listing resources and their SKUs

---

## Roadmap

- [ ] `get_cost_analysis` — query Azure Cost Management for spend by resource group
- [ ] `list_policy_assignments` — show Azure Policy compliance state
- [ ] `get_monitor_alerts` — list active Azure Monitor alerts
- [ ] `list_app_registrations` — Entra ID app registrations and permissions
- [ ] Managed Identity support for AKS pod deployment
- [ ] GitHub Actions workflow for CI validation

---

## Related Projects

| Repo | Purpose |
|---|---|
| [k8s-mcp-server](https://github.com/akkireddy-challa/k8s-mcp-server) | Kubernetes cluster diagnostics via MCP |
| [grafana-mcp-observability](https://github.com/akkireddy-challa/grafana-mcp-observability) | Grafana dashboards and alerts via MCP |
| [phoenix-mcp-eval](https://github.com/akkireddy-challa/phoenix-mcp-eval) | LLM tracing and evaluation via MCP |

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

Built by [Akkireddy Challa](https://github.com/akkireddy-challa) — Platform Engineer at Telia, Stockholm.

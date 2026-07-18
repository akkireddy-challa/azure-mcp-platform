"""azure-mcp-platform: MCP server for Azure resource management.

Exposes Azure resource groups, resources, AKS, AI Foundry, Key Vault,
Entra ID, and storage via the Model Context Protocol (MCP).

Author: Akkireddy Challa
License: MIT
"""

import os
import asyncio
from typing import Any

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.ai.ml import MLClient

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SUBSCRIPTION_ID = os.environ.get("AZURE_SUBSCRIPTION_ID", "")
TENANT_ID = os.environ.get("AZURE_TENANT_ID", "")

credential = DefaultAzureCredential()

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
server = Server("azure-mcp-platform")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="list_resource_groups",
            description="List all resource groups in the Azure subscription.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="list_resources",
            description="List resources in a resource group, optionally filtered by type.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_group": {"type": "string", "description": "Resource group name"},
                    "resource_type": {"type": "string", "description": "Optional Azure resource type filter"},
                },
                "required": ["resource_group"],
            },
        ),
        Tool(
            name="get_resource",
            description="Get details of a specific Azure resource.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_id": {"type": "string", "description": "Full Azure resource ID"},
                },
                "required": ["resource_id"],
            },
        ),
        Tool(
            name="get_aks_cluster",
            description="Get AKS cluster status, node pools, and Kubernetes version.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_group": {"type": "string"},
                    "cluster_name": {"type": "string"},
                },
                "required": ["resource_group", "cluster_name"],
            },
        ),
        Tool(
            name="list_ai_foundry_projects",
            description="List Azure AI Foundry (ML) workspaces and deployments.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_group": {"type": "string"},
                },
                "required": ["resource_group"],
            },
        ),
        Tool(
            name="get_key_vault_secrets",
            description="List secret names (not values) in an Azure Key Vault.",
            inputSchema={
                "type": "object",
                "properties": {
                    "vault_name": {"type": "string"},
                    "resource_group": {"type": "string"},
                },
                "required": ["vault_name", "resource_group"],
            },
        ),
        Tool(
            name="list_storage_accounts",
            description="List storage accounts and their access tiers in a resource group.",
            inputSchema={
                "type": "object",
                "properties": {
                    "resource_group": {"type": "string"},
                },
                "required": ["resource_group"],
            },
        ),
        Tool(
            name="list_entra_users",
            description="List Entra ID users and group memberships (read-only).",
            inputSchema={
                "type": "object",
                "properties": {
                    "group_id": {"type": "string", "description": "Entra group object ID (optional)"},
                },
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Route MCP tool calls to Azure SDK implementations."""

    if name == "list_resource_groups":
        client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
        groups = [rg.name for rg in client.resource_groups.list()]
        return [TextContent(type="text", text="\n".join(groups) or "No resource groups found.")]

    elif name == "list_resources":
        rg = arguments["resource_group"]
        rtype = arguments.get("resource_type")
        client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
        filter_str = f"resourceType eq '{rtype}'" if rtype else None
        resources = client.resources.list_by_resource_group(rg, filter=filter_str)
        lines = [f"{r.name} ({r.type})" for r in resources]
        return [TextContent(type="text", text="\n".join(lines) or "No resources found.")]

    elif name == "get_resource":
        resource_id = arguments["resource_id"]
        client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
        resource = client.resources.get_by_id(resource_id, api_version="2022-09-01")
        return [TextContent(type="text", text=str(resource.as_dict()))]

    elif name == "get_aks_cluster":
        client = ContainerServiceClient(credential, SUBSCRIPTION_ID)
        cluster = client.managed_clusters.get(arguments["resource_group"], arguments["cluster_name"])
        info = {
            "name": cluster.name,
            "location": cluster.location,
            "kubernetes_version": cluster.kubernetes_version,
            "provisioning_state": cluster.provisioning_state,
            "node_pools": [
                {"name": np.name, "count": np.count, "vm_size": np.vm_size}
                for np in cluster.agent_pool_profiles or []
            ],
        }
        return [TextContent(type="text", text=str(info))]

    elif name == "list_ai_foundry_projects":
        client = MLClient(credential, SUBSCRIPTION_ID, arguments["resource_group"])
        workspaces = [ws.name for ws in client.workspaces.list()]
        return [TextContent(type="text", text="\n".join(workspaces) or "No AI Foundry workspaces found.")]

    elif name == "get_key_vault_secrets":
        from azure.keyvault.secrets import SecretClient
        vault_url = f"https://{arguments['vault_name']}.vault.azure.net"
        secret_client = SecretClient(vault_url=vault_url, credential=credential)
        secrets = [s.name for s in secret_client.list_properties_of_secrets()]
        return [TextContent(type="text", text="\n".join(secrets) or "No secrets found (names only).")]

    elif name == "list_storage_accounts":
        client = StorageManagementClient(credential, SUBSCRIPTION_ID)
        accounts = client.storage_accounts.list_by_resource_group(arguments["resource_group"])
        lines = [f"{a.name} - tier: {a.access_tier}, sku: {a.sku.name}" for a in accounts]
        return [TextContent(type="text", text="\n".join(lines) or "No storage accounts found.")]

    elif name == "list_entra_users":
        # Requires Microsoft Graph API - placeholder for Graph SDK integration
        return [TextContent(type="text", text="Entra ID integration requires Microsoft Graph SDK. See README for setup.")]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
async def main():
    if not SUBSCRIPTION_ID:
        raise ValueError("AZURE_SUBSCRIPTION_ID environment variable is required.")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="azure-mcp-platform",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())

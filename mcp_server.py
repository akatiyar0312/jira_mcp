import os
import requests
from mcp.server.fastmcp import FastMCP
import asyncio

# ------------------------
# Create MCP server instance
# ------------------------
mcp = FastMCP(
    "jira_confluence_mcp",
    log_level="INFO"
)

# ------------------------
# Jira Tools
# ------------------------
JIRA_URL = os.getenv("JIRA_URL", "https://paymentsconfluence.atlassian.net")
JIRA_EMAIL = os.getenv("JIRA_EMAIL","aditikatiyar@gmail.com")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN","ATATT3xFfGF07x73BvuLVZxsj0keHMuIybrTQyKetvRJZIOE-C7U_OtnRv5rxQr5cUAIz1bae1GdNmX_cRhRuds9x4OxtE0ipukCHxtM_VV4GCmq6qhWpei-v3YchHHuLaUhEPBojaHFoRyB_gOnd2e3BxuzWmwBNLAUaXksl7q8-20M1CM3QQ4=45BEEC7C")

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL", "https://paymentsconfluence.atlassian.net/wiki")
CONFLUENCE_EMAIL = os.getenv("CONFLUENCE_EMAIL")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

jira_headers = {"Accept": "application/json"}
jira_auth = (JIRA_EMAIL, JIRA_API_TOKEN)

confluence_headers = {"Accept": "application/json"}
confluence_auth = (CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)

@mcp.tool()
def get_issue(issue_key: str):
    """Fetch a Jira issue by key"""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    print(f"[DEBUG] GET {url}")
    response = requests.get(url, headers=jira_headers, auth=jira_auth)
    print(f"[DEBUG] Status: {response.status_code}")
    response.raise_for_status()
    return response.json()

@mcp.tool()
def search_issues(jql: str, max_results: int = 5):
    """Search Jira issues using JQL"""
    url = f"{JIRA_URL}/rest/api/3/search"
    params = {"jql": jql, "maxResults": max_results}
    print(f"[DEBUG] GET {url} with {params}")
    response = requests.get(url, headers=jira_headers, params=params, auth=jira_auth)
    print(f"[DEBUG] Status: {response.status_code}")
    response.raise_for_status()
    return response.json()

# ------------------------
# Confluence Tools
# ------------------------
@mcp.tool()
def search_pages(query: str, limit: int = 5):
    """Search Confluence pages by query"""
    url = f"{CONFLUENCE_URL}/rest/api/content/search"
    params = {"cql": f'text ~ "{query}"', "limit": limit}
    print(f"[DEBUG] GET {url} with {params}")
    response = requests.get(url, headers=confluence_headers, params=params, auth=confluence_auth)
    print(f"[DEBUG] Status: {response.status_code}")
    response.raise_for_status()
    return response.json()

# ------------------------
# Health check + greet
# ------------------------
@mcp.tool()
def health():
    return {"status": "ok"}

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

# ------------------------
# Start MCP server on HTTP
# ------------------------
async def main():
    print("🚀 Starting Jira + Confluence MCP server on HTTP (port 8088)...")
    await mcp.run_streamable_http_async()

if __name__ == "__main__":
    asyncio.run(main())
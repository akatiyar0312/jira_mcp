import os
import requests
from mcp.server.fastmcp import FastMCP
import asyncio

# ------------------------
# Load required environment variables (fail fast if missing)
# ------------------------
JIRA_URL = os.environ.get("JIRA_URL", "https://paymentsconfluence.atlassian.net")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

#CONFLUENCE_URL = os.environ.get("CONFLUENCE_URL", "https://paymentsconfluence.atlassian.net/wiki")
#CONFLUENCE_EMAIL = os.environ.get("CONFLUENCE_EMAIL")
#CONFLUENCE_API_TOKEN = os.environ.get("CONFLUENCE_API_TOKEN")

# Check required variables and raise errors if not set
if not JIRA_EMAIL or not JIRA_API_TOKEN:
    raise EnvironmentError("JIRA_EMAIL and JIRA_API_TOKEN must be set in environment variables.")

#if not CONFLUENCE_EMAIL or not CONFLUENCE_API_TOKEN:
#    raise EnvironmentError("CONFLUENCE_EMAIL and CONFLUENCE_API_TOKEN must be set in environment variables.")

# ------------------------
# Create MCP server instance
# ------------------------
mcp = FastMCP(
    "jira_confluence_mcp",
    host="0.0.0.0",   # 👈 allow external HTTP access
    port=8088,
    stateless_http="true",
    log_level="INFO"
)

jira_headers = {"Accept": "application/json"}
jira_auth = (JIRA_EMAIL, JIRA_API_TOKEN)

confluence_headers = {"Accept": "application/json"}
#confluence_auth = (CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)


# ------------------------
# Helper function for safe API calls
# ------------------------
def safe_get(url, headers, auth, params=None):
    try:
        response = requests.get(url, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] GET request to {url} failed: {e}")
        return {"error": str(e)}

def safe_post(url, headers, auth, json_payload):
    try:
        response = requests.post(url, headers=headers, auth=auth, json=json_payload)
        if response.status_code != 201:
            print(f"[ERROR] POST {url} failed: {response.status_code} - {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] POST request to {url} failed: {e}")
        return {"error": str(e)}


# ------------------------
# Jira Tools
# ------------------------
@mcp.tool()
def get_issue(issue_key: str):
    """Fetch a Jira issue by key"""
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}"
    print(f"[DEBUG] GET {url}")
    return safe_get(url, jira_headers, jira_auth)



@mcp.tool()
def search_issues(jql: str, max_results: int = 5):
    """Search Jira issues using JQL"""
    url = f"{JIRA_URL}/rest/api/3/search"
    params = {"jql": jql, "maxResults": max_results}
    print(f"[DEBUG] GET {url} with {params}")
    return safe_get(url, jira_headers, jira_auth, params=params)



# ------------------------
# Health check + greet
# ------------------------
@mcp.tool()
def health():
    return {"status": "ok"}


@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.tool()
def create_issue(project_key: str, summary: str, description: dict, issue_type: str = "Task"):
    """Create a new Jira issue (with ADF description support)"""
    url = f"{JIRA_URL}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": description,   # 👈 send dict directly
            "issuetype": {"name": issue_type}
        }
    }

    print(f"[DEBUG] POST {url} with {payload}")
    return safe_post(
        url,
        headers={**jira_headers, "Content-Type": "application/json"},
        auth=jira_auth,
        json_payload=payload
    )


# ------------------------
# Start MCP server on HTTP
# ------------------------
async def main():
    print("🚀 Starting Jira + Confluence MCP server on HTTP (port 8088)...")
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())

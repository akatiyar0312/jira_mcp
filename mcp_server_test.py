import asyncio
from fastmcp import Client
from mcp_server import mcp   # ✅ import server instance

client = Client(mcp)

# -----------------------------
# Get issue by key
# -----------------------------
async def test_get_issue():
    async with client:
        result = await client.call_tool("get_issue", {"issue_key": "TEST-1"})
        print("✅ get_issue result:", result)



# -----------------------------
# Create issue in Jira
# -----------------------------
async def test_create_issue():
    adf_description = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "This issue was created via MCP API using ADF format."}
                ]
            }
        ]
    }

    async with client:
        result = await client.call_tool("create_issue", {
            "project_key": "TEST",
            "summary": "Test issue from MCP",
            "description": adf_description,   # ✅ pass dict, not string
            "issue_type": "Task"
        })
        print("✅ create_issue result:", result)
# -----------------------------
# Main runner
# -----------------------------
async def main():
    await test_get_issue()
    await test_create_issue()


if __name__ == "__main__":
    asyncio.run(main())

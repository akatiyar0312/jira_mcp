import asyncio
from fastmcp import Client
from mcp_server import mcp   # ✅ import server instance

client = Client(mcp)

async def test_greet():
    async with client:
        result = await client.call_tool("greet", {"name": "Ford"})
        print("✅ greet result:", result)

async def test_get_issue():
    async with client:
        # Replace TEST-123 with a real Jira issue key
        result = await client.call_tool("get_issue", {"issue_key": "TEST-1"})
        print("✅ get_issue result:", result)

async def main():
    await test_greet()
    await test_get_issue()

if __name__ == "__main__":
    asyncio.run(main())

import mcp.types
from fastmcp.client import Client
import asyncio

mcp_server_url = "http://localhost:8000/app"
async def get_mcp_tools() -> list[mcp.types.Tool]:
    """
    Returns a list of tools available in the MCP server.
    """
    mcp_client = Client(mcp_server_url)
    async with mcp_client:
        tools_list = await mcp_client.list_tools()
        return tools_list
    
async def main():
    tools_list = await get_mcp_tools()
    if tools_list:
        print(f"Available tools: \n {tools_list}")
    else:
        print("No tools found in the MCP server.")

if __name__ == "__main__":
    asyncio.run(main())

from fastmcp import Client
from typing import List
import requests
import asyncio
from mcp.types import Tool as McpTool
from langchain.tools import StructuredTool as LCTool
from pydantic import create_model, Field
from utils.agent_config import DEBUG_APP as dbg

def json_schema_to_pydantic_model(name, schema):
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    fields = {}
    type_map = {
        "integer": int,
        "number": float,
        "string": str,
        "boolean": bool,
    }
    for prop, prop_schema in properties.items():
        typ = type_map.get(prop_schema.get("type"), str)
        default = ... if prop in required else None
        field_args = {"title": prop_schema.get("title", prop)}
        fields[prop] = (typ, Field(default, **field_args))
    return create_model(name, **fields)

class APP_MCPTools:
    def __init__(self, mcp_servers: List[str]):
        self.mcp_servers = mcp_servers
        self.mcp_to_langchain_tools: list[LCTool] = []

    @classmethod
    async def create(cls, mcp_servers: List[str]):
        self = cls(mcp_servers)
        await self.initialize_tools()
        return self

    async def initialize_tools(self):
        for server in self.mcp_servers:
            try:
                dbg.info(f"Fetching tools from MCP server: {server}")
                mcp_tools = await self.get_tools_from_mcp_server(server)
                for tool in mcp_tools:
                    # dbg.info(f"MCP Tool = {tool}")
                    lc_tool = self.mcp_tool_to_langchain_tool(tool, server)
                    self.mcp_to_langchain_tools.append(lc_tool)
            except requests.exceptions.RequestException as e:
                dbg.error(f"Error fetching tools from {server}: {e}")

    @property
    def tools(self):
        return self.mcp_to_langchain_tools

    def __iter__(self):
        return iter(self.mcp_to_langchain_tools)

    def __len__(self):
        return len(self.mcp_to_langchain_tools)

    async def execute_remote_tool(self, tool_name: str, mcp_server_url: str, kwargs):
        client = Client(mcp_server_url)
        async with client:
            result = await client.call_tool(tool_name, kwargs)
        return result

    def mcp_tool_to_langchain_tool(self, tool: McpTool, mcp_server: str) -> LCTool:
        ArgsSchema = json_schema_to_pydantic_model(f"{tool.name}_InputSchema", tool.inputSchema)

        async def tool_func(**kwargs):
            return await self.execute_remote_tool(tool.name, mcp_server, kwargs)

        return LCTool.from_function(
            name=tool.name,
            description=getattr(tool, "description", "MCP tool"),
            func=tool_func,
            args_schema=ArgsSchema,
            coroutine=tool_func,
        )

    async def get_tools_from_mcp_server(self, mcp_server_url: str) -> list[McpTool]:
        client = Client(mcp_server_url)

        async with client:
            tools = await client.list_tools()
        return tools

KITE_MCP_SERVER = "https://mcp.kite.trade/sse"
LOCAL_MCP_SERVER = "http://127.0.0.1:8000/district"

async def main():
    # servers = [LOCAL_MCP_SERVER, KITE_MCP_SERVER]
    servers = [LOCAL_MCP_SERVER]
    mcp_client = await APP_MCPTools.create(servers)
    print(f"\nTools provided by MCP Servers {servers} :\n")
    print(f"Number of tools = {len(mcp_client.tools)}")
    for tool in mcp_client.tools:
        print(f"\n")
        print(tool)

if __name__ == "__main__":
    asyncio.run(main())

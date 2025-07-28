from fastmcp import FastMCP
from server.mcp_logging import dbg
from utils.app_config import mcp_server_name

app_mcp = FastMCP(mcp_server_name)
dbg.info(f"MCP Server, {mcp_server_name} Created")
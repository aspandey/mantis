from server.app_mcp import app_mcp
from server.mcp_logging import dbg
import utils.app_config as conf

if __name__ == "__main__":
    dbg.info(f"Starting MCP Server: {conf.mcp_server_name}")
    app_mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=conf.mcp_server_port,
        path="/app",
        log_level="debug",
    )
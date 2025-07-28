import os
import yaml
from dotenv import load_dotenv
from server.mcp_logging import dbg

load_dotenv()

def load_config() -> dict[str, str]:
    config = {}
    try:
        with open('./utils/config.yaml', 'r') as f:
            config_from_file = yaml.safe_load(f)
            if config_from_file:
                config.update(config_from_file)
    except FileNotFoundError:
        print("Warning: config.yaml not found. Using only environment variables for configuration.")
    except yaml.YAMLError as e:
        print(f"Error parsing config.yaml: {e}. Using only environment variables for configuration.")
    return config

def get_api_key(api_key_loc, key) -> str | None:
    api_key = os.getenv(key)
    if not api_key:
        try:
            with open(api_key_loc, "r") as key_file:
                for line in key_file:
                    if line.startswith(key):
                        api_key = line.strip().split("=", 1)[1]
                        break
        except FileNotFoundError:
            raise RuntimeError(f"{key} not set and API key file not found at {api_key_loc}")
    
    if not api_key:        
        dbg.error(f"API key {key} not found at {api_key_loc}.")
    
    return api_key


config = load_config()
log_file_location = config.get("log_file_location", "/var/log/app.log") 
mcp_server_port = config.get("mcp_server_port", 8000)
mcp_server_name = config.get("mcp_server_name", "app_mcp_server")
api_key_loc = config.get("API_KEY_LOC", "/usr/local/api_key")

dbg.info(f"Log File Location: {log_file_location}")
dbg.info(f"MCP Server URL: {mcp_server_port}")

weather_api_key = get_api_key(api_key_loc, "WEATHER_API_KEY")
secret = os.getenv("USER_SECRET")

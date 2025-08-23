import logging as DEBUG_APP
import yaml

def read_yaml_config(file_path: str) -> dict:
    """Read YAML configuration file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

con = read_yaml_config("./utils/config.yaml")

GENERATIVE_MODEL = con.get("GENERATIVE_MODEL", "llama3.2:latest")
EMBEDDING_MODEL= con.get("EMBEDDING_MODEL", "nomic-embed-text")
OLLAMA_API = con.get("OLLAMA_API", "http://localhost:11434/api")

MCP_SERVERS = con.get("MCP_SERVERS", {"local": "http://127.0.0.1:8000/app"})

LOG_FILE = con.get("AGENT_LOG_FILE", "/var/log/agent.logs")
DEBUG_APP.basicConfig(
    filename=LOG_FILE,
    level=DEBUG_APP.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s- %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

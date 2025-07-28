import logging as dbg

LOG_PATH = "server/logging.log"
dbg.basicConfig(
    filename=LOG_PATH,
    level=dbg.INFO,
    format="%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(funcName)s - %(message)s",
)

import logging

# ----------------- Server Configuration -----------------
HOST = "127.0.0.1"
CHUNK_SIZE = 1024 * 10
SERVERS = [("127.0.0.1", 5001), ("127.0.0.1", 5002)]
SOCKET_TIMEOUT = 5  # seconds

# ----------------- Database Configuration -----------------
DB_NAME = "wordcounts.db"

# ----------------- Logging Configuration -----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
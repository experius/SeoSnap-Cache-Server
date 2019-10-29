from rendertron_cache_server import server
from dotenv import load_dotenv


def start_server():
    load_dotenv()
    s = server.Server()
    s.start()

def make_server():
    load_dotenv()
    s = server.Server()
    return s

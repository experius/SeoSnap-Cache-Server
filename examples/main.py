from rendertron_cache_server import server, log

log.init()
s = server.Server()
s.app.run(port=5001)


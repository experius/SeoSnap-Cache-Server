from rendertron_cache_server import commands

s = commands.make_server()
application = s.get_app()


from cheroot import wsgi
from dwa import app

if __name__ == "__main__" :


    path_map = {
        '/' : app
    }

    address = "127.0.0.1", 8000
    disp = wsgi.PathInfoDispatcher(path_map)
    server = wsgi.Server(address, disp)

    server.start()
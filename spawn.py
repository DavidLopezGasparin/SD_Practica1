'''
Remote example spawning on a remote server. SERVER
@author: Daniel Barcelona Pons
'''
from pyactor.context import set_context, create_host, serve_forever
import sys

if __name__ == "__main__":
    set_context()
    port=1270+int(sys.argv[1])
    ip=2+int(sys.argv[1])
    host = create_host("http://127.0.0.%s:%s/"%(ip, port))
    registry = host.lookup_url('http://127.0.0.1:7777/regis', 'Registry', 'mapReduce')

    registry.bind('host%s'%sys.argv[1], host)

    serve_forever()

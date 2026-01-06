from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()

authorizer.add_user("user", "password", "ftp", perm="elradfmw")

authorizer.add_anonymous("ftp", perm="elr")

handler = FTPHandler
handler.authorizer = authorizer

server_address = ("", 2121)
server = FTPServer(server_address, handler)

print("FTP server started on port 2121")
server.serve_forever()


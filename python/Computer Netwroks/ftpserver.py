import os
import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a directory for the FTP server to store files
try:
    if not os.path.exists('ftp_files'):
        os.makedirs('ftp_files')
    logging.info('FTP directory created')
except OSError as e:
    logging.error(f'Error creating FTP directory: {e}')

# Set up the authorizer
authorizer = DummyAuthorizer()
authorizer.add_user('user', 'password', 'ftp_files', perm='elradfmw')

# Set up the handler
handler = FTPHandler
handler.authorizer = authorizer

# Set up the server
try:
    server = FTPServer(('localhost', 8080), handler)
    logging.info('FTP server started')
except Exception as e:
    logging.error(f'Error starting FTP server: {e}')

# Start the server
try:
    server.serve_forever()
except KeyboardInterrupt:
    logging.info('FTP server stopped')
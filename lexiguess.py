import argparse
import socket               # Import socket module

parser = argparse.ArgumentParser(description=
'LexiGuess, Networked program with server-client options for guessing a word.')
parser.add_argument("--mode", action='store', metavar='m',help="client or server mode")
parser.add_argument("--port", type=int, metavar='p', help="port number")
parser.add_argument("--word",metavar='w' ,help="word to be guessed")
parser.add_argument("--ip",metavar='i' ,help="IP address for client")
args = parser.parse_args()
if args.mode == "server":
    print ("server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = args.port                # Reserve a port for your service.
    s.bind(('', port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client. This where server waits
        print ('Got connection from'), addr
        c.send (b'Thank you for connecting')
        c.close()                # Close the connection
elif args.mode == "client":
    print ("client")
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    print (host)
    port = args.port              # Reserve a port for your service.

    s.connect((host, port))
    print (s.recv(1024))         #this is where client (or server) waits
    s.close                     # Close the socket when done
else:
    print("Error! Please choose server or client mode.")

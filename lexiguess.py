import argparse
import socket               # Import socket module

parser = argparse.ArgumentParser(description='LexiGuess, Networked program with server-client options for guessing a word.')
parser.add_argument("--mode", action='store', metavar='m',help="client or server mode")
parser.add_argument("--port", type=int, metavar='p', help="port number")
parser.add_argument("--word",metavar='w' ,help="word to be guessed")
parser.add_argument("--ip",metavar='i' ,help="IP address for client")
args = parser.parse_args()
if args.mode == "server":
    print ("server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
    host = args.ip
    print(host)
    port = args.port                # Reserve a port for your service.
    s.bind((host, port))
    word = []        # Bind to the port
    word = args.word
    k = len(word)
    print(word)
    print(k)
    board = []
    for i in range(0,k):
        board.append(i)
        board[i] = "_ "

    b = ''.join(board)
    print(b)
    n = 3
    check = 0
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client. This where server waits
        print ('Got connection from'), addr
        while check == 0 and n > 0:
            c.send(str(n).encode('uft-8'))
            c.send(board);

            guess = c.recv(1,socket,MSG_WAITALL)
            check = 1
            for i in range(0,k):
                if board[i] == guess:
                    check = 1;
                    break;
                elif board[i] == "_ " and guess == word[i]:
                    board[i] = guess
                    check =0

            if check:
                k = k-1

            check = 1

            for i range(0,k):
                if board[i] == "_ "
                check = 0
                break

            if check:
                c.send(str(k).encode('uft-8'))
        c.close()                # Close the connection
    s.close()
elif args.mode == "client":
    print ("client")
    s = socket.socket()         # Create a socket object
    host = args.ip            # Get local machine name
    print (host)
    port = args.port              # Reserve a port for your service.

    s.connect((host, port))
    print(s.recv(4, socket.MSG_WAITALL))        #this is where client (or server) waits
    s.close                     # Close the socket when done
else:
    print("Error! Please choose server or client mode.")

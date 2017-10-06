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
            c.send(str(k).encode('uft-8'))
            c.send(board);

            guess = c.recv(1,socket,MSG_WAITALL) #recieve guess letter
            check = 1
            #check letter with the word
            for i in range(0,k):
                if board[i] == guess:       #check letter is being guessed or not
                    check = 1;
                    break;
                
                if board[i] == "_ " and guess == word[i]: #replace word by the guess letter
                    board[i] = guess
                    check =0

            if check:       #if check is 1 decrement guess by 1
                n = n-1

            check = 1       #reset check

            for i range(0,k):       #check is there still missing letter if yes keep the game
                if board[i] == "_ ":
                    check = 0       #do not decrement guess
                    break

            if check:   #if check is 1 client has won
                c.send(str(255).encode('uft-8))
                
            else:
                #client has lost
                c.send(str(0).encode('uft-8'))
                
                
        c.close()                # Close the connection
    s.close()
elif args.mode == "client":
    print ("client")
    s = socket.socket()         # Create a socket object
    host = args.ip            # Get local machine name
    print (host)
    port = args.port              # Reserve a port for your service.

    s.connect((host, port))
    n = s.recv(1, socket.MSG_WAITALL))
    k = s.recv(1, socket.MSG_WAITALL))
    board = s.recv(k,socket.MSG_WAITALL))
    
    while n != 0 and n != 255:
        print(b'Board:' + board)
        print(b"Enter guess: ", end"")
        sys.stdout.flush()
        l = sys.stdinreadline()
        print(l)  #check letter is correct or not
        s.send(l)
        n = s.recv(1, socket.MSG_WAITALL))
        k = s.recv(1, socket.MSG_WAITALL))
        board = s.recv(k,socket.MSG_WAITALL))
        
    print(b'Board:' + board)
    if n = 0:
        print(b"You lost")
    elif n = 255:
        print(b" You won")
    s.close                     # Close the socket when done
else:
    print("Error! Please choose server or client mode.")

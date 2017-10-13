import argparse
import sys
import socket               # Import socket module
import os, signal #  Low level modules for threading and handling signals

parser = argparse.ArgumentParser(description='LexiGuess, Networked program with server-client options for guessing a word.')
parser.add_argument("--mode", action='store', metavar='m',help="client or server mode")
parser.add_argument("--port", type=int, metavar='p', help="port number")
parser.add_argument("--word",metavar='w' ,help="word to be guessed")
parser.add_argument("--ip",metavar='i' ,help="IP address for client")
args = parser.parse_args()

def getChar():
    inputChar = input("Enter Guess: ")
    allowedChars= 'abcdefghijklmnopqrstuvwxyz'
    while (len(inputChar) != 1 or inputChar not in allowedChars):
        inputChar =input("Enter Guess: ")
    return inputChar


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
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:

        c, addr = s.accept()     # Establish connection with client. This where server waits
        os.fork()
        print ('Got connection from'), addr
        while check == 0 and n > 0:
            c.send(str(n).encode('utf-8'))
            c.send(str(k).encode('utf-8'))
            c.send(b.encode('utf-8'));

            guess = c.recv(1,socket.MSG_WAITALL).decode('utf-8') #recieve guess letter
            check = 1
            #check letter with the word
            for i in range(0,k):

                if board[i] == guess:
                    check = 1
                    break;

                if board[i] == "_ " and word[i] == guess: #replace word by the guess letter
                    board[i] = guess+" "
                    check = 0


            b = ''.join(board)
            if check:       #if check is 1 decrement guess by 1
                n = n-1

            check = 1       #reset check

            for i in range(0,k):       #check is there still missing letter if yes keep the game
                if board[i] == "_ ":
                    check = 0       #do not decrement guess
                    break

        if check:   #if check is 1 client has won
            c.send(str(5).encode('utf-8'))
            c.send(str(k).encode('utf-8'))
            c.send(b.encode('utf-8'));

        else:
            #client has lost
            c.send(str(4).encode('utf-8'))
            c.send(str(k).encode('utf-8'))
            c.send(b.encode('utf-8'));

        c.close()                # Close the connection
        exit()
    s.close()
elif args.mode == "client":
    print ("client")
    s = socket.socket()         # Create a socket object
    host = args.ip            # Get local machine name
    print (host)
    port = args.port              # Reserve a port for your service.

    s.connect((host, port))
    n = s.recv(1, socket.MSG_WAITALL)
    k = s.recv(1, socket.MSG_WAITALL)
    board = s.recv(int(k)*2,socket.MSG_WAITALL)

    n = n.decode('utf-8')
    k = k.decode('utf-8')
    print('k ='+k)
    print('n ='+n)
    N = int(n)
    if N == 3:
        print("YES")

    while N != 4 and N != 5:
        print("Board:" + board.decode('utf-8') + "(" + n + " guesses left)")
        l = getChar()
        s.send(str(l).encode('utf-8'))
        gn = n
        n = s.recv(1, socket.MSG_WAITALL)
        n = n.decode('utf-8')
        N = int(n)
        k = s.recv(1, socket.MSG_WAITALL)
        board = s.recv(int(k)*2,socket.MSG_WAITALL)


    print("Board:" + board.decode('utf-8') + "(" + gn + " guesses left)")
    if N == 4:
        print("You lost")
    elif N == 5:
        print(" You won")
    s.close                     # Close the socket when done
else:
    print("Error! Please choose server or client mode.")

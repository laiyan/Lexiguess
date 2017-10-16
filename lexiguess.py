import argparse
import sys
import socket               # Import socket module
import os, signal #  Low level modules for threading and handling signals
import struct

#argument
parser = argparse.ArgumentParser(description='LexiGuess, Networked program with server-client options for guessing a word.')
parser.add_argument("--mode", action='store', metavar='m',help="client or server mode")
parser.add_argument("--port", type=int, metavar='p', help="port number")
parser.add_argument("--word",metavar='w' ,help="word to be guessed")
parser.add_argument("--ip",metavar='i' ,help="IP address for client")
args = parser.parse_args()

#guess letter method
def getChar():
    inputChar = input("Enter Guess: ")
    allowedChars= 'abcdefghijklmnopqrstuvwxyz'
    while (len(inputChar) != 1 or inputChar not in allowedChars):
        inputChar =input("Enter Guess: ")
    return inputChar

#game method for server
def game():
    word = []        # Bind to the port
    word = args.word
    k = len(word)
    print(word)
    print(k)
    board = []

    #dashline for board
    for i in range(0,k):
        board.append(i)
        board[i] = "_"
    b = ''.join(board)
    print(b)
    n = 3
    check = 0

    #if need to check and still have guess
    while check == 0 and n > 0:
        c.send(struct.pack(">i",1))
        c.send(str(n).encode('utf-8'))
        c.send(struct.pack(">i",k))
        c.send(b.encode('utf-8'));

        h = (c.recv(4, socket.MSG_WAITALL))
        h = int.from_bytes(h,byteorder = 'big')
        guess = c.recv(h,socket.MSG_WAITALL) #recieve guess letter
        guess = guess.decode('utf-8')
        check = 1
        #check letter with the word
        for i in range(0,k):

            if board[i] == guess:
                check = 1
                break;

            #replace word by the guess letter
            if board[i] == "_" and word[i] == guess:
                board[i] = guess
                check = 0


        b = ''.join(board)
        if check:       #if check is 1 decrement guess by 1
            n = n-1

        check = 1       #reset check

        #check is there still missing letter if yes keep the game
        for i in range(0,k):
            if board[i] == "_":
                check = 0       #do not decrement guess
                break

    if check:   #if check is 1 client has won
        c.send(struct.pack(">i",1))
        c.send(str(5).encode('utf-8')) #send 5 for won
        c.send(struct.pack(">i",k))
        c.send(b.encode('utf-8'));

    else:
        #if chclient has lost
        c.send(struct.pack(">i",1))
        c.send(str(4).encode('utf-8')) #send 4 for lost
        c.send(struct.pack(">i",k))
        c.send(b.encode('utf-8'));

#if arg is server
if args.mode == "server":
    print ("server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
    host = args.ip
    print(host)
    port = args.port                # Reserve a port for your service.
    s.bind((host, port))
    s.listen(5)                 # Now wait for client connection.
    while True:
        c, addr = s.accept()     # Establish connection with client. This where server waits
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        pid = os.fork()
        if pid == 0:
            print ('Got connection from'), addr
            game()
            c.close()                # Close the connection
            exit()
    #s.close()

#client mode
elif args.mode == "client":
    print ("client")
    s = socket.socket()         # Create a socket object
    host = args.ip            # Get local machine name
    print (host)
    port = args.port              # Reserve a port for your service.

    s.connect((host, port))
    h = (s.recv(4, socket.MSG_WAITALL))
    h = int.from_bytes(h,byteorder = 'big')
    n = s.recv(h,socket.MSG_WAITALL)
    k =(s.recv(4, socket.MSG_WAITALL))
    k = int.from_bytes(k, byteorder = 'big')
    board = s.recv(k,socket.MSG_WAITALL)

    n = n.decode('utf-8')
    print('n ='+n)
    N = int(n)
    if N == 3:
        print("YES")

    #while user doesn't won or lost
    while N != 4 and N != 5:
        print("Board:" + board.decode('utf-8') + "(" + n + " guesses left)")
        l = getChar()
        s.send(struct.pack(">i",1))
        s.send(str(l).encode('utf-8'))
        gn = n
        h = (s.recv(4, socket.MSG_WAITALL))
        h = int.from_bytes(h,byteorder = 'big')
        n = s.recv(h,socket.MSG_WAITALL)
        n = n.decode('utf-8')
        N = int(n)
        k =(s.recv(4, socket.MSG_WAITALL))
        k = int.from_bytes(k, byteorder = 'big')
        board = s.recv(k,socket.MSG_WAITALL)

    #if won or lost
    print("Board:" + board.decode('utf-8') + "(" + gn + " guesses left)")
    if N == 4:
        print("You lost")
    elif N == 5:
        print(" You won")
    s.close                     # Close the socket when done

#wrong argument for mode
else:
    print("Error! Please choose server or client mode.")

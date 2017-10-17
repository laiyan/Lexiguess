''' Server and client for a simple hangman game. '''
import argparse
import socket               # Import socket module
import os#  Low level modules for threading and handling signals
import signal
import struct

#argument
PARSER = argparse.ArgumentParser(
    description='LexiGuess,Networked program with server-client options for guessing a word.')
PARSER.add_argument("--mode", action='store', metavar='m', help="client or server mode")
PARSER.add_argument("--PORT", type=int, metavar='p', help="PORT number")
PARSER.add_argument("--word", metavar='w', help="word to be guessed")
PARSER.add_argument("--ip", metavar='i', help="IP address for client")
ARGS = PARSER.parse_args()

#guess letter method
def get_char():
    ''' for inputing the guess letter. '''
    inputchar = input("Enter Guess: ")
    allowed = 'abcdefghijklmnopqrstuvwxyz'
    while len(inputchar) != 1 or inputchar not in allowed:
        inputchar = input("Enter Guess: ")
    return inputchar

#game method for server
def game():
    ''' Game Function for the server. '''
    word = []        # Bind to the PORT
    word = ARGS.word
    k = len(word)
    BOARD = []

    #dashline for BOARD
    for i in range(0, k):
        BOARD.append(i)
        BOARD[i] = "_"
    B = ''.join(BOARD)
    N = 3
    check = 0

    #if need to check and still have guess
    while check == 0 and N > 0:
        C.send(struct.pack(">i", 1))
        C.send(str(N).encode('utf-8'))
        C.send(struct.pack(">i", k))
        C.send(B.encode('utf-8'))

        H = (C.recv(4, socket.MSG_WAITALL))
        H = int.from_bytes(H, byteorder='big')
        guess = C.recv(H, socket.MSG_WAITALL) #recieve guess letter
        guess = guess.decode('utf-8')
        check = 1
        #check letter with the word
        for i in range(0, k):

            if BOARD[i] == guess:
                check = 1
                break

            #replace word by the guess letter
            if BOARD[i] == "_" and word[i] == guess:
                BOARD[i] = guess
                check = 0


        B = ''.join(BOARD)
        if check:       #if check is 1 decrement guess by 1
            N = N-1

        check = 1       #reset check

        #check is there still missing letter if yes keep the game
        for i in range(0, k):
            if BOARD[i] == "_":
                check = 0       #do not decrement guess
                break

    if check:   #if check is 1 client has won
        C.send(struct.pack(">i", 1))
        C.send(str(5).encode('utf-8')) #send 5 for won
        C.send(struct.pack(">i", k))
        C.send(B.encode('utf-8'))

    else:
        #if chclient has lost
        C.send(struct.pack(">i", 1))
        C.send(str(4).encode('utf-8')) #send 4 for lost
        C.send(struct.pack(">i", k))
        C.send(B.encode('utf-8'))

#if arg is server
if ARGS.mode == "server":
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
    HOST = ARGS.ip
    PORT = ARGS.port               # Reserve a PORT for your service.
    S.bind((HOST, PORT))
    S.listen(5)                 # Now wait for client connection.
    while True:
        C, ADDR = S.accept()     # Establish connection with client. This where server waits
        signal.signal(signal.SIGCHLD, signal.SIG_IGN)
        PID = os.fork()
        if PID == 0:
            game()
            C.close()                # Close the connection
            exit()
    #S.close()

#client mode
elif ARGS.mode == "client":
    S = socket.socket()         # Create a socket object
    HOST = ARGS.ip            # Get local machine name
    PORT = ARGS.port              # Reserve a PORT for your service.

    S.connect((HOST, PORT))
    H = (S.recv(4, socket.MSG_WAITALL))
    H = int.from_bytes(H, byteorder='big')
    N = S.recv(H, socket.MSG_WAITALL)
    k = (S.recv(4, socket.MSG_WAITALL))
    k = int.from_bytes(k, byteorder='big')
    BOARD = S.recv(k, socket.MSG_WAITALL)

    N = N.decode('utf-8')
    N = int(N)
    #while user doesn't won or lost
    while N != 4 and N != 5:
        print("Board:" + BOARD.decode('utf-8') + "(" + N + " guesses left)")
        L = get_char()
        S.send(struct.pack(">i", 1))
        S.send(str(L).encode('utf-8'))
        GN = N
        H = (S.recv(4, socket.MSG_WAITALL))
        H = int.from_bytes(H, byteorder='big')
        N = S.recv(H, socket.MSG_WAITALL)
        N = N.decode('utf-8')
        N = int(N)
        k = (S.recv(4, socket.MSG_WAITALL))
        k = int.from_bytes(k, byteorder='big')
        BOARD = S.recv(k, socket.MSG_WAITALL)

    #if won or lost
    print("Board:" + BOARD.decode('utf-8') + "(" + GN + " guesses left)")
    if N == 4:
        print("You lost")
    elif N == 5:
        print(" You won")
    #S.close                     # Close the socket when done

#wrong argument for mode
else:
    print("Error! Please choose server or client mode.")

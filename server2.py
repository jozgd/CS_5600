
import socket
import pickle
from tictactoe import tictactoe

# user ids = 0, 1, 2
info = ["I'm 0", "I'm 1", "I'm 2"]

s = socket.socket()
print ("Socket successfully created")

port = 12345

s.bind(('', port))
print ("socket binded to %s" %(port))

s.listen(5)
print ("socket is listening")

# messages for ids 0, 1, 2
unsent_messages = [[], [], []]

while True:

    c, addr = s.accept() #establish connection
    with c:
        print ('Got connection from', addr )
        c.sendall('Who are you?'.encode()) #establish identity
        id = c.recv(1024).decode()
        dest = '-1'
        if not id:
            break
        while id not in ['0','1','2']:
            c.sendall('Who are you? (0,1,2)'.encode())
            id = c.recv(1024).decode()

        if len(unsent_messages[int(id)]) > 0:
            # send game move
            msg = unsent_messages[int(id)][0]
            game = msg[1]
            dest = msg[0]
            game_pickle = pickle.dumps(game)
            c.sendall(game_pickle)
            game_pickle = c.recv(1024)
            updated_game = pickle.loads(game_pickle)
            unsent_messages[int(dest)].append((id,updated_game))
            c.close()
            unsent_messages[int(id)].pop(0)
        else:
            c.sendall('Who would you like to start a game with?'.encode())
            dest = c.recv(1024).decode()
            while dest not in ['0','1','2']:
                c.sendall('Who would you like to start a game with? (0,1,2)'.encode())
                dest = c.recv(1024).decode()
            game = tictactoe(id,dest)
            game_pickle = pickle.dumps(game)
            c.sendall(game_pickle)
            game_pickle = c.recv(1024)
            updated_game = pickle.loads(game_pickle)
            c.close()
            unsent_messages[int(dest)].append((id,updated_game))

    #break #TEMP


import socket
import pickle
import tictactoe

s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# "Who are you?"
print (s.recv(1024).decode())
id = str(input())
s.sendall(id.encode())
recvd_msg = s.recv(1024)
try:
    recvd_msg = recvd_msg.decode()
except:
    recvd_msg = pickle.loads(recvd_msg)
# checking id input
while recvd_msg == 'Who are you? (0,1,2)':
    print(recvd_msg)
    id = str(input())
    s.sendall(id.encode())
    recvd_msg = s.recv(1024)
    try:
        recvd_msg = recvd_msg.decode()
    except:
        recvd_msg = pickle.loads(recvd_msg)

# play move if game already exists
if isinstance(recvd_msg, tictactoe.tictactoe):
    game = recvd_msg
    game.playTurn(id)
    game_pickle = pickle.dumps(game)
    s.sendall(game_pickle)
else:
    # Who would you like to start a game with?
    print(recvd_msg)
    dest = str(input())
    s.sendall(dest.encode())
    recvd_msg = s.recv(1024)
    try:
        recvd_msg = recvd_msg.decode()
    except:
        recvd_msg = pickle.loads(recvd_msg)
    # checking input
    while recvd_msg == 'Who would you like to start a game with? (0,1,2)':
        print(recvd_msg)
        dest = str(input())
        s.sendall(dest.encode())
        recvd_msg = s.recv(1024)
        try:
            recvd_msg = recvd_msg.decode()
        except:
            recvd_msg = pickle.loads(recvd_msg)

    # the next message should be a pickle containing a new game
    # game = pickle.loads(recvd_msg)
    recvd_msg.playTurn(id)
    game_pickle = pickle.dumps(recvd_msg)
    s.sendall(game_pickle)

s.close()

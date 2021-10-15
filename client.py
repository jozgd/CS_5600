
import socket
from tictactoe.py import tictactoe

s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# "Who are you?"
print (s.recv(1024).decode())
id = str(input())
while id:
    s.sendall(id.encode())
    recvd_msg = s.recv(1024).decode()
    if is_instance(recvd_msg, tictactoe):
        if not recvd_msg.active:
            recvd_msg.playTurn(id)
        else:
            recvd_msg.playTurn(id)
            s.sendall(recvd_msg.encode())

    else:
        print(recvd_msg)
        id = str(input())

# id = str(input()[0])
# s.sendall(id.encode())

s.close()


import socket
import pickle
from tictactoe import tictactoe
from helper_functions import dataToSend, chatMessage, sendData

s = socket.socket()

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
s.connect(('127.0.0.1', port))

id = str(input('Who are you? '))
sendData(s, dataToSend('id', int(id)))
resp = pickle.loads(s.recv(1024))
while resp.data == False:
    id = str(input('Who are you? '))
    sendData(s, dataToSend('id', int(id)))
    resp = pickle.loads(s.recv(1024))
print('Identity verified successfully!')

s.close()

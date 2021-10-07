
import socket

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
    print (s.recv(1024).decode())
    id = str(input())



# id = str(input()[0])
# s.sendall(id.encode())

s.close()

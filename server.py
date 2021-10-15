
import socket
from tictactoe import tictactoe

# user ids = 0, 1, 2
info = ["Im 0", "Im 1", "Im 2"]

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

    c, addr = s.accept() #establsih connection
    with c:
        print ('Got connection from', addr )
        c.sendall('Who are you?'.encode()) #esablish identity
        id = c.recv(1024).decode()
        if not id:
            break
        while id not in ['0','1','2']:
            c.sendall('Who are you? (0,1,2)'.encode())
            id = c.recv(1024).decode()

        if len(unsent_messages[int(id)]) > 0:
            c.sendall(unsent_messages[int(id)][0].encode())
            temp = unsent_messages[int(id)].pop()
            dest = temp.players[0]
            if dest == id:
                dest = temp.players[1]
        else:
            c.sendall("Who do you want to start a game with?".encode())
            dest = c.recv(1024).decode()
            message = tictactoe(dest,id)
            c.sendall(message.encode())

        gameUpdate = c.recv(1024).decode()
        #gameUpdate.players


        # new_messages = ''
        # for mess in unsent_messages[int(id)]:
        #     new_messages += 'Message from user {}: {}\n'.format(mess[0], mess[1])
        # if new_messages:
        #     c.sendall((new_messages + 'Hello {}, who are you sending to?'.format(id)).encode())
        #     unsent_messages[int(id)] = []
        # else:
        #     c.sendall(('Hello {}, who are you sending to?'.format(id)).encode()) #esablish destination
        # dest = c.recv(1024).decode()
        # while dest not in ['0','1','2']:
        #     c.sendall(('Hello {}, who are you sending to? (0,1,2)'.format(id)).encode())
        #     dest = c.recv(1024).decode()
        #
        # c.sendall(('Message to {}: what would you like to say?'.format(dest)).encode()) #esablish message
        # message = c.recv(1024).decode()
        #
        # c.sendall(('Message to {}: Sent'.format(dest)).encode()) #Confirmation
        c.close()

        unsent_messages[int(dest)].append((id,gameUpdate))











    #break #TEMP

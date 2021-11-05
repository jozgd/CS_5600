
import socket
import pickle
from tictactoe import tictactoe
from helper_functions import dataToSend, chatMessage, sendData

# Generic function for server to handle data received from client
def recvFromClient():
    data = pickle.loads(c.recv(1024))
    type = data.type
    if type == 'id':
        verifyIdentity(data)
    elif type == 'request':
        clientRequest(data)
    elif type == 'msg':
        all_messages.append(data.data)
        sendData(c, dataToSend('ok'))
    elif type == 'checkUnread':
        checkUnread(data)
    elif type == 'markRead':
        markRead(data)
    else:
        sendData(c, dataToSend('error', 'Server was unable to parse received data.'))
    return

# verify user identity
def verifyIdentity(req):
    print('verifyIdentity')
    id = req.data
    valid = True
    if id not in [0,1,2]:
        valid = False
    print('Client ID', id, 'is' if valid else 'is not', 'valid.')
    sendData(c, dataToSend('id', valid))
    return

# Get list of open chats/messages for a client's user ID
# req: dataToSend object
def clientRequest(req):
    type = req.data[0]
    if type == 'chats':
        getOpenChats(req)
    elif type == 'msgs':
        getMsgs(req)
        pass
    else:
        sendData(c, dataToSend('error', 'Server could not recognize request for data.'))
    return

# get list of open chats and return to client
def getOpenChats(req):
    req_user = req.data[1]
    chatting_users = []
    for msg in all_messages:
        if msg.sender == req_user and msg.receiver not in chatting_users:
            chatting_users.append(msg.receiver)
        elif msg.receiver == req_user and msg.sender not in chatting_users:
            chatting_users.append(msg.sender)
    sendData(c, dataToSend('chats', chatting_users))
    return

# get all messages betweent two users
def getMsgs(req):
    u1 = req.data[1]
    u2 = req.data[2]
    msgs = []
    for msg in all_messages:
        if msg.sender in (u1,u2) and msg.receiver in (u1,u2):
            if msg.unread == True:
                msg.unread = False
            msgs.append(msg)
    sendData(c, dataToSend('msgs', msgs))

# check for unread messages
def getUnreadMsgs(req):
    unreadMsgs = False
    req_user = req.data
    chatting_users = []
    for msg in all_messages:
        if msg.receiver == req_user and msg.unread == True and msg.sender not in chatting_users:
            unreadMsgs = True
            chatting_users.append(msg.sender)
    sendData(c, dataToSend('unread', (unreadMsgs, chatting_users)))
    return

# mark messages as read
def markRead(req):
    recv = req.data[0]
    send = req.data[1]
    for msg in all_messages:
        if msg.sender == send and msg.receiver == recv and msg.unread == True:
            msg.unread = False
    sendData(c, dataToSend('ok'))
    return

# user ids = 0, 1, 2
info = ["user 0", "user 1", "user 2"]

s = socket.socket()
# print ("Socket successfully created")

port = 12345

s.bind(('', port))
print ("socket binded to %s" %(port))

s.listen(5)
# print ("socket is listening")

# messages for ids 0, 1, 2
all_messages = []

while True:
    print('waiting for connection')
    c, addr = s.accept() #establish connection
    with c:
        recvFromClient()

    #break #TEMP

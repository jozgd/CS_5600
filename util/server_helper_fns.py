# Gabrielle
# Functions for use by server.py

import pickle
import socket
from util.helper_functions import *

# messages for ids 0, 1, 2
all_messages = []

# Generic function for server to handle data received from client
def recvFromClient(c):
    data = pickle.loads(c.recv(1024))
    type = data.type
    if type == 'id':
        verifyIdentity(c,data)
    elif type == 'request':
        clientRequest(c,data)
    elif type == 'msg':
        all_messages.append(data.data)
        sendData(c, dataToSend('ok'))
    elif type == 'checkUnread':
        getUnreadMsgs(c,data)
    elif type == 'markRead':
        markRead(c,data)
    else:
        sendData(c, dataToSend('error', 'Server was unable to parse received data.'))
    return

# verify user identity
def verifyIdentity(c, req):
    id = req.data
    valid = True
    if id not in [0,1,2]:
        valid = False
    print('Client ID', id, 'is' if valid else 'is not', 'valid.')
    sendData(c, dataToSend('id', valid))
    return

# Get list of open chats/messages for a client's user ID
# req: dataToSend object
def clientRequest(c, req):
    type = req.data[0]
    if type == 'chats':
        getOpenChats(c,req)
    elif type == 'msgs':
        getMsgs(c,req)
        pass
    else:
        sendData(c, dataToSend('error', 'Server could not recognize request for data.'))
    return

# get list of open chats and return to client
def getOpenChats(c, req):
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
def getMsgs(c, req):
    clientID = req.data[1]
    otherID = req.data[2]
    msgs = []
    for msg in all_messages:
        if msg.sender in (clientID,otherID) and msg.receiver in (clientID,otherID):
            msgs.append(msg)
            if msg.receiver == clientID and msg.unread == True:
                msg.unread = False
    sendData(c, dataToSend('msgs', msgs))

# check for unread messages
def getUnreadMsgs(c, req):
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
def markRead(c, req):
    recv = req.data[0]
    send = req.data[1]
    for msg in all_messages:
        if msg.sender == send and msg.receiver == recv and msg.unread == True:
            msg.unread = False
    sendData(c, dataToSend('ok'))
    return

# Gabrielle
# Functions for use by server.py

import pickle
import socket
from util.helper_functions import *
from tictactoe import tictactoe

# messages for ids 1, 2, 3
all_convos = []

all_convos.append(chatConvo(2, 1, [
    chatMessage('game', 1, 2, tictactoe(1,2))
]))

# Generic function for server to handle data received from client
def recvFromClient(c):
    data = pickle.loads(c.recv(4096))
    type = data.type
    if type == 'id':
        verifyIdentity(c,data)
    elif type == 'request':
        clientRequest(c,data)
    elif type == 'convo':
        updateConvo(c,data)
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
    if id < 1:
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
    elif type == 'convo':
        getConvo(c,req)
        pass
    else:
        sendData(c, dataToSend('error', 'Server could not recognize request for data.'))
    return

# get list of open chats and return to client
def getOpenChats(c, req):
    req_user = req.data[1]
    chatting_users = []
    for convo in all_convos:
        if convo.isInChat(req_user) and int(convo.isInChat(req_user)) not in chatting_users:
            chatting_users.append(int(convo.isInChat(req_user)))
    sendData(c, dataToSend('chats', chatting_users))
    return

# get all messages betweent two users
def getConvo(c, req):
    clientID = req.data[1]
    otherID = req.data[2]
    convoToSend = None
    for convo in all_convos:
        if convo.isInChat(clientID, otherID):
            for msg in convo.msgList:
                if msg.receiver == clientID and msg.unread == True:
                    msg.unread = False
            convoToSend = convo
            break
    sendData(c, dataToSend('convo', convoToSend))


# replace existing convo with updated one
def updateConvo(c, req):
    newConvo = req.data
    for i in range(len(all_convos)):
        if all_convos[i].isInChat(newConvo.user1, newConvo.user2):
            all_convos[i] = newConvo
            sendData(c, dataToSend('ok'))
            return
    all_convos.append(newConvo)
    sendData(c, dataToSend('ok'))


# check for unread messages
def getUnreadMsgs(c, req):
    unreadMsgs = False
    req_user = req.data
    chatting_users = []
    for convo in all_convos:
        for msg in convo.msgList:
            if msg.receiver == req_user and msg.unread == True and msg.sender not in chatting_users:
                unreadMsgs = True
                chatting_users.append(msg.sender)
                break
    sendData(c, dataToSend('unread', (unreadMsgs, chatting_users)))
    return

# mark messages as read
# I don't think this gets used anywhere right now, but it might be useful later
def markRead(c, req):
    recv = req.data[0]
    send = req.data[1]
    for convo in all_convos:
        if convo.isInChat(send, recv):
            for msg in convo:
                if msg.sender == send and msg.receiver == recv and msg.unread == True:
                    msg.unread = False
            break
    sendData(c, dataToSend('ok'))
    return

# Gabrielle
# Functions for use by client.py

import pickle
import socket
from util.helper_functions import *

# Define the port on which you want to connect
port = 12345

# we only call this function when data needs to be sent to server
# currently, server always sends a response (whether it be actual data or just
#   a confirmation that the action was successful)
def sendToServer(pkg):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    sendData(s, pkg)
    resp = pickle.loads(s.recv(1024))
    s.close()
    return resp


# validate client identity (for login)
def validateIdentity():
    valid = False
    while not valid:
        id = str(input('Who are you? '))
        try:
            id = int(id)
        except:
            pass
        else:
            valid = userExists(id)
    # print('Identity verified successfully!')
    return id


# validate user identity (when selecting user to chat with)
def selectUser():
    valid = False
    while not valid:
        recvID = str(input('Who do you want to message? '))
        try:
            recvID = int(recvID)
        except:
            pass
        else:
            valid = userExists(recvID)
    return recvID


# check if user 'id' exists
def userExists(id):
    resp = sendToServer(dataToSend('id', id))
    return resp.data


# menu for interacting with chats
def printChatMenu(ids):
    print('\nChatting Menu')
    for id in ids:
        print("- '" + str(id) + "': Open conversation with user " + str(id))
    print("- '+': Start a conversation with a new user")
    return


# gets list of open chats with client
def getChats(id):
    chats = sendToServer(dataToSend('request', ['chats', id]))
    return chats.data


# unread indicators are shown as an asterisk after the conversation name
def printChats(id, chats):
    unread = sendToServer(dataToSend('checkUnread', id))
    print('\nConversations')
    for i in chats:
        print('- User', str(i) + ('*' if i in unread.data[1] else ''))
    return


# gets all messages between client 'id' and user 'otherID'
def getMsgs(id, otherID):
    return sendToServer(dataToSend('request', ['msgs', id, otherID]))


# client writes and sends a message
def writeSendMsg(id, recvID):
    # todo: allow option to start game
    msg = str(input('Write your message below. (Press ENTER to send.)\n'))
    msgObj = chatMessage('msg', id, recvID, msg)
    ok = sendToServer(dataToSend('msg', msgObj))
    if ok.type == 'error':
        print(ok.data)
    return

# Gabrielle
# Functions for use by client.py

import pickle
import socket
from util.helper_functions import *

# Define the port on which you want to connect
port = 12345

def sendToServer(pkg):
    s = socket.socket()
    s.connect(('127.0.0.1', port))
    sendData(s, pkg)
    resp = pickle.loads(s.recv(1024))
    s.close()
    return resp


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


def userExists(id):
    resp = sendToServer(dataToSend('id', id))
    return resp.data


def printChatMenu(ids):
    print('\nChatting Menu')
    for id in ids:
        print("- '" + str(id) + "': Open conversation with user " + str(id))
    print("- '+': Start a conversation with a new user")
    return


def getChats(id):
    # todo: add capability to see if messages are unread
    chats = sendToServer(dataToSend('request', ['chats', id]))
    return chats.data


def printChats(id, chats):
    unread = sendToServer(dataToSend('checkUnread', id))
    print('\nConversations')
    for i in chats:
        print('- User', str(i) + ('*' if i in unread.data[1] else ''))
    return


def getMsgs(id, otherID):
    return sendToServer(dataToSend('request', ['msgs', id, otherID]))


def writeSendMsg(id, recvID):
    # todo: allow option to start game
    msg = str(input('Write your message below. (Press ENTER to send.)\n'))
    msgObj = chatMessage('msg', id, recvID, msg)
    ok = sendToServer(dataToSend('msg', msgObj))
    if ok.type == 'error':
        print(ok.data)
    return

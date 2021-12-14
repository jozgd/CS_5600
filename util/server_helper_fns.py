# Gabrielle
# Functions for use by server.py
import os
import pickle
import socket
from util.helper_functions import *
from tictactoe import tictactoe

# messages for ids 1, 2, 3
all_convos = []
maxGameID = 0

# all_convos.append(chatConvo(2, 1, [
#     chatMessage('game', 1, 2, tictactoe(1,2))
# ]))

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
    elif type == 'gameID':
        getNextGameID(c)
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
    #for convo in all_convos:
    #    if convo.isInChat(req_user) and int(convo.isInChat(req_user)) not in chatting_users:
    #        chatting_users.append(int(convo.isInChat(req_user)))
    for (root,dirs,files) in os.walk('users/' + str(req_user)):
        for x in files:
            id = x[:-4]
            try:
                id = int(id)
            except:
                print('failed to read user id', id)
                continue
            chatting_users.append(id)

    sendData(c, dataToSend('chats', chatting_users))
    return

# get all messages betweent two users
def getConvo(c, req):
    clientID = req.data[1]
    otherID = req.data[2]
    convoToSend = None
    #for convo in all_convos:
    #    if convo.isInChat(clientID, otherID):
    #        for msg in convo.msgList:
    #            if msg.receiver == clientID and msg.unread == True:
    #                msg.unread = False
    #        convoToSend = convo
    #        break

    filename = 'users/' + str(clientID) + '/' + str(otherID) + '.pkl'
    os.makedirs(os.path.dirname(filename), exist_ok=True) # make directory if not exist
    try:
        with open(filename, 'r+b') as f:
            convo = pickle.load(f)
            for msg in convo.msgList:
                if msg.receiver == clientID and msg.unread == True:
                    msg.unread = False
        convoToSend = convo
    except:
        # print('fails')
        pass
    if convoToSend:
        # push updated conversation to pickle files
        filename1 = 'users/' + str(convoToSend.user1) + '/' + str(convoToSend.user2) + '.pkl' # file path
        os.makedirs(os.path.dirname(filename1), exist_ok=True) # make directory if not exist
        with open(filename1, 'w+b') as f: # dump binary
            pickle.dump(convoToSend,f)
        filename2 = 'users/' + str(convoToSend.user2) + '/' + str(convoToSend.user1) + '.pkl' # file path
        os.makedirs(os.path.dirname(filename2), exist_ok=True) # make directory if not exist
        with open(filename2, 'w+b') as f: # dump binary
            pickle.dump(convoToSend,f)

    sendData(c, dataToSend('convo', convoToSend))


# replace existing convo with updated one
def updateConvo(c, req):
    newConvo = req.data
    # for i in range(len(all_convos)):
    #     if all_convos[i].isInChat(newConvo.user1, newConvo.user2):
    #         all_convos[i] = newConvo
    #         sendData(c, dataToSend('ok'))
    #         return
    # all_convos.append(newConvo)

    filename1 = 'users/' + str(newConvo.user1) + '/' + str(newConvo.user2) + '.pkl' # file path
    os.makedirs(os.path.dirname(filename1), exist_ok=True) # make directory if not exist
    with open(filename1, 'w+b') as f: # dump binary
        pickle.dump(newConvo,f)

    filename2 = 'users/' + str(newConvo.user2) + '/' + str(newConvo.user1) + '.pkl' # file path
    os.makedirs(os.path.dirname(filename2), exist_ok=True) # make directory if not exist
    with open(filename2, 'w+b') as f: # dump binary
        pickle.dump(newConvo,f)

    sendData(c, dataToSend('ok'))


# check for unread messages
def getUnreadMsgs(c, req):
    unreadMsgs = False
    req_user = req.data
    chatting_users = []
    unread_users = []
    # for convo in all_convos:
    #     for msg in convo.msgList:
    #         if msg.receiver == req_user and msg.unread == True and msg.sender not in chatting_users:
    #             unreadMsgs = True
    #             chatting_users.append(msg.sender)
    #             break

    for (root,dirs,files) in os.walk('users/' + str(req_user)):
        for x in files:
            id = x[:-4]
            try:
                id = int(id)
            except:
                print('failed to read user id', id)
                continue
            chatting_users.append(id)
    for usr in chatting_users:
        try:
            with open('users/' + str(req_user) + '/' + str(usr) + '.pkl', 'r+b') as f:
                convo = pickle.load(f)
                for msg in convo.msgList:
                    if msg.receiver == req_user and msg.unread == True and msg.sender not in unread_users:
                        unreadMsgs = True
                        unread_users.append(msg.sender)
                        break
        except:
            # print('fails')
            pass
        # print(convo.msgList)

    sendData(c, dataToSend('unread', (unreadMsgs, unread_users)))
    return

# mark messages as read
# I don't think this gets used anywhere right now, but it might be useful later
def markRead(c, req): # unused?
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


# returns the expected ID of the NEXT NEW GAME OBJECT
def getNextGameID(c):
    # max_id = 0
    # for convo in all_convos:
    #     for msg in convo.msgList:
    #         if msg.type == 'game':
    #             game = msg.data
    #             if game.id > max_id:
    #                 max_id = game.id
    # sendData(c, dataToSend('gameID', max_id+1))
    global maxGameID
    maxGameID += 1
    sendData(c, dataToSend('gameID', maxGameID))

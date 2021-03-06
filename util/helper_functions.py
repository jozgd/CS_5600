# Gabrielle
# Classes and functions for use by ANY host

import pickle
import socket
from tictactoe import tictactoe


# Generic class for data sent between client & server
class dataToSend:
    def __init__(self, type, data=None):
        # type of data sent to client can be one of ['id', 'chats', 'msgs', 'ok', 'error', 'unread']
        # type of data sent to server can be one of ['id', 'request', 'msg', 'checkUnread', 'markRead']
        self.type = type
        # expected data for each type of data sent to client:
        # - id: True/False (used for id verification)
        # - chats: list of user ids with open chats
        # - msgs: list of chatMessage objects (see below)
        # - ok: None (used to confirm action performed successfully)
        # - unread: tuple(True/False, user id(s)) (used to indicate new msgs)
        # - error: string containing error message
        #
        # expected data for each type of data sent to server:
        # - id: user id to verify/login
        # - request: either ['chats', client ID] or ['msgs', client ID, other ID]
        # - msg: chatMessage object
        # - checkUnread: client ID
        # - markRead: [client ID, other ID]
        self.data = data


# keeps track of message ids. I don't know if this will work tbh
msg_id = 0

# Generic class to hold data for one chat message
class chatMessage:
    def __init__(self, type, sender, receiver, data):
        global msg_id
        self.msg_id = msg_id
        msg_id += 1
        # type can be one of ['msg', 'game']
        self.type = type
        self.sender = sender
        self.receiver = receiver
        self.unread = True
        # expected data with each type:
        #     msg: string containing message
        #     game: game object (for now)
        self.data = data

    # for CLI only
    def printMsg(self, viewer):
        # if type == 'msg', just print the text
        # if type == 'game', allow the user to take their turn
        if self.type == 'msg':
            print(('*' if self.unread and self.receiver == viewer else '') + str(self.sender) + ': "' + self.data + '"')
        elif self.type == 'game':
            self.data.playTurn(viewer)
        return


# chat conversation class to store a conversation between two users
class chatConvo:
    def __init__(self, user1, user2, msgList=[]):
        # user ids involved in conversation
        self.user1 = user1
        self.user2 = user2
        # msgList is a list of chatMessage objects. defaults to empty list
        self.msgList = msgList

    # adds message to msgList
    def addMessage(self, msg):
        if msg.type == 'msg':
            self.msgList.append(msg)
        elif msg.type == 'game':
            gameToReplace = None
            for m in self.msgList:
                if m.type == 'game' and m.data.id == msg.data.id:
                    gameToReplace = m
                    break
            if gameToReplace:
                self.msgList[self.msgList.index(gameToReplace)] = msg
            else:
                self.msgList.append(msg)

    # checks if user(s) belong to chat. not sure if this will be useful when
    #   file management is implemented
    def isInChat(self, user1, user2=None):
        if user2:
            if (user1, user2) == (self.user1, self.user2) or (user1, user2) == (self.user2, self.user1):
                return True
        else:
            if user1 in (self.user1, self.user2):
                return str(self.user2) if user1 == self.user1 else str(self.user1)
        return False


# Generic function for pickling/sending data to host named 'dest'
def sendData(dest, pkg):
    dest.sendall(pickle.dumps(pkg))
    return

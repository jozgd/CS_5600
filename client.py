
import socket
import pickle
from tictactoe import tictactoe
import util.helper_functions as hf
import util.client_helper_fns as chf

# client ID (0,1,2)
id = None

if __name__ == "__main__":
    # "Who are you?"
    id = chf.validateIdentity()
    # get chats
    chats = chf.getChats(id)
    opt = None
    # loop through menu
    while True:
        # chats will refresh every time menu is reloaded
        # todo (when GUI is built): add auto-refresh
        chats = chf.getChats(id)
        chf.printChats(id, chats)
        chf.printChatMenu(chats)
        opt = str(input('Select an option (type \'~\' to exit): '))
        print()
        # client selected user chat to open
        if opt in [str(x) for x in chats]:
            otherID = int(opt)
            msgs = chf.getMsgs(id, otherID)
            for msg in msgs.data:
                msg.printMsg(id)
            # todo: add in game functionality
            opt2 = str(input('\nReply? (y/N) '))
            if opt2 != '' and opt2[0].lower() == 'y':
                chf.writeSendMsg(id, otherID)
        # client wants to start a new conversation
        elif opt == '+':
            recvID = chf.selectUser()
            chf.writeSendMsg(id, recvID)
        # client wants to quit
        elif opt == '~':
            break

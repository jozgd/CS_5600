
import socket
import pickle
from tictactoe import tictactoe
import util.helper_functions as hf
import util.client_helper_fns as chf

# client ID (0,1,2)
id = None

if __name__ == "__main__":
    id = chf.validateIdentity()
    chats = chf.getChats(id)
    # if chats == []:
    #     print('\nYou have no conversations.')
    #     new = str(input('Would you like to start a new one? (y/N) '))
    #     if new != '' and new[0].lower() == 'y':
    #         recvID = chf.selectUser()
    #         chf.writeSendMsg(recvID)
    opt = '+'
    while opt in [str(x) for x in chats] + ['+']:
        chats = chf.getChats(id)
        chf.printChats(id, chats)
        chf.printChatMenu(chats)
        opt = str(input('Select an option (press ENTER to exit): '))
        print()
        # client selected user chat to open
        if opt in [str(x) for x in chats]:
            otherID = int(opt)
            msgs = chf.getMsgs(id, otherID)
            for msg in msgs.data:
                msg.printMsg(id)
            opt2 = str(input('\nReply? (y/N) '))
            if opt2 != '' and opt2[0].lower() == 'y':
                chf.writeSendMsg(id, otherID)
        # client wants to start a new conversation
        elif opt == '+':
            recvID = chf.selectUser()
            chf.writeSendMsg(id, recvID)
        # client wants to quit
        elif opt == '':
            break


import socket
import pickle
from tictactoe import tictactoe
import util.helper_functions as hf
import util.server_helper_fns as shf

# user ids = 0, 1, 2
info = ["user 0", "user 1", "user 2"]

if __name__ == "__main__":
    s = socket.socket()
    # print ("Socket successfully created")
    port = 12345
    s.bind(('', port))
    print ("socket binded to %s" %(port))
    s.listen(5)
    # print ("socket is listening")

    while True:
        c, addr = s.accept() #establish connection
        with c:
            shf.recvFromClient(c)

        #break #TEMP

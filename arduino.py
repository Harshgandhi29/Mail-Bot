from pyfirmata import *
import time

def light(port,pin):
    board = Arduino(port)

    iterator = util.Iterator(board)
    iterator.start()
    Tv1 = board.get_pin(f'd:{pin}:o')

    time.sleep(1.0)
    Tv1.write(1)
    print(Tv1.read())
    board.exit()

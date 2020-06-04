from pyfirmata import *
import time

def light(port,pin):
    board = Arduino(port)

    iterator = util.Iterator(board)
    iterator.start()
    #pin = int(pin)
    Tv1 = board.get_pin(f'd:{pin}:o')

    time.sleep(1.0)
    Tv1.write(1)
    print(Tv1.read())
   #time.sleep(4.0)
   # Tv1.write(0)
    board.exit()

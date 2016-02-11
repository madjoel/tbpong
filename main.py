#!/usr/bin/python
# ----------------------
# Small Pong game
# @author Matthieu Laqua
# ----------------------

import time, termbox

# main function
def main():
    tb = termbox.Termbox()
    somestr = "Hello Termbox!"
    for i in range(len(somestr)):
        tb.change_cell(i,1, ord(somestr[i]), 0, 0)
    tb.present()
    time.sleep(3)
    tb.close()

# entrypoint
if __name__ == "__main__":
    main()


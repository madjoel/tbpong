#!/usr/bin/python
# ----------------------
# Small Pong game
# @author Matthieu Laqua
# ----------------------

import time, math, termbox

# main function
def main():
    tb = termbox.Termbox()
    somestr = "Hello Termbox!"
    for i in range(len(somestr)):
        tb.change_cell(i+1,1, ord(somestr[i]), 0, 0)

    render_border(tb)
    b = Ball(math.floor(tb.width()/2), math.floor(tb.height()/2))
    b.render(tb)
    tb.present()
    time.sleep(1)
    b.move(5, 5)
    b.render(tb)

    tb.present()
    time.sleep(3)
    tb.close()

# render a basic border
def render_border(p_tb, p_char='#'):
    p_char = ord(p_char)
    width, height = p_tb.width(), p_tb.height()
    for x in range(width):
        p_tb.change_cell(x, 0, p_char, 0, 0)
        p_tb.change_cell(x, height-1, p_char, 0, 0)
    for y in range(height):
        p_tb.change_cell(0, y, p_char, 0, 0)
        p_tb.change_cell(width-1, y, p_char, 0, 0)

# ball class
class Ball:
    def __init__(self, p_posx=1, p_posy=1, p_char='O'):
        self._posx = p_posx
        self._posy = p_posy
        self._char = ord(p_char)

    def render(self, p_tb):
        p_tb.change_cell(self._posx, self._posy, self._char, 0, 0)

    def move(self, p_x, p_y):
        self._posx += p_x
        self._posy += p_y

# entrypoint
if __name__ == "__main__":
    main()


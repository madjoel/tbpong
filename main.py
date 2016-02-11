#!/usr/bin/python
# ----------------------
# Small Pong game
# @author Matthieu Laqua
# ----------------------

import time, math, termbox

# main function
def main():
    tb = termbox.Termbox()
    pad_l = Paddle(tb, 'l', 10)
    pad_r = Paddle(tb, 'r', 10)
    ball = Ball(tb)

    while True: # game loop
        tb.clear()

        pad_l.render()
        pad_r.render()
        ball.render()

        tb.present()

        event = tb.peek_event(50)
        if event:
            (type, ch, key, mod, w, h, x, y) = event
            if type == termbox.EVENT_KEY:
                if key in [termbox.KEY_ESC, termbox.KEY_CTRL_C] or ch == 'q':
                    break

    tb.close()

# ball class
class Ball:
    def __init__(self, p_tb, p_char='O'):
        self._tb = p_tb
        self._posx = math.floor(self._tb.width()/2)
        self._posy = math.floor(self._tb.height()/2)
        self._char = ord(p_char)

    def render(self):
        self._tb.change_cell(self._posx, self._posy, self._char, 0, 0)

    def move(self, p_x, p_y):
        self._posx += p_x
        self._posy += p_y

# paddle class
class Paddle:
    def __init__(self, p_tb, p_align, p_width, p_char='|'):
        self._tb = p_tb
        self._align = p_align
        self._width = p_width
        self._char = ord(p_char)
        self._y = math.floor(self._tb.height()/2) - math.floor(self._width/2)
        if   self._align == "l": self._x = 1
        elif self._align == "r": self._x = self._tb.width() - 2
        else: raise Exception("Illegal pos '" + p_align + "', must be in ['l', 'r']")

    def render(self):
        for y in range(self._width):
            self._tb.change_cell(self._x, self._y + y, self._char, 0, 0)

    def move(self, p_delta):
        self._y += p_delta

# entrypoint
if __name__ == "__main__":
    main()


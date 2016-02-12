#!/usr/bin/python
# ----------------------
# Small Pong game
# @author Matthieu Laqua
# ----------------------

import time, math, termbox

# main function
def main():
    game = Game()
    game.start()

# main game class
class Game:
    def __init__(self):
        self._tb = termbox.Termbox()
        self._pad_l = Paddle(self._tb, 'l', 10)
        self._pad_r = Paddle(self._tb, 'r', 10)
        self._ball = Ball(self._tb)
        self._running = False
    
    def start(self):
        self._running = True
        self.main_loop()
    
    def stop(self):
        self._running = False

    def render_all(self):
        self._tb.clear()
        self._pad_l.render()
        self._pad_r.render()
        self._ball.render()
        self._tb.present()

    def do_actions(self):
        self._ball.move(1, 1)

    def handle_input_and_sleep(self):
        elapsed = time.perf_counter()
        event = self._tb.peek_event(30)
        if event:
            (type, ch, key, mod, w, h, x, y) = event
            if type == termbox.EVENT_KEY:
                if key in [termbox.KEY_ESC, termbox.KEY_CTRL_C] or ch == 'q':
                    self.stop()
                elif key == termbox.KEY_ARROW_UP:
                    self._pad_l.move(-1)
                elif key == termbox.KEY_ARROW_DOWN:
                    self._pad_l.move(1)
        elapsed = time.perf_counter() - elapsed
        if elapsed < 0.03: time.sleep(0.03 - elapsed)

    def main_loop(self):
        while self._running: # game loop
            self.do_actions()
            self.render_all()
            self.handle_input_and_sleep()

        self._tb.close()

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


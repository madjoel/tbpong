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
        self._stopped = True
        self._running = False

    def start(self):
        self._stopped = False
        self.main_loop()

    def stop(self):
        self._stopped = True

    def play_pause(self):
        self._running = not self._running

    def render_all(self):
        self._tb.clear()
        self._pad_l.render()
        self._pad_r.render()
        self._ball.render()
        self._tb.present()

    def do_actions(self):
        out_on_side = self._ball.is_out()
        if out_on_side:
            if out_on_side == 'r':
                pass # increase score, reset ball, etc...
            elif out_on_side == 'l':
                pass # increase score, reset ball, etc...

        if self._ball.coll_top_or_bot():
            self._ball.repulse_y()

        ball_x_dir = self._ball.get_x_direction()
        if ball_x_dir == 'r':
            if self._ball.coll_with_paddle(self._pad_r):
                self._ball.repulse_x()
        else:
            if self._ball.coll_with_paddle(self._pad_l):
                self._ball.repulse_x()

        self._ball.move()
        self._pad_r.move(self._ball._vecy)

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
                elif key == termbox.KEY_SPACE:
                    self.play_pause()
        elapsed = time.perf_counter() - elapsed
        if elapsed < 0.03: time.sleep(0.03 - elapsed)

    def main_loop(self):
        while not self._stopped: # game loop
            if self._running:
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
        self._vecx = 1
        self._vecy = 1
        self._char = ord(p_char)

    def render(self):
        self._tb.change_cell(self._posx, self._posy, self._char, 0, 0)

    def move(self):
        self._posx += self._vecx
        self._posy += self._vecy

    def repulse_y(self):
        self._vecy *= (-1)

    def repulse_x(self):
        self._vecx *= (-1)

    def coll_top_or_bot(self):
        return (self._posy <= 0) or (self._posy >= (self._tb.height()-1))

    def coll_with_paddle(self, p_paddle):
        return (self._posx == p_paddle._posx) and \
                (self._posy >= p_paddle._posy and self._posy <= p_paddle._posy+p_paddle._width)

    def get_x_direction(self):
        return 'r' if self._vecx > 0 else 'l'

    def is_out(self):
        if   self._posx <= 0: return 'l'
        elif self._posx >= self._tb.width()-1: return 'r'
        else: return False

# paddle class
class Paddle:
    def __init__(self, p_tb, p_align, p_width, p_char='|'):
        self._tb = p_tb
        self._align = p_align
        self._width = p_width
        self._char = ord(p_char)
        self._posy = math.floor(self._tb.height()/2) - math.floor(self._width/2)
        if   self._align == "l": self._posx = 1
        elif self._align == "r": self._posx = self._tb.width() - 2
        else: raise Exception("Illegal pos '" + p_align + "', must be in ['l', 'r']")

    def render(self):
        for y in range(self._width):
            self._tb.change_cell(self._posx, self._posy + y, self._char, 0, 0)

    def move(self, p_delta):
        self._posy += p_delta

# entrypoint
if __name__ == "__main__":
    main()


#!/usr/bin/python
# ----------------------
# Small Pong game
# @author Matthieu Laqua
# ----------------------

import time, math, termbox, random

# main function
def main():
    game = Game()
    game.start()

# helper functions
def between(val, lower, upper):
    if (val >= lower):
        if (val <= upper):
            return True
    return False

# main game class
class Game:
    def __init__(self):
        self._tb = termbox.Termbox()
        self._score = Score(self._tb)
        self._pad_l = Paddle(self._tb, 'l', 9)
        self._pad_r = Paddle(self._tb, 'r', 9)
        self._ball = Ball(self._tb)
        self._stopped = True
        self._paused = True

    def start(self):
        self._stopped = False
        self.main_loop()

    def stop(self):
        self._stopped = True

    def play_pause(self):
        self._paused = not self._paused

    def reset(self, also_score=False):
        if not self._paused:
            self.play_pause()
        self._ball.init_reset()
        self._pad_l.init_reset()
        self._pad_r.init_reset()
        if also_score:
            self._score.init_reset()

    def render_all(self):
        self._tb.clear()
        self._score.render()
        self._pad_l.render()
        self._pad_r.render()
        self._ball.render()
        self._tb.present()

    def do_actions(self):
        out_on_side = self._ball.is_out()
        if out_on_side:
            if out_on_side == 'r':
                self._score.inc_l()
            elif out_on_side == 'l':
                self._score.inc_r()
            self.reset()
            return # if out don't do other actions

        if self._ball.coll_top_or_bot():
            self._ball.repulse_y()

        if self._ball.get_x_direction() == 'r':
            self.handle_collision(self._ball.coll_with_paddle(self._pad_r))
        else:
            self.handle_collision(self._ball.coll_with_paddle(self._pad_l))

        self._ball.move()
        self._pad_r.move(self._ball._vecy)

    def handle_collision(self, p_coll_pos):
        if p_coll_pos:
            if p_coll_pos == 'u':
                self._ball._vecy = -1
            elif p_coll_pos == 'm':
                self._ball._vecy = 0
            elif p_coll_pos == 'd':
                self._ball._vecy = 1
            self._ball.repulse_x()

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
            if not self._paused:
                self.do_actions()
            self.render_all()
            self.handle_input_and_sleep()

        self._tb.close()

# ball class
class Ball:
    def __init__(self, p_tb, p_char='O'):
        random.seed(a=time.perf_counter())
        self._tb = p_tb
        self._char = ord(p_char)
        self.init_reset()

    def init_reset(self):
        self._posx = math.floor(self._tb.width()/2) # middle
        self._posy = random.choice(range(5, self._tb.height() -6)) # random
        self._vecx = random.choice([-1,1])
        self._vecy = random.choice([-1,0,1])

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
        if (self._posx == p_paddle._posx):
            if between(self._posy, p_paddle._posy, p_paddle._posy + (math.floor(p_paddle._width/3) -1)):
                return 'u'
            elif between(self._posy, p_paddle._posy + math.floor(p_paddle._width/3), p_paddle._posy + (math.floor(p_paddle._width/3)*2 -1)):
                return 'm'
            elif between(self._posy, p_paddle._posy + math.floor(p_paddle._width/3)*2, p_paddle._posy + p_paddle._width -1):
                return 'd'
            else:
                return False
        else:
            return False

    def get_x_direction(self):
        return 'r' if self._vecx > 0 else 'l'

    def get_y_direction(self):
        return 'd' if self._vecy > 0 else 'u'

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
        self.init_reset()
        if   self._align == "l": self._posx = 1
        elif self._align == "r": self._posx = self._tb.width() - 2
        else: raise Exception("Illegal pos '" + p_align + "', must be in ['l', 'r']")

    def init_reset(self):
        self._posy = math.floor(self._tb.height()/2) - math.floor(self._width/2)

    def render(self):
        for y in range(self._width):
            self._tb.change_cell(self._posx, self._posy + y, self._char, 0, 0)

    def move(self, p_delta):
        self._posy += p_delta

# score class
class Score:
    def __init__(self, p_tb):
        self._tb = p_tb
        self.init_reset()

    def init_reset(self):
        self._val_l = 0
        self._val_r = 0

    def render(self):
        center_x = math.floor(self._tb.width()/2)
        for y in range(self._tb.height()):
            self._tb.change_cell(center_x, y, ord('.'), 0, 0) # draw middle line
        self._tb.change_cell(center_x, 1, ord(':'), 0, 0)
        self._tb.change_cell(center_x-2, 1, ord(str(self._val_l)), 0, 0)
        self._tb.change_cell(center_x+2, 1, ord(str(self._val_r)), 0, 0)

    def inc_l(self):
        self._val_l += 1

    def inc_r(self):
        self._val_r += 1

# entrypoint
if __name__ == "__main__":
    main()


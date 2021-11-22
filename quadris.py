#!/usr/bin/python3

# Quadris game

# IDEAS:
# - Multiplayer: use same random seed
# - Leader board
# - Rotate cw and ccw

import random, sys
import console


_mdebug = 0


# Tetriminoes
SHAPES = [
    # (initial x-offset, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], ... rotations)
    # "I"
    (3, [(0, 0), (1, 0), (2, 0), (3, 0)], [(1, -2), (1, -1), (1, 0), (1, 1)]),
    # "O"
    (4, [(0, 0), (1, 0), (0, 1), (1, 1)]),
    # "T"
    (3, [(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (2, 1), (1, 2)], [(0, 0), (1, 0), (2, 0), (1, 1)], [(0, 1), (1, 0), (1, 1), (1, 2)]),
    # "S"
    (3, [(1, 0), (2, 0), (0, 1), (1, 1)], [(0, -1), (0, 0), (1, 0), (1, 1)]),
    # "Z"
    (3, [(0, 0), (1, 0), (1, 1), (2, 1)], [(1, -1), (0, 0), (1, 0), (0, 1)]),
    # "J"
    (3, [(0, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (2, 0), (1, 1), (1, 2)], [(0, 0), (1, 0), (2, 0), (2, 1)], [(1, 0), (1, 1), (0, 2), (1, 2)]),
    # "L"
    (3, [(2, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (2, 2)], [(0, 0), (1, 0), (2, 0), (0, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)]),
]


class Quadris(console.console):
    # Lines per level
    LINES_PER_LEVEL = 10
    DELAY = 300

    def __init__(self):
        super().__init__(led_width=10, led_height=20)
        
        self.assign_button(0, self.key_left, sequence='<Left>')
        self.assign_button(0, self.key_right, '<Right>')
        self.assign_button(0, self.key_rotate, '<Up>')
        self.assign_button(0, self.key_drop, '<Down>')
        
        # Number of completed lines
        self.lines = 0
        # self.points = 0 # IDEA: does a "tetris" of 4 lines give more points?
        # Level (affects speed and maybe graphics)
        self.level = 1
        # Current shape
        self.shapeid = None # 0 -> 6
        self.shaperot = 0 # Orientation
        self.shapecoords = None # [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        # Board
        self.board = [[0] * self.width for i in range(self.height)]
        # Score
        self.score = 0
        
        self.after_dropid = 'None'
        
        self.newshape()

    def leds_set(self, state, *coords):
        for tup in coords:
            x, y = tup
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                continue
            self.set_led(x, y, state)

    def leds_on(self, *coords):
        self.leds_set(1, *coords)

    def leds_off(self, *coords):
        self.leds_set(0, *coords)

    def newshape(self):
        # Select shape
        self.shapeid = random.randrange(len(SHAPES))
        # self.shapeid = 0
        self.shaperot = 0
        xoffset, *rots = SHAPES[self.shapeid][:]
        coords = rots[0]
        # Move to center of board
        self.shapecoords = [(x + xoffset, y) for x, y in coords]
        # Will it fit
        for x, y in self.shapecoords:
            if self.board[y][x]:
                #print("Game over, score:", self.score)
                self.game_over(0)
                return
        # Draw shape
        self.leds_on(*self.shapecoords)
        # Start drop timer
        self.start_drop_timer()

    def start_drop_timer(self):
        self.after_cancel(self.after_dropid)
        self.after_dropid = self.after(self.DELAY, self.dropper)

    def dropper(self):
        # See if possible to move down
        for x, y in self.shapecoords:
            if y + 1 == self.height:
                break
            if self.board[y + 1][x]:
                break
        else:
            # If yes: move it
            self.leds_off(*self.shapecoords)
            self.shapecoords = [(x, y + 1) for x, y in self.shapecoords]
            self.leds_on(*self.shapecoords)
            self.start_drop_timer()
            return
        
        # Not possible to move down
        
        # If partially off-screen (any -ve coords), game-over
        if any(y < 0 for x, y in self.shapecoords):
            # Do not remove the partial shape - looks better if we keep it
            #print("Game over (offscreen shape)")
            self.game_over(1)
            return
        
        self.stickit()

    def stickit(self):
        # Stick it in place - it is no longer falling
        if _mdebug: print(f'Stick {self.shapecoords}')
        ymodified = set()
        for x, y in self.shapecoords:
            self.board[y][x] = 1
            ymodified.add(y)
        
        # Check for completed lines
        completed = []
        for y in sorted(ymodified):
            if sum(self.board[y]) == self.width:
                completed.append(y)
        if completed:
            # IDEA: disable keyboard shape movement, animate line removal
            # Undraw all lines down to last complete one
            # print()
            # print('#' * 80)
            # print(f'Completed lines: {completed}')
            for y in range(completed[-1] + 1):
                # print(f'Erase line {y}')
                self.leds_off(*((x, y) for x in range(self.width)))
            # Adjust board
            for y in range(completed[-1], -1 + len(completed), -1):
                self.board[y] = self.board[y - len(completed)]
            for y in range(len(completed)):
                self.board[y] = [0] * self.width
            # for row in self.board:
                # print(f'  {row}')
            # Draw all lines down to last complete one
            for y in range(completed[-1] + 1):
                # print('Redraw line {y}:', self.board[y])
                self.leds_on(*((x, y) for x in range(self.width) if self.board[y][x]))
            print()
            self.score += 1
        
        self.newshape()

    # 'dx' -- change in x position
    # 'dy' -- change in y position
    def move(self, dx=0, dy=0):
        # See if possible to move
        for x, y in self.shapecoords:
            if not 0 <= x + dx < self.width:
                return False
            if y + dy < 0:
                # Allow hanging off top of screen
                continue
            if y + dy >= self.height:
                return False
            if self.board[y + dy][x + dx]:
                return False
        self.leds_off(*self.shapecoords)
        self.shapecoords = [(x + dx, y + dy) for x, y in self.shapecoords]
        self.leds_on(*self.shapecoords)
        return True

    def key_left(self, ev=None):
        self.move(dx=-1)

    def key_right(self, ev=None):
        self.move(dx=1)

    def key_drop(self, ev=None):
        if self.move(dy=1):
            self.start_drop_timer()
        else:
            # Cannot move down, so stick it
            self.stickit()

    def key_rotate(self, ev=None):
        # Look for a rotated shape
        xoffset, *rots = SHAPES[self.shapeid][:]
        newshaperot = (self.shaperot + 1) % len(rots)
        if self.shaperot == newshaperot:
            # No rotations available
            return
        
        # Take off coords of first LED in current rotation to get location in new rotation
        xpos, ypos = self.shapecoords[0]
        x1, y1 = rots[self.shaperot][0]
        xpos, ypos = xpos - x1, ypos - y1
        
        # Check if it would fit
        for x, y in rots[newshaperot]:
            x += xpos
            y += ypos
            if y < 0:
                # Allow going off top of screen (while falling)
                continue
            if y >= self.height:
                return
            if x < 0 or x >= self.width:
                return
            if self.board[y][x]:
                return
        
        # Rotate
        self.leds_off(*self.shapecoords)
        self.shaperot = newshaperot
        self.shapecoords = [(x + xpos, y + ypos) for x, y in rots[self.shaperot]]
        self.leds_on(*self.shapecoords)
    def game_over(self, event):
        if event == 0:
            #Normal game over, the player ran out of space
            print('Game over, score:', self.score)
        elif event == 1:
            #Off-screen shape, the player ran out of space
            print('Game over, score:', self.score)
        elif event == -1:
            print('Something weird happened')
        sys.exit()


def main():
    quan = Quadris()
    quan.start_loop()


if __name__ == '__main__':
    main()

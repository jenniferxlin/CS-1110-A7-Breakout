# play.py
# Jennifer Lin (jl3263) and Michelle Wang (mqw4)
# December 8, 2016
# Borrowed and altered code from Instructor Walker M. White (wmw2).
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App.
Instances of Play represent a single game.  If you want to restart a new game, you are
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *
import random


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.

    This subcontroller has a reference to the ball, paddle, and bricks. It animates the
    ball, removing any bricks as necessary.  When the game is won, it stops animating.
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.

    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with
        _bricks [list of Brick]: the list of bricks still remaining
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Breakout.  Only add the getters and setters that you need for
    Breakout.

    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants."""
    
    #GETTER(S)
    def getTries(self):
        """Returns: number of tries left"""
        return self._tries
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializer to create the paddles and bricks for the game."""
        
        self._paddle = Paddle(x = GAME_WIDTH/2, y=PADDLE_OFFSET, width = PADDLE_WIDTH,
                            height = PADDLE_HEIGHT, fillcolor = colormodel.ORANGE,
                            linecolor = colormodel.ORANGE)
        self._bricks = self.multi_bricks()
        self._ball = None
        self._tries = NUMBER_TURNS
        self._serves = 0

    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    # Altered placeSquares function from review slides written by Walker M. White (wmw2).
    def multi_bricks(self):
        """Returns: a multidimensional list of the alternating-colored bricks."""
        
        bricklist = [] #Make new list for columns
        c = 0
        while c < BRICKS_IN_ROW:
            brickrow = [] #Make new list for rows
            if (c + 10) % 10 == 0 and 1:
                color = RED
            if (c + 10) % 10 == 2 and 3:
                color = ORANGE
            if (c + 10) % 10 == 4 and 5:
                color = YELLOW
            if (c + 10) % 10 == 6 and 7:
                color = GREEN
            if (c + 10) % 10 == 8 and 9:
                color = CYAN
            r = 0 
            while r < BRICK_ROWS:
                brick = Brick(left=(BRICK_SEP_H/2 + (r) * (BRICK_WIDTH + BRICK_SEP_H)),
                              top= (GAME_HEIGHT - BRICK_Y_OFFSET - (c)*(BRICK_HEIGHT+BRICK_SEP_V)),
                              width = BRICK_WIDTH, height = BRICK_HEIGHT,
                              fillcolor = color, linecolor = color)
                brickrow.append(brick)
                r = r + 1
            bricklist.extend(brickrow)
            c= c + 1
        return bricklist
    #End of altered code
    
    def updatePaddle(self, input):
        "Moves the paddle left or right when left or right arrow keys are pressed."
        
        projected_move_right = self._paddle.right + PADDLE_MOVE
        projected_move_left = self._paddle.left - PADDLE_MOVE
        if ((min(projected_move_left,0) is 0) and input.is_key_down('left')):
            self._paddle.x -= PADDLE_MOVE
        elif ( (max(projected_move_right, GAME_WIDTH) is GAME_WIDTH ) and input.is_key_down('right')):
            self._paddle.x += PADDLE_MOVE

    def serveBall(self):
        """Serves the ball from random point on the game display."""
        
        self._ball = Ball(x=random.randrange(0,GAME_WIDTH),y=GAME_HEIGHT/2,width=10,height=10,fillcolor=RED)

    def updateBall(self,gamewidth,gameheight):
        """Updates the direction of the ball after it hits the paddle or bricks.
        
        Parameter gamewidth: width of game display
        Preconditon: gamewidth is a non-negative number (int or float)
        
        Parameter gameheight: height of game display
        Preconditon: gameheight is a non-negative number (int or float)"""
        
        self._ball.leftRightBounds(gamewidth)
        self._ball.topBound(gameheight)
        self._ball.stepX()
        self._ball.stepY()
        for x in self._bricks:
            if(x.collides(self._ball)):
                cling = Sound('cup1.wav')
                cling.play()
                self._ball.fillcolor = GREEN
                self._ball.negateDir();
                self._bricks.remove(x)
        if(self._paddle.collides(self._ball)):
            boing = Sound('bounce.wav')
            boing.play()
            self._ball.fillcolor = RED
            self._ball.negateDir()

    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self, view):
        """Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play.
        In order to draw them, you either need to add getters for these attributes or you
        need to add a draw method to class Play.  We suggest the latter.  See the example
        subcontroller.py from class."""

        self._paddle.draw(view)
        for x in self._bricks:
            x.draw(view)
        if self._ball is not None:
            self._ball.draw(view)

    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def hasDied(self,gameheight):
        """Returns: True if the paddle misses the ball.
        
        Parameter gameheight: height of game display
        Preconditon: gameheight is a non-negative number (int or float)"""
        
        if(self._ball.bottomBound(gameheight)):
            self._tries = self._tries - 1;
            self._ball = None;
            return True

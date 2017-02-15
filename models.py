# models.py
# Jennifer Lin (jl3263) and Michelle Wang (mqw4)
# December 8, 2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle."""
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self, x, y, width, height, fillcolor, linecolor):
        """Initializer to create a new paddle.
        
        Parameter x: the x coordinate of the center of the paddle
        Precondition: x is a number (int or float)
        
        Parameter y: the y coordinate of the center of the paddle
        Precondition: y is a number (int or float)
        
        Parameter width: the width of the paddle
        Precondition: width is a non-negative number (int or float)
        
        Parameter height: the height of the paddle
        Precondition: height is a non-negative number (int or float)
        
        Parameter fillcolor: the fill color of the paddle
        Precondition: fillcolor is an object of colormodel.RGB or colormodel.HSV 
        
        Parameter linecolor: the color of the paddle's borders
        Precondition: linecolor is an object of colormodel.RGB or colormodel.HSV"""
        
        GRectangle.__init__(self, x = x, y = y, width = width, height = height,
                            fillcolor = fillcolor, linecolor = linecolor)
        
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        
        leftX = ball.getLeftX()
        rightX = ball.getRightX()
        topY = ball.getTopY()
        bottomY = ball.getBottomY()
        if self.contains(leftX,bottomY):
            return True
        elif self.contains(rightX,bottomY):
            return True
        else:
            return False


class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle."""
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self, left, top, width, height, fillcolor, linecolor):
        """Initializer to create a brick.
        
        Parameter left: the left edge of the brick
        Precondition: left is a number (int or float)
        
        Parameter right: the right edge of the brick
        Precondition: right is a number (int or float)
        
        Parameter width: the width of the paddle
        Precondition: width is a non-negative number (int or float)
        
        Parameter height: the height of the paddle
        Precondition: height is a non-negative number (int or float)
        
        Parameter fillcolor: the fill color of the paddle
        Precondition: fillcolor is an object of colormodel.RGB or colormodel.HSV 
        
        Parameter linecolor: the color of the paddle's borders
        Precondition: linecolor is an object of colormodel.RGB or colormodel.HSV"""
        
        GRectangle.__init__(self, left = left, top = top, width = width,
                            height = height, fillcolor = fillcolor, linecolor = linecolor)
        
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        
        leftX = ball.getLeftX()
        rightX = ball.getRightX()
        topY = ball.getTopY()
        bottomY = ball.getBottomY()
        if self.contains(leftX,topY):
            return True
        elif self.contains(leftX,bottomY):
            return True
        elif self.contains(rightX,topY):
            return True
        elif self.contains(rightX,bottomY):
            return True
        else:
            return False


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above."""
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def stepX(self):
        """Returns: the new x-coordinate of the ball after it has moved"""
        self.x = self.x + self._vx
    
    def stepY(self):
        """Returns: the new y-coordinate of the ball after it has moved"""
        self.y = self.y + self._vy
    
    def negateDir(self):
        """Returns: the negative value of velocity in y direction"""
        self._vy = self._vy * (-1)
    
    def getLeftX(self):
        """Returns: the x-coordinate of left side of ball"""
        return self.x - self.width/2
    
    def getRightX(self):
        """Returns: the x-coordinate of right side of ball"""
        return self.x + self.width/2
    
    def getTopY(self):
        """Returns: the y-coordinate of the top of the ball"""
        return self.y + self.height/2
    
    def getBottomY(self):
        """Returns: the y-coordinate of the bottom of the ball"""
        return self.y - self.height/2
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self, x, y, width, height, fillcolor):
        """Initializer to set random velocity to the ball.
        
        Parameter x: the x coordinate of the center of the ball
        Precondition: x is a number (int or float)
        
        Parameter y: the y coordinate of the center of the ball
        Precondition: y is a number (int or float)
        
        Parameter width: the width of the paddle
        Precondition: width is a non-negative number (int or float)
        
        Parameter height: the height of the paddle
        Precondition: height is a non-negative number (int or float)
        
        Parameter fillcolor: the fill color of the paddle
        Precondition: fillcolor is an object of colormodel.RGB or colormodel.HSV """
        
        GEllipse.__init__(self, x = x, y = y, width = width, height = height,
                          fillcolor = fillcolor)
        self._vy = -5.0
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1,1])
        
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def leftRightBounds(self,game_width):
        """Negates velocity in x direction when ball hits left or right side
        of the window frame.
        
        Parameter game_width: width of game display
        Preconditon: game_width is a non-negative number (int or float)"""
        if (self.right >= game_width) or (self.left <= 0):
            self._vx = (-1) * self._vx

    def topBound(self,game_height):
        """Negates velocity in y direction when ball hits left or right side
        of the window frame.
        
        Parameter game_height: height of game display
        Preconditon: game_height is a non-negative number (int or float)"""
        if (self.top >= game_height):
            self._vy = (-1) * self._vy

    def bottomBound(self,game_height):
        """Returns: True if bottom of the ball hits the bottom of game display.
        
        Parameter game_height: height of game display
        Preconditon: game_height is a non-negative number (int or float)"""
        if (self.bottom <= 0):
            return True


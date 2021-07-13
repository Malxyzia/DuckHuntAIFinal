"""
Duck Module:
    - Handles situations and events that relate to the duck by creating a 'duck' object

Inspired from:
https://github.com/mwrouse/DuckHunt-Python (mwrouse, 30/05/2015)

Sprites from:
https://www.spriters-resource.com/nes/duckhunt/sheet/13056/

"""

# Importing necessary libraries
import pygame
import pygame_gui as gui
import random

# Defining 'Duck' Object for handling events involving the duck within the game.
class Duck:

    """
    'Duck' Object:

    Dependencies:
        - pygame
        - pygame_gui
        - random

    """

    def __init__(self, round, manager, masterPanel, fxKey, volume):

        """
        Initialises all properties of the object when created.

            - :parameter round..............Contains which round the game is currently on in order to adjust speed
                                            and point allocations
            - :parameter manager............Stores the manager which keeps track of all gui elements and draws them.
            - :parameter masterPanel........Contains the UIPanel object which makes up the game area of the screen.
            - :parameter volume.............Volume of sound effects

        """

        # Assigning GUI-related References
        self.manager = manager
        self.panel = masterPanel

        # Duck Properties
        self.colour = random.choice(['red', 'black', 'blue'])
        self.round = round - 1
        self.points = 100 * round
        self.alive = True
        self.completelyDead = False
        self.justShot = False
        self.position = (0, 0)
        self.direction = random.choice([True, False])
        self.straight = False
        self.escaped = False

        # Directional Constants
        self.right = True
        self.left = False

        # Load Sprite Images
        self.flyRight = [self._transform(pygame.image.load(f"sprites/{self.colour}/duck1.png")),
                         self._transform(pygame.image.load(f"sprites/{self.colour}/duck2.png")),
                         self._transform(pygame.image.load(f"sprites/{self.colour}/duck3.png"))]

        self.flyStraightRight = [self._transform(pygame.image.load(f"sprites/{self.colour}/duck4.png")),
                                 self._transform(pygame.image.load(f"sprites/{self.colour}/duck5.png")),
                                 self._transform(pygame.image.load(f"sprites/{self.colour}/duck6.png"))]

        self.flyLeft = [self._transform(pygame.image.load(f"sprites/{self.colour}/duck7.png")),
                        self._transform(pygame.image.load(f"sprites/{self.colour}/duck8.png")),
                        self._transform(pygame.image.load(f"sprites/{self.colour}/duck9.png"))]

        self.flyStraightLeft = [self._transform(pygame.image.load(f"sprites/{self.colour}/duck10.png")),
                                self._transform(pygame.image.load(f"sprites/{self.colour}/duck11.png")),
                                self._transform(pygame.image.load(f"sprites/{self.colour}/duck12.png"))]

        self.die = [self._transform(pygame.image.load(f"sprites/{self.colour}/duckDie1.png")),
                    self._transform(pygame.image.load(f"sprites/{self.colour}/duckDie2.png")),
                    self._transform(pygame.image.load(f"sprites/{self.colour}/duckDie3.png"))]

        # Create Spawn Position
        self.position = (random.randint(100, 1820), 800)

        # Create and queue duck sprite element to manager. Ducks always start by flying to the right.
        self.image = gui.elements.UIImage(
                                    pygame.Rect(self.position[0], self.position[1], 100, 100),
                                    self.flyRight[0],
                                    container=self.panel,
                                    manager=self.manager)

        # Animation Properties
        self.dx = 0.5 + (0.3 * self.round) if self.direction is True else -0.5 - (0.3 * self.round)
        self.dy = -0.5 - (0.2 * self.round)
        self.dieDelay = 0               # Delay Duck Falling
        self.continueDeath = False
        self.animationCount = 0
        self.frame = 0                  # Current Animation Frame
        self.directionCount = 0         # Count to determine when to switch directions

        self.movementDelay = 0

        # Sound Effect
        self.fx = pygame.mixer.Sound(file="./sounds/duck-drop.ogg")
        self.fx.set_volume(volume)
        self.fxKey = fxKey

    # Internal Methods (Private):

    def _transform(self, image, size=(200, 200)):

        """
        Private internal method to transform sprite images to appropriate sizes for screen.

            - :parameter image..........Image object to be transformed
            - :parameter size...........Desired image size. Default is 200x200 pixels.

        :returns Modified image object
        """

        # Sets the background to be rendered as transparent
        image.set_colorkey((163, 239, 165))

        # Returns transformed image
        return pygame.transform.scale(image, size)

    def _replace(self, image):

        """
        Private internal that replaces the current image of the duck to a new one. Used for animating.

            - :parameter image........Image object that will replace the current sprite image displayed.

        """

        # Destroy current image from manager
        self.image.kill()

        # Create and queue new sprite image into manager
        self.image = gui.elements.UIImage(
            pygame.Rect(self.position[0], self.position[1], 100, 100),
            image,
            container=self.panel,
            manager=self.manager)

    # Duck Methods (Public):

    def changeDirection(self):

        """
        Method that determines (and changes) which direction the duck moves.

        """

        # Coin toss that determines whether the duck switches direction (left --> right or vice versa)
        if random.randint(1, 2) == 1:

            # Switch the duck's direction
            if self.direction == self.right:
                self.direction = self.left
                self.dx = -.5 - (0.1 * self.round)

            else:
                self.direction = self.right
                self.dx = .5 + (0.1 * self.round)

        # Coin toss to decide if it will fly straight or not
        if random.randint(1, 2) == 1:

            # Change duck to straight or up
            self.straight = not self.straight

    def shot(self):
        """
        Method that indicates that the duck has been shot and initiates all processes relating to the duck's death.

        """

        # Set the duck to dead
        self.alive = False

        # Replace duck's current sprite with the first 'death' sprite
        self._replace(self.die[0])

        # Re-initialise all animation variables for death animation
        self.frame = 0
        self.animationCount = 0

        # Freeze the duck
        self.dx = 0
        self.dy = 0

        # Display score above duck's head
        # Gets the duck's position by grabbing the sprite's rect object and getting the centre x and top y position
        self.deathPosition = (self.image.get_abs_rect().topleft[0], self.image.get_abs_rect().top - 20)
        self.deathText = gui.elements.UILabel(
            pygame.Rect(self.deathPosition[0], self.deathPosition[1], 100, 25),
            f"{self.points}",
            container=self.panel,
            manager=self.manager,
            object_id="#death_text")


    def update(self, gameState, events):

        """
        Method which updates the duck's sprite.

        """

        if not gameState == 'paused' and gameState:

            # Check if the duck is alive
            if self.alive:

                # Check whether the duck has escaped.
                if self.image.get_relative_rect().bottom < 0 or self.image.get_relative_rect().right < 0 or self.image.get_relative_rect().left > 1920:

                    # Duck is off the screen. Destroy sprite and set the attribute escaped to True
                    self.image.kill()
                    self.escaped = True

                # Check if the duck should try and change directions
                if self.directionCount < 100:

                    # Increment counter if not
                    self.directionCount += 1

                else:

                    # Otherwise, change directions and reset counter
                    self.changeDirection()
                    self.directionCount = 0

                # Check if the duck is going straight and change velocity accordingly
                if self.straight:

                    # If flying straight, set y-velocity to 0 (so it doesn't fly upwards or downwards)
                    self.dy = 0

                    # Check whether the duck is flying to the left or right, and adjust velocity accordingly
                    if self.direction == self.right:
                        self.dx = 0.5 + (0.3 * self.round)

                    else:
                        self.dx = -0.5 - (0.3 * self.round)

                else:

                    # Duck is flying upwards
                    self.dy = -0.5 - (0.2 * self.round)

                # Update the animation frames based on duck's velocity
                if not self.alive:

                    # Set death animation frames
                    self.frames = [self.die[1], self.die[2]]

                elif self.direction == self.right:
                    if self.straight:
                        self.frames = [self.flyStraightRight[1], self.flyStraightRight[2], self.flyStraightRight[1],
                                       self.flyStraightRight[0]]

                    else:
                        self.frames = [self.flyRight[1], self.flyRight[2], self.flyRight[1], self.flyRight[0]]

                elif self.direction == self.left:
                    if self.straight:
                        self.frames = [self.flyStraightLeft[1], self.flyStraightLeft[2], self.flyStraightLeft[1],
                                       self.flyStraightLeft[0]]

                    else:
                        self.frames = [self.flyLeft[1], self.flyLeft[2], self.flyLeft[1], self.flyLeft[0]]

                # Ensure that the frame count does not exceed the frame list
                if self.frame > len(self.frames) - 1:
                    self.frame = 0

            else:

                # Duck is dead. Destroy once it hits the ground
                if self.image.get_relative_rect().bottom >= 850:

                    # Play sound effect
                    if self.fxKey:
                        self.fx.play()

                    # Destroy the sprite
                    self.image.kill()

                    # Check if the death score is still on the screen
                    if self.deathText is not None:

                        # If so, kill the element and set it to none.
                        self.deathText.kill()
                        self.deathText = None

                    # Declare the duck completely dead with no further actions, signifying that it can be removed
                    # from event queue
                    self.completelyDead = True

    def animate(self):

        """
        Method which animates the duck. Is called by the tick(<gameState>) method.

        """

        # Increments animation count
        self.animationCount += 1

        # Limiter/cap which defines animation (frame) rate
        if self.animationCount >= 12:

            # Change animation for falling dead duck
            if not self.alive:

                # Check if it is time to start the death animation
                if self.continueDeath:

                    # Set speed of falling duck
                    self.dy = 5

                    # Advance the death animation
                    frames = [self.die[2], self.die[1]]

                    # Replace sprite with death image accordingly
                    self._replace(frames[self.frame])

                    # Increment frame
                    self.frame += 1

                    # Make sure the frame stays within the correct range
                    if self.frame > len(frames) - 1:
                        self.frame = 0

            # Change animation for duck if not dead
            else:

                # Ensure that frames coming in do not exceed frame length
                if self.frame > len(self.frames) - 1:
                    self.frame = 0

                # Update sprite
                self._replace(self.frames[self.frame])

                # Increment frame
                self.frame += 1

                # Ensure frame stays within correct range
                if self.frame > len(self.frames) - 1:
                    self.frame = 0

            # Reset the animation counter
            self.animationCount = 0

    def checkClick(self, mousePos):

        """
        Method which handles clicks when they occur, and determine whether the duck has been shot.

        """

        # Check whether mouse is in duck's hitbox when clicked
        if self.image.get_abs_rect().collidepoint(mousePos[0], mousePos[1]):

            # Guard against double tapping
            if not self.alive:
                return None

            # Duck was shot - Kill it
            self.shot()

            # Indicate duck has been shot
            return True

        # Indicate shot has missed
        return False

    def tick(self, gameState):
        """
        Method that handles each 'tick' of the game for duck object.

        """

        # Process tick only if game is not paused
        if not gameState == 'paused':

            # Check whether duck is alive
            if not self.alive:

                # This will display the point value above the head and when it's done the duck will start to fall
                if self.dieDelay > 50 and not self.continueDeath:
                    self.dy = 5

                    self.continueDeath = True
                    self.frame = 0

                    # Kill death text image
                    if self.deathText != None:
                        self.deathText.kill()

                    self.deathText = None

                # Continue delaying death animation
                elif not self.continueDeath:
                    self.dieDelay += 1

            # This will help birds continue to fly
            # At the correct angle and direction after resuming from a pause
            elif (self.dx == 0) and (self.dy != 0):
                if not self.straight:
                    if self.direction == self.right:
                        self.dx = .5 + (0.3 * self.round)

                    else:
                        self.dx = -.5 - (0.3 * self.round)

            # Update the Duck's animation
            self.animate()

        # Check whether game has been paused
        elif gameState == 'paused':

            # Game is Paused - Freeze the duck
            self.dx = 0
            self.dy = 0


        # Update the position of itself based on its velocity
        self.position = (self.position[0] + self.dx, self.position[1] + self.dy)
        self.movementDelay = 0


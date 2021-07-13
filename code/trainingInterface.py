# Import necessary libraries
import pygame
import pygame_gui as gui
import time

# Import parent object
from code.duckHunt import DuckHuntInstance


class TrainingInterface(DuckHuntInstance):

    """
        TrainingInterface

        A child object of the DuckHuntInstance object.
        It is an object which hosts all functionalities needed for training an AI, whilst reusing features
        of the parent object

        Dependencies:
            - pygame
            - pygame_gui (gui)
            - DuckHuntInstance

    """

    def __init__(self, masterScreen, manager, aiModelLeft, aiModelRight, fxKey, sound, musicVol, aiBuffer, trainingSet):

        # Inherit parent attrtibutes
        super().__init__(masterScreen, manager, fxKey, sound, musicVol)

        # Initialise AI Variables
        self.nnX = aiModelLeft
        self.nnY = aiModelRight
        self.speedCap = 1
        self.speedCount = 0
        self.aiBuffer = aiBuffer
        self.bufferCount = 0
        self.trainingSetSize = int(trainingSet)
        self.trainingSetCounter = 0
        self.xHistory = []
        self.yHistory = []
        self.xLabelHistory = []
        self.yLabelHistory = []
        self.guess = (self.screen.screenSize[0] // 2, self.screen.screenSize[1] // 2)
        self.shots = 0

    # Small function which rounds numbers to desired number of decimal places
    def _rounding(self, val, digits):
        return round(val + 10 ** (-len(str(val)) - 1), digits)

    # Overridden subroutine which creates the pause screen
    def createPauseScreen(self):

        """
        Overidden as there are significant position shifting that would be otherwise difficult to correct

        """

        # Create Graphical Elements
        self.pauseOverlay = gui.elements.UIPanel(
                                    pygame.Rect((-2, 2, 1925, 1085)),
                                    manager=self.manager,
                                    starting_layer_height=5,
                                    object_id="#pause_overlay")

        pauseOverlaySize = self.pauseOverlay.get_container().get_size()

        self.pauseBox = gui.elements.UIPanel(
                                    pygame.Rect(pauseOverlaySize[0] // 2 - 500, pauseOverlaySize[1] // 2.5 - 160, 1000, 400),
                                    manager=self.manager,
                                    container=self.pauseOverlay,
                                    starting_layer_height=0,
                                    object_id="#pause_box")

        pauseBoxSize = self.pauseBox.get_container().get_size()

        self.pauseText = gui.elements.UILabel(
                                    pygame.Rect(pauseBoxSize[0] // 2 - 300, pauseBoxSize[1] // 4 - 50, 600, 100),
                                    "Paused",
                                    manager=self.manager,
                                    container=self.pauseBox,
                                    object_id="#pause_text")

        self.quitButton = gui.elements.UIButton(
                                    pygame.Rect(pauseBoxSize[0] // 4 - 150, pauseBoxSize[1] // 3 * 2 - 25, 300, 50),
                                    "Save & Quit",
                                    manager=self.manager,
                                    container=self.pauseBox,
                                    object_id="#quit_button")
        self.resumeButton = gui.elements.UIButton(
                                    pygame.Rect((pauseBoxSize[0] // 4 * 3) - 150, pauseBoxSize[1] // 3 * 2 - 50, 300, 100),
                                    "Resume",
                                    manager=self.manager,
                                    container=self.pauseBox,
                                    object_id="#resume_button")

        # Link buttons to function dictionary
        self.screen.functionDictionary[self.quitButton] = '1.7'
        self.screen.functionDictionary[self.resumeButton] = '4.1'

    # Prevent creation of a game over screen
    def createGameOverScreen(self):
        return

    # Subroutine which handles how the AI makes a guess
    def handleAI(self):

        # Get the position of each alive duck on the screen
        ducks = [(duck.image.get_abs_rect().centerx, duck.image.get_abs_rect().centery)for duck in self.duckList if duck.alive is True]

        # If there's none, just exit
        if len(ducks) == 0:
            return

        # Define the kill box of the AI (Don't want AI to spawn camp duck before they appear on screen)
        targets = [duck for duck in ducks if duck[1] < 700 or duck[0] < 50 or duck[0] > 1870]

        # If no ducks are in the kill zone, exit
        if len(targets) == 0:
            return

        # Set AI's sights to the first duck on the list
        targetPos = targets[0]

        # Process AI's guess
        _xInput = [targetPos[0] / 1920, 0, self.guess[0] / 1920, 0]
        _yInput = [targetPos[1] / 1080, 0, self.guess[1] / 1080, 0]
        xPrediction = self.nnX.query(_xInput)
        yPrediction = self.nnY.query(_yInput)

        # Round AI's guess to 3 decimal places
        self.guess = (self._rounding(xPrediction[0][0] * 1920, 3), self._rounding(yPrediction[0][0] * 1080, 3))

        # If AI guesses way off the screen, reset its guess to the centre of the screen
        if self.guess[0] > 2000:
            self.guess = (self.screen.screenSize[0] // 2, self.guess[1])
        if self.guess[1] > 2000:
            self.guess = (self.guess[0], self.screen.screenSize[1] // 2)

        # Check to see if the Ai's shot hits any ducks
        hitList = [duck.checkClick(self.guess) for duck in self.duckList]

        # If it hits a duck
        if hitList[0] is True:

            # Add the guess to the history of correct guesses
            self.xHistory.append(_xInput)
            self.yHistory.append(_yInput)

            # Append the correct label onto the history
            self.xLabelHistory.append([xPrediction[0][0], xPrediction[1][0]])
            self.yLabelHistory.append([yPrediction[0][0], yPrediction[1][0]])

            # Shuffle the history
            self.nnX.mix(self.xHistory, self.xLabelHistory)
            self.nnY.mix(self.yHistory, self.yLabelHistory)

            # Tell AI to adjust itself to its correct shots
            self.nnX.adjust(self.xHistory, self.xLabelHistory)
            self.nnY.adjust(self.yHistory, self.yLabelHistory)

        else:

            # Set the labels according to how it missed
            xLabel = [0, 1] if self.guess[0] > targetPos[0] else [1, 0]
            yLabel = [0, 1] if self.guess[1] > targetPos[1] else [1, 0]

            # Tell it to teach itself, knowing that it guessed wrong.
            self.nnX.adjust([_xInput], [xLabel])
            self.nnY.adjust([_yInput], [yLabel])

        # Increment training set counter
        self.trainingSetCounter += 1

        # Increment the number of shots it has taken and the total amount of duck hits it has
        self.shots += 1
        self.totalDuckHit += len([i for i in hitList if i is True])

        # Check if training counter is the same as the set size
        if self.trainingSetCounter >= self.trainingSetSize:

            # Save the model
            self.screen.autosaveNotice.visible = 1
            self.nnX.save(self.screen.model, "Left")
            self.nnY.save(self.screen.model, "Right")

            # Reset training set
            self.trainingSetCounter = 0
            self.xHistory = []
            self.yHistory = []
            self.xLabelHistory = []
            self.yLabelHistory = []
            self.screen.autosaveNotice.visible = 0

        # Return coordinates of Ai's Guess
        return (int(self.guess[0]) - 50, int(self.guess[1]) - 50)


    # Overridden subroutine to process events going to this interface
    def processEvents(self, events):
        """
        Overridden to custom-fit training process
        """
        # Default AI Guess to None
        cursor = None

        # Check to see whether it has has reached it's game speed counter
        if self.speedCount < self.speedCap or self.speedCap < 0:

            # If not, increment then pass
            self.speedCount += 1
            return

        # Reset game speed buffer
        self.speedCount = 0

        # Check if game is running
        if not self.paused and self.game:

            # Has the start round sequence initiated?
            if self.startRounds is True:

                # Has the animation timer passed 200?
                if self.startRoundCounter > 200:

                    # If so, indicate to move on from start round sequence
                    self.startRounds = False
                    self.startRoundCounter = 0

                    # Erase start round text and spawn ducks
                    self.roundText.kill()
                    self.spawnBirds()

                else:

                    # Instantly end start round counter
                    self.startRoundCounter += 200

            # Check if there are currently no ducks on the screen, and that an end round sequence has not been initiated
            elif len(self.duckList) == 0 and not self.startRounds and not self.endRounds:

                # Spawn Ducks
                self.spawnBirds()

            else:
                tempList = []

                # Has AI's buffer thinking speed been met?
                if self.bufferCount > self.aiBuffer:

                    # Get AI's shot
                    cursor = self.handleAI()

                    # Reset Buffer
                    self.bufferCount = 0

                else:

                    # Increment Buffer
                    self.bufferCount += 1

                # Update each duck on the screen
                for duck in self.duckList:
                    duck.update(self.state, events)
                    duck.tick(self.state)

                    # Check if duck is completely dead
                    if duck.completelyDead is True:

                        # Increment points
                        self.score += duck.points

                    # Duck has escaped.....
                    elif duck.escaped is True:
                        pass

                    else:

                        tempList.append(duck)

                # Update Duck List
                self.duckList = tempList

            # Get time elpased from the start of the training session
            timeNow = time.time()
            seconds = int((timeNow -self.timer) % 60)

            # Update Display System Text
            self.screen.timeDisplay.enable()
            self.screen.timeDisplay.set_text(f"Time: {int((timeNow - self.timer) // 60)}:{'0' * (1 if len(str(seconds)) < 2 else 0) + str(seconds)}")
            self.screen.timeDisplay.rebuild()
            self.screen.timeDisplay.disable()

            self.screen.hitDisplay.enable()
            percentage = round((self.totalDuckHit / self.totalDuckCount if self.totalDuckCount != 0 else 1), 4) * 100
            self.screen.hitDisplay.set_text(f"Hit/Total: {self.totalDuckHit}/{self.totalDuckCount} "
                      f"({percentage})%")
            self.screen.hitDisplay.rebuild()
            self.screen.hitDisplay.disable()

            self.screen.accuracyDisplay.enable()
            accuracy = round((self.totalDuckHit / (self.shots if self.shots != 0 else 100)), 4) * 100
            accuracy = 100.00 if accuracy > 100 else accuracy
            self.screen.accuracyDisplay.set_text(f"Accuracy: {accuracy}%")
            self.screen.accuracyDisplay.rebuild()
            self.screen.accuracyDisplay.disable()

            # Return coordinates of the AI's shot
            return cursor

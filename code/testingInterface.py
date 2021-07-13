# Import necessary libraries
import pygame
import pygame_gui as gui
import time

# Import parent object
from code.duckHunt import DuckHuntInstance

# This interface is a child interface of DuckHuntInstance, but optimised for testing an AI
class TestingInterface(DuckHuntInstance):

    """

    TestingInterface

    A child object of the DuckHuntInstance object.
    It is an object which hosts all functionalities needed for testing an AI, whilst reusing features
    of the parent object

    Dependencies:
        - pygame
        - pygame_gui (gui)
        - DuckHuntInstance

    """

    # Initialise
    def __init__(self, masterScreen, manager, aiModelLeft, aiModelRight, fxKey, sound, musicVol):

        # Inherit all attributes from parent
        super().__init__(masterScreen, manager, fxKey, sound, musicVol)

        # Store neural networks
        self.nnX = aiModelLeft
        self.nnY = aiModelRight

        # Default (starting) AI Guess [Centre of Screen]
        self.guess = (self.screen.screenSize[0] // 2, self.screen.screenSize[1] // 2)


    # Small function which rounds numbers to desired number of decimal places
    def _rounding(self, val, digits):
        return round(val + 10 ** (-len(str(val)) - 1), digits)

    # Subroutine which handles how the AI makes a guess
    def handleAI(self):

        # Get the position of each alive duck on the screen
        ducks = [(duck.image.get_abs_rect().centerx, duck.image.get_abs_rect().centery) for duck in self.duckList if
                 duck.alive is True]

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

        # If there was not a single hit
        if not (True in hitList or None in hitList):

            # Process it as a miss
            self._missed()

        # Increment the number of ducks hit
        self.duckHit += len([i for i in hitList if i is True])
        self.totalDuckHit += len([i for i in hitList if i is True])

        # Update the duck meter
        self.screen.duckImage.kill()
        duckMeter = pygame.transform.scale(pygame.image.load(f"images/duckMeter{self.duckHit}.png"), (240, 30))
        self.screen.duckImage = gui.elements.UIImage(
            pygame.Rect(self.screen.duckPanelSize[0] // 2 - 20, self.screen.duckPanelSize[1] // 2 - 20, 240, 30),
            duckMeter,
            container=self.screen.duckPanel,
            manager=self.manager)

        # Return the AI's shot as coordinates (for cursor drawing)
        return (int(self.guess[0]) - 50, int(self.guess[1]) - 50)

    # Overridden subroutine which creates pause screen to modify the button link to function dictionary
    def createPauseScreen(self):

        # Run parnet method
        super().createPauseScreen()

        # Adjust button link
        self.screen.functionDictionary[self.quitButton] = '4.3'

    # Overridden subroutine which creates game over screen to get rid of the naming text box, and to adjust button link
    def createGameOverScreen(self):

        # Run parent method
        super().createGameOverScreen()

        # Get rid of the name query
        self.nameQuery.kill()
        self.nameQueryLabel.kill()

        # Adjust button link
        self.screen.functionDictionary[self.replayButton] = '1'

    # Subroutine which saves the score of the AI
    def saveScores(self):

        # Adjust and format the current leaderboard
        name = self.screen.model
        index = self.leaderboardScores.index(self.indexItem)
        item = self.leaderboardScores[index]
        saveList = [i[1] for i in self.leaderboardScores]
        saveList[index] = (name, item[1][1])
        saveList = saveList[:10]

        # Write to text file
        with open("./data/game-data/scores.txt", "w") as f:
            for item in saveList:
                if saveList.index(item) == 9:
                    f.write(f"{item[0]}:{item[1]}")
                else:
                    f.write(f"{item[0]}:{item[1]}\n")

    # Overridden subroutine to process events going to this interface
    def processEvents(self, events):

        "Overridden to accomodate AI guessing"

        # Default AI Guess to None
        cursor = None

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

                    # Increment start round counter
                    self.startRoundCounter += 1

            # Check if there are currently no ducks on the screen, and that an end round sequence has not been initiated
            elif len(self.duckList) == 0 and not self.startRounds and not self.endRounds:

                # Check if 8 ducks hae been shot
                if self.duckCount >= 8 and self.endRounds is False:

                    # Initiate an 'end-round' sequence
                    self.endRounds = True

                    # End the round
                    self.endRound()

                else:

                    # Spawn ducks
                    self.spawnBirds()

                    # Check if end round sequence has trigggered
            elif self.endRounds is True:

                # Have we surpassed the counter (time buffer) for ending a round?
                if self.endRoundCounter > 120:

                    # Indicate end of end round sequence
                    self.endRounds = False
                    self.endRoundCounter = 0

                    # Start new round
                    self.startRound()

                else:

                    # Increment end round counter
                    self.endRoundCounter += 1

            else:
                tempList = []

                # Get coordinates of AI's shot
                cursor = self.handleAI()

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

            # Get time elpased from the start of the testing
            timeNow = time.time()
            seconds = int((timeNow - self.timer) % 60)

            # Update Display System Text
            self.screen.timeElapsed.set_text(
                f"Time: {int((timeNow - self.timer) // 60)}:{'0' * (1 if len(str(seconds)) < 2 else 0) + str(seconds)}")
            self.screen.score.set_text(f"Score: {'0' * (7 - len(str(self.score)))}{self.score}")
            self.screen.roundInfo.set_text(f"Round {self.round}")

            # Return coordinates of the AI's shot
            return cursor

        else:

            # If the game is not paused...
            if not self.paused:
                # For some reason, this is required to completely clear the screen for the game over screen
                self.screen.duckImage.kill()

# Import standard libaries
import pygame
import pygame_gui as gui
import time

# Import Duck Object
from code.ducks import Duck


class DuckHuntInstance:

    """

    Duck Hunt Object which contains the game itself, and all the methods needed to run it.

    Acts as a parent object for all other game interfaces


    """

    def __init__(self, masterScreen, manager, fxKey, volume, musicVol):

        """"
            - <masterScreen>    ---> Screen object which the interface is currently running on

            - <manager>         ---> Screen manager of the current screen which the interface is running on

            - <fxKey>           ---> Whether Sound FX has been enabled

            - <volume>         ---> Volume of SFX

            - <musicVol>       --> Volume of Music

        """

        # Initialise object variables
        self.game = False
        self.screen = masterScreen
        self.manager = manager
        self.FX = fxKey

        # Initialise all game variables
        self.score = 0
        self.duckList = []
        self.duckCount = 0
        self.duckHit = 0
        self.totalDuckCount = 0
        self.totalDuckHit = 0
        self.paused = False
        self.round = 0
        self.state = False
        self.startRoundCounter = 0
        self.startRounds = True
        self.endRounds = False
        self.endRoundCounter = 0
        self.timer = None
        self.leaderboardScores = []
        self.spawnDelay = False
        self.spawnCount = 0
        self.lifeState = 0
        self.pauseOverlay = None
        self.initial = False
        self.volume = volume

        # Create the game panel, where all sprites are and where the 'play area' is defined as
        self.gamePanel = gui.elements.UIPanel(
                                pygame.Rect((0, 0, 1920, 800)),
                                manager=self.manager,
                                starting_layer_height=0,
                                object_id="#game_panel")

        # Preload all sound effects
        self.gunshotFX = pygame.mixer.Sound(file="./sounds/gun-shot.ogg")
        self.gameOverFX = pygame.mixer.Sound(file="./sounds/game-over.ogg")

        # Set the volume of the sound effects and the music
        self.gunshotFX.set_volume(volume)
        self.gameOverFX.set_volume(musicVol)

        # Stores the image paths of the life panel
        self.lifeDict = {
            0 : "images/lifeBarGreen.png",
            1 : "images/lifeBarYellow.png",
            2 : "images/lifeBarRed.png",
            3 : "images/lifeBarEmpty.png"
        }

    # Subroutine which starts the game
    def startGame(self):

        # Update Object variables
        self.game = True
        self.state = False

        # Start the round
        self.startRound()

        # Start the self-timer
        self.timer = time.time()

    # Start a new round
    def startRound(self):
        self.state = True
        self.startRounds = True

        # Increment the round counter
        self.round += 1

        # Draw the 'new round' text
        panelSize = self.gamePanel.get_container().get_size()
        self.roundText = gui.elements.UILabel(
                                        pygame.Rect(panelSize[0] // 2 - 200, panelSize[1] // 2 - 75, 400, 150),
                                        f"Round {self.round}",
                                        container=self.gamePanel,
                                        manager=self.manager,
                                        object_id="#round_text")

    # Subroutine which spawns new ducks
    def spawnBirds(self):

        # Initially, make sure once the pause screen has been created, hide it to avoid re-rendering
        if self.initial:

            # Hide the pause screen
            self.pauseGame(False)
            self.initial = False

        # Increment the total amount of ducks spawned, and the current cycle count
        self.duckCount += 2
        self.totalDuckCount += 2

        # Create two new duck objects in a list
        self.duckList = [Duck(self.round, self.manager, self.gamePanel, self.FX, self.volume),
                         Duck(self.round, self.manager, self.gamePanel, self.FX, self.volume)]

    # Subroutine which pauses the game
    def pauseGame(self, key=True):

        # Check whether it should pause or resume the game
        if key:

            # Update the state of the game
            self.state = 'paused'
            self.paused = True

            # Create/show the pause screen
            self.createPauseScreen() if self.pauseOverlay is None else self.pauseOverlay.show()

        else:

            # Update the state of the game
            self.state = True
            self.paused = False

            # Hide the pause screen
            self.pauseOverlay.hide()

    # Subroutine which draws the pause screen (creates all the elements)
    def createPauseScreen(self):

        # Create the graphical elements
        self.pauseOverlay = gui.elements.UIPanel(
                                    pygame.Rect((0, 0, 1925, 1080)),
                                    manager=self.manager,
                                    starting_layer_height=5,
                                    object_id="#pause_overlay")

        pauseOverlaySize = self.pauseOverlay.get_container().get_size()
        self.pauseBox = gui.elements.UIPanel(
                                    pygame.Rect(pauseOverlaySize[0] // 2 - 500, pauseOverlaySize[1] // 2.5 - 200, 1000, 400),
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
                                    pygame.Rect(pauseBoxSize[0] // 4 - 100, pauseBoxSize[1] // 3 * 2 - 25, 200, 50),
                                    "Quit",
                                    manager=self.manager,
                                    container=self.pauseBox,
                                    object_id="#quit_button")

        self.resumeButton = gui.elements.UIButton(
                                    pygame.Rect((pauseBoxSize[0] // 4 * 3) - 150, pauseBoxSize[1] // 3 * 2 - 50, 300, 100),
                                    "Resume",
                                    manager=self.manager,
                                    container=self.pauseBox,
                                    object_id="#resume_button")

        # Link the buttons to the function dictionary in the master screen
        self.screen.functionDictionary[self.quitButton] = '4.2'
        self.screen.functionDictionary[self.resumeButton] = '4.1'

    # Subroutine which creates the 'game over' screen
    def createGameOverScreen(self):

        # Create graphical elements
        self.gameEndOverlay = gui.elements.UIPanel(
            pygame.Rect((0, 0, 1925, 1080)),
            manager=self.manager,
            starting_layer_height=5,
            object_id="#game_over_overlay")

        gameEndOverlaySize = self.gameEndOverlay.get_container().get_size()
        self.endBox = gui.elements.UIPanel(
            pygame.Rect(gameEndOverlaySize[0] // 2 - 700, gameEndOverlaySize[1] // 2.25 - 400, 1400, 800),
            manager=self.manager,
            container=self.gameEndOverlay,
            starting_layer_height=0,
            object_id="#game_over_box")

        endBoxSize = self.endBox.get_container().get_size()

        self.endHeader = gui.elements.UILabel(
            pygame.Rect(endBoxSize[0] // 2 - 300, endBoxSize[1] // 6 - 50, 600, 100),
            "Game Over!",
            manager=self.manager,
            container=self.endBox,
            object_id="#game_over_header")

        # Get the scores recorded and update it onto the text box
        scores = self.processScores()
        self.leaderboard = gui.elements.UITextBox(
            f"<font face='calibri' color='#FFFFFF' size=6.5><b>Leaderboard:</b> <br> <br>"
            f"{'<br> <br>'.join(scores)}"
            f"</font>",
            pygame.Rect(endBoxSize[0] // 5 * 1.6 - 150, endBoxSize[1] // 2 - 150, 300, 300),
            manager=self.manager,
            container=self.endBox,
            object_id="#leaderboard")

        # Get the total time spent on the game
        timeNow = time.time()
        seconds = int((timeNow - self.timer) % 60)

        self.endGameBriefing = gui.elements.UITextBox(
            f"<font face='calibri' color='#FFFFFF' size=6.5>"
            f"Final Score:        {self.score}<br> <br>"
            f"Time Spent:       {int((timeNow - self.timer) // 60)}:{'0' * (1 if len(str(seconds)) < 2 else 0) + str(seconds)}<br> <br>"
            f"Round:                {self.round}<br> <br>"
            f"Accuracy:           {int((self.totalDuckHit / self.totalDuckCount if self.totalDuckCount != 0 else 1) * 100)}%</font>",
            pygame.Rect(endBoxSize[0] // 5 * 3.6 - 200, endBoxSize[1] // 2 - 150, 400, 300),
            manager=self.manager,
            container=self.endBox,
            parent_element=self.endBox,
            object_id="#game_over_text")

        self.nameQueryLabel = gui.elements.UILabel(
            pygame.Rect(endBoxSize[0] // 2 + 35, endBoxSize[1] // 3 * 2 + 10, 300, 50),
            "Enter Name:",
            manager=self.manager,
            container=self.endBox,
            object_id="#name_label"
        )

        # Create a text box where the user can write their name
        self.nameQuery = gui.elements.UITextEntryLine(
            pygame.Rect(endBoxSize[0] // 2 + 310, endBoxSize[1] // 3 * 2 + 10, 180, 100),
            manager=self.manager,
            container=self.endBox,
            object_id="#name_entry_box")

        # Limit the textbox to 10 characters, default value is 'Human', and forbids special characters
        self.nameQuery.set_text_length_limit(10)
        self.nameQuery.set_text("Human")
        self.nameQuery.set_forbidden_characters(["\\", "/", ".", "@", "-", " ", "`", "~", "{", "}", ",", "'", "\"", "%", "_", "$", "~", "#", '&', "^"])

        self.exitButton = gui.elements.UIButton(
            pygame.Rect(endBoxSize[0] // 4 * 1.25 - 100, endBoxSize[1] // 6 * 5 - 25, 200, 50),
            "Exit",
            manager=self.manager,
            container=self.endBox,
            object_id="#quit_button")

        self.replayButton = gui.elements.UIButton(
            pygame.Rect(endBoxSize[0] // 4 * 2.75 - 175, endBoxSize[1] // 6 * 5 - 25, 350, 50),
            "Play Again",
            manager=self.manager,
            container=self.endBox,
            object_id="#resume_button")

        # Link the buttons to the function dictionary of the master screen
        self.screen.functionDictionary[self.replayButton] = '0'
        self.screen.functionDictionary[self.exitButton] = '5'

        # Kill all other elements that are no longer needed (the system text)
        self.screen.timeElapsed.kill()
        self.screen.roundInfo.kill()
        self.screen.score.kill()
        self.screen.panel.kill()

    # Subroutine which unpacks the recorded high scores
    def processScores(self):
        with open("./data/game-data/scores.txt", "r") as f:
            for i in f.readlines():
                i = i.rstrip()
                i = i.split(":")

                # Appends the scores to a list
                self.leaderboardScores.append([f"{i[1]} [{i[0]}]", (i[0], int(i[1]))])

            # Formats each score entry
            self.indexItem = [f"<b><i>{self.score} (You)</i></b>", ("##########", self.score)]
            self.leaderboardScores.append(self.indexItem)

            # Sort the list
            self.leaderboardScores.sort(key=lambda x: x[1][1], reverse=True)

        # Return the sorted high score list with the user's score inserted
        return [i[0] for i in self.leaderboardScores]

    # Subroutine which saves the scores by writing to text file
    def saveScores(self):

        # Get the name chosen by the user
        name = self.nameQuery.get_text()

        # Gets the last item (capped at 9 entries)
        index = self.leaderboardScores.index(self.indexItem)
        item = self.leaderboardScores[index]

        # Creates a list with the names and scores in the leaderboard
        saveList = [i[1] for i in self.leaderboardScores]

        # If name entry is blank, return to default value
        if name == "":
            name = "Human"

        # Format list
        saveList[index] = (name, item[1][1])
        saveList = saveList[:10]

        # Write to text file
        with open("./data/game-data/scores.txt", "w") as f:
            for item in saveList:
                if saveList.index(item) == 9:
                    f.write(f"{item[0]}:{item[1]}")
                else:
                    f.write(f"{item[0]}:{item[1]}\n")

    # Subroutine which handles the ending of a round
    def endRound(self):

        # Reset round variables, including life
        self.duckCount = 0
        self.duckHit = 0
        self.lifeState = 0

        # Update Life image
        self.updateLife()

        # Reset the duck meter
        self.screen.duckImage.kill()
        duckImage = pygame.transform.scale(pygame.image.load("images/duckMeter0.png"), (240, 30))
        self.screen.duckImage = gui.elements.UIImage(
                                    pygame.Rect(self.screen.duckPanelSize[0] // 2 - 20, self.screen.duckPanelSize[1] // 2 - 20, 240, 30),
                                    duckImage,
                                    container=self.screen.duckPanel,
                                    manager=self.manager)

    # Subroutine which updates the life meter
    def updateLife(self):

        # Kill the current image
        self.screen.lifeImage.kill()

        # Redraw the image
        newLifeBar = pygame.transform.scale(pygame.image.load(self.lifeDict[self.lifeState]), (240, 30))
        self.screen.lifeImage = gui.elements.UIImage(
            pygame.Rect(self.screen.lifePanelSize[0] // 2 - 80, self.screen.lifePanelSize[1] // 2 - 15,
                        240, 30),
            newLifeBar,
            container=self.screen.lifePanel,
            manager=self.manager)

    # Subroutine which handles instances when the user has missed a duck
    def _missed(self):

        # Advances the life state by 1 (closer to death)
        self.lifeState += 1

        # Update life image
        self.updateLife()

        # Checks if user has exhausted all lives
        if self.lifeState == 3:

            # End the game
            return self.endGame()

    # Subroutine which handles the ending of a game
    def endGame(self):

        # Indicate the game has finished
        self.game = False
        self.state = False

        # Kill all ducks that remain on the screen
        if len(self.duckList) != 0:
            for duck in self.duckList:
                duck.image.kill()
            self.duckList = []

        # Create the game over screen
        self.createGameOverScreen()

        # Play the game over music
        self.gameOverFX.play()

        # Set the user's mouse to be visible again
        pygame.mouse.set_visible(True)

    # Subroutine which handles a user's click
    def handleClicks(self, valid):

        # Checks if the user has clicked in the game area, and that the game is not paused
        if valid and len(self.duckList) != 0 and self.paused is False and self.game:

            # Check if sound effects are allowed
            if self.FX:

                # Play gunshot noise
                self.gunshotFX.play()

            # Check to see whether each duck has been hit. checkClick returns True/False
            hitList = [duck.checkClick(pygame.mouse.get_pos()) for duck in self.duckList]

            # If there hasn't been a single hit
            if not (True in hitList or None in hitList):

                # Process it as a miss
                self._missed()

            # Increment the amount of ducks that have been hit accoridng to the number of Trues
            self.duckHit += len([i for i in hitList if i is True])
            self.totalDuckHit += len([i for i in hitList if i is True])

            # Redraw the duck meter
            self.screen.duckImage.kill()
            duckMeter = pygame.transform.scale(pygame.image.load(f"images/duckMeter{self.duckHit}.png"), (240, 30))
            self.screen.duckImage = gui.elements.UIImage(
                                    pygame.Rect(self.screen.duckPanelSize[0] // 2 - 20, self.screen.duckPanelSize[1] // 2 - 20, 240, 30),
                                    duckMeter,
                                    container=self.screen.duckPanel,
                                    manager=self.manager)

    # Subroutine which handles all events by the user when interacting with this interface
    def processEvents(self, events):

        # Check if game is paused/has started
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

                # Go through each duck still alive
                for duck in self.duckList:

                    # Update the duck, and animate it
                    duck.update(self.state, events)
                    duck.tick(self.state)

                    # Check if duck is completely dead
                    if duck.completelyDead is True:

                        # Add score
                        self.score += duck.points

                    # Duck Escaped... do nothing
                    elif duck.escaped is True:
                        pass

                    else:

                        tempList.append(duck)

                # Update duck list with remaining alive ducks
                self.duckList = tempList

            # Get time that has passed since starting the game
            timeNow = time.time()
            seconds = int((timeNow -self.timer) % 60)

            # Update the system display text
            self.screen.timeElapsed.set_text(f"Time: {int((timeNow - self.timer) // 60)}:{'0' * (1 if len(str(seconds)) < 2 else 0) + str(seconds)}")
            self.screen.score.set_text(f"Score: {'0'*(7-len(str(self.score)))}{self.score}")
            self.screen.roundInfo.set_text(f"Round {self.round}")

        else:

            # If the game is not paused...
            if not self.paused:

                # For some reason, this is required to completely clear the screen for the game over screen
                self.screen.duckImage.kill()

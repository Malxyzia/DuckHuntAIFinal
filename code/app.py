# Import all necessary libraries
# Standard Libraries:
import pygame
import ctypes
import pygame_gui as gui
import pickle
import os
import shutil

# Written Modules
from code.mainScreen import MainScreenInstance
from code.playScreen import PlayScreenInstance
from code.trainScreen import TrainScreenInstance
from code.settingsScreen import SettingsScreenInstance
from code import NN
from code.duckHunt import DuckHuntInstance
from code.trainingInterface import TrainingInterface
from code.testingInterface import TestingInterface

class App:

    """
        Object representing the App itself.
        Utilises separate object instances of each 'mode' in order to manage different screen states.

        Dependencies:
            - pygame
            - ctypes
            - pygame_gui (gui)
            - os
            - shutill


    """


    # Initialise Object
    def __init__(self, screenSize):

        # Initialise Pygame Library
        pygame.init()

        # Create Program Window
        pygame.display.set_caption('Duck Hunt: AI Edition')
        icon = pygame.transform.scale(pygame.image.load("images/icon.png"), (32, 32))
        pygame.display.set_icon(icon)

        # Adjust DPI Awareness for Windows OS
        awareness = ctypes.c_int()
        errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))

        # Set DPI Awareness  (Windows 10 and 8)
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)

        # Initialise program clock
        self.clock = pygame.time.Clock()

        # Pre-load all background images and sizes
        self.bgSize = (1925, 1085)
        self.background = pygame.Surface(self.bgSize)
        self.mainBG = pygame.transform.scale(pygame.image.load("images/editedStage.png"), self.bgSize)
        self.trainBG = pygame.transform.scale(pygame.image.load("images/trainBackground.png"), self.bgSize)
        self.configBG = pygame.transform.scale(pygame.image.load("images/settingsScreen.png"), self.bgSize)

        # Create and display window
        self.windowSurface = pygame.display.set_mode(screenSize)

        # Initialise App Constants
        self.running = True
        self.screenSize = screenSize

        # Preload + Create screen managers to handle graphical elements
        # Note: The screen codes for each screen are the following:
        # 0 = Play Screen, 1 = Train Screen, 2 = Settings Screen, 5 = Main Menu
        self.managers = {
            '0' : gui.UIManager(self.screenSize, "./themes/playScreen.json"),
            '1' : gui.UIManager(self.screenSize, "./themes/trainScreen.json"),
            '2' : gui.UIManager(self.screenSize, "./themes/settingsScreen.json"),
            '5' : gui.UIManager(self.screenSize, "./themes/mainScreen.json")
        }

        # Set Current Screen Manager to Main Menu
        self.manager = self.managers['5']

        # Create an object instance for the main screen
        self.currentScreen = MainScreenInstance(self.screenSize, self.manager)

        # Initialise Play Screen Variables / Constants
        self.game = False
        self.validate = True
        self.gameInstance = None

        # Create custom event for play screen
        self.gameEvent = pygame.USEREVENT + 1

        # Preload cursor images and display surfaces
        self.cursorSurface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.cursorImageClassic = pygame.transform.scale(pygame.image.load("images/crosshair.png"), (100, 100))
        self.cursorImageComplex = pygame.transform.scale(pygame.image.load("images/crosshair1.png"), (100, 100))
        self.cursorImageSimple = pygame.transform.scale(pygame.image.load("images/crosshair2.png"), (100, 100))
        self.cursorRect = (self.screenSize[0] // 2 - 50, self.screenSize[1] // 2 - 50)

        # Initialise Train Screen Variables / Constants
        self.training = False
        self.initialTraining = False
        self.trainInstance = None
        self.trainSpeedDict = {}
        self.trainDiffDict = {}
        self.model = ()
        self.testOption = False
        self.trainSpeedDict = None
        self.trainDiffDict = None

        # Create custom event for train screen
        self.initialTrainEvent = pygame.USEREVENT + 2
        self.trainEvent = pygame.USEREVENT + 3

        # Initialise Function Dictionary
        # This links all the buttons from other object instances to functions in this object.
        # Ensures all interactable elements are linked to processes
        self.masterDirectory = {
                '0' : self.play,
                '1' : self.train,
                '1.1' : self.initialTrainSelection,
                '1.2' : self.returnInitialTraining,
                '1.3' : self.processTraining,
                '1.4' : self.swapModes,
                '1.5' : self.adjustTrainingSpeed,
                '1.6' : self.adjustTrainingDifficulty,
                '1.7' : self.saveQuit,
                '2' : self.settings,
                '2.1' : self.swapPage,
                '2.2' : self.bgSwap,
                '2.3' : self.handlePSOptions,
                '2.4' : self.handleTSOptions,
                '2.5' : self.handleTrainSetOptions,
                '2.6' : self.handleBufferOptions,
                '2.7' : self.writeSave,
                '2.8' : self.clearScores,
                '2.9.1' : self.promptWarning,
                '2.9.2' : self.returnSettingScreen,
                '2.9.3' : self.deleteModel,
                '3' : self.quit,
                '4' : self.pause,
                '4.1' : self.resume,
                '4.2' : self.gameOver,
                '4.3' : self.testOver,
                '5': self.returnMenu,
            }


        # Initialise all setting variables

        self.settingsPanelDict = None
        self.config = False

        self.bgConfig = [0, 0, 1]
        self.backgroundOptions = [
            ("Default", self.mainBG),
            ("Serenity", self.trainBG),
            ("Sunset", self.configBG)
        ]

        self.bgLeftButtons = None
        self.bgRightButtons = None
        self.crosshair = 0
        self.tCrosshair = 0
        self.crosshairOptions = [
            ("Classic", self.cursorImageClassic),
            ("Complex", self.cursorImageComplex),
            ("Simple", self.cursorImageSimple)
        ]

        self.optionsPS = None
        self.gameFX = True
        self.optionsTS = None
        self.trainFX = True

        self.trainSetOptions = ["500", "1000", "5000", "10000"]
        self.bufferOptions = [
            ("Slow", 8),
            ("Normal", 4),
            ("Fast", 2),
            ("Instant", 0)
        ]

        self.optionsTrainingSet = None
        self.optionsBuffer = None
        self.trainingSetNum = 2
        self.bufferNum = 1
        self.masterSettings = []

        # Create custom event for settings screen
        self.configEvent = pygame.USEREVENT + 4

        # Sound Variables
        # Stores previous values for sound/music
        self.prevMusic = 0
        self.prevSound = 0

        # Current values for sound/music
        self.musicVol = 0.5
        self.soundVol = 0.5

        # Unload settings from config.txt and apply them to the app
        self._unloadSettings()

        # Play Initial Menu Music
        pygame.mixer.music.load("./sounds/start1.mp3")
        pygame.mixer.music.set_volume(self.musicVol)
        pygame.mixer.music.play()

        # Draw background onto screen
        self.background.blit(self.backgroundOptions[self.bgConfig[0]][1], (-2, -2))

    # Subroutine which reads config.txt and applies all settings from the text file into the app
    def _unloadSettings(self):

        # Open text file for input
        with open("./data/game-data/config.txt", "r") as f:

            # Reads lines and strips newline characters and white space away
            temp = [line.rstrip() for line in f.readlines()]

            # Assign values to relevant app variables for different settings
            self.musicVol = float(temp[0])
            self.soundVol = float(temp[1])
            self.bgConfig = [int(temp[2]), int(temp[3]), int(temp[4])]
            self.crossHair = int(temp[5])
            self.tCrosshair = int(temp[6])
            self.gameFX = bool(int(temp[7]))
            self.trainFX = bool(int(temp[8]))
            self.trainingSetNum = int(temp[9])
            self.bufferNum = int(temp[10])

    # Subroutine which sets the app's running attribute to false, causing it to safely quit.
    def quit(self, x=None):
        self.running = False

    # Subroutine which is called whenever the pause button is pressed.
    # It will pause the game/training and disable the pause button
    def pause(self, x=None):

        # Disable pause button to prevent users from clicking it whilst paused
        self.currentScreen.pauseButton.disable()

        # Pauses the game/training depending on whether it the user is on the train or play screen
        self.trainInstance.pauseGame() if self.training else self.gameInstance.pauseGame()

    # Subroutine which resumes the training/game and enables the pause button
    def resume(self, x=None):

        # Enable pause button, making it interactable again
        self.currentScreen.pauseButton.enable()

        # Unpauses the game
        self.trainInstance.pauseGame(False) if self.training else self.gameInstance.pauseGame(False)

    # Subroutine which starts the play section of the app.
    def play(self, button):

        # Clears the screen and resets the manager.
        self.manager.clear_and_reset()

        # Starts queueing the custom event for play screen. This custom event enables the app to observe the screen
        # and respond to events that may occur even if the user is not actively interacting with the screen.
        pygame.time.set_timer(self.gameEvent, 6)

        # Set manage to play screen manager
        self.manager = self.managers['0']

        # Reset and redraw the background
        self.background.fill((0, 0, 0))
        self.background.blit(self.backgroundOptions[self.bgConfig[1]][1], (-2, -2))

        # Redraw the cursor
        self.cursorSurface.fill((0, 0, 0, 0))
        self.cursorSurface.blit(self.crosshairOptions[self.crosshair][1], (0, 0))

        # Stop any music. Ensures music from a different screen does not carry over
        pygame.mixer.music.stop()

        # Check to see if user is replaying the game (from game over sequence)
        if self.gameInstance is not None:
            if button == self.gameInstance.replayButton:

                # Save/record scores
                self.gameInstance.saveScores()

        # Create a play instance object
        self.currentScreen = PlayScreenInstance(self.screenSize, self.manager)

        # Create the Play Screen and initialise game variable
        self.currentScreen.createScreen()
        self.game = True

        # Set the mouse cursor to be invisible
        pygame.mouse.set_visible(False)

        # Create game instance object
        self.gameInstance = DuckHuntInstance(self.currentScreen, self.manager, self.gameFX, self.soundVol, self.musicVol)

        # Start the game
        self.gameInstance.startGame()

    # Subroutine which handles returning to the main menu screen
    def returnMenu(self, x=None):

        # Clears the screen and resets the manager.
        self.manager.clear_and_reset()

        # Reset all custom events and stop them from posting
        pygame.time.set_timer(self.gameEvent, 0)
        pygame.time.set_timer(self.initialTrainEvent, 0)
        pygame.time.set_timer(self.trainEvent, 0)
        pygame.time.set_timer(self.configEvent, 0)

        # Save scores (check whether it is from the testing section or the play section)
        if self.training and self.testOption:
            self.trainInstance.saveScores()
        elif self.game:
            self.gameInstance.saveScores()

        # Stop all music/SFX from playing
        pygame.mixer.music.stop()
        pygame.mixer.stop()

        # Reset Game and Train Variables
        self.game = False
        self.training = False
        self.initialTraining = False
        self.gameInstance = None
        self.trainInstance = None

        # Redraw Background
        self.background.fill((0, 0, 0))
        self.background.blit(self.backgroundOptions[self.bgConfig[0]][1], (-2, -2))

        # Set current screen manager to main menu manager
        self.manager = self.managers['5']

        # Create a new main menu instance
        self.currentScreen = MainScreenInstance(self.screenSize, self.manager)

        # Play main menu tune
        pygame.mixer.music.load("./sounds/start1.mp3")
        pygame.mixer.music.set_volume(self.musicVol)
        pygame.mixer.music.play()

        # Create main menu screen
        self.currentScreen.createScreen()

    # Subroutine which handles when a game over situation occurs.
    # This is usually when the user forcibly ends a game, such as quitting from the pause menu.
    def gameOver(self, x=None):

        # Checks if the pause menu is still on the screen
        if self.gameInstance.paused:

            # Erase the pause screen
            self.gameInstance.pauseGame(False)

        # End the game by calling the subroutine attached to the game object
        self.gameInstance.endGame()

    # Subroutine similar to self.gameOver(), except that it is applied to a game over situation in the test section
    # This is usually when the user forcibly ends the test session; by quitting from pause menu
    def testOver(self, x=None):

        # Checks if the pause menu is still on the screen
        if self.trainInstance.paused:

            # Erase the pause screen
            self.trainInstance.pauseGame(False)

        # End the game by calling the subroutine attached to the train object
        self.trainInstance.endGame()

    # Subroutine which handles launching the train section of the app
    def train(self, x=None):

        # Clears the screen and resets the manager.
        self.manager.clear_and_reset()

        # Starts queueing the custom event to check for certain events independent of the user's interaction
        pygame.time.set_timer(self.initialTrainEvent, 6)

        # Set screen manager to the train sreen manager
        self.manager = self.managers['1']

        # Stop all audio from the previous screen
        pygame.mixer.music.stop()
        pygame.mixer.stop()

        # Redraw background
        self.background.fill((0, 0, 0))
        self.background.blit(self.backgroundOptions[self.bgConfig[2]][1], (-2, -2))

        # Initialise Training Variables
        self.initialTraining = True
        self.testOption = False

        # Create train screen object instance
        self.currentScreen = TrainScreenInstance(self.screenSize, self.manager)

        # Create and draw the initial train screen
        self.currentScreen.createInitialScreen()

    # Subroutine which handles the transition from the initial train screen to the train/test section
    def initialTrainSelection(self, x=None):

        # Get the user's selection (for AI Model)
        self.model = self.currentScreen.dropDown.selected_option

        # Check if the selection is to create a new AI
        if self.model == "New AI":

            # Create new neural network model objects
            nnX = NN.NeuralNetwork([4, 2, 2], 0.001, 10)
            nnY = NN.NeuralNetwork([4, 2, 2], 0.001, 10)

            # Variable to reference the current model being used by the app
            self.model = (nnX, nnY, self.model)

            # Create the 'name the model' screen and exit this subroutine
            return self.currentScreen.createNewModelScreen()

        else:

            # Open and read the selected AI Models
            with open(f"data/ai-models/{self.model}/{self.model}Left.pkl", "rb") as f:
                nnX= pickle.load(f)
            with open(f"data/ai-models/{self.model}/{self.model}Right.pkl", "rb") as g:
                nnY = pickle.load(g)

            # Variable to reference the current model being used by the app
            self.model = (nnX, nnY, self.model)

        # Proceed to launching the train/test interface
        self.processTraining(True)

    # Subroutine which handles an instance where the user returns to the initial training screen
    # by cancelling the creation of a new AI model
    def returnInitialTraining(self, x=None):

        # Stop any audio from overlaying from the previous screen
        pygame.mixer.stop()

        # Kill the naming overlay box
        self.currentScreen.namingOverlay.kill()

    # Subroutine which handles the transition from the initial train screen to the testing/training interface
    def processTraining(self, key):

        # Check to see if a new model has been created [key is passed from self.initialTrainingSelection() if True]
        if key != True:

            # Get the name the user has entered in the text box
            name = self.currentScreen.nameEntry.get_text()

            # Check for invalid names and display the appropriate error message
            if name == "":
                self.currentScreen.errorMessage.visible = 1
                self.currentScreen.errorMessage.set_text("Please enter a valid name")
                return

            elif name in sorted([f.name for f in os.scandir("./data/ai-models") if f.is_dir()]):
                self.currentScreen.errorMessage.visible = 1
                self.currentScreen.errorMessage.set_text("A model with that name already exists")
                return

            # If the name is acceptable, create a new folder to store the AI Models
            os.mkdir(f"data/ai-models/{name}")

        else:

            # Obtain the name of the model
            name = self.model[2]

        # Set the training/testing screen's model attribute to the name of the model for reference
        self.currentScreen.model = name

        # Recalibrate the training/testing variables
        self.initialTraining = False
        self.training = True

        # Update the queueing of custom events.
        # No longer need the initial training screen observer event, instead queue the train screen observer event
        pygame.time.set_timer(self.initialTrainEvent, 0)
        pygame.time.set_timer(self.trainEvent, 6)

        # Clear and reset the screen
        self.manager.clear_and_reset()

        # Check whether app should launch test mode or train mode
        # Then, create the appropriate interface instance object and create the screen
        if self.testOption:
            self.trainInstance = TestingInterface(self.currentScreen, self.manager, self.model[0], self.model[1], self.trainFX,
                                                  self.soundVol, self.musicVol)
            self.currentScreen.createTestScreen()

        else:
            self.trainInstance = TrainingInterface(self.currentScreen, self.manager, self.model[0], self.model[1], self.trainFX,
                                                  self.soundVol, self.musicVol, self.bufferOptions[self.bufferNum][1],
                                                   self.trainSetOptions[self.trainingSetNum])
            self.currentScreen.createScreen()

            # Initialise dictionaries to house the options and their relating values of the training interface
            # These are used to adjust the training speed/difficulty of the ducks
            # Structure: <Button> : (<value>, <active? (0 = inactive, 1 = active)>, <Minor Display Text>, <Display Text>)

            self.trainSpeedDict = {
                self.currentScreen.slowButton: (2, 0, '0.5x'),
                self.currentScreen.stopButton: (-1, 0, '||'),
                self.currentScreen.standardButton: (1, 1, '1x'),
                self.currentScreen.fastButton: (0, 0, '2x')
            }
            self.trainDiffDict = {
                self.currentScreen.easyButton: [1, 1, 'Easy', 'Easy'],
                self.currentScreen.normalButton: [5, 0, 'Norm', 'Normal'],
                self.currentScreen.hardButton: [10, 0, 'Hard', 'Hard']
            }

        # Redraw the cursor with crosshair
        self.cursorSurface.fill((0, 0, 0, 0))
        self.cursorSurface.blit(self.crosshairOptions[self.tCrosshair][1], (0, 0))

        # Initiate the training/testing interface
        self.trainInstance.startGame()

    # Subroutine which handles the swapping between choosing to train or test the AI in the initial train screen
    def swapModes(self, x=None):

        # Check whether the test option has been selected
        if not self.testOption:

            # Indicate test option has now been selected
            self.testOption = True

            # Disable the test toggle and enable the train toggle
            self.currentScreen.testToggleButton.disable()
            self.currentScreen.trainToggleButton.enable()

        else:

            # Indicate test option has been unselected
            self.testOption = False

            # Disable the train toggle and enable the test toggle
            self.currentScreen.testToggleButton.enable()
            self.currentScreen.trainToggleButton.disable()

    # Subroutine which handles the event where the user adjusts the training speed of the AI
    def adjustTrainingSpeed(self, button):

        # Go through each button in the dictionary and check to see if that button matches the button the user has
        # has pressed. Apply the values associated with the button, and enable + deselect the rest of the buttons
        for item in self.trainSpeedDict:

            # Check if buutton matches the button clicked by user
            if item == button and self.trainSpeedDict[item][1] == 0:

                # Indicate it is now active
                self.trainSpeedDict[item] = (self.trainSpeedDict[item][0], 1, self.trainSpeedDict[item][2])

                # Apply the changes in values to the training interface
                self.trainInstance.speedCap = self.trainSpeedDict[item][0]

                # Change the text on the display to indicate change
                self.currentScreen.speedLabel.set_text(f"Current Speed: {self.trainSpeedDict[item][2]}")
                self.currentScreen.speedDisplay.enable()
                self.currentScreen.speedDisplay.set_text(f"Game Speed: {self.trainSpeedDict[item][2]}")
                self.currentScreen.speedDisplay.rebuild()
                self.currentScreen.speedDisplay.disable()

                # Disable the button that has been seleceted
                button.disable()

            else:

                # Indicate that the button is not active
                self.trainSpeedDict[item] = (self.trainSpeedDict[item][0], 0, self.trainSpeedDict[item][2])

                # Enable the button (to be interactable)
                item.enable()

    # Subroutine which, similar to the above subroutine, handles the the event where the user adjusts
    # the difficulty of the ducks in training
    def adjustTrainingDifficulty(self, button):

        # Go through each button in the dictionary and check to see if that button matches the button the user has
        # has pressed. Apply the values associated with the button, and enable + deselect the rest of the buttons
        for item in self.trainDiffDict:

            # Check if buutton matches the button clicked by user
            if item == button and self.trainDiffDict[item][1] == 0:

                # Indicate it is now active
                self.trainDiffDict[item][1] = 1

                # Apply the changes in values to the training interface
                self.trainInstance.round = self.trainDiffDict[item][0]

                # Change the text on the display to indicate change
                self.currentScreen.difficultyLabel.set_text(f"Current Difficulty: {self.trainDiffDict[item][2]}")
                self.currentScreen.difficultyDisplay.set_text(f"Duck Difficulty: {self.trainDiffDict[item][3]}")
                self.currentScreen.difficultyDisplay.rebuild()
                self.currentScreen.difficultyDisplay.disable()

                # Disable the button that has been seleceted
                button.disable()

            else:

                # Indicate that the button is not active
                self.trainDiffDict[item][1] = 0

                # Enable the button (to be interactable)
                item.enable()

    # Subroutine which is triggered when the user exits training mode. Saves the AI Models.
    def saveQuit(self, x=None):

        # Save AI Models through the object's save method
        self.trainInstance.nnX.save(self.currentScreen.model, "Left")
        self.trainInstance.nnY.save(self.currentScreen.model, "Right")

        # Return to initial train screen
        self.train()


    def settings(self, x=None):

        # Clear and reset the screen
        self.manager.clear_and_reset()

        # Queue the settings screen observer event to observe the settings screen for certain subroutines
        pygame.time.set_timer(self.configEvent, 6)

        # Indicate that the user is currently on the settings screen
        self.config = True

        # Set the screen manager to the settings manager
        self.manager = self.managers['2']

        # Stop all audio from previous screen
        pygame.mixer.music.stop()

        # Redraw background
        self.background.fill((0, 0, 0))
        self.background.blit(self.configBG, (-2, -2))

        # Create settings screen instance object for reference then create/draw the screen
        self.currentScreen = SettingsScreenInstance(self.screenSize, self.manager, self)
        self.currentScreen.createScreen()
        self.currentScreen.generatePlaySettings()
        self.currentScreen.generateTrainSettings()

    # Subroutine which handles the swapping of 'pages' inside the settings screen.
    def swapPage(self, button):

        # Check to see if this is the first time (in runtime) that a page is being swapped
        # Note: The reason this can't be initialised at the start is because these elements don't exist until
        # the object instance is created. Which only occurs when a screen is launched
        if self.settingsPanelDict is None:

            # If so, link the buttons to their corresponding display panel
            # Format: <Button> : [<Active? (0 = False, 1 = True>, <Display Panel>]
            self.settingsPanelDict = {
                self.currentScreen.generalButton : [1, self.currentScreen.generalPanel],
                self.currentScreen.playButton : [0, self.currentScreen.playPanel],
                self.currentScreen.trainButton : [0, self.currentScreen.trainPanel]
            }

        # Go through each button in the dictionary and see if it matches the one the user has clicked
        # If so, hide the current display panel and display the new display panel
        for item in self.settingsPanelDict:

            # Check if the buttons match
            if item == button and self.settingsPanelDict[button][0] == 0:

                # Indicate the new panel is active
                self.settingsPanelDict[item][0] = 1

                # Disable button from being pressed
                item.disable()

                # Redraw panels
                self.currentScreen.currentPage.hide()
                self.currentScreen.currentPage = self.settingsPanelDict[item][1]
                self.currentScreen.currentPage.show()
                self.currentScreen.deleteButton.enable()
                self.currentScreen.deleteButton.disable()
                self.currentScreen.aiSelectionBox.rebuild()

            else:

                # Indicate display panel is not active
                self.settingsPanelDict[item][0] = 0

                # Make the button interactable
                item.enable()

    # Subroutine which handles the buttons and graphical elements involved in changing the backgrounds in the settings
    def bgSwap(self, button):

        # Check whether this is occuring the first time (in runtime)
        if self.bgLeftButtons is None:

            # Initialise and link the screen elements together (left buttons, right buttons, and text in the middle)
            self.bgLeftButtons = [self.currentScreen.arrowLeftMS, self.currentScreen.arrowLeftPS,
                                  self.currentScreen.arrowLeftTS]

            self.bgRightButtons = [self.currentScreen.arrowRightMS, self.currentScreen.arrowRightPS,
                                  self.currentScreen.arrowRightTS]

            self.optionCapsuleLabels = [self.currentScreen.optionCapsuleMS, self.currentScreen.optionCapsulePS,
                                        self.currentScreen.optionCapsuleTS]

        # Check if the button pressed belonged to the left side or the right side
        if button in self.bgLeftButtons:

            # Get the index of the button which was pressed
            index = self.bgLeftButtons.index(button)

            # Shift the corresponding option (Main screen, play screen or train screen) to the left
            self.bgConfig[index] -= 1
        else:
            # Get the
            # index of the button which was pressed
            index = self.bgRightButtons.index(button)

            # Shift the corresponding option (Main screen, play screen or train screen) to the right
            self.bgConfig[index] += 1

        # Check each item in background configuration and rectify any values that exceed the boundaries
        # i.e. Over two, or less than 0
        for item in self.bgConfig:
            if item > 2:
                self.bgConfig[self.bgConfig.index(item)] = 0
            elif item < 0:
                self.bgConfig[self.bgConfig.index(item)] = 2

        # Set the text in the middle to the corresponding option currently selected
        self.optionCapsuleLabels[index].set_text(self.backgroundOptions[self.bgConfig[index]][0])

    # Subroutine which handles the buttons and graphical elements involved in changing the play screen options
    def handlePSOptions(self, button):

        # Check whether this is occuring the first time (in runtime)
        if self.optionsPS is None:

            # Initialise the buttons and their corresponding values
            self.optionsPS = [
                (self.currentScreen.arrowLeftC, -1),
                (self.currentScreen.arrowRightC, 1),
            ]

        # List comprehension which creates a list with the buttons associated with the crosshair function
        searchList = [i[0] for i in self.optionsPS]

        # Check to see if button clicked relates to the crosshair customisation
        if button in searchList:

            # Get the index of the button
            index = searchList.index(button)

            # Change the crosshair preference
            self.crosshair += self.optionsPS[index][1]

            # Rectify any invalid values by wrapping it around
            if self.crosshair > 2:
                self.crosshair = 0
            elif self.crosshair < 0:
                self.crosshair = 2

            # Change the text display of this option to reflect the changes made
            self.currentScreen.optionCapsuleC.set_text(self.crosshairOptions[self.crosshair][0])

        else:

            # Change the text of the button to its opposite (on => off and vice versa)
            button.set_text("Off") if self.gameFX else button.set_text("On")

            # Invert the current value (a simple 'NOT' function)
            self.gameFX = not self.gameFX

    # Subroutine which handles the graphical elements/buttons associated with the general train screen options
    def handleTSOptions(self, button):

        # Check whether this is occuring the first time (in runtime)
        if self.optionsTS is None:

            # Initialise the buttons and their corresponding values
            self.optionsTS = [
                (self.currentScreen.arrowLeftCAI, -1),
                (self.currentScreen.arrowRightCAI, 1),
            ]

        # List comprehension which creates a list with the buttons associated with the crosshair function
        searchList = [i[0] for i in self.optionsTS]

        # Check to see if button clicked relates to the crosshair customisation
        if button in searchList:

            # Get the index of the button
            index = searchList.index(button)

            # Change the crosshair preference
            self.tCrosshair += self.optionsTS[index][1]

            # Rectify any invalid values by wrapping it around
            if self.tCrosshair > 2:
                self.tCrosshair = 0
            elif self.tCrosshair < 0:
                self.tCrosshair = 2

            # Change the text display of this option to reflect the changes made
            self.currentScreen.optionCapsuleCAI.set_text(self.crosshairOptions[self.tCrosshair][0])
        else:
            # Change the text of the button to its opposite (on => off and vice versa)
            button.set_text("Off") if self.trainFX else button.set_text("On")

            # Invert the current value (a simple 'NOT' function)
            self.trainFX = not self.trainFX


    # Subroutine which handles the graphical elements involved in changing the training set options
    def handleTrainSetOptions(self, button):
        
        # Check whether this is occuring the first time (in runtime)
        if self.optionsTrainingSet is None:
            
            # Initialise the buttons and their corresponding values
            self.optionsTrainingSet = [
                (self.currentScreen.arrowLeftTSet, -1),
                (self.currentScreen.arrowRightTSet, 1)
            ]
            
        # List comprehension which creates a list of the button elements only
        searchList = [i[0] for i in self.optionsTrainingSet]
        
        # Get index of button clicked
        index = searchList.index(button)
        
        # Update the training set preference
        self.trainingSetNum += self.optionsTrainingSet[index][1]
        
        # Rectify invalid values by wrapping around it
        if self.trainingSetNum > 3:
            self.trainingSetNum = 0
        elif self.trainingSetNum < 0:
            self.trainingSetNum = 3
            
        # Change display text to reflect change
        self.currentScreen.optionCapsuleTSet.set_text(self.trainSetOptions[self.trainingSetNum])

    # Subroutine which handles the graphical components involved in changing the AI thinking speed
    def handleBufferOptions(self, button):

        # Check whether this is occuring the first time (in runtime)
        if self.optionsBuffer is None:

            # Initialise the buttons and their corresponding values
            self.optionsBuffer = [
                (self.currentScreen.arrowLeftBuffer, -1),
                (self.currentScreen.arrowRightBuffer, 1)
            ]

        # List comprehension which creates a list of the button elements only
        searchList = [i[0] for i in self.optionsBuffer]

        # Get index of button clicked
        index = searchList.index(button)

        # Update the buffer preference
        self.bufferNum += self.optionsBuffer[index][1]

        # Rectify invalid values by wrapping around it
        if self.bufferNum > 3:
            self.bufferNum = 0
        elif self.bufferNum < 0:
            self.bufferNum = 3

        # Change display text to reflect change
        self.currentScreen.optionCapsuleBuffer.set_text(self.bufferOptions[self.bufferNum][0])

    # Subroutine which executes every time the user exist the settings screen
    # Writes all the setting preferences to a text file
    def writeSave(self, x=None):

        # Gets the music and sound preferences of the user and converts them into a value between 0 and 1
        self.musicVol = self.currentScreen.musicSlider.get_current_value()/100
        self.soundVol = self.currentScreen.soundSlider.get_current_value()/100

        # Open text file to write the preferences in
        with open("./data/game-data/config.txt", "w") as f:
            f.write(f"{self.musicVol}\n"
                    f"{self.soundVol}\n"
                    f"{self.bgConfig[0]}\n"
                    f"{self.bgConfig[1]}\n"
                    f"{self.bgConfig[2]}\n"
                    f"{self.crosshair}\n"
                    f"{self.tCrosshair}\n"
                    f"{1 if self.gameFX else 0}\n"
                    f"{1 if self.trainFX else 0}\n"
                    f"{self.trainingSetNum}\n"
                    f"{self.bufferNum}")

        # Reset all initialised settings variables
        self.config = False
        self.optionsTrainingSet = None
        self.optionsPS = None
        self.optionsTS = None
        self.optionsBuffer = None
        self.optionCapsuleLabels = None
        self.bgRightButtons = None
        self.bgLeftButtons = None
        self.settingsPanelDict = None

        # Return to main menu
        self.returnMenu()

    # Subroutine which clears all leaderboard scores
    def clearScores(self, x=None):
        # Open text file automatically wipes the file
        f = open("./data/game-data/scores.txt", "w")

        # Close to save file
        f.close()

    # Subroutine which makes a warning prompt pop up to warn user from deleting an AI Model
    def promptWarning(self, x=None):

        # Get the name of the model the user is considerng to delete
        option = self.currentScreen.aiSelectionBox.get_single_selection()

        # Create a warning prompt with the following text
        self.currentScreen.createWarningScreen(
            f"Are you sure you want to delete AI Model: [ {option} ]?",
            "This cannot be undone or recovered."
        )

    # Subroutine used to return to the setting screen by dismissing the warning prompt
    def returnSettingScreen(self, x=None):

        # Erase the warning prompt
        self.currentScreen.warningOverlay.kill()

    # Subroutine called to delete an AI Model
    def deleteModel(self, x=None):

        # Get the option the user has selected
        option = self.currentScreen.aiSelectionBox.get_single_selection()

        # Delete the directory (of the model) and all contents inside the directory
        shutil.rmtree(f"data/ai-models/{option}")

        # Dismiss the warning prompt
        self.returnSettingScreen()

        # Reset the selection box with a new, updated version of all model available to be deleted.
        self.currentScreen.aiSelectionBox.set_item_list(self.currentScreen._unpackOptions())

    # Subroutine which 'continuously runs'. Is effectively the app's 'game loop'
    def run(self):

        # Create the main menu screen
        self.currentScreen.createScreen()

        # Game loop
        while self.running:

            # Find the interval between the last clock tick
            deltaTime = self.clock.tick(60) / 1000.0

            # Get all events that have occurred during that tick
            events = pygame.event.get()

            # Get the position of the mouse
            mousePos = pygame.mouse.get_pos()

            # Run through each event that has occurred
            for event in events:

                # If the user has clicked the red 'x' button on the window (they really shouldn't :( ), safely exit
                if event.type == pygame.QUIT:
                    self.quit(True)

                # Check if the app is currently in the 'play section'
                if self.game:

                    # Check if mouse has moved
                    if event.type == pygame.MOUSEMOTION:

                        # Set the crosshair position to be where the mouse is
                        self.cursorRect = (mousePos[0] - 50, mousePos[1] - 50)

                    # Check if the event is an observer event
                    if event.type == self.gameEvent:

                        # Check to see if the game is paused
                        if not self.gameInstance.paused:

                            # Check whether the mouse is in the display section at the bottom where the pause button and
                            # game information is.
                            # Set the value to False if so, otherwise true
                            self.validate = False if (self.screenSize[0] // 2 - 700 < mousePos[0] < self.screenSize[
                                0] // 2 + 700) and (mousePos[1] > ((self.screenSize[1] // 10) * 9 - 70)) else True
                        else:

                            # If the game is paused, set validation to false
                            self.validate = False if self.gameInstance.paused else True

                        # Pass events to game instance object to do its own processing
                        self.gameInstance.processEvents(events)

                    # Check if mouse has clicked
                    if event.type == pygame.MOUSEBUTTONUP:

                        # If the mouse has clicked, check to see whether they clicked on the display section
                        self.validate = False if (self.screenSize[0] // 2 - 700 < mousePos[0] < self.screenSize[
                            0] // 2 + 700) and (mousePos[1] > ((self.screenSize[1] // 10) * 9 - 70)) else True

                        # Process the click within the game instance
                        self.gameInstance.handleClicks(self.validate)

                # Check to see if app is currently in initial training screen
                if self.initialTraining:

                    # Check to see if event is an observer event
                    if event.type == self.initialTrainEvent:

                        # Get the current selected AI Model
                        option = self.currentScreen.dropDown.selected_option

                        # If the test option is chosen
                        if self.testOption:

                            # Check if the selected model is creating a new one
                            if option == "New AI":

                                # Display warning message
                                self.currentScreen.invalidMessage.visible = 1
                                self.currentScreen.startButton.disable()

                            else:

                                # Otherwise make the warning disappear
                                self.currentScreen.invalidMessage.visible = 0
                                self.currentScreen.startButton.enable()
                        else:
                            # Otherwise make the warning disappear
                            self.currentScreen.invalidMessage.visible = 0
                            self.currentScreen.startButton.enable()

                # Check to see if the app is currently in the 'training/testing' section
                if self.training:

                    # Check if train screen observer event
                    if event.type == self.trainEvent:

                        # Process events inside the train instance (ask AI for decision)
                        cursor = self.trainInstance.processEvents(events)

                        # Set the position of the cursor to the response given by the AI
                        self.cursorRect = cursor if cursor is not None else self.cursorRect

                # Check if the app is currently in the settings section
                if self.config:

                    # Check if it is an observer event
                    if event.type == self.configEvent:

                        # Get the current value of the music and sound sliders
                        musicPercentage = int(self.currentScreen.musicSlider.get_current_value())
                        soundPercentage = int(self.currentScreen.soundSlider.get_current_value())

                        # Check to see if the values have changed. If they have, change the text beside the sliders
                        if musicPercentage != self.prevMusic:
                            self.currentScreen.musicPercentage.set_text(str(musicPercentage))
                            self.prevMusic = musicPercentage

                        if soundPercentage != self.prevSound:
                            self.currentScreen.soundPercentage.set_text(str(soundPercentage))
                            self.prevSound = soundPercentage

                        # Check if the user has selected any AI model for deletion
                        if self.currentScreen.aiSelectionBox.get_single_selection() == None:

                            # If not, disable the delete button
                            self.currentScreen.deleteButton.disable()
                        else:

                            # Enable the delete button
                            self.currentScreen.deleteButton.enable()

                # Tell the screen manager to process all the other events
                self.manager.process_events(event)

                # Check to see if the user has interacted with any graphical elements
                if event.type == pygame.USEREVENT:

                    # Check if it is a button
                    if event.user_type == gui.UI_BUTTON_PRESSED:

                        # Check if button is in dictionary
                        if event.ui_element in self.currentScreen.functionDictionary:
                            # Run the subroutine associated with the button
                            self.masterDirectory[self.currentScreen.functionDictionary[event.ui_element]](event.ui_element)

            # Update the screen through the screen manager
            self.manager.update(deltaTime)

            # Redraw the background
            self.windowSurface.blit(self.background, (0, 0))

            # Draw the new screen
            self.manager.draw_ui(self.windowSurface)

            # Check to see whether either:
            #       1. A game is running and it is not paused, and that the mouse is not in the display section
            #       2. A game is running, but the mouse is in the display section
            #       3. The app is currently in training
            if self.game and self.validate and not self.gameInstance.paused and self.gameInstance.game:

                # Make the user's mouse cursor invisible
                pygame.mouse.set_visible(False)

                # Draw the crosshair where the mouse is
                self.windowSurface.blit(self.cursorSurface, self.cursorRect)

            elif self.game and not self.validate:

                # Make the mouse cursor visible
                pygame.mouse.set_visible(True)

            elif self.training:

                # Check to see if the training is not paused, and is running
                if not self.trainInstance.paused and self.trainInstance.game:

                    # Sometimes, the AI decision will return None (no change to its position);
                    # hence, ignore if the cursor yields None, ignore
                    try:

                        # Draw the cursor to where the AI has decided to shoot
                         self.windowSurface.blit(self.cursorSurface, self.cursorRect)
                    except TypeError:
                        pass

            # Update the display completely
            pygame.display.update()

        # Quit the program
        pygame.quit()

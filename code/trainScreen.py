# Import necessary libraries
import pygame
import pygame_gui as gui

# Import screen prototype
from code.screenPrototype import screenDesign

class TrainScreenInstance(screenDesign):

    """

        Object for handling the train screen. Only deals with elements on the screen,
        not the training process itself.

        Dependencies:
            - pygame
            - pygame_gui (gui)
            - screenPrototype

    """

    # Inherit parent attributes
    def __init__(self, screenSize, manager):

        # Inherit parent properties
        super().__init__(screenSize, manager)

        # Initialise Model currently running variable
        self.model = None

    # Subroutine which creates the initial training screen
    def createInitialScreen(self):

        # Create graphical elements
        self.initialOverlay = gui.elements.UIPanel(
            pygame.Rect((0, 0, 1925, 1085)),
            manager=self.manager,
            starting_layer_height=5,
            object_id="#initial_overlay")

        initialOverlaySize = self.initialOverlay.get_container().get_size()

        self.initialBox = gui.elements.UIPanel(
            pygame.Rect(initialOverlaySize[0] // 2 - 700, initialOverlaySize[1] // 2 - 400, 1400, 800),
            manager=self.manager,
            container=self.initialOverlay,
            starting_layer_height=0,
            object_id="#initial_box")

        initialBoxSize = self.initialBox.get_container().get_size()

        self.pauseText = gui.elements.UILabel(
            pygame.Rect(initialBoxSize[0] // 2 - 300, initialBoxSize[1] // 4 - 50, 600, 100),
            "Select AI Model:",
            manager=self.manager,
            container=self.initialBox,
            object_id="#initial_header")

        options = self._unpackOptions(True)

        self.dropDown = gui.elements.UIDropDownMenu(
                                options,
                                options[0],
                                pygame.Rect(initialBoxSize[0] // 2 - 150, initialBoxSize[1] // 2 - 37.5, 300, 75),
                                manager=self.manager,
                                container=self.initialBox,
                                expansion_height_limit=150,
                                object_id="#drop_down_ai")

        self.trainToggleButton = gui.elements.UIButton(
            pygame.Rect(initialBoxSize[0] // 2 - 150, initialBoxSize[1] // 3 * 2 - 75, 100, 50),
            "Train",
            manager=self.manager,
            container=self.initialBox,
            object_id="#option_button")

        self.trainToggleButton.disable()

        self.testToggleButton = gui.elements.UIButton(
            pygame.Rect(initialBoxSize[0] // 2 + 50, initialBoxSize[1] // 3 * 2 - 75, 100, 50),
            "Test",
            manager=self.manager,
            container=self.initialBox,
            object_id="#option_button")

        self.functionDictionary[self.trainToggleButton] = '1.4'
        self.functionDictionary[self.testToggleButton] = '1.4'

        self.invalidMessage = gui.elements.UILabel(
            pygame.Rect(initialBoxSize[0] // 2 - 300, initialBoxSize[1] // 3 * 2 - 20, 600, 50),
            "New AI models cannot be tested.",
            manager=self.manager,
            container=self.initialBox,
            object_id="#invalid_message")

        self.invalidMessage.visible = 0

        self.returnButton = gui.elements.UIButton(
            pygame.Rect(initialBoxSize[0] // 4 - 100, initialBoxSize[1] // 4 * 3 - 25, 200, 50),
            "Return",
            manager=self.manager,
            container=self.initialBox,
            object_id="#return_button")

        self.startButton = gui.elements.UIButton(
            pygame.Rect((initialBoxSize[0] // 4 * 3) - 100, initialBoxSize[1] // 4 * 3 - 25, 200, 50),
            "Start",
            manager=self.manager,
            container=self.initialBox,
            object_id="#start_button")

        # Link buttons with functiomn dictionary
        self.functionDictionary[self.returnButton] = '5'
        self.functionDictionary[self.startButton] = '1.1'

    # Create the training screen
    def createScreen(self):

        # Create graphical elements
        self.panel = gui.elements.UIPanel(
            pygame.Rect(self.screenSize[0] // 2 - 700, (self.screenSize[1] // 10 * 9) - 70, 1400, 160),
            starting_layer_height=0,
            manager=self.manager,
            object_id="#main_train_panel")

        panelSize = self.panel.get_container().get_size()

        self.pauseButton = gui.elements.UIButton(
            pygame.Rect(panelSize[0] // 2 - 50, panelSize[1] // 2 - 50, 100, 100),
            "",
            manager=self.manager,
            container=self.panel,
            object_id="#pause_button")

        self.functionDictionary[self.pauseButton] = '4'

        self.speedPanel = gui.elements.UIPanel(
            pygame.Rect(panelSize[0] // 5 - 250, panelSize[1] // 2 - 50, 550, 100),
            starting_layer_height=0,
            container=self.panel,
            manager=self.manager,
            object_id="#speed_panel")

        self.speedPanelSize = self.speedPanel.get_container().get_size()

        self.speedLabel = gui.elements.UILabel(
                                        pygame.Rect(self.speedPanelSize[0] // 80, self.speedPanelSize[1] // 2 - 50, 250, 100),
                                        "Current Speed: 1x",
                                        container=self.speedPanel,
                                        manager=self.manager,
                                        object_id="#speed_text")

        self.slowButton = gui.elements.UIButton(
                        pygame.Rect(self.speedPanelSize[0] // 2 + 25, self.speedPanelSize[1] // 2 - 25, 50, 50),
                        "0.5x",
                        container=self.speedPanel,
                        manager=self.manager,
                        object_id="#speed_button")

        self.stopButton = gui.elements.UIButton(
                        pygame.Rect(self.speedPanelSize[0] // 2 + 90, self.speedPanelSize[1] // 2 - 25, 50, 50),
                        "||",
                        manager=self.manager,
                        container=self.speedPanel,
                        object_id="#speed_button")

        self.standardButton = gui.elements.UIButton(
                        pygame.Rect(self.speedPanelSize[0] // 2 + 155, self.speedPanelSize[1] // 2 - 25, 50, 50),
                        "1x",
                        manager=self.manager,
                        container=self.speedPanel,
                        object_id="#speed_button")

        # Disable the default option (it's already active)
        self.standardButton.disable()

        self.fastButton = gui.elements.UIButton(
                        pygame.Rect(self.speedPanelSize[0] // 2 + 220, self.speedPanelSize[1] // 2 - 25, 50, 50),
                        "2x",
                        manager=self.manager,
                        container=self.speedPanel,
                        object_id="#speed_button")


        self.difficultyPanel = gui.elements.UIPanel(
                                    pygame.Rect((panelSize[0] // 5 * 4) - 260, panelSize[1] // 2 - 50, 500, 100),
                                    starting_layer_height=0,
                                    container=self.panel,
                                    manager=self.manager,
                                    object_id="#difficulty_panel")

        self.difficultyPanelSize = self.difficultyPanel.get_container().get_size()

        self.difficultyLabel = gui.elements.UILabel(
            pygame.Rect(self.difficultyPanelSize[0] // 80, self.difficultyPanelSize[1] // 2 - 50, 300, 100),
            "Current Difficulty: Easy",
            container=self.difficultyPanel,
            manager=self.manager,
            object_id="#difficulty_text")

        self.easyButton = gui.elements.UIButton(
            pygame.Rect(self.difficultyPanelSize[0] // 2 + 80, self.difficultyPanelSize[1] // 2 - 25, 50, 50),
            "E",
            manager=self.manager,
            container=self.difficultyPanel,
            object_id="#difficulty_button")

        # Disable the default button (already active)
        self.easyButton.disable()

        self.normalButton = gui.elements.UIButton(
            pygame.Rect(self.difficultyPanelSize[0] // 2 + 145, self.difficultyPanelSize[1] // 2 - 25, 50, 50),
            "N",
            manager=self.manager,
            container=self.difficultyPanel,
            object_id="#difficulty_button")

        self.hardButton = gui.elements.UIButton(
            pygame.Rect(self.difficultyPanelSize[0] // 2 + 205, self.difficultyPanelSize[1] // 2 - 25, 50, 50),
            "H",
            manager=self.manager,
            container=self.difficultyPanel,
            object_id="#difficulty_button")

        # Link all buttons to function dictionary
        self.functionDictionary[self.slowButton] = "1.5"
        self.functionDictionary[self.standardButton] = "1.5"
        self.functionDictionary[self.stopButton] = "1.5"
        self.functionDictionary[self.fastButton] = "1.5"
        self.functionDictionary[self.easyButton] = "1.6"
        self.functionDictionary[self.normalButton] = "1.6"
        self.functionDictionary[self.hardButton] = "1.6"


        # Create AI Model Info Text Display
        self.nameDisplay = gui.elements.UIButton(
            pygame.Rect(self.screenSize[0] // 100, self.screenSize[1] // 20 - 30, 440, 60),
            f"Current Model: [{self.model}]",
            manager=self.manager,
            object_id="#system_train_text")

        self.nameDisplay.disable()

        self.speedDisplay = gui.elements.UIButton(
            pygame.Rect(self.screenSize[0] // 100, self.screenSize[1] // 20 + 30, 440, 60),
            "Game Speed: 1x",
            manager=self.manager,
            object_id="#system_train_text")

        self.speedDisplay.disable()

        self.difficultyDisplay = gui.elements.UIButton(
            pygame.Rect(self.screenSize[0] // 100, self.screenSize[1] // 20 + 90, 440, 60),
            "Duck Difficulty: Easy",
            manager=self.manager,
            object_id="#system_train_text")

        self.difficultyDisplay.disable()

        self.timeDisplay = gui.elements.UIButton(
            pygame.Rect(self.screenSize[0] // 100, self.screenSize[1] // 20 + 150, 440, 60),
            "Time: 00:00",
            manager=self.manager,
            object_id="#system_train_text")

        self.timeDisplay.disable()

        self.hitDisplay = gui.elements.UIButton(
            pygame.Rect(self.screenSize[0] // 100, self.screenSize[1] // 20 + 210, 440, 60),
            "Hit/Total: 0/0",
            manager=self.manager,
            object_id="#system_train_text")

        self.hitDisplay.disable()

        self.accuracyDisplay = gui.elements.UIButton(
            pygame.Rect(self.screenSize[0] // 100, self.screenSize[1] // 20 + 270, 440, 60),
            "Accuracy: 0.00%",
            manager=self.manager,
            object_id="#system_train_text")


        # Create autosave notice (very inconspicuous)
        self.autosaveNotice = gui.elements.UILabel(
            pygame.Rect(self.screenSize[0] - 220, 10, 200, 50),
            "Autosaving...",
            manager=self.manager,
            object_id="#save_text"
        )

        self.autosaveNotice.visible = 0

        self.accuracyDisplay.disable()


    # Subroutinne which creates the naming screen when creating a new AI
    def createNewModelScreen(self):

        # Create Graphical elements
        self.namingOverlay = gui.elements.UIPanel(
            pygame.Rect(self.screenSize[0] // 2 - 700, self.screenSize[1] // 2 - 400, 1400, 800),
            manager=self.manager,
            starting_layer_height=7,
            object_id="#naming_overlay")

        namingOverlaySize = self.namingOverlay.get_container().get_size()

        self.namingBox = gui.elements.UIPanel(
            pygame.Rect(namingOverlaySize[0] // 2 - 500, namingOverlaySize[1] // 2 - 250, 1000, 500),
            manager=self.manager,
            container=self.namingOverlay,
            starting_layer_height=0,
            object_id="#naming_box")

        namingBoxSize = self.namingBox.get_container().get_size()

        self.namingLabel = gui.elements.UILabel(
            pygame.Rect(namingBoxSize[0] // 2 - 150, namingBoxSize[1] // 5 - 25, 300, 50),
            "New AI Name:",
            manager=self.manager,
            container=self.namingBox,
            object_id="#naming_label"
        )

        self.cancelButton = gui.elements.UIButton(
            pygame.Rect(namingBoxSize[0] // 4 - 100, namingBoxSize[1] // 4 * 3 - 25, 200, 50),
            "Cancel",
            manager=self.manager,
            container=self.namingBox,
            object_id="#cancel_button")

        self.acceptButton = gui.elements.UIButton(
            pygame.Rect(namingBoxSize[0] // 4 * 3 - 100, namingBoxSize[1] // 4 * 3 - 25, 200, 50),
            "Confirm",
            manager=self.manager,
            container=self.namingBox,
            object_id="#confirm_button")

        self.nameEntry = gui.elements.UITextEntryLine(
            pygame.Rect(namingBoxSize[0] // 2 - 200, namingBoxSize[1] // 2 - 50, 400, 100),
            manager=self.manager,
            container=self.namingBox,
            object_id="#naming_entry_box")

        # Limit the characters allowed for a name and set forbidden symbols
        self.nameEntry.set_text_length_limit(15)
        self.nameEntry.set_forbidden_characters(["\\", "/", ".", "@", "-", " ", "`", "~", "{", "}", ",", "'", "\"", "%", "$", "#", "^", "~", "_", "&"])

        self.errorMessage = gui.elements.UILabel(
            pygame.Rect(namingBoxSize[0] // 2 - 350, namingBoxSize[1] // 2 + 25, 700, 35),
            "Error Message",
            manager=self.manager,
            container=self.namingBox,
            object_id="#error_message"
        )

        self.errorMessage.visible = 0

        # Link buttons to function dictionary
        self.functionDictionary[self.cancelButton] = '1.2'
        self.functionDictionary[self.acceptButton] = '1.3'


    # Subroutine which creates the testing screen
    def createTestScreen(self):

        # Create Graphical Elements
        self.panel = gui.elements.UIPanel(
            pygame.Rect(self.screenSize[0] // 2 - 700, (self.screenSize[1] // 10 * 9) - 70, 1400, 160),
            starting_layer_height=0,
            manager=self.manager,
            object_id="#main_panel")

        panelSize = self.panel.get_container().get_size()

        self.pauseButton = gui.elements.UIButton(
            pygame.Rect(panelSize[0] // 2 - 50, panelSize[1] // 2 - 50, 100, 100),
            "",
            manager=self.manager,
            container=self.panel,
            object_id="#pause_button")

        self.functionDictionary[self.pauseButton] = '4'

        self.lifePanel = gui.elements.UIPanel(
            pygame.Rect(panelSize[0] // 5 - 250, panelSize[1] // 2 - 50, 500, 100),
            starting_layer_height=0,
            container=self.panel,
            manager=self.manager,
            object_id="#life_panel")

        self.lifePanelSize = self.lifePanel.get_container().get_size()

        self.lifeText = gui.elements.UILabel(
            pygame.Rect(self.lifePanelSize[0] // 80, self.lifePanelSize[1] // 2 - 50, 150, 100),
            "Lives:",
            container=self.lifePanel,
            manager=self.manager,
            object_id="#life_text")

        lifeBar = pygame.transform.scale(pygame.image.load("images/lifeBarGreen.png"), (240, 30))
        self.lifeImage = gui.elements.UIImage(
            pygame.Rect(self.lifePanelSize[0] // 2 - 80, self.lifePanelSize[1] // 2 - 15, 240, 30),
            lifeBar,
            container=self.lifePanel,
            manager=self.manager)

        self.duckPanel = gui.elements.UIPanel(
            pygame.Rect((panelSize[0] // 5 * 4) - 250, panelSize[1] // 2 - 50, 500, 100),
            starting_layer_height=0,
            container=self.panel,
            manager=self.manager,
            object_id="#duck_panel")

        self.duckPanelSize = self.duckPanel.get_container().get_size()

        self.duckText = gui.elements.UILabel(
            pygame.Rect(self.duckPanelSize[0] // 80, self.duckPanelSize[1] // 2 - 75, 200, 150),
            "Ducks Left:",
            container=self.duckPanel,
            manager=self.manager,
            object_id="#duck_text")

        duckMeter = pygame.transform.scale(pygame.image.load("images/duckMeter0.png"), (240, 30))
        self.duckImage = gui.elements.UIImage(
            pygame.Rect(self.duckPanelSize[0] // 2 - 20, self.duckPanelSize[1] // 2 - 20, 240, 30),
            duckMeter,
            container=self.duckPanel,
            manager=self.manager)

        self.roundInfo = gui.elements.UILabel(
            pygame.Rect(self.screenSize[0] // 2 - 120, self.screenSize[1] // 20 - 30, 240, 60),
            "Round 1",
            manager=self.manager,
            object_id="#system_text")

        self.timeElapsed = gui.elements.UILabel(
            pygame.Rect(self.screenSize[0] // 10 - 220, self.screenSize[1] // 20 - 30, 440, 60),
            "Time: 00:00",
            manager=self.manager,
            object_id="#system_text")

        self.score = gui.elements.UILabel(
            pygame.Rect((self.screenSize[0] // 10 * 9) - 220, self.screenSize[1] // 20 - 30, 440, 60),
            "Score: 0000000",
            manager=self.manager,
            object_id="#system_text")

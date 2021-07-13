# Import necessary libraries
import pygame
import pygame_gui as gui

# Import screen prototype
from code.screenPrototype import screenDesign

class SettingsScreenInstance(screenDesign):

    """
        Object for handling the settings screen.

        Dependencies:
            - pygame
            - pygame_gui (gui)
            - screenPrototype


    """

    # Inherit attributes from parent obejct
    def __init__(self, screenSize, manager, app):
        super().__init__(screenSize, manager)

        # Stores the current page the user is on
        self.currentPage = None

        # Represents the app itself
        self.app = app

    # Subroutine which create a warning prompt
    def createWarningScreen(self, headerMessage, labelMessage):

        # Create graphical elemenst
        self.warningOverlay = gui.elements.UIPanel(
            pygame.Rect(self.screenSize[0] // 2 - 800, self.screenSize[1] // 2 - 450, 1600, 900),
            manager=self.manager,
            starting_layer_height=100,
            object_id="#warning_overlay")

        warningOverlaySize = self.warningOverlay.get_container().get_size()

        self.warningBox = gui.elements.UIPanel(
            pygame.Rect(warningOverlaySize[0] // 2 - 500, warningOverlaySize[1] // 2 - 250, 1000, 500),
            manager=self.manager,
            container=self.warningOverlay,
            starting_layer_height=0,
            object_id="#warning_box")

        warningBoxSize = self.warningBox.get_container().get_size()

        self.namingLabel = gui.elements.UILabel(
            pygame.Rect(warningBoxSize[0] // 2 - 150, warningBoxSize[1] // 5 - 25, 300, 50),
            "Warning:",
            manager=self.manager,
            container=self.warningBox,
            object_id="#warning_label"
        )

        self.warningtextHeader = gui.elements.UILabel(
            pygame.Rect(warningBoxSize[0] // 2 - 400, warningBoxSize[1] // 2 - 75, 800, 50),
            headerMessage,
            manager=self.manager,
            container=self.warningBox,
            object_id="#warning_text"
        )

        self.warningtextLabel = gui.elements.UILabel(
            pygame.Rect(warningBoxSize[0] // 2 - 300, warningBoxSize[1] // 2 - 25, 600, 50),
            labelMessage,
            manager=self.manager,
            container=self.warningBox,
            object_id="#warning_text"
        )

        self.cancelButton = gui.elements.UIButton(
            pygame.Rect(warningBoxSize[0] // 4 - 100, warningBoxSize[1] // 4 * 3 - 25, 200, 50),
            "Cancel",
            manager=self.manager,
            container=self.warningBox,
            object_id="#cancel_button")

        self.acceptButton = gui.elements.UIButton(
            pygame.Rect(warningBoxSize[0] // 4 * 3 - 100, warningBoxSize[1] // 4 * 3 - 25, 200, 50),
            "Confirm",
            manager=self.manager,
            container=self.warningBox,
            object_id="#confirm_button")

        # Link buttons to the function dictionary
        self.functionDictionary[self.cancelButton] = '2.9.2'
        self.functionDictionary[self.acceptButton] = '2.9.3'

    # Subroutine which creates the main settings screen
    def createScreen(self):

        # Create graphical elementss
        self.overlay = gui.elements.UIPanel(
            pygame.Rect(-2, -2, self.screenSize[0] + 5, self.screenSize[1] + 5),
            manager=self.manager,
            starting_layer_height=5,
            object_id="#overlay"
        )

        self.configBox = gui.elements.UIPanel(
            pygame.Rect(self.screenSize[0] // 2 - 800, self.screenSize[1] // 2 - 450, 1600, 900),
            manager=self.manager,
            container=self.overlay,
            starting_layer_height=3,
            object_id="#config_box"
        )

        self.configBoxSize = self.configBox.get_container().get_size()

        self.rowPanel = gui.elements.UIPanel(
            pygame.Rect(self.configBoxSize[0] // 20 - 1, self.configBoxSize[1] // 10 - 25, 800, 50),
            manager=self.manager,
            container=self.configBox,
            starting_layer_height=3,
            object_id="#option_panel"
        )

        self.screenHeader = gui.elements.UILabel(
            pygame.Rect(self.configBoxSize[0] // 10 * 8.5 - 150, self.configBoxSize[1] // 10 - 65, 300, 100),
            "Settings",
            manager=self.manager,
            container=self.configBox,
            object_id="#header_text"
        )

        self.generalButton = gui.elements.UIButton(
            pygame.Rect(-2, -2, 200, 50),
            "General",
            manager=self.manager,
            container=self.rowPanel,
            object_id="#tab_button"
        )

        self.generalButton.disable()

        self.playButton = gui.elements.UIButton(
            pygame.Rect(192, -2, 150, 50),
            "Play",
            manager=self.manager,
            container=self.rowPanel,
            object_id="#tab_button"
        )

        self.trainButton = gui.elements.UIButton(
            pygame.Rect(336, -2, 150, 50),
            "Train",
            manager=self.manager,
            container=self.rowPanel,
            object_id="#tab_button"
        )

        # Link buttons with the function dictionary
        self.functionDictionary[self.generalButton] = '2.1'
        self.functionDictionary[self.playButton] = '2.1'
        self.functionDictionary[self.trainButton] = '2.1'

        # Create the general settings pages
        self.generateGeneralSettings()

    # Subroutine which creates the exit buttons for each page (they're all the same!)
    def createExitButtons(self):

        # Create graphical element (per page)
        self.exitButton = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 10 * 9 - 100, self.generalPanelSize[1] // 10 * 9 - 25, 200, 50),
            "Save and Exit",
            container=self.generalPanel,
            manager=self.manager,
            object_id="#exit_button"
        )

        # Link button with function dictionary
        self.functionDictionary[self.exitButton] = '2.7'

        self.exitButton = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 10 * 9 - 100, self.generalPanelSize[1] // 10 * 9 - 25, 200, 50),
            "Save and Exit",
            container=self.playPanel,
            manager=self.manager,
            object_id="#exit_button"
        )

        # Link button with function dictionary
        self.functionDictionary[self.exitButton] = '2.7'

        self.exitButton = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 10 * 9 - 100, self.generalPanelSize[1] // 10 * 9 - 25, 200, 50),
            "Save and Exit",
            container=self.trainPanel,
            manager=self.manager,
            object_id="#exit_button"
        )

        # Link button with function dictionary
        self.functionDictionary[self.exitButton] = '2.7'

    # Creates the general settings page
    def generateGeneralSettings(self):

        # Create graphical elements
        self.generalPanel = gui.elements.UIPanel(
            pygame.Rect(self.configBoxSize[0] // 20, self.configBoxSize[1] // 10 + 20, 1440, 700),
            manager=self.manager,
            container=self.configBox,
            starting_layer_height=4,
            object_id="#setting_display"
        )

        self.generalPanelSize = self.generalPanel.get_container().get_size()

        # Sets the current page attrtibute to this panel
        self.currentPage = self.generalPanel

        self.UIHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 150, self.generalPanelSize[1] // 10 - 50, 300, 100),
            "UI Adjustments:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_header_text"
        )

        self.backgroundOptionText = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 - 15, 250, 50),
            "Backgrounds:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#sub_option_header_text"
        )

        self.backgroundOptionMS = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 - 75, self.generalPanelSize[1] // 5 + 50, 200, 50),
            "Main Screen:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.arrowLeftMS = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 125, self.generalPanelSize[1] // 5 + 50, 50, 50),
            "<",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#arrow"
        )

        self.optionCapsuleMS = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 175, self.generalPanelSize[1] // 5 + 50, 100, 50),
            f"{self.app.backgroundOptions[self.app.bgConfig[0]][0]}",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.arrowRightMS = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 275, self.generalPanelSize[1] // 5 + 50, 50, 50),
            ">",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#arrow"
        )

        self.backgroundOptionPS = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 - 80, self.generalPanelSize[1] // 5 + 100, 200, 50),
            "Play Screen:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.arrowLeftPS = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 125, self.generalPanelSize[1] // 5 + 100, 50, 50),
            "<",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#arrow"
        )

        self.optionCapsulePS = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 175, self.generalPanelSize[1] // 5 + 100, 100, 50),
            f"{self.app.backgroundOptions[self.app.bgConfig[1]][0]}",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.arrowRightPS = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 275, self.generalPanelSize[1] // 5 + 100, 50, 50),
            ">",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#arrow"
        )

        self.backgroundOptionTS = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 - 75, self.generalPanelSize[1] // 5 + 150, 200, 50),
            "Train Screen:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.arrowLeftTS = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 125, self.generalPanelSize[1] // 5 + 150, 50, 50),
            "<",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#arrow"
        )

        self.optionCapsuleTS = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 175, self.generalPanelSize[1] // 5 + 150, 100, 50),
            f"{self.app.backgroundOptions[self.app.bgConfig[2]][0]}",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.arrowRightTS = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 275, self.generalPanelSize[1] // 5 + 150, 50, 50),
            ">",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#arrow"
        )

        self.soundOptionText = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 * 3 - 25, 300, 50),
            "Music & Sounds:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#sub_option_header_text"
        )

        self.musicOption = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 - 75, self.generalPanelSize[1] // 5 * 3 + 50, 150, 50),
            "Music:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.musicSlider = gui.elements.UIHorizontalSlider(
            pygame.Rect(self.generalPanelSize[0] // 7 + 125, self.generalPanelSize[1] // 5 * 3 + 55, 250, 35),
            start_value=self.app.musicVol * 100,
            value_range=(0, 100),
            manager=self.manager,
            container=self.generalPanel,
            object_id="#slider_control"
        )

        self.musicPercentage = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 400, self.generalPanelSize[1] // 5 * 3 + 55, 50, 50),
            f"{int(self.app.musicVol * 100)}",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#percentage_text"
        )

        self.soundOption = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 - 75, self.generalPanelSize[1] // 5 * 3 + 100, 150, 50),
            "SFX:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_text"
        )

        self.soundSlider = gui.elements.UIHorizontalSlider(
            pygame.Rect(self.generalPanelSize[0] // 7 + 125, self.generalPanelSize[1] // 5 * 3 + 105, 250, 35),
            start_value=self.app.soundVol * 100,
            value_range=(0, 100),
            manager=self.manager,
            container=self.generalPanel,
            object_id="#slider_control"
        )

        self.soundPercentage = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 400, self.generalPanelSize[1] // 5 * 3 + 105, 50, 50),
            f"{int(self.app.soundVol * 100)}",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#percentage_text"
        )

        self.UIHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 4 * 3 - 200, self.generalPanelSize[1] // 10 - 50, 300, 100),
            "Leaderboard:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#option_header_text"
        )

        self.backgroundOptionText = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 4 * 3 - 150, self.generalPanelSize[1] // 5 - 15, 250, 50),
            "Clear Scores:",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#sub_option_header_text"
        )

        self.resetButton = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 4 * 3 + 100, self.generalPanelSize[1] // 5 - 15, 200, 50),
            "Clear",
            manager=self.manager,
            container=self.generalPanel,
            object_id="#reset_button"
        )

        # Link all buttons to the function dictionary
        self.functionDictionary[self.arrowLeftMS] = '2.2'
        self.functionDictionary[self.arrowLeftPS] = '2.2'
        self.functionDictionary[self.arrowLeftTS] = '2.2'
        self.functionDictionary[self.arrowRightMS] = '2.2'
        self.functionDictionary[self.arrowRightPS] = '2.2'
        self.functionDictionary[self.arrowRightTS] = '2.2'
        self.functionDictionary[self.resetButton] = '2.8'

    # Subroutine which creates the play screen options page. (Called as an initialiser)
    def generatePlaySettings(self):

        # Create graphical elements
        self.playPanel = gui.elements.UIPanel(
            pygame.Rect(self.configBoxSize[0] // 20, self.configBoxSize[1] // 10 + 20, 1440, 700),
            manager=self.manager,
            container=self.configBox,
            starting_layer_height=4,
            object_id="#setting_display"
        )

        self.playPanelSize = self.generalPanel.get_container().get_size()

        self.UIHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 150, self.generalPanelSize[1] // 10 - 50, 400, 100),
            "Graphics and Sounds:",
            manager=self.manager,
            container=self.playPanel,
            object_id="#option_header_text"
        )

        self.crosshairOptionText = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 - 15, 250, 50),
            "Crosshair:",
            manager=self.manager,
            container=self.playPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowLeftC = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 125, self.generalPanelSize[1] // 5 - 15, 50, 50),
            "<",
            manager=self.manager,
            container=self.playPanel,
            object_id="#arrow"
        )

        self.optionCapsuleC = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 175, self.generalPanelSize[1] // 5 - 15, 150, 50),
            f"{self.app.crosshairOptions[self.app.crosshair][0]}",
            manager=self.manager,
            container=self.playPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowRightC = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 325, self.generalPanelSize[1] // 5 - 15, 50, 50),
            ">",
            manager=self.manager,
            container=self.playPanel,
            object_id="#arrow"
        )

        self.fxOptionText = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 + 55, 250, 50),
            "Sound Effects:",
            manager=self.manager,
            container=self.playPanel,
            object_id="#sub_option_header_text"
        )

        self.optionFXButton = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 225, self.generalPanelSize[1] // 5 + 55, 50, 50),
            f"{'On' if self.app.gameFX else 'Off'}",
            manager=self.manager,
            container=self.playPanel,
            object_id="#check_button"
        )

        # Link button with function dictionary
        self.functionDictionary[self.arrowLeftC] = '2.3'
        self.functionDictionary[self.arrowRightC] = '2.3'
        self.functionDictionary[self.optionFXButton] = '2.3'

        # Hide the panel
        self.playPanel.hide()

    # Subroutine which creates the training settings page (called as an initialiser)
    def generateTrainSettings(self):

        # Create Graphical Elements
        self.trainPanel = gui.elements.UIPanel(
            pygame.Rect(self.configBoxSize[0] // 20, self.configBoxSize[1] // 10 + 20, 1440, 700),
            manager=self.manager,
            container=self.configBox,
            starting_layer_height=4,
            object_id="#setting_display"
        )

        self.trainPanelSize = self.generalPanel.get_container().get_size()

        self.UIHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 150, self.generalPanelSize[1] // 10 - 50, 400, 100),
            "Graphics and Sounds:",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#option_header_text"
        )

        self.crosshairOptionText = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 - 15, 250, 50),
            "Crosshair:",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowLeftCAI = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 125, self.generalPanelSize[1] // 5 - 15, 50, 50),
            "<",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#arrow"
        )

        self.optionCapsuleCAI = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 175, self.generalPanelSize[1] // 5 - 15, 150, 50),
            f"{self.app.crosshairOptions[self.app.tCrosshair][0]}",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowRightCAI = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 325, self.generalPanelSize[1] // 5 - 15, 50, 50),
            ">",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#arrow"
        )

        self.fxOptionText = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 + 55, 250, 50),
            "Sound Effects:",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#sub_option_header_text"
        )

        self.optionTFXButton = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 225, self.generalPanelSize[1] // 5 + 55, 50, 50),
            f"{'On' if self.app.trainFX else 'Off'}",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#check_button"
        )

        self.AIHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 200, self.generalPanelSize[1] // 5 * 2 + 20, 400, 100),
            "AI Behaviour:",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#option_header_text"
        )

        self.trainsetHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 * 2 + 130, 300, 50),
            "Training Set Size:",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowLeftTSet = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 175, self.generalPanelSize[1] // 5 * 2 + 130, 50, 50),
            "<",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#arrow"
        )

        self.optionCapsuleTSet = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 225, self.generalPanelSize[1] // 5 * 2 + 130, 150, 50),
            f"{self.app.trainSetOptions[self.app.trainingSetNum]}",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowRightTSet = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 375, self.generalPanelSize[1] // 5 * 2 + 130, 50, 50),
            ">",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#arrow"
        )

        # Link button with function dictionary
        self.functionDictionary[self.arrowLeftTSet] = '2.5'
        self.functionDictionary[self.arrowRightTSet] = '2.5'

        self.aiBufferHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 8 - 100, self.generalPanelSize[1] // 5 * 2 + 230, 300, 50),
            "AI Thinking Speed:",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowLeftBuffer = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 175, self.generalPanelSize[1] // 5 * 2 + 230, 50, 50),
            "<",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#arrow"
        )

        self.optionCapsuleBuffer = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 7 + 225, self.generalPanelSize[1] // 5 * 2 + 230, 150, 50),
            f"{self.app.bufferOptions[self.app.bufferNum][0]}",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#sub_option_header_text"
        )

        self.arrowRightBuffer = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 7 + 375, self.generalPanelSize[1] // 5 * 2 + 230, 50, 50),
            ">",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#arrow"
        )

        self.UIHeader = gui.elements.UILabel(
            pygame.Rect(self.generalPanelSize[0] // 4 * 3 - 200, self.generalPanelSize[1] // 10 - 50, 400, 100),
            "Delete AI Models:",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#option_header_text"
        )

        self.aiSelectionBox = gui.elements.UISelectionList(
            pygame.Rect(self.generalPanelSize[0] // 4 * 3 - 150, self.generalPanelSize[1] // 10 + 50, 400, 300),
            item_list=self._unpackOptions(),
            starting_height=4,
            manager=self.manager,
            allow_multi_select=False,
            allow_double_clicks=False,
            container=self.trainPanel,
            object_id="#ai_selection_list"
        )

        self.deleteButton = gui.elements.UIButton(
            pygame.Rect(self.generalPanelSize[0] // 4 * 3 - 65, self.generalPanelSize[1] // 5 * 3.5 - 25, 250, 75),
            "Delete Model",
            manager=self.manager,
            container=self.trainPanel,
            object_id="#delete_button"
        )

        # Link button with function dictionary
        self.functionDictionary[self.arrowLeftCAI] = '2.4'
        self.functionDictionary[self.arrowRightCAI] = '2.4'
        self.functionDictionary[self.optionTFXButton] = '2.4'
        self.functionDictionary[self.deleteButton] = '2.9.1'
        self.functionDictionary[self.arrowLeftBuffer] = '2.6'
        self.functionDictionary[self.arrowRightBuffer] = '2.6'

        # Hide the training Panel
        self.trainPanel.hide()

        # ADDITIONAL NOTE:
        # Since all create<page> methods are called all at once, they are an initialiser
        # This means they will only be called once per entrance to settings
        # Switching between pages won't call these methods. Just show/hide to save processing more than necessary

        # Create all the exit buttons
        self.createExitButtons()

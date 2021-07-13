# Import necessary libraries
import pygame
import pygame_gui as gui

# Import Screen Prototype
from code.screenPrototype import screenDesign


class PlayScreenInstance(screenDesign):

    """
        Object for handling the play screen. Only deals with elements on the play screen,
        not the game itself.

        Dependencies:
            - pygame
            - pygame_gui (gui)
            - screenPrototype


    """

    # Inherit properties from screen prototype
    def __init__(self, screenSize, manager):

        super().__init__(screenSize, manager)

    # Subroutine which creates the graphical elements of the screen
    def createScreen(self):

        # Create graphical elements
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
                                        pygame.Rect(self.screenSize[0]//2 - 120, self.screenSize[1]//20 - 30, 240, 60),
                                        "Round 1",
                                        manager=self.manager,
                                        object_id="#system_text")


        self.timeElapsed = gui.elements.UILabel(
                                        pygame.Rect(self.screenSize[0]//10 - 220, self.screenSize[1]//20 - 30, 440, 60),
                                        "Time: 00:00",
                                        manager=self.manager,
                                        object_id="#system_text")

        self.score = gui.elements.UILabel(
                                        pygame.Rect((self.screenSize[0]//10 * 9) - 220, self.screenSize[1]//20 - 30, 440, 60),
                                        "Score: 0000000",
                                        manager=self.manager,
                                        object_id="#system_text")




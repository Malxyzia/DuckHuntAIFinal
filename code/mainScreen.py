# Importing necessary libraries
import pygame
import pygame_gui as gui
from code.screenPrototype import screenDesign

class MainScreenInstance(screenDesign):

    """
        Object for handling the main screen.

        Dependencies:
            - pygame
            - pygame_gui (gui)
            - screenPrototype


    """

    # Inherit from screen prototype
    def __init__(self, screenSize, manager):

        super().__init__(screenSize, manager)

    # Subroutine which creates the graphical elements of the screen
    def createScreen(self):

        # Create graphical elements
        image = pygame.image.load("images/titleText.png")
        image = pygame.transform.scale(image, (1036, 312))
        title = gui.elements.UIImage(pygame.Rect((self.screenSize[0] // 2 - 518,
                                                  self.screenSize[1] // 5 - 176),
                                                 image.get_rect().size),
                                     image,
                                     manager=self.manager)

        self.playButton = gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screenSize[0] // 2 - 150, self.screenSize[1] // 2 - 80),
                                      (300, 100)),
            text='Play',
            manager=self.manager)

        self.trainButton = gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screenSize[0] // 2 - 150, self.screenSize[1] // 2 - 80 + 120),
                                      (300, 100)),
            text='Train',
            manager=self.manager)

        self.settingsButton = gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screenSize[0] // 2 - 150, self.screenSize[1] // 2 - 80 + 240),
                                      (300, 100)),
            text='Settings',
            manager=self.manager)

        self.exitButton = gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screenSize[0] // 2 - 150, self.screenSize[1] // 2 - 80 + 360),
                                      (300, 100)),
            text='Exit',
            manager=self.manager)

        # Link all buttons to the function dictionary
        self.functionDictionary[self.playButton] = '0'
        self.functionDictionary[self.trainButton] = '1'
        self.functionDictionary[self.settingsButton] = '2'
        self.functionDictionary[self.exitButton] = '3'


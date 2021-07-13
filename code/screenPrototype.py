# Import standard library
import os

# Parent Object which serves as a template for all screens
class screenDesign:

    """

    Screen Design:

    Object which serves as a blueprint for all other screen objects.

    """

    def __init__(self, screenSize, manager):

        """
        :param screenSize:  Size of the Screen
        :param manager:     Screen Manager
        """

        # Assign the screen manager
        self.manager = manager

        # Assign the screen size
        self.screenSize = screenSize

        # Function dictionary; a reference dictionary which links the screen's buttons to a number which corresponds to
        # the app's masterDictionary, launching subroutines of the app
        self.functionDictionary = {}

    # Analyses all available AI models and returns a list of them
    def _unpackOptions(self, startingOption=False):
        options = []

        # If initial training screen?
        if startingOption:

            # Insert option 'New AI
            options = ['New AI']

        # Find every directory inside the folder 'ai-models' and add their name into the list
        for entry in sorted([f.name for f in os.scandir("./data/ai-models") if f.is_dir()]):
            options.append(entry)

        # Return the list of folder names (represents AI Models)
        return options

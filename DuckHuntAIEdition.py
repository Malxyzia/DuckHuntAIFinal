"""
Software Design and Development 2020 HSC Major Project

DUCK HUNT: AI EDITION by Hayton Lam

Description:
A rendition of the classic Nintendo game "Duck Hunt" with a unique twist of including
neural-network, machine-learning AIs that learn to play the game. The game itself
is playable for users, although it functions on slightly altered rules.

Programmed in Python

Dependencies:
    - All code contained in the "code" folder


Comments:
    - This file acts as a launcher file, nothing else.

"""

# Import application code from the code folder
from code.app import App

print("\n-------------------------------------------------------\n")
print("Coded by Hayton Lam as part of the SDD Major Project 2020\n")
print("Starting application...\n")
print("Welcome to Duck Hunt AI Edition!")
print("\n-------------------------------------------------------")
print("\n\n")

# Run the application at the currently fixed resolution 1920x1080
app = App((1920, 1080))
app.run()

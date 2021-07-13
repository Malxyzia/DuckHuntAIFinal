import numpy
import scipy.special
import pickle
import random
import math

"""
Inspired from:

https://github.com/victorqribeiro/bangBangML

"""


class NeuralNetwork:

    """

    Object which represents a neural network model of an AI

    """


    def __init__(self, nn, learningRate, iterations):

        # Define the structure of the neural network
        self.layers = {'length': 0}
        for i in range(len(nn) - 1):
            self.layers[i] = {}
            self.layers[i]['weights'] = numpy.random.randn(nn[i + 1], nn[i])
            self.layers[i]['bias'] = numpy.random.randn(nn[i + 1], 1)
            self.layers[i]['activate'] = 'relu'
            self.layers['length'] += 1

        # Set the learning rate (change in gradiet)
        self.learningRate = learningRate

        # Set the amount of iterations the model should go through per adjustment
        self.epochs = iterations

        # Stores available neuron-activating functions
        self.activationFunctions = {
            'sigmoid':
                {
                    'f': scipy.special.expit,
                    "f'": self.diffSigmoid
                },

            'relu':
                {
                    'f': self.relu,
                    "f'": self.diffRelu
                }
        }

    # Differentiation of the sigmoid function
    def diffSigmoid(self, x):
        return x * (1 - x)

    # Rectilinear function
    def relu(self, x):
        return x * (x > 0)

    # Differentiation of the Rectilinear Function
    def diffRelu(self, x):
        return 0 if x < 0 else 1

    # Subroutine that asks the AI to make a decision on where to shoot, given game information
    def query(self, gameInformation):

        """
        Purpose:

        Instructions as to where the AI should shoot.

        :param gameInformation:
            [<targetX>,<targetY>, <cursorX>, <cursorY>] (Expected 4 elements)

        :return instruction:
            [<instructionX>, <instructionY>] (Expected 2 elements)
        """

        # The output matrix
        instruction = numpy.array([[info] for info in gameInformation]) if isinstance(gameInformation,
                                                                                      list) is True else gameInformation
        # For each layer in the network:
        for i in range(self.layers['length']):

            # Multiply matrices together with the corresponding weights
            instruction = self.layers[i]['weights'].__matmul__(instruction)
            self.layers[i]['instruction'] = instruction

            # Adjust the decision with the bias
            self.layers[i]['instruction'] = self.layers[i]['instruction'].__add__(self.layers[i]['bias'])

            # Activate each neuron with the activation function
            for index, inactiveN in enumerate(self.layers[i]['instruction']):
                activeN = self.activationFunctions[self.layers[i]['activate']]['f'](inactiveN)
                numpy.put(self.layers[i]['instruction'], index, activeN)

        # Return the AI's decision
        return self.layers[self.layers['length'] - 1]['instruction']


    # Subroutine used to fit the trend given into the AI model (help it learn)
    def adjust(self, instructions, labels):

        """
        Purpose:


        :param instructions:
            Historical data relating to all previous successful hits.

        :param labels:
            Whether they are considered successful hits or not.

        :return:
        """

        # Initialise the current iteration
        iteration = 0

        # Continue this process for the amount of iterations defined
        while iteration < self.epochs:

            for i in range(len(instructions)):

                # Create a new array based on the instructions
                input = numpy.array([[set] for set in instructions[i]])

                # Makes a decision
                self.query(input)


                # Find the error between the actual answer and the AI's guess
                calculatedError = numpy.array([[factor] for factor in labels[i]])

                calculatedError = calculatedError.__sub__(self.layers[self.layers['length'] - 1]['instruction'])

                # Going in reverse, from the instruction node
                for i in range(self.layers['length'] - 1, -1, -1):

                    # Get the gradient of the instruction node (the output layer)
                    gradient = self.layers[i]['instruction'].copy()

                    # Activate each neuron in the gradient
                    for index, inactiveN in enumerate(gradient):
                        activeN = self.activationFunctions[self.layers[i]['activate']]["f'"](inactiveN)
                        numpy.put(gradient, index, activeN)

                    # Make a matrix of the gradients for each 'neuron'
                    gradient = gradient.__mul__(calculatedError)

                    gradient = gradient.__mul__(self.learningRate)

                    # This represents the delta gradient, or the difference
                    layer = self.layers[i - 1]['instruction'].copy() if i else input.copy()
                    layer = layer.transpose()

                    delta = gradient.__matmul__(layer)

                    # Compare the gradients between the correct input and the AI's decision/guess
                    # Hence adjust the biases and weights ('learns')
                    self.layers[i]['weights'] = self.layers[i]['weights'].__add__(delta)
                    self.layers[i]['bias'] = self.layers[i]['bias'].__add__(gradient)

                    # Calculate the total error
                    error = self.layers[i]['weights'].copy()
                    error = error.transpose()
                    calculatedError = error.__matmul__(calculatedError)

                # Increment iteration count
                iteration += 1

    # Subroutine which randomises the ordering of the historical data (makes sure AI does not rote learn)
    def mix(self, x, y):

        # Goes through each item of the list
        for i in range(len(y)):

            # Randomly shuffle the positions of teh items
            position = int(numpy.floor(random.random() * len(y)))
            tempY = y[i]
            tempX = x[i]
            y[i] = y[position]
            x[i] = x[position]
            y[position] = tempY
            x[position] = tempX

    # Subroutine that saves the model, 'pickling' it as binary encoding to save its data.
    def save(self, name, brainName):

        # Write a .pkl file which contains this object and all the data stored.
        with open(f"data/ai-models/{name}/{name}{brainName}.pkl", "wb") as export:
            pickle.dump(self, export, pickle.HIGHEST_PROTOCOL)

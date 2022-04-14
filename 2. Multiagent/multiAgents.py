# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #print('successorGameState:\n', successorGameState, sep = '')
        #print('newPos: ', list(newPos))
        #print('newFood: ', list(newFood))
        #print('newGhostStates: ', *newGhostStates)
        #print('newScaredTimes: ', list(newScaredTimes))

        "*** YOUR CODE HERE ***"
        foodDist = 9999
        foodList = newFood.asList()
        for food in foodList:
            foodDist = min(foodDist, manhattanDistance(food, newPos))
        if not foodList:
            foodDist = 0

        ghostDist = 9999
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0:
                ghostDist = min(ghostDist, manhattanDistance(ghost.getPosition(), newPos)) 

        if ghostDist < 2:
            return -9999

        return successorGameState.getScore() - 3 / (ghostDist + 1) + 5 / (foodDist + 1)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, 0, 0)[1]

    def minimax(self, gameState, depth, agentIndex):
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            return self.max_value(gameState, depth, agentIndex)
        else:
            return self.min_value(gameState, depth, agentIndex)


    def max_value(self, gameState, depth, agentIndex):
        value = float('-inf')
        retAction = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            succ = gameState.generateSuccessor(agentIndex, action)
            tempValue = self.minimax(succ, depth, agentIndex + 1)[0]
            if tempValue > value:
                value, retAction = tempValue, action

        return value, retAction


    def min_value(self, gameState, depth, agentIndex):
        value = float('inf')
        retAction = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            succAgent, succDepth = 0, depth + 1
        else:
            succAgent, succDepth = agentIndex + 1, depth

        for action in actions:
            succ = gameState.generateSuccessor(agentIndex, action)
            tempValue = self.minimax(succ, succDepth, succAgent)[0]
            if tempValue < value:
                value, retAction = tempValue, action

        return value, retAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float('-inf')
        beta = float('inf')
        return self.minimax(gameState, 0, 0, alpha, beta)[1]

    def minimax(self, gameState, depth, agentIndex, alpha, beta):
        #print('alpha: {}, beta: {}'.format(alpha, beta))
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            return self.max_value(gameState, depth, agentIndex, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)


    def max_value(self, gameState, depth, agentIndex, alpha, beta):
        value = float('-inf')
        retAction = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)

        for action in actions:
            succ = gameState.generateSuccessor(agentIndex, action)
            tempValue = self.minimax(succ, depth, agentIndex + 1, alpha, beta)[0]
            if tempValue > beta:
                return tempValue, retAction
            if tempValue > value:
                value, retAction = tempValue, action
            alpha = max(alpha, value)

        return value, retAction


    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        value = float('inf')
        retAction = Directions.STOP
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            succAgent, succDepth = 0, depth + 1
        else:
            succAgent, succDepth = agentIndex + 1, depth

        for action in actions:
            succ = gameState.generateSuccessor(agentIndex, action)
            tempValue = self.minimax(succ, succDepth, succAgent, alpha, beta)[0]
            if tempValue < alpha:
                return tempValue, retAction
            if tempValue < value:
                value, retAction = tempValue, action
            beta = min(beta, value)

        return value, retAction
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

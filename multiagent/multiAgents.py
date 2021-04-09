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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        smallestDistance = -1
        for foodCoordinate in newFood.asList():
            dis1 = manhattanDistance(newPos, foodCoordinate)
            if (dis1 < smallestDistance) or (smallestDistance == -1):
                smallestDistance = float(dis1)
        penalty = 0
        for ghostCoordinate in successorGameState.getGhostPositions():
            dis2 = manhattanDistance(newPos, ghostCoordinate)
            if dis2 <= 1:
                penalty += 1
        temp = 1/smallestDistance
        return successorGameState.getScore() + temp - penalty

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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        def minimax(gameAgent, gameDepth, gameState):
            if (gameState.isWin() is True) or (gameState.isLose() is True) or (gameDepth == self.depth):
                return self.evaluationFunction(gameState)
            elif gameAgent == 0:
                temp = []
                for state in gameState.getLegalActions(gameAgent):
                    temp.append(minimax(gameAgent + 1, gameDepth, gameState.generateSuccessor(gameAgent, state)))
                return max(temp)
            else:
                temp = []
                if gameState.getNumAgents() == gameAgent+1:
                    gameDepth = gameDepth + 1
                    for state in gameState.getLegalActions(gameAgent):
                        temp.append(minimax(0, gameDepth, gameState.generateSuccessor(gameAgent, state)))
                    return min(temp)
                else:
                    for state in gameState.getLegalActions(gameAgent):
                        temp.append(minimax(gameAgent + 1, gameDepth, gameState.generateSuccessor(gameAgent, state)))
                    return min(temp)
        maximum = float("-inf")
        for state in gameState.getLegalActions(0):
            temp = minimax(1, 0, gameState.generateSuccessor(0, state))
            if maximum < temp:
                maximum = temp
                gameAction = state
        return gameAction

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxValue(gameAgent, gameDepth, gameState, a, b):
            temp = float("-inf")
            for state in gameState.getLegalActions(gameAgent):
                temp = max(temp, arPruning(gameAgent + 1, gameDepth, gameState.generateSuccessor(gameAgent, state), a, b))
                if b < temp:
                    return temp
                a = max(a, temp)
            return temp

        def minValue(gameAgent, gameDepth, gameState, a, b):
            temp = float("inf")
            if gameState.getNumAgents() == gameAgent + 1:
                gameDepth = gameDepth + 1
                for state in gameState.getLegalActions(gameAgent):
                    temp = min(temp, arPruning(0, gameDepth, gameState.generateSuccessor(gameAgent, state), a, b))
                    if a > temp:
                        return temp
                    b = min(b, temp)
                return temp
            else:
                for state in gameState.getLegalActions(gameAgent):
                    temp = min(temp, arPruning(gameAgent + 1, gameDepth, gameState.generateSuccessor(gameAgent, state), a, b))
                    if a > temp:
                        return temp
                    b = min(b, temp)
                return temp
        def arPruning (gameAgent, gameDepth, gameState, a, b):
            if (gameState.isWin() is True) or (gameState.isLose() is True) or (gameDepth == self.depth):
                return self.evaluationFunction(gameState)
            elif gameAgent == 0:
                return maxValue(gameAgent, gameDepth, gameState, a, b)
            else:
                return minValue(gameAgent, gameDepth, gameState, a, b )
        maximum = float("-inf")
        a = float("-inf")
        b = float("inf")
        for state in gameState.getLegalActions(0):
            temp = arPruning(1, 0, gameState.generateSuccessor(0, state), a, b)
            if maximum < temp:
                maximum = temp
                gameAction = state
            if maximum > b:
                return maximum
            a = max(a, maximum)
        return gameAction

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
        def expectimax(gameAgent, gameDepth, gameState):
            if (gameState.isWin() is True) or (gameState.isLose() is True) or (gameDepth == self.depth):
                return self.evaluationFunction(gameState)
            elif gameAgent == 0:
                temp = []
                for state in gameState.getLegalActions(gameAgent):
                    temp.append(expectimax(gameAgent + 1, gameDepth, gameState.generateSuccessor(gameAgent, state)))
                return max(temp)
            else:
                temp = []
                if gameState.getNumAgents() == gameAgent + 1:
                    gameDepth = gameDepth + 1
                    for state in gameState.getLegalActions(gameAgent):
                        temp.append(expectimax(0, gameDepth, gameState.generateSuccessor(gameAgent, state)))
                    length = len(gameState.getLegalActions(gameAgent))
                    return float(sum(temp)) / length
                else:
                    for state in gameState.getLegalActions(gameAgent):
                        temp.append(expectimax(gameAgent + 1, gameDepth, gameState.generateSuccessor(gameAgent, state)))
                    length = len(gameState.getLegalActions(gameAgent))
                    return float(sum(temp)) / length
        maximum = float("-inf")
        for state in gameState.getLegalActions(0):
            temp = expectimax(1, 0, gameState.generateSuccessor(0, state))
            if maximum < temp:
                maximum = temp
                gameAction = state
        return gameAction

        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    powerRemaining = len(currentGameState.getCapsules())
    foodList = newFood.asList()
    distanceToFood =[0]
    for coordinate in foodList:
        distanceToFood.append(manhattanDistance(newPos, coordinate))
    ghostPos =[]
    for ghost in newGhostStates:
        ghostPos.append(ghost.getPosition())
    ghostDistance =[0]
    for coordinate in ghostPos:
        ghostDistance.append(manhattanDistance(newPos, coordinate))
    result = 0
    noFood = len(newFood.asList(False))
    totalScoredTime = sum(newScaredTimes)
    totalGhostDistance = sum(ghostDistance)
    temp = 0
    if sum(distanceToFood) > 0:
        temp = 1.0/sum(distanceToFood)
    result += currentGameState.getScore() + temp + noFood
    if totalScoredTime > 0:
        result += totalScoredTime + (-1 * powerRemaining) + (-1 * totalGhostDistance)
    else:
        result += totalGhostDistance + powerRemaining
    return result

    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction

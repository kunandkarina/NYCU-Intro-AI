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
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        # raise NotImplementedError("To be implemented")

        def minmax(depth, agent, gameState):

            # terminal condition
            if gameState.isWin() or gameState.isLose() or depth > self.depth:
                return self.evaluationFunction(gameState)
            
            # all legal actions for agents' next step
            actions = gameState.getLegalActions(agent)   # actions type: lists
 
            # store value of every possible action
            actionScores = []
            # run all legal action
            for action in actions:
                # nextState: gamestate after taking legal action
                nextState = gameState.getNextState(agent, action)
                # all agent are done, pacman go to next level
                if (agent + 1) >= gameState.getNumAgents():
                    actionScores.append(minmax(depth+1, 0, nextState))
                    # actionScore = minmax(depth+1, 0, nextState)
                    # actionScores.append(actionScore)
                # ghost n will use ghost n-1's state
                else: 
                    actionScores.append(minmax(depth, agent+1, nextState))
                    # actionScore = minmax(depth, agent + 1, nextState)
                    # actionScores.append(actionScore)
           
            # performing minmax procedure
            # pacman: return max value
            if agent == 0:
                if depth == 1:      # return the next action when comes back to the root
                    for i in range(len(actionScores)):
                        if actionScores[i] == max(actionScores):
                            return actions[i]
                else:
                    actionScore = max(actionScores)

            # ghosts: return min value
            else:
                actionScore = min(actionScores)
            return actionScore

        # implement minmax agent
        return minmax(1, 0, gameState)            
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        # raise NotImplementedError("To be implemented")
        def AlphaBeta(depth, agent, gameState, alpha, beta):
            
            # terminal condition
            if gameState.isWin() or gameState.isLose() or depth > self.depth:
                return self.evaluationFunction(gameState)
            
            # all legal actions for pacmans' next step
            actions = gameState.getLegalActions(agent)

            # store value of every possible action
            actionScores = []
            for action in actions:
                # nextState: gamestate after taking legal action
                nextState = gameState.getNextState(agent, action)
                # all agent are done, pacman go to next level
                if (agent + 1) >= gameState.getNumAgents():
                    # actionScores.append(AlphaBeta(depth + 1, 0, nextState, alpha, beta))
                    actionScore = AlphaBeta(depth + 1, 0, nextState, alpha, beta)
                    actionScores.append(actionScore)
                # ghost n will use ghost n-1's state
                else:
                    # actionScores.append(AlphaBeta(depth, agent + 1, nextState, alpha, beta))
                    actionScore = AlphaBeta(depth, agent + 1, nextState, alpha, beta)
                    actionScores.append(actionScore)
                
                # pruning the branches
                # pacman / maximize 
                if agent == 0:
                    if actionScore > beta:
                        return actionScore
                    alpha = max(alpha, actionScore)
                
                # ghost / minimize
                else:
                    if actionScore < alpha:
                        return actionScore
                    beta = min(beta, actionScore)

            # performing minmax procedure
            # pacman : return the maximum actionscore
            if agent == 0:
                if depth == 1:      # return the next action when comes back to the root
                    for i in range(len(actionScores)):
                        if actionScores[i] == max(actionScores):
                            return actions[i]
                else:
                    actionScore = max(actionScores)
            # ghost : return the minimim actionscore        
            else:
                actionScore = min(actionScores)
            return actionScore
            
        # initialize alpha and beta
        alpha = -float('inf')
        beta = float('inf')

        # implement alphabeta pruning
        return AlphaBeta(1, 0, gameState, alpha, beta)
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        # raise NotImplementedError("To be implemented")
        def Expectimax(depth, agent, gameState):
            
            # terminal condition
            if gameState.isWin() or gameState.isLose() or depth > self.depth:
                return self.evaluationFunction(gameState)
            
            # all legal actions for pacmans' next step
            actions = gameState.getLegalActions(agent)

            # store value of every possible action
            actionScores = []
            for action in actions:
                # nextState: gamestate after taking legal action
                nextState = gameState.getNextState(agent, action)
                # all agent are done, pacman go to next level
                if (agent + 1) >= gameState.getNumAgents():
                    actionScores.append(Expectimax(depth + 1, 0, nextState))
                # ghost n will use ghost n-1's state
                else:
                    actionScores.append(Expectimax(depth, agent + 1, nextState))

            # expextimax procedure
            # pacman : return the maximun actionScore
            if agent == 0:    
                if depth == 1:   # return the next action when comes back to the root
                    for i in range(len(actionScores)):
                        if actionScores[i] == max(actionScores):
                            return actions[i]
                else:
                    actionScore = max(actionScores)
            # ghosts : choose expectation score instead of minimum
            else:
                actionScore = float(sum(actionScores)/len(actionScores))
            return actionScore

        # implement expextimax agent
        return Expectimax(1, 0, gameState)
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    pos = currentGameState.getPacmanPosition()          # pacman's current position
    food = currentGameState.getFood()                   # foods list
    capsules = currentGameState.getCapsules()           # capsules list
    ghostStates = currentGameState.getGhostStates()     # ghost's current state
    score = currentGameState.getScore()                 # current score
    # Set up the weight
    WEIGHT_FOOD = 5.0
    WEIGHT_CAPSULE = 30.0
    WEIGHT_GHOST = -10.0
    WEIGHT_SCARED_GHOST = 250.0

    # while the food is closer, we'll get higher score
    foodDis = [util.manhattanDistance(pos, foodPos) for foodPos in food.asList()]
    if len(foodDis):
        score += WEIGHT_FOOD / min(foodDis)    
    else:
        score += WEIGHT_FOOD

    # while the capsule is closer, we'll get higher score
    capDis = [util.manhattanDistance(pos, capPos) for capPos in capsules]
    if len(capDis):
        score += WEIGHT_CAPSULE / min(capDis)  
    else:
        score += WEIGHT_CAPSULE

    # while facing ghosts
    for ghost in ghostStates:
        distance = util.manhattanDistance(pos, ghost.getPosition())
        if distance > 0:
            if ghost.scaredTimer > 0:
                # while approaching scared ghost, higher the score
                score += WEIGHT_SCARED_GHOST / distance
            else:
                # while approaching ghosts, lower the score
                score += WEIGHT_GHOST / distance

    return score    
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction

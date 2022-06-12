# myTeam.py
# ---------
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


import dis
from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from distanceCalculator import Distancer
#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
                first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the nightly contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """

    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''


    def chooseAction(self, gameState):
        """
        Picks among actions randomly.
        """
        actions = gameState.getLegalActions(self.index)

        '''
        You should change this in your own agent.
        '''

        return random.choice(actions)

class ReflexCaptureAgent(CaptureAgent):
    """
    A base class for reflex agents that chooses score-maximizing actions
    """

    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        self.holdFood = 0 # 초기에 agent가 가지고 있는 음식의 개수

        CaptureAgent.registerInitialState(self, gameState)
        distancer = Distancer(gameState.data.layout)
        distancer.getMazeDistances()

        if self.red: # 레드 팀일 때는 중간보다 한 칸 왼쪽을 중심으로 간주
            self.middle = [(gameState.data.layout.width // 2 - 1, i) for i in range(1, gameState.data.layout.height) if not gameState.hasWall(gameState.data.layout.width // 2 - 1, i)]
        else: # 블루 팀일 때는 중간보다 한 칸 오른쪽을 중심으로 간주
            self.middle = [(gameState.data.layout.width // 2 + 1, i) for i in range(1, gameState.data.layout.height) if not gameState.hasWall(gameState.data.layout.width // 2 + 1, i)]

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)  
        values = [self.evaluate(gameState, a) for a in actions]

        maxValue = max(values) # 점수가 가장 좋은 action들을 선택
        bestActions = [a for a, v in zip(actions, values) if v == maxValue]

        foodLeft = len(self.getFood(gameState).asList())
        if foodLeft <= 2: # 게임의 극후반부일 때에서 분기된 케이스
            bestDist = 9999
            for action in actions:
                successor = self.getSuccessor(gameState, action)
                pos2 = successor.getAgentPosition(self.index)
                dist = self.getMazeDistance(self.start,pos2)
                if dist < bestDist:
                    bestAction = action
                    bestDist = dist
            return bestAction

        retAction = random.choice(bestActions) # 위에서 선택한 action 중 1개 선택
        successor = self.getSuccessor(gameState, retAction)

        if not successor.getAgentState(self.index).isPacman: # ghost로 돌아오면 가지고 있는 음식 개수를 0개로 초기화
            self.holdFood = 0
        else: # pacman인 상태가 유지되는 동안에 먹는 음식 개수를 더한다.
            self.holdFood += len(self.getFood(gameState).asList()) - len(self.getFood(successor).asList())

        return retAction

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != util.nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

    def getFeatures(self, gameState, action):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
        return features

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.  They can be either
        a counter or a dictionary.
        """
        return {'successorScore': 1.0}

class OffensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """
    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        foodList = self.getFood(successor).asList()
        myPos = successor.getAgentState(self.index).getPosition()

        if len(foodList) > 0: # 가장 가까운 food와의 거리를 구한다.
            minDistanceToFood = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistanceToFood

        features['justDied'] = 0 # 리스폰 지점과 아주 가까이 있으면 빠르게 탈출
        if self.getMazeDistance(myPos, self.start) < 3:
            features['justDied'] = 99999

        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]

        minDistanceToOpponent = min([self.getMazeDistance(myPos, a.getPosition()) for a in enemies if a.scaredTimer == 0] + [4])
        if minDistanceToOpponent < 4: # 적에게 큰 위협을 받는 거리를 4 미만으로 간주
            features['distanceToOpponent'] = minDistanceToOpponent
            features['successorScore'] = -0.1 * len(foodList)
        elif minDistanceToOpponent < 2: # 2 미만일 때는 아주 큰 위협
            features['distanceToOpponent'] = -1000 * minDistanceToOpponent
            features['successorScore'] = -len(foodList)
        else: # 4 이상일 때는 비교적 안전한 것으로 모두 동일하게 간주
            features['distanceToOpponent'] = 5
            features['successorScore'] = len(self.getFood(gameState).asList()) - len(foodList)

        capsuleList = self.getCapsules(successor)
        features['distanceToCapsule'] = 0
        if len(capsuleList) > 0: # 가장 가까운 capsule과의 거리를 구한다.
            minDistanceToCapsule = min([self.getMazeDistance(myPos, capsule) for capsule in capsuleList])
            features['distanceToCapsule'] = minDistanceToCapsule
            if len(self.getCapsules(gameState)) > len(capsuleList) and minDistanceToOpponent > 3: # capsule을 먹을 수 있고 적과 멀리 떨어져 있으면 capsule과의 거리 가중치를 0으로 설정
                features['distanceToCapsule'] = 0
        else:
            features['distanceToCapsule'] = -100 * len(self.getCapsules(gameState))

        scaredGhost = [filter(lambda x: x.scaredTimer > 0, invaders)] # 적 중에서 scared 상태인 ghost에 대해 kill을 하도록 유도
        features['scaredGhost'] = len(self.getOpponents(successor))
        if len(scaredGhost) > 0:
            features['scaredGhost'] = -len(scaredGhost)

        minDistanceToMiddle = min([self.getMazeDistance(myPos, mid) for mid in self.middle])
        features['distanceToMiddle'] = minDistanceToMiddle
        if self.holdFood == 0: # 가지고 있는 음식의 개수가 0이면 계속해서 음식을 먹으러 간다
            features['distanceToMiddle'] = 0
        else: # 음식을 가지고 있는 상황에서는 점수를 얻으러 가는 것을 고려한다.
            features['distanceToMiddle'] = 5 * minDistanceToMiddle

        features['stop'] = 0
        features['reverse'] = 0
        if action == Directions.STOP: # stop은 대부분의 경우에서 좋은 action이 아니라는 것을 고려 
            features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction] # 현재의 action과 반대도 고려
        if action == rev: 
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {'successorScore': 100,
                'justDied': -1,
                'distanceToFood': -2,
                'distanceToOpponent': 30,
                'distanceToCapsule': -10,
                'scaredGhost': -5,
                'distanceToMiddle': -8,
                'stop': -100,
                'reverse': -2}

class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        foodList = self.getFood(successor).asList()
        features['successorScore'] = -len(foodList) #self.getScore(successor)
        
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        minDistanceToMiddle = min([self.getMazeDistance(myPos, mid) for mid in self.middle])
        features['distanceToMiddle'] = minDistanceToMiddle

        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman: features['onDefense'] = 0

        # Computes distance to invaders we can see
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]

        features['numInvaders'] = len(invaders)
        features['notDefence'] = 0
        minDistanceToOpponent = min([self.getMazeDistance(myPos, a.getPosition()) for a in enemies])
        if len(invaders) == 0 and minDistanceToOpponent > 10: # 침입자가 없고 가장 가까운 적과의 거리가 10을 초과하면 안전한 상황으로 간주
            features['notDefence'] = 1
            features['invaderDistance'] = 0

        if self.holdFood > 0: # 음식을 가지고 있는 상황에서는 점수를 얻으러 가는 것을 고려한다.
            features['distanceToMiddle'] = minDistanceToMiddle

        if len(invaders) > 0: # 침입자가 생기면 중간에서 머무르기보다 침입자에게 집중한다.
            features['invaderDistance'] = min(dists)
            features['distanceToMiddle'] = 0
    
        if len(foodList) > 0:
            minDistanceToFood = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistanceToFood

        myTeam = [successor.getAgentState(i) for i in self.getTeam(successor)]
        scaredGhost = [a for a in myTeam if not a.isPacman and a.getPosition() != None and a.scaredTimer > 0]
        if len(scaredGhost) > 0:  # 자신이 scared 상태가 됐을 때의 경우
            if min(dists + [4]) < 4: # 잡히지 않을 최소한의 거리를 유지한다.
                features['invaderDistance'] = 10 * len(scaredGhost)
            elif min(dists + [4]) < 2:
                features['invaderDistance'] = 10000 * len(scaredGhost)

        features['stop'] = 0
        features['reverse'] = 0
        if action == Directions.STOP: 
            features['stop'] = 1
        rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
        if action == rev: 
            features['reverse'] = 1

        return features

    def getWeights(self, gameState, action):
        return {'numInvaders': -10000,
                'onDefense': 100,
                'invaderDistance': -50,
                'successorScore': 100,
                'notDefence': 1000,
                'distanceToFood': 3,
                'distanceToMiddle': -20,
                'stop': -100,
                'reverse': -2}
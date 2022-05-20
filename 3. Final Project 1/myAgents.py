# myAgents.py
# ---------------
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

from game import Agent
from searchProblems import PositionSearchProblem

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        global position, action, goal

        if self.index not in action:
            flag = False if state.getNumFood() < len(goal) else True
            temp = self.findPathToClosestDot(AnyFoodSearchProblem(state, self.index), flag)
            if temp[1] == ['Stop']:
                action[self.index] = temp[1]
            goal.add(temp[0])
            position[self.index] = temp[0]
            action[self.index] = temp[1]

        if len(action[self.index]) == 1 and action[self.index][0] == 'Stop':
            return 'Stop'
        
        if not action[self.index]:
            goal.discard(position[self.index])
            flag = False if state.getNumFood() < len(goal) else True
            temp = self.findPathToClosestDot(AnyFoodSearchProblem(state, self.index), flag)
            if temp[1] == ['Stop']:
                action[self.index] = temp[1]
            goal.add(temp[0])
            position[self.index] = temp[0]
            action[self.index] = temp[1]

        if len(action[self.index]) == 1 and action[self.index][0] == 'Stop':
            return 'Stop'

        return action[self.index].pop()
        

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE ***"
        global position, action, goal
        position = {}
        action = {}
        goal = set()


    def findPathToClosestDot(self, problem, flag):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """

        "*** YOUR CODE HERE ***"
        global goal
        
        startPosition = problem.getStartState()
        queue = util.Queue()
        visited, track = {}, {}
        check, count = 0, 0

        queue.push((startPosition, []))
        visited[startPosition] = 'Stop'
        
        while not queue.isEmpty() and count < 548:
            curr = queue.pop()
            visited[curr[0]] = curr[1]
            count += 1
            
            if problem.isGoalState(curr[0]):
                if flag:
                    if curr[0] not in goal:
                        check = curr[0]
                        break
                else:
                    check = curr[0]
                    break
            
            for pos, act, cost in problem.getSuccessors(curr[0]):
                if pos not in visited and pos not in track:
                    queue.push((pos, act))
                    track[pos] = curr[0]
        
        if not check or count == 548:
            return 0, ['Stop']
        
        returnGoal = check
        returnRoute = []
        while check in track:
                temp = track[check]
                returnRoute.append(visited[check])
                check = temp
        
        return returnGoal, returnRoute


"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

# Copy/paste the same as MyAgent to check my code for all test cases via autograder.py.

class ClosestDotAgent(Agent):

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        global position, action, goal

        if self.index not in action:
            flag = False if state.getNumFood() < len(goal) else True
            temp = self.findPathToClosestDot(AnyFoodSearchProblem(state, self.index), flag)
            if temp[1] == ['Stop']:
                action[self.index] = temp[1]
            goal.add(temp[0])
            position[self.index] = temp[0]
            action[self.index] = temp[1]

        if len(action[self.index]) == 1 and action[self.index][0] == 'Stop':
            return 'Stop'
        
        if not action[self.index]:
            goal.discard(position[self.index])
            flag = False if state.getNumFood() < len(goal) else True
            temp = self.findPathToClosestDot(AnyFoodSearchProblem(state, self.index), flag)
            if temp[1] == ['Stop']:
                action[self.index] = temp[1]
            goal.add(temp[0])
            position[self.index] = temp[0]
            action[self.index] = temp[1]

        if len(action[self.index]) == 1 and action[self.index][0] == 'Stop':
            return 'Stop'

        return action[self.index].pop()
        

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE ***"
        global position, action, goal
        position = {}
        action = {}
        goal = set()


    def findPathToClosestDot(self, problem, flag):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """

        "*** YOUR CODE HERE ***"
        global goal
        
        startPosition = problem.getStartState()
        queue = util.Queue()
        visited, track = {}, {}
        check, count = 0, 0

        queue.push((startPosition, []))
        visited[startPosition] = 'Stop'
        
        while not queue.isEmpty() and count < 548:
            curr = queue.pop()
            visited[curr[0]] = curr[1]
            count += 1
            
            if problem.isGoalState(curr[0]):
                if flag:
                    if curr[0] not in goal:
                        check = curr[0]
                        break
                else:
                    check = curr[0]
                    break
            
            for pos, act, cost in problem.getSuccessors(curr[0]):
                if pos not in visited and pos not in track:
                    queue.push((pos, act))
                    track[pos] = curr[0]
        
        if not check or count == 548:
            return 0, ['Stop']
        
        returnGoal = check
        returnRoute = []
        while check in track:
                temp = track[check]
                returnRoute.append(visited[check])
                check = temp
        
        return returnGoal, returnRoute

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        if self.food[x][y] == True:
            return True
        return False


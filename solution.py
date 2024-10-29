class Solution(object):
    def maxMoves(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        starting_frontier = []
        for i in range(len(grid)):
            starting_frontier.append(Node( (i,0,grid[i][0]) ) )

        problem = Problem(grid)
        return self.a_star(problem, starting_frontier)

    
    def a_star(self, problem, frontier):
        best = 0

        f = lambda n: n.path_cost + problem.h(n)    
        node = None 
        explored = set()

        while(len(frontier) > 0):
            node = frontier.pop()
            if problem.goal_test(node.state):
                break
            
            if node.solution() > best:
                best = node.solution()

            explored.add(node.state)

            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)
        
        if node.solution() > best:
            best = node.solution()
        
        return best

class Problem:
    def __init__(self, grid, goal=None):
        self.grid = grid
        self.m = len(grid)
        self.n = len(grid[0])
        self.goal = goal

    def actions(self, state):
        res = []
        i,j,val = state

        #if we reach the rightmost col of the grid
        if j == self.n-1:
            return res

        if i>0 and self.grid[i-1][j+1] > val:
            res.append('up')
        if self.grid[i][j+1] > val:
            res.append('forward')
        if i<self.m-1 and self.grid[i+1][j+1] > val:
            res.append('down')

        return res

    def result(self, state, action):
        i,j,_ = state

        if action == 'up':
            return (i-1,j+1,self.grid[i-1][j+1])
        elif action == 'forward':
            return (i,j+1,self.grid[i][j+1])
        return (i+1,j+1,self.grid[i+1][j+1])

    def goal_test(self, state):
        #If we are in the last column we reach the highest possible 
        #number of moves
        return state[1] == self.n-1

    def path_cost(self, c, state1, action, state2):
        return c - 1

    def h(self, node):
        #If next chosen value z has a value near to the current one x
        #then the probability to find a value y greater than z is 
        #minimized since it does not span a big interval on the set
        #of natural numbers set. This is a "local" heuristic.
        
        #Index 2 is relative to the node's value.
        #Remember: we know that the "series" is strictly monotonically increasing,
        #therefore h(n) > 0 for each n.
        return node.state[2] - node.parent.state[2]
        

class Node:
    '''
    A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.
    '''

    def __init__(self, state, parent=None, action=None, path_cost=0):
        #Create a search tree Node, derived from a parent by an action.
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, node):
        #Values comparison
        return self.state[2] < node.state[2]

    def expand(self, problem):
        #List the nodes reachable in one step from this node.
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(
                                                    self.path_cost, self.state, 
                                                    action, next_state))
        return next_node

    def solution(self):
        #Rerurns the column number. For the problem specifications this number
        #is equal to the moves we performed until this (self) node.
        return self.state[1]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

import sys, os
from copy import deepcopy
try:
    import queue
except ImportError:
    import Queue as queue

#Initial State of puzzle
class Node:
    def __init__(self, data, moves):
        self.data = deepcopy(data)
        self.moves = deepcopy(moves)
        self.Aggregate = 0
        self.Heu = 0
        self.Current = len(moves)
        self.NewCost()

    #Check Priority Queue
    def __lt__(self, other):
        return self.Aggregate < other.Aggregate

    #Define Heuristic function which is Manhattan Distance from the current to the final state of each number.
    def Heuristic(self):
        Distance = 0
        m = list(self.data)
        for i in range(4):
            for j in range(4):
                Row_Position = (m[i][j] - 1) / 4
                Column_Position = (m[i][j] - 1) % 4
                if (Column_Position == j or Row_Position == i) and (
                            (Row_Position == 0 and i == 3 or Row_Position == 3 and i == 0) or (
                                            Column_Position == 0 and j == 3 or Column_Position == 3 and j == 0)):
                    Distance += 1
                else:
                    Distance += abs(i - Row_Position) + abs(j - Column_Position)

        self.Heu = Distance

    #Astar algorithm adding cost of moving the number from current to final position and current cost from initial state.
    def NewCost(self):
        self.Heuristic()
        self.Current = len(self.moves)
        self.Aggregate = self.Current + self.Heu

#Check if final state is reached
def is_goal(node):
    data = list(node.data)
    for i in range(4):
        for j in range(4):
            if int(data[i][j]) != int(i * 4 + j + 1):
                return False;
    return True

#Sliding Rows Left or Right
def Move_Row(node, list, rotate):
    if rotate == 'L':
        k = node.data[list]
        first = k.pop(0)
        k.append(first)
        move = 'L' + str(list + 1)
        node.moves.append(move)
    else:
        k = node.data[list]
        last = k.pop(3)
        k.insert(0, last)
        move = 'R' + str(list + 1)
        node.moves.append(move)

#Sliding Columns Up or Down
def Move_Col(node, list, rotate):
    if rotate == 'U':
        k = []
        for i in range(0, 4):
            k.append(node.data[i][list])
        first = k.pop(0)
        k.append(first)
        for i in range(0, 4):
            node.data[i][list] = k[i]
        move = 'U' + str(list + 1)
        node.moves.append(move)
    else:
        k = []
        for i in range(0, 4):
            k.append(node.data[i][list])
        last = k.pop(3)
        k.insert(0, last)
        for i in range(0, 4):
            node.data[i][list] = k[i]
        move = 'D' + str(list + 1)
        node.moves.append(move)

#Successor function evaluate the NewCost for each of the Up, Down, Left, Right moves
def successor(node):
    data = node.data[0:]
    moves = node.moves[0:]
    nexts = []
    for i in range(0, 4):

        Up = Node(data, moves)
        Move_Col(Up, i, 'U')
        Up.NewCost()
        nexts.append(Up)

        Down = Node(data, moves)
        Move_Col(Down, i, 'D')
        Down.NewCost()
        nexts.append(Down)

        Left = Node(data, moves)
        Move_Row(Left, i, 'L')
        Left.NewCost()
        nexts.append(Left)

        Right = Node(data, moves)
        Move_Row(Right, i, 'R')
        Right.NewCost()
        nexts.append(Right)

    return nexts

def get_string(node):
    current_string = ''
    for i in range(0, 4):
        for j in range(0, 4):
            if len(str(node.data[i][j])) < 2:
                current_string = current_string + ' ' + str(node.data[i][j])
            else:
                current_string += str(node.data[i][j])
            if j == 3:
                current_string += '\n'
    return current_string

#After reading the current State if it is not goal state then successor function is called. Each of the State is added to the priority queue, so get the highest priority value from the fringe
def puzzle(Start):
    array = queue.PriorityQueue()
    visited = set()
    if (is_goal(Start)):
        return Start
    array.put(Start)
    isgoal = False
    while True:
        node = array.get()
        if (is_goal(node)):
            isgoal = True
            return node
            break
        else:
            nexts = successor(node)
            for next in nexts:
                if get_string(next) not in visited:
                    array.put(next)
            visited.add(get_string(next))

def printable_path(node):
    path = ''
    for move in node.moves:
        path += move + ' '
    return path

def main():
       data = []
       with open(sys.argv[1], 'r') as file:
          for line in file:
            data.append([int(x) for x in line.split()]);
       Start = Node(data, [])
       print printable_path(puzzle(Start))

main()

from project_od.utils import PriorityQueue, around_4
from functools import cache

class GridAgent:
    class Node:
        def __init__(self, pos, parent=None, cost=0) -> None:
            self.pos = pos
            self.parent = parent
            self.cost = cost
        
        def backtrack(self):
            node, path_back = self, []
            while node:
                path_back.append(node.pos)
                node = node.parent
            return list(reversed(path_back))[1:]

        def __eq__(self, other):
            return isinstance(other, GridAgent.Node) and self.pos == other.pos

        def __hash__(self):
            return hash(self.pos)

        def __lt__(self, node):
            return self.pos < node.pos
        
    def __init__(self, grid, wall=[], slow=[]) -> None:
        self.grid = grid
        self.wall = wall
        self.slow = slow

    @cache
    def shortest_path(self, src, target):
        node = self.grid_astar(src, target)
        if node != None:
            return node.backtrack()
        return []
                
    def distance(self, pos, target):
        return sum(abs(st - ta) for st, ta in zip(pos, target))

    def cost(self, cost, pos):
        if self.grid[pos[1]][pos[0]] in self.slow:
            return cost + 3
        return cost + 1

    def grid_astar(self, src, target):
        distance = cache(self.distance)
        function = cache(lambda node: node.cost / 2 + distance(node.pos, target))
        node = GridAgent.Node(src)
        border = PriorityQueue(function)
        border.add(node)
        explored = set()
        while not border.isEmpty():
            node = border.pop()
            if node.pos == target:
                return node
            explored.add(node.pos)

            # Combo action and result
            for np in around_4(*node.pos):
                if np[1] < len(self.grid) and np[0] < len(self.grid[np[1]]) and self.grid[np[1]][np[0]] not in self.wall:
                    child = GridAgent.Node(np, node, self.cost(node.cost, np))

                    if child not in border:
                        if child.pos not in explored:
                            border.add(child)
                    else:
                        if function(child) < border[child]:
                            border.remove(child)
                            border.add(child)
        return None
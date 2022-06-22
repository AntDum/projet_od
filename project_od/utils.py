from random import shuffle
from math import sqrt, floor
from heapq import heappush, heappop, heapify
from copy import deepcopy, copy

def norm(x, _min, _max):
    return (x - _min) / (_max - _min)

def lerp(x, _min, _max):
    return (_max - _min) * x + _min

def bezier_lin(t, p_0, p_1):
    return p_0 + (p_1 - p_0) * t

def bezier_quad(t, p_0, p_1, p_2):
    return p_1 + (1-t)**2*(p_0 - p_1) + t**2*(p_2 - p_1)

def bezier_cub(t, p_0, p_1, p_2, p_3):
    return (1-t)**3*p_0 + 3*(1-t)**2*t*p_1 + 3*(1-t)*t**2*p_2 + t**3*p_3

bezier = bezier_cub

def map(x, source_min, source_max, dest_min, dest_max):
    return lerp(norm(x, source_min, source_max), dest_min, dest_max)

def clamp(x, min_val, max_val):
    return min(max(x, min_val), max_val)

class Perlin:
    grad2 = [[-1,1],[0,1],[1,1],
            [-1,0],       [1,0],
            [-1,-1],[0,-1],[1,-1]]

    def __call__(self, x, y, smouth=20, rounded=3) -> float:
        return round((self.noise(x/smouth,y/smouth)), rounded)

    def __init__(self):
        size = 62740

        self.p = list(range(size))

        shuffle(self.p)

        self.p += self.p

    def dot(self, g,x,y):
        return g[0] * x + g[1] * y

    def noise(self, xin, yin):
        # Skew the input space to determine which simplex cell we're in
        F2 = 0.5 * (sqrt(3.0) - 1.0)
        s = (xin + yin) * F2 # Hairy factor for 2D

        i =  floor(xin + s)
        j =  floor(yin + s)

        G2 = (3.0 - sqrt(3.0)) / 6.0
        t = (i + j) * G2
        # Unskew the cell origin back to (x,y) space
        X0 = i  -t
        Y0 = j - t
        # The x,y distances from the cell origin
        x0 = xin - X0
        y0 = yin - Y0


        # Determine which simplex we are in.
        #i1, j1 Offsets for second (middle) corner of simplex in (i,j) coords

        # lower triangle, XY order: (0,0)->(1,0)->(1,1)
        if(x0 > y0):
            i1 = 1
            j1 = 0
        # upper triangle, YX order: (0,0)->(0,1)->(1,1)
        else:
            i1 = 0
            j1 = 1

        #     A step of (1,0) in (i,j) means a step of (1-c,-c) in (x,y),
        # and a step of (0,1) in (i,j) means a step of (-c,1-c) in (x,y),
        # where c = (3-sqrt(3))/6

        # Offsets for middle corner in (x,y) unskewed coords
        x1 = x0 - i1 + G2
        y1 = y0 - j1 + G2

        # Offsets for last corner in (x,y) unskewed coords
        x2 = x0 - 1.0 + 2.0 * G2
        y2 = y0 - 1.0 + 2.0 * G2

        # Work out the hashed gradient indices of the three simplex corners
        ii = i & 255
        jj = j & 255

        gi0 = self.p[ii + self.p[jj]] % 8
        gi1 = self.p[ii + i1 + self.p[jj+j1]] % 8
        gi2 = self.p[ii+1 + self.p[jj+1]] % 8

        #n0, n1, n2 Noise contributions from the three corners

        # Calculate the contribution from the three corners
        t0 = 0.5 - x0**2 - y0**2
        if(t0 < 0):
            n0 = 0
        else:
            t0 *= t0
            n0 = t0 * t0 * self.dot(Perlin.grad2[gi0], x0, y0)

        t1 = 0.5 - x1**2 - y1**2
        if(t1 < 0):
            n1 = 0
        else:
            t1 *= t1
            n1 = t1 * t1 * self.dot(Perlin.grad2[gi1], x1, y1)

        t2 = 0.5 - x2**2 - y2**2
        if(t2 < 0):
            n2 = 0
        else:
            t2 *= t2
            n2 = t2 * t2 * self.dot(Perlin.grad2[gi2], x2, y2)

        # Add contributions from each corner to get the final noise value.
        # The result is scaled to return values in the interval [-1,1].
        return 70 * (n0 + n1 + n2)


class PriorityQueue:
    def __init__(self, function=lambda x: x):
        self.queue = []
        self.function = function

    def __str__(self) -> str:
        return ' '.join([str(i) for i in self.queue])
    
    def __len__(self) -> int:
        return len(self.queue)
    
    def isEmpty(self) -> bool:
        return len(self) == 0

    def add(self, item, key=None) -> None:
        if key==None:
            heappush(self.queue, (self.function(item), item))
        else:
            heappush(self.queue, (key, item))


    def insert(self, key, item) -> None:
        heappush(self.queue, (key, item))

    def pop(self):
        return heappop(self.queue)[1]
    
    def __iter__(self):
        r = copy(self)
        for _ in range(len(r)):
            yield r.pop()

    def __copy__(self):
        r = PriorityQueue()
        r.queue = copy(self.queue)
        r.function = copy(self.function)
        return r

    def remove(self, key):
        pos = None
        for i, (_, item) in enumerate(self.queue):
            if item == key:
                pos = i
                break
        if pos != None:
            ele = self.queue[pos]
            del self.queue[pos]
            heapify(self.queue)
            return ele[1]

    def __getitem__(self, key):
        for value, item in self.queue:
            if item == key:
                return value

    def __contains__(self, key):
        for _, item in self.queue:
            if item == key:
                return True
        return False

def around_4(x, y):
    return (x-1,y),(x, y-1),(x+1,y),(x,y+1)

def around_8(x, y):
    return (x-1,y),(x-1,y-1),(x, y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1)
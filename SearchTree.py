import queue
import random
import time
import gif_creator
import board_creator

from State import State


class SearchTree:

    def __init__(self,starter=None,random=False,hei=None,wid=None,col=5):
        if random:
            self.play(hei,wid)
        else:
            assert starter is not None
            self.root = State(starter,len(starter),len(starter[0]),c=col)
        self.H = self.root.hei
        self.W = self.root.wid
        self.size = self.H * self.W
        self.bestScore = 0
        self.howtowin = []
        self.winner = None
        self.logger = ""


    def log(self):
        with open("smartlogger.txt","a+") as f:
            print(self.logger,file=f)

    def play(self,hei,wid):
        if hei is None or wid is None:
            hei = random.randint(1,10)
            wid = random.randint(1,10)
        if hei*wid < 120:
            board = [[random.randint(0,4) for _ in range(wid)]for __ in range(hei)]
            s = State(board,hei,wid,5)
            self.root = s
        else:
            raise Exception("Size of the board can't exceed 120.")


    def descendants(self,n):
        nc = [False]
        def util(current):
            if time.time() - t > 10:
                nc[0] = True
                return
            current.generateChildren()
            if not current.end:
                counter = 0
                for s in current.childrenStates:
                    if counter > n:
                        break
                    util(s)
                    counter += 1
            else:
                if current.value > self.bestScore:
                    self.bestScore = current.value
                    self.howtowin = current.route
                    self.winner = current
        t = time.time()
        util(self.root)
        if not nc[0]:
            self.logger = f"{self.size};DESC;{n};{self.bestScore};{round(time.time()-t,2)}"
        else:
            self.logger = f"{self.size};DESC;{n};-;-"
        self.log()


    def stepreduction(self, branches,proposed):
        t = time.time()
        q = queue.Queue()
        q.put(self.root)
        cdepth = 0
        values = []
        lower = -1
        nc = False
        while not q.empty():
            if time.time() - t > 10:
                nc = True
                return
            act = q.get()
            if act.depth == cdepth:
                if act.value >= lower:
                    act.generateChildren(proposed)
                    if act.end:
                        if act.value > self.bestScore:
                            self.winner = act
                            self.bestScore = act.value
                            self.howtowin = act.route
                    else:
                        for c in act.childrenStates:
                            q.put(c)
                            values.append(c.value)
            else:
                values.sort()
                cdepth += 1
                if branches < len(values):
                    lower = values[len(values)-branches-1]
                else:
                    lower = values[0]
                if act.value >= lower:
                    act.generateChildren(proposed)
                    if act.end:
                        if act.value > self.bestScore:
                            self.winner = act
                            self.bestScore = act.value
                            self.howtowin = act.route
                    else:
                        for c in act.childrenStates:
                            q.put(c)
                            values.append(c.value)
                else:
                    values = []
        if nc:
            self.logger = f"{self.size};STRED;{branches} {proposed};-;-"
        else:
            self.logger = f"{self.size};STRED;{branches} {proposed};{self.bestScore};{round(time.time() - t, 2)}"
        self.log()

    def randomWalk(self):
        t = time.time()
        current = self.root
        nc = False
        while True:
            if time.time() - t > 10:
                nc = True
                break
            current.generateChildren()
            if current.end:
                break
            z = random.randint(0,len(current.childrenStates)-1)
            current = current.childrenStates[z]
        self.winner = current
        self.bestScore = current.value
        self.howtowin = current.route
        if nc:
            self.logger = f"{self.size};RANDWALK;;-;-"
        else:
            self.logger = f"{self.size};RANDWALK;;{self.bestScore};{round(time.time() - t, 2)}"
        self.log()

    def backtrack(self):
        route = []
        current = self.winner
        while current != self.root:
            route.append(current.board)
            route.append(current.beforeFall)
            current = current.parent
        route.append(self.root.board)
        return route[::-1]

    def solutionGif(self):
        res = self.backtrack()
        board_creator.boardpaint(res)
        gif_creator.do()






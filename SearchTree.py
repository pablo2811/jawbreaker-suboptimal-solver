import queue
import random
import time
import gif_creator
import board_creator
import os

from State import State


class SearchTree:

    def __init__(self, starter=None, object=True, hei=None, wid=None, col=5, maxtime=20):
        if not object:
            self.play(hei, wid)
        else:
            assert starter is not None
            self.root = State(starter, len(starter), len(starter[0]), c=col)
        self.H = self.root.hei
        self.W = self.root.wid
        self.size = self.H * self.W
        self.bestScore = 0
        self.howtowin = []
        self.winner = None
        self.logger = ""
        self.maxtime = maxtime

    def log(self, file):
        os.chdir("logs")
        with open(f"{file}.txt", "a+") as f:
            print(self.logger, file=f)
        os.chdir("..")

    def play(self, hei, wid):
        if hei is None or wid is None:
            hei = random.randint(1, 15)
            wid = random.randint(1, 15)
        if hei * wid < 226:
            board = [[random.randint(0, 4) for _ in range(wid)] for __ in range(hei)]
            s = State(board, hei, wid, 5)
            self.root = s
        else:
            raise Exception("Size of the board can't exceed 225.")

    def descendants(self, n):
        nc = [False]

        def util(current):
            if time.time() - t > self.maxtime:
                nc[0] = True
                return
            current.generateChildren()
            if not current.end:
                counter = 0
                for s in current.childrenStates:
                    if counter >= n:
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
            self.logger = f"{self.size};{n};{self.bestScore};{round(time.time() - t, 2)}"
            self.log(file="desclog")

    def stepreduction(self, branches, predicted_gain=True):
        self.bestScore = 0
        self.howtowin = 0
        self.winner = None
        t = time.time()
        q = queue.Queue()
        q.put(self.root)
        cdepth = 0
        values = []
        lower = -1
        nc = False
        while not q.empty():
            if time.time() - t > self.maxtime:
                nc = True
                break
            act = q.get()
            if act.depth == cdepth:
                if predicted_gain:
                    z = act.value + act.predicted_gain
                else:
                    z = act.value
                if z >= lower:
                    act.generateChildren(branches)
                    if act.end:
                        if act.value > self.bestScore:
                            self.winner = act
                            self.bestScore = act.value
                            self.howtowin = act.route
                    else:
                        for c in act.childrenStates:
                            q.put(c)
                            if predicted_gain:
                                z = c.value + c.predicted_gain
                            else:
                                z = c.value
                            values.append(z)
            else:
                values.sort()
                cdepth += 1
                if branches < len(values):
                    lower = values[-branches]
                else:
                    lower = values[0]
                if predicted_gain:
                    z = act.value + act.predicted_gain
                else:
                    z = act.value
                if z >= lower:
                    act.generateChildren(branches)
                    if act.end:
                        if act.value > self.bestScore:
                            self.winner = act
                            self.bestScore = act.value
                            self.howtowin = act.route
                    else:
                        for c in act.childrenStates:
                            q.put(c)
                            if predicted_gain:
                                z = c.value + c.predicted_gain
                            else:
                                z = c.value
                            values.append(z)
                else:
                    values = []
        if not nc:
            if predicted_gain:
                name = "stredpg"
            else:
                name = "stred"
            self.logger = f"{self.size};{branches};{self.bestScore};{round(time.time() - t, 2)}"
            self.log(file=f"{name}log")

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
            z = random.randint(0, len(current.childrenStates) - 1)
            current = current.childrenStates[z]
        self.winner = current
        self.bestScore = current.value
        self.howtowin = current.route
        if not nc:
            self.logger = f"{self.size};{self.bestScore};{round(time.time() - t, 2)}"
            self.log("randomwalklog")

    def backtrack(self):
        route = []
        current = self.winner
        scores = []
        while current != self.root:
            scores.append(current.value)
            route.append(current.board)
            route.append(current.beforeFall)
            current = current.parent
        route.append(self.root.board)
        return route[::-1],scores[::-1]

    def solutionGif(self, name):
        if self.winner is not None:
            res,scores = self.backtrack()
            board_creator.boardpaint(res,scores)
            gif_creator.do(name)

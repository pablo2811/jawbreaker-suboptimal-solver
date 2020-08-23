import copy


class State:
    def __init__(self, board, h, w, c, parent=None, value=0, route=None,beforefall=None,depth=0):
        if route is None:
            self.route = []
        else:
            self.route = route
        self.board = board
        self.parent = parent
        self.hei = h
        self.wid = w
        self.col = c
        self.end = False
        self.childrenStates = []
        self.value = value
        self.beforeFall = beforefall
        self.depth = depth

    def findChains(self):
        network = dict()
        for i in range(self.hei):
            for j in range(self.wid):
                network[(i, j)] = []
                if self.board[i][j] != -1:
                    checks = [(-1,0),(1,0),(0,-1),(0,1)]
                    for e in checks:
                        if self.hei > i + e[0] >= 0 and 0 <= j + e[1] < self.wid :
                            if self.board[i + e[0]][j + e[1]] == self.board[i][j]:
                                network[(i, j)].append((i + e[0],j + e[1]))

        def util(current):
            fields.append(current)
            visited[current] = 1
            for nei in network[current]:
                if not visited[nei]:
                    util(nei)

        visited = dict()
        for i in range(self.hei):
            for j in range(self.wid):
                visited[(i,j)] = 0
        chains = []
        for i in range(self.hei):
            for j in range(self.wid):
                fields = []
                if not visited[(i,j)]:
                    util((i,j))
                if len(fields) >= 2:
                    chains.append(fields)
        return chains

    def generateChildren(self,n=None):
        c = self.findChains()
        if not c:
            self.end = True
            return
        if n is not None:
            upper = n
        else:
            upper = len(c)
        c = sorted(c,key=len,reverse=True)
        counter  = 0
        for chain in c:
            if counter > upper:
                break
            new_board = copy.deepcopy(self.board)
            for field in chain:
                new_board[field[0]][field[1]] = -1
            beforefall = copy.deepcopy(new_board)
            for z in range(self.wid):
                good = []
                for x in range(self.hei-1,-1,-1):
                    if new_board[x][z] != -1:
                        good.append(new_board[x][z])
                for x in range(self.hei - 1, self.hei-len(good)-1, -1):
                    new_board[x][z] = good[self.hei-1-x]
                for x in range(self.hei-len(good)-1,-1,-1):
                    new_board[x][z] = -1
            val = len(chain)*(len(chain)-1)
            via = copy.deepcopy(self.route)
            via.append(chain[0])
            self.childrenStates.append(State(new_board,self.hei,self.wid,self.col,parent=self,value=val+self.value,route=via,beforefall=beforefall,depth=self.depth+1))
            counter += 1

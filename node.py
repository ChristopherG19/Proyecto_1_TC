from asyncio.windows_events import NULL

class Node():
    def __init__(self, symbol=NULL):
        self.symbol = symbol
        self.pos = '-'

        self.left = NULL
        self.right = NULL
        self.asigned = False
        self.nullable = False
        self.leaf = False

        self.firstpos = []
        self.lastpos = []
        self.followpos = []

    def __repr__(self):

        retString = ""
        if (type(self.left) == Node and type(self.right) == Node):
            retString = str(self.symbol) + ',\t' + str(self.pos) + ',\t' + str(self.nullable) + ',\t' + str(self.firstpos) + ',\t' + str(self.lastpos) + ',\t' + str(self.followpos) + ',\t' + self.left.getSymbol() + ',\t' + self.right.getSymbol()
        else:
            retString = str(self.symbol) + ',\t' + str(self.pos) + ',\t' + str(self.nullable) + ',\t' + str(self.firstpos) + ',\t' + str(self.lastpos) + ',\t' + str(self.followpos) 
        return retString

    def setAsLeaf(self):
        self.leaf = True

    def setAsign(self):
        self.asigned = True

    def setNullable(self):
        self.nullable = True

    def setPos(self, pos):
        self.pos = pos

    def setLeft(self, left):
        self.left = left

    def setRight(self, right):
        self.right = right

    def addFirstPos(self, n):
        self.firstpos.append(n)

    def addLastPos(self, n):
        self.lastpos.append(n)

    def addFollowPos(self, n):
        if (n not in self.followpos):
            self.followpos.append(n)

    def isLeaf(self):
        return self.leaf

    def isAsigned(self):
        return self.asigned

    def isNullable(self):
        return self.nullable

    def getSymbol(self):
        return self.symbol

    def getPos(self):
        return self.pos

    def getLeft(self):
        return self.left

    def getLeftPos(self):
        return self.left.getPos()

    def getRight(self):
        return self.right

    def getRightPos(self):
        return self.right.getPos()
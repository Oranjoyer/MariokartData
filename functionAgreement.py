class Agree:
    def __init__(self,votesNeeded,total):
        self.votesNeeded = votesNeeded
        self.itemTuple = tuple([None for _ in range(total)])
    def addVal(self,val):
        self.itemTuple = (val,) + self.itemTuple[:-1]
        if(self.itemTuple.count(val)>=self.votesNeeded):
            return True, val
        return False, None
    def reset(self):
        self.itemTuple = tuple([None for _ in range(len(self.itemTuple))])
import sys

class Frame:
    def __init__(self, name:str) -> None:
          self.name : str = name
          self.page : int = int(0)
          self.used : bool = False # használt-e, ha True nem szabadíthaó fel, ha False felszabadítható
          self.lock : int = 0

    def store(self, page:int):
        if (page > 99 or page < 1):
            raise AttributeError("page must be in (1, 99) interval") 
        self.page = int(page)
        self.used = True
        self.lock = 3

    def use(self):
        if (self.page != 0):
            self.used = False

    def data(self) -> int:
        return int(self.page)
    
    def is_used(self):
        return self.used
    
    def step(self):
        if(self.lock >= 0):
            self.lock -= 1
        if (self.lock < 0):
            self.use()

class FIFO:
    
    def __init__(self, *args : Frame) -> None:
        self.frames : list = []
        self.idx : int = 0
        for i in args:
            self.frames.append(i)

    def skip(self):
        self.idx += 1
        if (self.idx > len(self.frames) -1):
            self.idx = 0

    def next(self) -> Frame:
        ret = self.frames[self.idx]
        self.idx += 1
        if (self.idx > len(self.frames) -1):
            self.idx = 0
        return ret
    
    def step(self):
        for i in self.frames:
            i.step()

    def size(self) -> int:
        return len(self.frames)

def lookup(page : int, *frames : Frame):
    for i in frames:
        if (i.data() == page):
            return i
    return None

def find_not_used(fifo : FIFO):
    for i in range(fifo.size()-1):
        this : Frame = fifo.next()
        if (not this.is_used()):
            return this
    return None

def main():
    out : str = ""
    moves : int = 0
    A = Frame("A")
    B = Frame("B")
    C = Frame("C")
    store : FIFO = FIFO(A, B, C)
    be = input()
    line = be.split(',')
    for i in line:
        store.step()
        write = False
        i = int(i)
        if (i < 0):
            i = -i
            write = True
        this : Frame = lookup(i, A, B, C)
        if (this != None):
            this.use()
            out += "-"
            continue
        not_used = find_not_used(store)
        if(not_used == None):
            out += "*"
            moves += 1
            continue
        not_used.store(i)
        out += not_used.name
        moves += 1

    ##print(out + '\n' + str(moves), end='')
    sys.stdout.write(out + '\n' + str(moves))

if '__main__' == __name__:
    main()
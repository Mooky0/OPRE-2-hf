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
        self.used = False
        self.lock = 3

    def use(self):
        if (self.page != 0):
            self.used = True

    def data(self) -> int:
        return int(self.page)
    
    def is_used(self):
        return self.used
    
    def step(self):
        if(self.lock > 0):
            self.lock -= 1

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
    
    def pop(self) -> Frame:
        tmp : Frame = self.frames[0]
        self.frames.pop(0)
        return tmp
    
    def push(self, frame : Frame):
        self.frames.append(frame)

    def delete(self, frame : Frame):
        self.frames.remove(frame)

    def step(self):
        for i in self.frames:
            i.step()

    def size(self) -> int:
        return len(self.frames)
    
    def all_used(self) -> bool:
        for i in self.frames:
            if i.lock == 0 and i.used == False:
                return False
        return True    

    def lookup(self, page : int):
        for i in self.frames:
            if (i.data() == page):
                return i
        return None

    def find_not_used(self) -> Frame:
        i = 0
        while(i < len(self.frames)):
            if (self.frames[i].lock > 0):
                i += 1
                continue
            if (self.frames[i].is_used()):
                self.frames[i].used = False
                tmp : Frame = self.frames[i]
                self.frames.remove(self.frames[i])
                self.frames.append(tmp)
            else:
                return self.frames[i]
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
        i = abs(int(i))
        this : Frame = store.lookup(i)
        if (this != None):
            this.use()
            out += "-"
            store.step()
        else:
            not_used = store.find_not_used()
            if(not_used == None):
                out += "*"
                moves += 1
                store.step()
            else:
                store.step()
                not_used.store(i)
                out += not_used.name
                moves += 1

    sys.stdout.write(out + '\n' + str(moves))

if '__main__' == __name__:
    main()
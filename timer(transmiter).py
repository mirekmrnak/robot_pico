from utime import ticks_ms, ticks_diff, ticks_add

class Timer():
    '''
    Třídu zle zavolat v nadřazeném modulu. Zde si funkce tvoří globalní proměnnou, kde si ukládá časy.
    Tzn. pokud je toto počítadlo v cyklu While, nenastaví se pokaždé nové časy --> hodnoty jsou uloženy mimo funkci 
    '''
    def __init__(self, t):
        self.t = t*1000
        self.deadline = 0

    def check(self):
        if ticks_diff(self.deadline, ticks_ms()) > 0:
            return False
            
        else:
            self.deadline = ticks_add(ticks_ms(), int(self.t))
            return True
import LogicGate as lg
import ArithmeticLogicUnit as alu
import numpy as np

def SRLatch(s,r,q):
    return lg.nor(lg.nor(s,q),r)

def DLatch(data,we,qi):
    s = int(data and we)
    r = int(not data and we)
    q = SRLatch(s,r,qi)
    return q

def DFF(data,qi,clock=1):
    we = clock # in the real world, this should be "we = (not clock) and clock"
    return DLatch(data,we,qi)

class Bit:
    def __init__(self,q=0):
        self.out = q
    
    def next(self,inputs,load,clock=1):
        data = lg.mux(self.out,inputs,load)
        self.out = DFF(data,self.out,clock)
        return self.out

class Register:
    def __init__(self):
        self.register = [""]*16
        for i in range(16):
            self.register[i] = Bit()
    
    def next(self, inputs, load, clock=1):
        data = lg.mux16bit([b.out for b in self.register],inputs,load)
        for i,d in enumerate(data):
            self.register[i].next(d,load)
        return [b.out for b in self.register]
    
    def __str__(self):
        return str([b.out for b in self.register])

class RAMn:
    def __init__(self,n):
        self.memory = [""]*n
        for i in range(n):
            self.memory[i] = Register()
        self.out = [0]*16
    
    def next(self, inputs, address, load, clock=1):
        reg = self.memory[int("".join(map(str,address)), base=2)]
        self.out = reg.next(inputs,load,clock)
        return self.out

    def __str__(self):
        s = ""
        for reg in self.memory:
            s += str(reg)+"\n"
        return s

# simplified RAM
class RAM:
    def __init__(self,n):
        self.memory = np.zeros([n,16])
        self.out = [0]*16
    
    def next(self,inputs,address,load,clock=1):
        reg = self.memory[int("".join(map(str,address)), base=2)]
        data = lg.mux16bit(reg,inputs,load)
        if clock:
            self.memory[int("".join(map(str,address)), base=2)] = data
        self.out = list(reg.astype(int))
        return self.out
    
    def load(self,address):
        return self.next([0]*16,address,load=0)
    
    def write(self,inputs,address):
        return self.next(inputs,address,load=1)
    
    def __str__(self):
        return str(self.memory)

class PC:
    def __init__(self):
        self.reg = [0]*16
    
    def next(self,inputs,inc,res,load,clock=1):
        if res and clock:
            self.reg = [0]*16
        elif load and clock:
            self.reg = inputs
        elif inc and clock:
            self.reg = alu.inc16bit(self.reg)
        else:
            self.reg = self.reg
        
        return self.reg
    
    def __str__(self):
        return str(self.reg)
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

class Register_:
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

class RAM8:
    def __init__(self,n=8):
        self.memory = [""]*n
        for i in range(n):
            self.memory[i] = Register_()
        self.out = [0]*16
    
    def next(self, inputs, address, load, clock=1):
        loads = lg.dmux8way(load,address)
        for l,reg in zip(loads,self.memory):
            reg.next(inputs,l,clock)
        self.out = lg.mux8way16bit(self.memory[0],self.memory[1],self.memory[2],self.memory[3],
                                self.memory[4],self.memory[5],self.memory[6],self.memory[7],address)
        self.out = [b.out for b in self.out.register]
        return self.out

    def __str__(self):
        s = ""
        for reg in self.memory:
            s += str(reg)+"\n"
        return s

class RAM64:
    def __init__(self,n=8):
        self.memory = [""]*n
        for i in range(n):
            self.memory[i] = RAM8()
        self.out = [0]*16
    
    def next(self, inputs, address, load, clock=1):
        # len(address) = 6
        loads = lg.dmux8way(load,address[:3])
        for l,ram8 in zip(loads,self.memory):
            ram8.next(inputs,address[3:],l,clock)
        self.out = lg.mux8way16bit(self.memory[0],self.memory[1],self.memory[2],self.memory[3],
                                self.memory[4],self.memory[5],self.memory[6],self.memory[7],address[:3]).memory
        self.out = lg.mux8way16bit(self.out[0],self.out[1],self.out[2],self.out[3],
                                self.out[4],self.out[5],self.out[6],self.out[7],address[3:])
        self.out = [b.out for b in self.out.register]
        return self.out

    def __str__(self):
        s = ""
        for ram in self.memory:
            s += str(ram)
        return s

# simplified implementation Version

class Register:
    def __init__(self):
        self.register = np.zeros([16])
        self.out = list(self.register.astype(int))
    
    def next(self, inputs, load, clock=1):
        data = lg.mux16bit(self.register,inputs,load)
        for i,d in enumerate(data):
            self.register[i] = d
        self.out = list(self.register.astype(int))
        return self.out
    
    def __str__(self):
        return str(self.register)

    def num(self):
        return int("".join(map(str, self.register.astype(int))),base=2)

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
    
    def num(self):
        return int("".join(list(map(str, self.reg))),base=2)

import numpy as np
import LogicGate as lg
import ArithmeticLogicUnit as alu
import SequentialCircuit as sc
import CPU as cpu

class Computer:
    def __init__(self):
        self.cpu = cpu.CPU()
        self.memory = sc.RAM(24576)
        self.rom = sc.RAM(16384*2)
        self.address = [0]*15
        self.pc = [0]*15

    def loadProgram(self,code):
        for i,c in enumerate(code):
            for j,b in enumerate(c):
                self.rom.memory[i,j] = b
    
    def start(self):
        inst = self.rom.load(self.pc)
        print(inst)
        inM = self.memory.load(self.address)
        print(inM)
        outM, writeM, self.address, self.pc = self.cpu.excute(inst=inst,inM=inM,reset=0,clock=1)
        print(type(self.pc))
        print(type(self.address))
        if writeM:
            self.memory.write(outM,self.address)
    
    def __str__(self):
        s = ""
        s += "CPU:\n"+str(self.cpu)
        s += "Memory:\n"+str(self.memory)
        s += "ROM:\n"+str(self.rom)

if __name__ == "__main__":
    computer = Computer()
    code = [[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
            [1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,0,0,0,1,1,0,0,0,0,1,0,0,0]]
    computer.loadProgram(code)
    print(computer.rom)
    for i in range(10):
        computer.start()
        print(computer.memory.memory[:32])
    
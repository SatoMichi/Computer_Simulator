import LogicGate as lg
import ArithmeticLogicUnit as alu
import SequentialCircuit as sc

class CPU:
    def __init__(self):
        self.regA = sc.Register()
        self.regD = sc.Register()
        self.pc = sc.PC()
        self.alu = alu.ALU16bit
        self.aluout = [0]*16

    def excute(self,inst,inM,reset,clock=1):
        writeM = int(inst[0] and inst[-4])
        loadD = int(inst[0] and inst[-5])
        #print("loadD: ",loadD)
        loadA = int(not inst[0] or inst[-6])
        #print("loadA: ",loadA)
        
        #print(self.aluout)
        regAin = lg.mux16bit(inst,self.aluout,inst[0])
        regAout = self.regA.out
        self.regA.next(regAin,loadA,clock)
        
        address = regAout[1:]

        
        self.regD.next(self.aluout,loadD,clock)
        regDout = self.regD.out
        

        aluInput2 = lg.mux16bit(regAout,inM,inst[3])
        print("inD: ",int("".join(map(str,regDout)),base=2))
        print("inA/M: ",int("".join(map(str,aluInput2)),base=2))
        
        self.aluout, zr, ng = self.alu(regDout,aluInput2,inst[4:10])
        outM = self.aluout

        self.regD.next(self.aluout,loadD,clock)
        regDout = self.regD.out
        

        jlt = int(inst[-3] and ng)
        jeq = int(inst[-2] and zr)
        zeroOrneg = int(zr or ng)
        jgt = int(inst[-1] and not zeroOrneg)
        jle = int(jlt or jeq)
        jumpA = int(jgt or jle)
        loadPC = int(inst[0] and jumpA)
        #print("loadPC: ",loadPC)
     
        pc = self.pc.next(regAout,True,reset,loadPC,clock)[1:]

        return outM, writeM, address, pc

    def __str__(self):
            s = ""
            s += "Register A: "+str(self.regA.num())+"\n"
            s += "Register D: "+str(self.regD.num())+"\n"
            s += "Register PC: "+str(self.pc.num())+"\n"
            return s


if __name__ == "__main__":
    cpu = CPU()

    code1= [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
            [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
            [1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], 
            [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], 
            [1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], 
            [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], 
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], 
            [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1]]

    code2 = [[0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1],
             [1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
             [1,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0],
             [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
             [1,1,1,0,0,0,1,1,0,0,0,0,1,0,0,0]]
    
    outM = [0]*16
    writeM = 0
    address = [0]*15
    pc = [0]*15
    memory = [[0]*16]*32

    for inst in code1:
        print(inst)
        #print("address: ",int("".join(map(str,address)),base=2))
        inM = memory[int("".join(map(str,address)),base=2)]   
        #print("inM: "+str(int("".join(map(str,inM)),base=2)))
        outM, writeM, address, pc = cpu.excute(inst,inM,0)
        if writeM:
            memory[int("".join(map(str,address)),base=2)] = outM
        print("outM: "+str(int("".join(map(str,outM)),base=2)))
        print("writeM: ",writeM)
        print("address: "+str(int("".join(map(str,address)),base=2)))
        print("pc: "+str(int("".join(map(str,pc)),base=2)))
        print(cpu)
        for i,m in enumerate(memory):
            print(i," : ",int("".join(map(str,m)),base=2))


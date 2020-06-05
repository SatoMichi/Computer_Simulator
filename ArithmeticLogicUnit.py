import numpy as np
import LogicGate as lg

def halfAdder(a,b):
    carry = int(a and b)
    result = lg.xor(a,b)
    return result,carry

def fullAdder(a,b,c):
    s1,c1 = halfAdder(a,b)
    result,c2 = halfAdder(s1,c)
    carry = int(c1 or c2)
    return result,carry

def adder16bit(input1,input2):
    input1.reverse()
    input2.reverse()
    result = []
    carry = 0
    for a,b in zip(input1,input2):
        s,c = fullAdder(a,b,carry)
        result.append(s)
        carry = c
    result.reverse()
    return result

def inc16bit(a):
    return adder16bit(a,[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1])

def ALU16bit(a,b,cont):
    # cont = [zx,nx,zy,ny,f,no]
    if cont[0]:
        a = [0]*16
    if cont[1]:
        a = lg.not16bit(a)
    if cont[2]:
        b = [0]*16
    if cont[3]:
        b = lg.not16bit(b)
    if cont[4]:
        out = adder16bit(a,b)
    else:
        out = lg.and16bit(a,b)
    if cont[5]:
        out = lg.not16bit(out)
    zr = 1 if out == [0]*16 else 0
    ng = 1 if out[0] == 1 else 0

    return out, zr, ng

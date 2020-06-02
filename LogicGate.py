import numpy as np
# AND OR NOT is basic gates therefore not implemented
# if _ then _ else _ is also assumed to be implemented as basic gate (mux gate can be interpleted as if_then_else_ gate)

# Basic gate
def nand(a,b):
	return int(not (a and b))

def xor(a,b):
	return int(((not a) and b) or (a and (not b)))

# mux, dmux
def mux(a,b,sel):
	return a if sel == 0 else b

def dmux(a,sel):
	out = np.zeros([2])
	out[sel] = a
	return out

# multi bit basic gates
def not16bit(inputs):
	return [int(not a) for a in inputs]

def and16bit(inputs1, inputs2):
	return [a and b for a,b in zip(inputs1, inputs2)]

def or16bit(inputs1, inputs2):
	return [a or b for a,b in zip(inputs1,inputs2)]

def nand16bit(inputs1, inputs2):
	return [nand(a,b) for a,b in zip(inputs1,inputs2)]

def xor16bit(inputs1, inputs2):
	return [xor(a,b) for a,b in zip(inputs1,inputs2)]

# multi bit mux
def mux16bit(inputs1, inputs2, sel):
	return inputs1 if sel == 0 else inputs2

# multi input basic gates
def and8way(inputs):
	return int(all(inputs))

def or8way(inputs):
	return int(any(inputs))

# multi input mux
def mux4way16bit(inputs1, inputs2, inputs3, inputs4, sels):
	if sels == [0,0]:
		return inputs1
	elif sels == [0,1]:
		return inputs2
	elif sels == [1,0]:
		return inputs3
	else:
		return inputs4

def mux8way16bit(inputs1, inputs2, inputs3, inputs4, inputs5, inputs6, inputs7, inputs8, sels):
	if sels == [0,0,0]:
		return inputs1
	elif sels == [0,0,1]:
		return inputs2
	elif sels == [0,1,0]:
		return inputs3
	elif sels == [0,1,1]:
		return inputs4
	elif sels == [1,0,0]:
		return inputs5
	elif sels == [1,0,1]:
		return inputs6
	elif sels == [1,1,0]:
		return inputs7
	else:
		return inputs8

# multi output dmux
def dmux4way(a,sels):
	out = np.zeros([4])
	idx = int("".join(map(str,sels)), base=2)
	out[idx] = a
	return out

def dmux8way(a,sels):
	out = np.zeros([8])
	idx = int("".join(map(str,sels)), base=2)
	out[idx] = a
	return out

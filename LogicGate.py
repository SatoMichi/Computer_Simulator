# AND OR NOT is not be implemented

def nor(a,b):
	return not(a or b)

def MUX8(a,b,c,d,e,f,g,h, cont):
	if cont == 0:
		return a
	elif cont == 1:
		return b
	elif cont == 2:
		return c
	elif cont == 3:
		return d
	elif cont == 4:
		return e
	elif cont == 5:
		return f
	elif cont == 6:
		return g
	elif cont == 7:
		return h

from LogicGate import nor

class SRLatch:
	def __init__(self):
		self.s = 0
		self.r = 0
		self.out = 0
		self.nout = 1
	def set(self):
		self.s = 1
		self.nout = nor(self.s,self.out)
		self.out = nor(self.r, self.nout)
		self.s  = 0
	def reset(self):
		self.r = 1
		self.out = nor(self.r, self.nout)
		self.nout = nor(self.s,self.out)
		self.r = 0

class DFlipFlop:
	def __init__(self):
		self.sr = SRLatch()
		self.clock = False
	def clock(self):
		nclock = not self.clock
		self.clock = nclock
	def write(self,d):
		if d and self.clock:
			self.sr.set()
		elif not d and self.clock:
			self.sr.reset()

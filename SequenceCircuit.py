import LogicGate as lg
import numpy as np

def SRLatch(s,r,q):
    return lg.nor(lg.nor(s,q),r)

def DLatch(data,we,qi):
    s = int(data and we)
    r = int(not data and we)
    q = SRLatch(s,r,qi)
    return q
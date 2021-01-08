import numpy as np
def nextpow2(n):
    return np.ceil(np.log2(np.abs(n))).astype('long')

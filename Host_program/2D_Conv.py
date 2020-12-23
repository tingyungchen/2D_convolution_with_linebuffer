
# coding: utf-8

# In[3]:


from __future__ import print_function

import sys
import numpy as np
from time import time
import matplotlib.pyplot as plt 

sys.path.append('/home/xilinx')
from pynq import Overlay
from pynq import allocate

if __name__ == "__main__":
    print("Entry:", sys.argv[0])
    print("System argument(s):", len(sys.argv))

    print("Start of \"" + sys.argv[0] + "\"")

    ol = Overlay("/home/xilinx/IPBitFile/yclin/conv_desing.bit")
    ipConv = ol.filter11x11_strm_0
    ipDMAin = ol.axi_dma_0
    ipDMAout = ol.axi_dma_1

    TEST_IMG_ROWS = 135
    TEST_IMG_COLS = 240


    numSamples = TEST_IMG_ROWS * TEST_IMG_COLS
    src = allocate(shape=(numSamples,), dtype=np.uint32)
    
    chkr_size = 5
    max_pix_val = 255
    min_pix_val = 0
    for i in range(TEST_IMG_ROWS):
        chkr_pair_val = [0, 0]
        if (int((int(i) / int(chkr_size))) % 2 == 0):
            chkr_pair_val[0] = max_pix_val
            chkr_pair_val[1] = min_pix_val
        else:
            chkr_pair_val[0] = min_pix_val
            chkr_pair_val[1] = max_pix_val
        for j in range(TEST_IMG_COLS):
            idx = int((int(j) / int(chkr_size))) % 2
            pix_val = chkr_pair_val[idx]
            src[i*TEST_IMG_COLS + j] = pix_val

    inBuffer0 = allocate(shape=(numSamples,), dtype=np.uint32)
    outBuffer0 = allocate(shape=(numSamples,), dtype=np.uint32)
    for i in range(numSamples):
        inBuffer0[i] = src[i]

    ipConv.write(0x10, int(TEST_IMG_COLS))
    ipConv.write(0x18, int(TEST_IMG_ROWS))
    ipConv.write(0x00, 0x01)
    ipDMAin.sendchannel.transfer(inBuffer0)
    ipDMAout.recvchannel.transfer(outBuffer0)
    ipDMAin.sendchannel.wait()
    ipDMAout.recvchannel.wait()

    for idx in range(10):
        print("Index {0}: {1}".format(idx, outBuffer0[idx]))


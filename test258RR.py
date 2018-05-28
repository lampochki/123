import numpy as np
import numpy.fft as fft
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import struct
import os
import fnmatch


matches=[]
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith('.npy'):
            print file
            matches.append(file)
print matches
to=len(matches)
for i in range(to):
	fn=str(matches[i])
	corr=np.load(fn)
	aver=34
	#print np.shape
	spec_chan=corr.shape[1]
	periods=corr.shape[0]
	aver_data=np.zeros((aver-1,spec_chan),dtype=np.complex)
	for k in range(periods/aver):
		aver_data[0:33]+=corr[k*aver:(k+1)*aver-1]
	np.save('aver'+str(fn),aver_data)
	print 'done'
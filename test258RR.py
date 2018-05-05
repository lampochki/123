import struct
import os
import numpy as np
import numpy.fft as fft
import fnmatch

np.set_printoptions(threshold=5)



pp='RR'
bn=258
matches=[]
for path, dirs, files in os.walk(os.getcwd()):
        for result in [os.path.abspath(os.path.join(path, filename)) for
                filename in files if fnmatch.fnmatch(filename,'*.b0000')]:
            matches.append(result)
print matches
to=len(matches)
print to
for fi in range(8):
	for i in range (to-1,-1,-1):
		print i
		fn=str(matches[i])
		#fn=str('/home/difx/06/RUP009_20130218_18_CRAB/sched-key4_test/s000'+f+str(i))
		size=os.path.getsize(fn)
		current_head=0
		head_count=0
		accum_periods=0
		x=0
		all_periods=0
		with open(fn, 'rb') as sw:
			sync=int(struct.unpack('i', sw.read(4))[0])
			sync_search=0 
			sync_distance=0
			while sync_search!=sync:
				sync_distance+=1
				sw.seek(sync_distance)
				sync_search=int(struct.unpack('i', sw.read(4))[0])
			print 'distance between syncwords', sync_distance
			spec_chan=(sync_distance-74)/8
			while head_count<size/sync_distance:
				sw.seek(sync_distance*current_head)
				sync=str(sw.read(4))
				head_version,=struct.unpack('i', sw.read(4))
				baseline_number,=struct.unpack('i', sw.read(4))
				MJD,=struct.unpack('i', sw.read(4))
				seconds,=struct.unpack('d', sw.read(8))
				config_index,=struct.unpack('i', sw.read(4))
				source_index,=struct.unpack('i', sw.read(4))
				freq_index,=struct.unpack('i', sw.read(4))
				polarisation_pair=str(sw.read(2))
				pulsar_bin,=struct.unpack('i', sw.read(4))
				data_weight,=struct.unpack('d', sw.read(8))
				U,=struct.unpack('d', sw.read(8))
				V,=struct.unpack('d', sw.read(8))
				W,=struct.unpack('d', sw.read(8))
				if baseline_number==bn and polarisation_pair==pp and freq_index==fi:
					accum_periods+=1
				current_head+=1
				head_count+=1
			head_count=0
			current_head=0
			data=np.zeros((accum_periods,spec_chan), dtype=np.complex)
			while head_count<size/sync_distance:
				sw.seek(sync_distance*current_head)
				sync=str(sw.read(4))
				head_version,=struct.unpack('i', sw.read(4))
				baseline_number,=struct.unpack('i', sw.read(4))
				MJD,=struct.unpack('i', sw.read(4))
				seconds,=struct.unpack('d', sw.read(8))
				config_index,=struct.unpack('i', sw.read(4))
				source_index,=struct.unpack('i', sw.read(4))
				freq_index,=struct.unpack('i', sw.read(4))
				polarisation_pair=str(sw.read(2))
				pulsar_bin,=struct.unpack('i', sw.read(4))
				data_weight,=struct.unpack('d', sw.read(8))
				U,=struct.unpack('d', sw.read(8))
				V,=struct.unpack('d', sw.read(8))
				W,=struct.unpack('d', sw.read(8))
				if baseline_number==bn and polarisation_pair==pp and freq_index==fi:
					for y in range (spec_chan):
						data[x,y]= complex(struct.unpack('f', sw.read(4))[0], 
							struct.unpack('f', sw.read(4))[0])
					x+=1
				head_count+=1
				current_head+=1
			all_periods+=accum_periods
		#np.save(str(i)+'bn'+str(bn)+'fq'+str(fi),data)
		print data

		aver=33
 		periods=np.shape(data)[0]
 		data_aver=np.zeros((aver,spec_chan), dtype=np.complex)
 		for a in range(periods/aver):
			data_aver[0:aver]+=data[a*aver:(a+1)*aver]
 		ifft_data=abs(fft.ifft(data_aver,axis=-2))
 		np.save('aver'+str(i)+'bn'+str(bn)+'fq'+str(fi),ifft_data)
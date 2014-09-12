import os
import struct
import wave
from equaliser import *
import sys

def play_file(name_of_file,flag):
	params = []
	l=wave_file(name_of_file)
	fmt,integer_data = l.pcm_channels()
	p = l.wf.getparams()
	if flag == 1:
		player = os.fork()
		if player == 0:
			l.play()
			sys.exit(1)
		else:
			'''
			print "enter stop to stop"
			ch = raw_input()
			if ch == 'stop':
				os.kill(player,9)
				ch=raw_input()
				if ch=='end':
					sys.exit()
			'''
	else:
		return integer_data,fmt,p

def amp_scaling(factor,data1,fmt1,params1):
	temp = []
	for i in data1:
		if factor*i > 32767:
			temp.append(32767)
		elif factor*i < -32767:
			temp.append(-32767)
		else:
			temp.append(factor*i)
	return temp,fmt1,params1

def time_scaling(time,data1,fmt1,params1):
	temp = []
	new_params = []
	if time == 1:
		return data1,fmt1,params1
	elif time < 1:
		time = int((1/time))
		for i in data1[::time]:
			temp.append(i)
		newfmt = str(len(temp)) + fmt1[-1]
	else:
		for i in data1:
			temp.append(i)
			for j in xrange(time):
				temp.append(0)
		newfmt = str(len(temp)) + fmt1[-1]
	for i in params1:
		new_params.append(i)

	new_params[3] = len(temp) / params1[0]

	return temp,newfmt,tuple(new_params)

def time_shift(time,data1,fmt1,params1):
	temp = []	
	if time >= 0:
		num_zeroes=time*params1[2]*params1[0]
		for i in xrange(num_zeroes):
			temp.append(0)
		for i in data1:
			temp.append(i)
		newfmt=str(len(temp))+fmt1[-1]
		return temp,newfmt,params1
	else :
		new_params = []
		for i in xrange(-1*time*params1[2]*params1[0],len(data1)):
			val=data1[i]
			temp.append(val)
		for i in params1:
			new_params.append(i)
    		new_params[3]+=params1[2]*time
		newfmt=str(len(temp))+fmt1[-1]
		return temp,newfmt,tuple(new_params)

def time_reversal(data1,fmt1,params1):
	temp = []
	for i in data1[::-1]:
		temp.append(i)
	return temp,fmt1,params1

def mixing(data1,fmt1,params1,data2,fmt2,params2):
	temp = []
	i=0
	j=0
	len1 = len(data1)
	len2 = len(data2)
	while i<len1 and j<len2:
		if data1[i]+data2[j] >32767:
			temp.append(32767)
		elif data1[i]+data2[j] < -32767:
			temp.append(-32767)
		else:
			temp.append(data1[i]+data2[j])
		i+=1
		j+=1
	while i<len1:
		temp.append(data1[i])
		i+=1
	while j<len2:
		temp.append(data2[j])
		j+=1
	newfmt = str(len(temp))+fmt1[-1]
	p=((params1[0]+params2[0])/2,(params1[1]+params2[1])/2,(params1[2]+params2[2])/2,(params1[3]+params2[3])/2,params1[4],params1[5])
	return temp,newfmt,p

def modulation(data1,fmt1,params1,data2,fmt2,params2):
	temp = []
	i=0
	j=0
	len1 = len(data1)
	len2 = len(data2)
	while i<len1 and j<len2:
		if data1[i]*data2[j] >32767:
			temp.append(32767)
		elif data1[i]*data2[j] < -32767:
			temp.append(-32767)
		else:
			temp.append(data1[i]*data2[j])
		i+=1
		j+=1
	while i<len1:
		temp.append(data1[i])
		i+=1
	while j<len2:
		temp.append(data2[j])
		j+=1
	newfmt = str(len(temp))+fmt1[-1]
	p=((params1[0]+params2[0])/2,(params1[1]+params2[1])/2,(params1[2]+params2[2])/2,(params1[3]+params2[3])/2,params1[4],params1[5])
	return temp,newfmt,p

def pack(data1,fmt1,params1):
	out = struct.pack(fmt1,*data1)
	w = wave.open("output.wav","wb")
	w.setparams(params1)
	w.writeframes(out)
	w.close()


'''
data1,fmt1,params1 = play_file(sys.argv[1],0)
data1,fmt1,params1 = time_scaling(2,data1,fmt1,params1)
pack(data1,fmt1,params1)
play_file('output.wav',1)

def main():
	data1,fmt1,params1 = play_file(sys.argv[1],0)
	data2,fmt2,params2 = play_file(sys.argv[2],0)
	data3,fmt3,params3 = play_file(sys.argv[3],0)
	data1,fmt1,params1 = mixing(data1,fmt1,params1,data2,fmt2,params2)
	data1,fmt1,params1 = mixing(data1,fmt1,params1,data3,fmt3,params3)
	data1,fmt1,params1 = time_reversal(data1,fmt1,params1)
	data1,fmt1,params1 = time_shift(3,data1,fmt1,params1)
	data1,fmt1,params1 = amp_scaling(1,data1,fmt1,params1)
	pack(data1,fmt1,params1)
	play_file('output.wav',1)

if __name__ == '__main__':
	main()
'''

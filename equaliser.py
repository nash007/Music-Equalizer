import wave
import pyaudio
import sys
import struct
import os

chunk = 1024

class wave_file(object):
	def __init__(self,name):
		self.name = name
		self.wf = wave.open(name, 'rb')

	def pcm_channels(self):
		"""
		Given a file-like object or file path representing a wave file,
		decompose it into its constituent PCM data streams.
		Input: A file like object or file path
		Output: A list of lists of integers representing the PCM coded data stream channels
		and the sample rate of the channels (mixed rate channels not supported)
		"""
		self.num_channels = self.wf.getnchannels()
		self.sample_rate = self.wf.getframerate()
		self.sample_width = self.wf.getsampwidth()
		self.num_frames = self.wf.getnframes()

		self.raw_data = self.wf.readframes( self.num_frames ) # Returns byte data

		self.total_samples = self.num_frames * self.num_channels

		if self.sample_width == 1: 
			self.fmt = "%iB" % self.total_samples # read unsigned chars
		elif self.sample_width == 2:
			self.fmt = "%ih" % self.total_samples # read signed 2 byte shorts
		else:
		   raise ValueError("Only supports 8 and 16 bit audio formats.")

		self.integer_data = struct.unpack(self.fmt, self.raw_data)

		self.channels = [ [] for time in range(self.num_channels) ]

		for index, value in enumerate(self.integer_data):
			bucket = index % self.num_channels
			self.channels[bucket].append(value)

		return self.fmt,self.integer_data

	def play(self):
		p = pyaudio.PyAudio()
		self.stream = p.open(format = p.get_format_from_width(self.wf.getsampwidth()),
							channels = self.wf.getnchannels(),
							rate = self.wf.getframerate(),
							output = True)
		self.stream.write(self.raw_data)
		self.stream.close()
		p.terminate()

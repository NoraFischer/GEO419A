import zipfile
import os

def unpack(path, filename):
	''' Unpack a zip file.

	:param path: String, Path of the folder where the file is located.
	:param filename: String, Name of the zip file.
	'''
	# set working directory
	os.chdir(path)
	# unzip file
	with zipfile.ZipFile(filename) as zf:
		zf.extractall()

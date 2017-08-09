import numpy as np
import matplotlib.pyplot as plt
import os.path
import json
import scipy
import argparse
import math
import pylab
from sklearn.preprocessing import normalize
caffe_root = '/SegNet/caffe-segnet/' 			# Change this to the absolute directoy to SegNet Caffe
import sys
sys.path.insert(0, caffe_root + 'python')
import matplotlib.cm as cm

colors = cm.nipy_spectral(np.linspace(0, 1, 12))
# print colors[0][:3]
# quit()

import caffe

# Import arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--weights', type=str, required=True)
parser.add_argument('--iter', type=int, required=True)
args = parser.parse_args()

caffe.set_mode_gpu()

net = caffe.Net(args.model,
                args.weights,
                caffe.TEST)


for i in range(0, args.iter):

	net.forward()

	image = net.blobs['data'].data
	label = net.blobs['label'].data
	predicted = net.blobs['prob'].data
	image = np.squeeze(image[0,:,:,:])
	output = np.squeeze(predicted[0,:,:,:])
	ind = np.argmax(output, axis=0)

	r = ind.copy()
	g = ind.copy()
	b = ind.copy()
	r_gt = label.copy()
	g_gt = label.copy()
	b_gt = label.copy()

	Unlabelled = [255,255,255]			# 0
	OilBottle = colors[1][:3]*255		# 1
	Phone = colors[2][:3]*255			# 2
	Robot = colors[3][:3]*255			# 3
	Toothpaste = [60,40,222]			# 4
	TissueBox = colors[5][:3]*255		# 5
	BlueFunnel = [192,128,128]			# 6
	Drill = [64,64,128]					# 7
	Car = [64,0,128]					# 8
	Pedestrian = [64,64,0]				# 9
	Bicyclist = [0,128,192]				# 10
	Somethingelse = [10,0,10]			# 11

	# Unlabelled = [255,255,255]			# 0
	# OilBottle = [128,0,0]				# 1
	# Phone = [255,0,0]					# 2
	# Robot = [0,0,128]					# 3
	# Toothpaste = [60,40,222]			# 4
	# TissueBox = [128,128,0]				# 5
	# BlueFunnel = [192,128,128]			# 6
	# Drill = [64,64,128]					# 7
	# Car = [64,0,128]					# 8
	# Pedestrian = [64,64,0]				# 9
	# Bicyclist = [0,128,192]				# 10
	# Somethingelse = [10,0,10]			# 11

	label_colours = np.array([Unlabelled, OilBottle, Phone, Robot, Toothpaste, TissueBox, BlueFunnel, Drill, Car, Pedestrian, Bicyclist, Somethingelse])
	for l in range(0,11):
		r[ind==l] = label_colours[l,0]
		g[ind==l] = label_colours[l,1]
		b[ind==l] = label_colours[l,2]
		r_gt[label==l] = label_colours[l,0]
		g_gt[label==l] = label_colours[l,1]
		b_gt[label==l] = label_colours[l,2]

	rgb = np.zeros((ind.shape[0], ind.shape[1], 3))
	rgb[:,:,0] = r/255.0
	rgb[:,:,1] = g/255.0
	rgb[:,:,2] = b/255.0
	rgb_gt = np.zeros((ind.shape[0], ind.shape[1], 3))
	rgb_gt[:,:,0] = r_gt/255.0
	rgb_gt[:,:,1] = g_gt/255.0
	rgb_gt[:,:,2] = b_gt/255.0

	image = image/255.0

	image = np.transpose(image, (1,2,0))
	output = np.transpose(output, (1,2,0))
	image = image[:,:,(2,1,0)]


	#scipy.misc.toimage(rgb, cmin=0.0, cmax=255).save(IMAGE_FILE+'_segnet.png')

	formatted_i = "%05d" % i

	print "processing ", formatted_i

	plt.figure()
	plt.imshow(image,vmin=0, vmax=1)
	plt.savefig("/home/peteflo/spartan/src/CorlDev/data/segnet_examples/mixed-5-scenes/" + formatted_i + "_01.png")
	plt.close()

	plt.figure()
	plt.imshow(rgb_gt,vmin=0, vmax=1)
	plt.savefig("/home/peteflo/spartan/src/CorlDev/data/segnet_examples/mixed-5-scenes/" + formatted_i + "_02.png")
	plt.close()
	
	plt.figure()
	plt.imshow(rgb,vmin=0, vmax=1)
	plt.savefig("/home/peteflo/spartan/src/CorlDev/data/segnet_examples/mixed-5-scenes/" + formatted_i + "_03.png")
	plt.close()

print 'Success!'


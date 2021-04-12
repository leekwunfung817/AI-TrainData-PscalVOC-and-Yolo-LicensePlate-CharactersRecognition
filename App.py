# cd /Users/leekwunfung/Documents/GitHub/TrainingDataSynthesis-ImageAddNoise
# python3 App.py
import AddNoise
import cv2

from shutil import copyfile
import random
import os

fDir = './data/'
tDir = './dataWithNoise/'

def duplicate(fn,func,img):
	# hash_ = random.getrandbits(128)
	# ffn = str(hash_)+'_'+func
	ffn = fn+'_'+func
	cv2.imwrite(tDir+ffn+'.jpg',img)

	ffp = fDir+fn+'.txt'
	tfp = tDir+ffn+'.txt'
	if os.path.exists(ffp):
		copyfile(ffp, tfp)

	ffp = fDir+fn+'.xml'
	tfp = tDir+ffn+'.xml'
	if os.path.exists(ffp):
		copyfile(ffp, tfp)

def pro(fn):
	print(fn)
	img = cv2.imread(fDir+fn+'.jpg')
	if img is None:
		return
	duplicate(fn,'rain',AddNoise.add_rain(img))
	duplicate(fn,'snowNrain',AddNoise.add_snow( AddNoise.add_rain(img) ) )
	duplicate(fn,'rectangleNrain',AddNoise.rectangle( AddNoise.add_rain(img) ))
	duplicate(fn,'speckleNshadow',AddNoise.speckle( AddNoise.add_shadow(img) ) )
	duplicate(fn,'shadowNrain',AddNoise.add_shadow( AddNoise.add_rain(img) ) )
	duplicate(fn,'speckleNrain',AddNoise.add_rain( AddNoise.speckle(img) ) )
	duplicate(fn,'allNoise',AddNoise.allNoise(img))

import os
for file in os.listdir(fDir):
	if '.jpg' in file:
		pro(file.replace('.jpg',''))
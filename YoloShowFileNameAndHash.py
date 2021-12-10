import os
import cv2

import hashlib

# txtPath='data.unrecognized.20211207.cut/'
txtPath='data/'
targetFullPath=txtPath.replace('/','.cut/')
if not os.path.exists(targetFullPath):
	os.makedirs(targetFullPath)

	
files = os.listdir(txtPath)
if txtPath=='.':
	txtPath=''
xmlPath=txtPath
picPath=txtPath

hsh = cv2.img_hash.BlockMeanHash_create()


def predefined_classes():
	i = 0
	count = 0
	arr={}
	for line in open(txtPath+'predefined_classes.txt','r').readlines():
		arr[str(i)]=line.strip()
		i+=1
	return arr
image_counter=0
dict_=predefined_classes()
print('dict_:',dict_)
for ii, name in enumerate(files):
	image_counter+=1
	if not '.txt' in name:
		continue
	fullPath = txtPath+name
	image_path_name=name[0:-4]
	fullPathImg = picPath+image_path_name+".jpg"
	txtFile=open(fullPath,"r")
	txtList = txtFile.readlines()
	img = cv2.imread(fullPathImg)
	if img is None:
		continue
	# print('fullPath:',fullPath)
	# print('fullPathImg:',fullPathImg)

	Pheight,Pwidth,Pdepth=img.shape
	box_row=''
	# print(' ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ')

	# print('Pheight Pwidth')
	# print(txtPath,name,Pheight,Pwidth)
	line_counter=0
	for i in txtList:
		line_counter+=1
		# print(' ===== ===== ===== ===== =====')
		oneline = i.strip().split(" ")

		c_num=oneline[0]

		c_x=float(oneline[1])
		c_y=float(oneline[2])
		o_w=float(oneline[3])
		o_h=float(oneline[4])

		# print('c_x c_y o_w o_h:',(c_x,c_y,o_w,o_h))

		x_min=c_x-(o_w/2)
		y_min=c_y-(o_h/2)
		x_max=c_x+(o_w/2)
		y_max=c_y+(o_h/2)

		# print('x_min y_min x_max y_max',(x_min,y_min,x_max,y_max))

		x_min*=Pwidth
		y_min*=Pheight
		x_max*=Pwidth
		y_max*=Pheight

		# print('x_min y_min x_max y_max',(x_min,y_min,x_max,y_max))

		x_min=int(x_min)
		y_min=int(y_min)
		x_max=int(x_max)
		y_max=int(y_max)

		crop_img = img[y_min:y_max, x_min:x_max]
		crop_img_hash = hsh.compute(crop_img)[0]

		# crop_img_hash = ''.join( crop_img_hash.to_bytes(2, 'big') ).decode('utf-8')

		# bl = b''
		# for int_ in crop_img_hash:
		# 	bl+=int_.tobytes('A')

		crop_img_hash = hashlib.md5(crop_img_hash).hexdigest()
		target_path_=targetFullPath+dict_[c_num]+'_'+crop_img_hash+'.jpg'
		print('Filename',name,'Cut',crop_img_hash)
		showName=str(image_counter)+"_"+str(line_counter)+"_"+dict_[c_num]


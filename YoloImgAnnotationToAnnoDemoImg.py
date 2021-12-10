import os
import cv2

import hashlib

txtPath='data.unrecognized.20211207.cut/'
# txtPath='data/'
targetFullPath=txtPath.replace('/','.annoDemo/')
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

dict_=predefined_classes()
print('dict_:',dict_)
for i, name in enumerate(files):
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
	print('fullPath:',fullPath)
	print('fullPathImg:',fullPathImg)

	Pheight,Pwidth,Pdepth=img.shape
	box_row=''
	print(' ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ')

	img_hash = hashlib.md5(img).hexdigest()
	target_path_=targetFullPath+img_hash+'.jpg'
	print(target_path_,img.shape,img_hash)

	print('Pheight Pwidth')
	print(txtPath,name,Pheight,Pwidth)
	for i in txtList:
		print(' ===== ===== ===== ===== =====')
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

		strockWidth=o_w/100
		img = cv2.rectangle(img, (x_min,y_min), (x_max,y_max), (0,0,255), int(strockWidth))
		img = cv2.putText(img, dict_[c_num], (x_min,y_min+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), int(strockWidth), cv2.LINE_AA)
	cv2.imwrite(target_path_,img)

	cv2.imshow("cropped", img)
	cv2.waitKey(1)

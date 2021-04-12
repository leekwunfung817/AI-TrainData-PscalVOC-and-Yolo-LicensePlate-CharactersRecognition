import numpy as np
np.seterr(invalid='ignore')
import os
import cv2
import math


def add_snow(image):    
	image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS) ## Conversion to HLS    
	image_HLS = np.array(image_HLS, dtype = np.float64)     
	brightness_coefficient = 2.5     
	snow_point=140 ## increase this for more snow    
	image_HLS[:,:,1][image_HLS[:,:,1]<snow_point] = image_HLS[:,:,1][image_HLS[:,:,1]<snow_point]*brightness_coefficient ## scale pixel values up for channel 1(Lightness)    
	image_HLS[:,:,1][image_HLS[:,:,1]>255]  = 255 ##Sets all values above 255 to 255    
	image_HLS = np.array(image_HLS, dtype = np.uint8)    
	image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB) ## Conversion to RGB    
	return image_RGB

 #  rain
 ##### ##### ##### ##### ##### 
def generate_random_lines(imshape,slant,drop_length):    
	drops=[]    
	for i in range(math.floor( imshape[0]/2 )): ## If You want heavy rain, try increasing this        
		# if slant<0:            
		# 	x= np.random.randint(slant,imshape[1])        
		# else:            
		x= np.random.randint(0,imshape[1]-slant)        
		y= np.random.randint(0,imshape[0]-drop_length)        
		drops.append((x,y))
	return drops            

def add_rain(image):        
	image = image.astype(np.float32)
	imshape = image.shape    
	slant_extreme=10    
	slant= np.random.randint(-slant_extreme,slant_extreme)     
	drop_length=20    
	drop_width=1
	drop_color=(200,200,200) ## a shade of gray    
	rain_drops= generate_random_lines(imshape,slant,drop_length)        
	# print('rain_drops',len(rain_drops))
	for rain_drop in rain_drops:        
		cv2.line(image,(rain_drop[0],rain_drop[1]),(rain_drop[0]+slant,rain_drop[1]+drop_length),drop_color,drop_width)    
	image= cv2.blur(image,(6,6)) ## rainy view are blurry        
	brightness_coefficient = 0.7 ## rainy days are usually shady     
	image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS) ## Conversion to HLS    
	image_HLS[:,:,1] = image_HLS[:,:,1]*brightness_coefficient ## scale pixel values down for channel 1(Lightness)    
	image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB) ## Conversion to RGB    
	return image_RGB

 #  ploygon shadow
 ##### ##### ##### ##### ##### 
def generate_shadow_coordinates(imshape, no_of_shadows=1):    
	vertices_list=[]    
	for index in range(no_of_shadows):        
		vertex=[]        
		for dimensions in range(np.random.randint(3,15)): ## Dimensionality of the shadow polygon            
			vertex.append(( imshape[1]*np.random.uniform(),imshape[0]//3+imshape[0]*np.random.uniform()))        
		vertices = np.array([vertex], dtype=np.int32) ## single shadow vertices         
		vertices_list.append(vertices)    
	return vertices_list ## List of shadow vertices

def add_shadow(image,no_of_shadows=3):    
	image = image.astype(np.float32)
	image_HLS = cv2.cvtColor(image,cv2.COLOR_RGB2HLS) 
	## Conversion to HLS    
	mask = np.zeros_like(image)     
	imshape = image.shape    
	vertices_list= generate_shadow_coordinates(imshape, no_of_shadows) 
	#3 getting list of shadow vertices    
	for vertices in vertices_list:         
		cv2.fillPoly(mask, vertices, 255) ## adding all shadow polygons on empty mask, single 255 denotes only red channel        
	image_HLS[:,:,1][mask[:,:,0]==255] = image_HLS[:,:,1][mask[:,:,0]==255]*0.5 ## if red channel is hot, image's "Lightness" channel's brightness is lowered     
	image_RGB = cv2.cvtColor(image_HLS,cv2.COLOR_HLS2RGB) 
		## Conversion to RGB    
	return image_RGB

















def rectangle(image):
	for x in range(1,8):
		overlay = image.copy()
		row,col,ch = image.shape

		w, h = np.random.randint(100,500), np.random.randint(100,500)
		x, y = np.random.randint(0,row), np.random.randint(0,col),   # Rectangle parameters
		r,g,b = np.random.randint(0, 255),np.random.randint(0, 255),np.random.randint(0, 255)
		cv2.rectangle(overlay, (x, y), (x+w, y+h), (r,g,b), -1)  # A filled rectangle
		alpha = 0.3  # Transparency factor.
		# Following line overlays transparent rectangle over the image
		image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)
	return image

def speckle(image):
	row,col,ch = image.shape
	gauss = np.random.randn(row,col,ch)
	gauss = gauss.reshape(row,col,ch)        
	noisy = image + (image * gauss)
	return noisy

 #  main
 ##### ##### ##### ##### ##### 

def allNoise(image):
	image = rectangle(image)
	image = speckle(image)
	image = add_shadow(image)
	image = add_rain(image)
	return image

import cv2 as cv
import numpy as np 
import imutils
import random

####Chuong trinh con
def resiz1(image,k):
	(w,h) = image.shape
	w_dot = int(w*k)
	h_dot = int(h*k)
	return cv.resize(image,(h_dot,w_dot), interpolation = cv.INTER_CUBIC)

def imcrop1(image,crop_window_size):
	(h,w) = image.shape
	x1 = int(w/2 - crop_window_size/2)
	x2 = int(w/2 + crop_window_size/2)
	y1 = int(h/2 - crop_window_size/2)
	y2 = int(h/2 + crop_window_size/2)
	return image[y1:y2,x1:x2]

def imcrop2(image,crop_window_size):
	(h,w,d) = image.shape
	x1 = int(w/2 - crop_window_size/2)
	x2 = int(w/2 + crop_window_size/2)
	y1 = int(h/2 - crop_window_size/2)
	y2 = int(h/2 + crop_window_size/2)
	return image[y1:y2,x1:x2,:]

# def hormoCritia(image,region):
# 	(x,y,w,h) = region
# 	partition = image[y:y+h,x:x+w]
# 	return np.mean(partition)

# def notHormo(image,region):
# 	return hormoCritia(image,region) < hormoCritia(image,(0,0,image.shape[1],image.shape[0]))

# def isHormo(image,region):
# 	return hormoCritia(image,region) >= hormoCritia(image,(0,0,image.shape[1],image.shape[0]))

def isHormo(image,region,thresh_val):
	(x,y,w,h) = region
	partition = image[y:y+h,x:x+w]
	for indexx in range(0,w):
		for indexy in range(0,h):
			if (partition[indexy,indexx] < thresh_val):
				return False
	return True

def isAdj(region1,region2):
	(x1,y1,w1,h1) = region1
	(x2,y2,w2,h2) = region2

	if w1 > w2:
		(x1,y1,w1,h1) = region2
		(x2,y2,w2,h2) = region1

	if (x1 + w1) == x2 or (x2 + w2) == x1:
		if y1 >= y2 and y1 < (y2 + h2 - 1):
			return True
		if (y1 + h1) <= (y2 + h2) and (y1 + h1 - 1) > y2:
			return True
		if h1 == 1 and h2 == 1 and y1 == y2:
			return True

	if (y1 + h1) == y2 or (y2 + h2) == y1:
		if x1 >= x2 and x1 < (x2 + w2 - 1):
			return True
		if (x1 + w1) <= (x2 + w2) and (x1 + w1 - 1) > x2:
			return True
		if w1 == 1 and w2 == 1 and x1 == x2:
			return True

	return False

def splitRegion(region):
	(x,y,w,h) = region
	if(w == 1 or h == 1):
		new_region = [(region)]
	else:
		new_region = [(x,y,w//2,h//2),
		(x+w//2,y,w//2,h//2),
		(x+w//2,y+h//2,w//2,h//2),
		(x,y+h//2,w//2,h//2)]
	return new_region

def display(image,region):
	(x,y,w,h) = region
	image_tmp = np.zeros((image.shape),dtype = np.uint8)
	image_tmp[y:y+h,x:x+w] = image[y:y+h,x:x+w]
	cv.imshow("Quater",image_tmp)

def getValue(image,region):
	(x,y,w,h) = region
	return image[y:y+h,x:x+h]

def setValue(image,region,value):
	(x,y,w,h) = region
	image[y:y+h,x:x+w] = value
	
####



####Doc anh
# im0 = cv.imread('view.jpg')
# im = cv.cvtColor(im0,cv.COLOR_BGR2GRAY)
# crop_window_size = 512
# imcr = imcrop1(im,512)
# imcr_C = imcrop2(im0,512)

im0 = cv.imread('imcr.jpg')
imcr = cv.cvtColor(im0,cv.COLOR_BGR2GRAY)
####

####Hang so lay nguong
T = 150
####

####Split
ProcessList = splitRegion((0,0,imcr.shape[1],imcr.shape[0]))
# print(ProcessList)
regionList = []

t = 0
print('Split process:')
while True:

	t = t + 1
	if t == 4:
		t = 0
	print('Loading' + '.'*t + ' '*(3-t),end="\r")

	if len(ProcessList) == 0:
		break
	else:
		region = ProcessList[0]
	ProcessList.remove(region)

	if(isHormo(imcr,region,T)):
		regionList.append(region)
	elif splitRegion(region) == [region]:
		pass
	else:
		ProcessList.extend(splitRegion(region))
print('Completed'+' '*6)
####

####Merge
mergeList = []
ProcessList = regionList[:]
t = 0
print('\nMerge process:')
while True:
	t = t + 1
	if t == 4:
		t = 0
	print('Loading' + '.'*t + ' '*(3-t),end="\r")
	if len(ProcessList) == 0:
		break
	else:
		region = ProcessList[0]
	ProcessList.remove(region)
	bigRegion = []
	bigRegion.append(region)
	checkedList = []
	while True:
		bigRegion_tmp = bigRegion
		for region in bigRegion_tmp:
			if region not in checkedList:
				ProcessList_tmp = ProcessList[:]
				for testRegion in ProcessList_tmp:
					if(isAdj(region,testRegion)):
						bigRegion.append(testRegion)
						ProcessList.remove(testRegion)
		checkedList = bigRegion_tmp
		if len(bigRegion_tmp) == len(bigRegion):
			break
	mergeList.append(bigRegion)
print('Completed'+' '*6)
####

print('\nCo ' + str(len(mergeList)) +' hinh')

tmp = np.zeros((imcr.shape[0],imcr.shape[1]),dtype= np.uint8)
i = 0
value = 0
for bigRegion in mergeList:
	i = i + 1
	value = value + 50
	for region in bigRegion:
		cv.imshow("Tmp",tmp)
		setValue(tmp,region,value)
		k = cv.waitKey(1) & 0xFF
		if k == 27:
			break
	print('region ' + str(i) + ' was drawn')
	k = cv.waitKey(1) & 0xFF
	if k == 27:
		break

# i = 0
total = 0
for bigRegion in mergeList:
	total = total + len(bigRegion)
	# for region in bigRegion:
	# 	print(region)
	# print('Above is bigRegion ' + str(i))
	# i = i + 1

print('\n')
print(len(regionList) == total)
print('press any key to end process')
cv.waitKey(0)
cv.destroyAllWindows()



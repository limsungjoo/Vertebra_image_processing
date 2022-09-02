import numpy as np
from PIL import Image
from glob import glob
import SimpleITK as sitk
from tqdm import tqdm
from collections import defaultdict
import cv2


def readcsv2dict(csvfile):
	ddict = defaultdict(list)
	for line in open(csvfile).readlines()[1:]:
		ddict[line.strip().split(",")[0].strip()].append(tuple(line.strip().split(",")[1:]))

	return ddict

point_dict = readcsv2dict("points.csv")
# print(list(point_dict.keys()))
file_list = glob("img_GE/*/*.jpg")

for key in point_dict.keys():
	point_dict[key] = sorted(point_dict[key],key = lambda slist:int(slist[3]),reverse=True)

# print(point_dict["5821621_W_ser4324img00104.jpg"])
# print(point_dict["7970117_W_ser6930img00104.jpg"])

n = 0
for num,dcm_file in enumerate(tqdm(file_list)):
	filename = 	"_".join(dcm_file.split("/")[-1].split("_")[:3]).split(".")[0].strip()+".jpg"
	# print(filename)

	if point_dict[filename] == []:
		continue
	
	image = cv2.imread(dcm_file,0)

	points = point_dict[filename]
	for pn,point in enumerate(points):
		try:
			center_x = int(point[2])
			center_y = int(point[3])
			# if point[7] =="true" or point[8] == "true":
			# 	continue

			if pn == 0:
				y_top = int(abs(int(points[pn+1][3]) - center_y) / 2)+20
				y_bottom = int(abs(int(points[pn+1][3]) - center_y) / 2)+20

			elif pn == len(point_dict[filename])-1:
				y_top = int(abs(int(points[pn-1][3]) - center_y) / 2)+20
				y_bottom = int(abs(int(points[pn-1][3]) - center_y) / 2)+20
			
			else:
				y_top = int(abs(int(points[pn-1][3]) - center_y) / 2)+20
				y_bottom = int(abs(int(points[pn+1][3]) - center_y) / 2)+20

			if center_x-200 <0:
				x_left = center_x
				continue
			else:
				x_left = 200

			if center_x+200 >= image.shape[1]:
				x_right = image.shape[1] - center_x -1
				continue
			else:
				x_right = 200

			if center_y-y_bottom <0:
				y_bottom = center_y
				continue

			if center_y+y_top >= image.shape[0]:
				y_top = image.shape[0] - center_y -1
				continue

			crop_img = image[center_y-y_bottom:center_y+y_top,center_x-x_left:center_x+x_right]

			folder = "VF" if point[7] =="1" else "Non-VF"
			# if point[7] =="1":
			# 	print("yes")
			cv2.imwrite("img_vertebras/"+folder+"/"+filename+"_"+str(pn)+".jpg",crop_img)

		except:
			pass
	

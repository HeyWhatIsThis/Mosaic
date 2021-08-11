import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import os
import math
import time


MainImage= Image.open('d.jpg')
MainImage.show()
width, height = MainImage.size
print(width,height)
newsize= (500,500)
MainImage=MainImage.resize(newsize)
width, height= MainImage.size
print(MainImage.size)
tiles = []
for i in range(0, 50):
  for j in range(0, 50):
    left = i * width/50
    right = left + width/50
    top = j * height/50
    bottom = top + height/50
    box = (left, top, right, bottom)
    tiles.append(MainImage.crop(box))


color_data = []

for tile in tiles: 

    width, height = tile.size
    pixels = []
    for x in range(width):
        for y in range(height):
            pixels.append(tile.load()[x, y])
    
    r = 0
    g = 0
    b = 0
    for pixel in pixels:
        r += pixel[0]
        g += pixel[1]
        b += pixel[2]
        
    r = r/len(pixels)
    g = g/len(pixels)
    b = b/len(pixels)
    
    color_data.append((r, g, b))
color_nump_data=np.array(color_data)       

imageCombos = []

img_path= r"C:\Users\Dalton\SamplePhoto"
for imageCombo in os.listdir(img_path):
    imageCombos.append(Image.open(os.path.join(img_path,imageCombo)))
imageCombosnump=np.array(imageCombos)    
imageEdits= []
for imageCombo in imageCombosnump :
    Editimage=imageCombo.resize((10,10))
    imageEdits.append(Editimage)
    r,g,b = Editimage.split()
    thatnewnew=Image.merge("RGB", (b,g,r))
    graynewnew=ImageOps.grayscale(Editimage)
    rgbgray=graynewnew.convert('RGB')
    imageEdits.append(thatnewnew)
    imageEdits.append(rgbgray)
    
    
    print("yes")

imageEditsnump=np.array(imageEdits)


#
editPixels = []
edit_data=[]
count=0



for imageEdit in imageEdits:
  editPixels.append(imageEdit.load())
for editPixel in editPixels:
  
  width, height = imageEditsnump[count].size
  pixelsacks =[]
  for i in range (0,width):
    for j in range (0,height):
      pixelsacks.append(editPixels[count][i,j])
  edit_data.append(pixelsacks.copy())
  pixelsacks.clear()    
  count+=1      
print(edit_data[2])
print(edit_data[15])
print(edit_data[0])

y_actual=[0,3,2,1]
y_predicted=[0,3,2,1]

MSE = np.square(np.subtract(y_actual,y_predicted)).mean() 
rmse=math.sqrt(MSE)
print(MSE)



Mosaic=[]
counter=0
rmsediff = []
minpositions=[]
for tile in tiles:
  
  for j in range(0,len(edit_data)):
    #finding rmse value
    MSE = np.square(np.subtract(color_nump_data[counter],edit_data[j])).mean() 
    rmse=math.sqrt(MSE)
    
    #adding rmse value to array
    rmsediff.append(rmse)
    #finding postion of minimum rsme value
  minpos=rmsediff.index(min(rmsediff))
  minpositions.append(minpos)
  rmsediff.clear()
  counter+=1
  print(counter)

minspositionsnump=np.array(minpositions)

print("editdata:" )
print(len(edit_data))
print("tiles:" )
print( len( tiles))
print("colordata:")
print( len(  color_nump_data))
print("minpos:")
print(len( minpositions))
print("image edits")
print(len( imageEdits))
print("rmsediff")
print(len(rmsediff))


final_image= Image.new('RGB',(500,500),(255,255,255))
count=0
for i in range(0, 50):
  for j in range(0, 50):
    left =round(i * 500/50)
    top =round( j * 500/50)
    
    final_image.paste(imageEditsnump[minspositionsnump[count]],(left,top))
    count+=1
final_image.show()
time.sleep(5)

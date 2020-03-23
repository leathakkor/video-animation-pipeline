import cv2
import numpy as np
import glob

import cv2
import os

import os 
import cv2  
from PIL import Image  


image_folder = '/home/tyoung/Pictures/movies/'
video_name = 'video.avi'





  
# Checking the current directory path 
#print(os.getcwd())  
  
# Folder which contains all the images 
# from which video is to be generated 
#os.chdir("C:\\Python\\Geekfolder2")   
#path = "C:\\Python\\Geekfolder2"
  
mean_height = 0
mean_width = 0
  
num_of_images = len(os.listdir(image_folder)) 
# print(num_of_images) 
  
for file in os.listdir(image_folder): 
    im = Image.open(os.path.join(image_folder, file)) 
    width, height = im.size 
    mean_width += width 
    mean_height += height 
    # im.show()   # uncomment this for displaying the image 
  
# Finding the mean height and width of all images. 
# This is required because the video frame needs 
# to be set with same width and height. Otherwise 
# images not equal to that width height will not get  
# embedded into the video 
mean_width = int(mean_width / num_of_images) 
mean_height = int(mean_height / num_of_images) 
  
# print(mean_height) 
# print(mean_width) 
  
# Resizing of the images to give 
# them same width and height  
for file in os.listdir(image_folder): 
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith("png"): 
        # opening image using PIL Image 
        im = Image.open(os.path.join(image_folder, file))  
   
        # im.size includes the height and width of image 
        width, height = im.size    
        print(width, height) 
  
        # resizing  
        imResize = im.resize((mean_width, mean_height), Image.ANTIALIAS)  
        imResize.save( file, 'JPEG', quality = 95) # setting quality 
        # printing each resized image name 
        print(im.filename.split('\\')[-1], " is resized")  
  
  
# Video Generating function 
def generate_video(): 
    # ~ image_folder = '.' # make sure to use your folder 
    #video_name = 'mygeneratedvideo.avi'
    #os.chdir("C:\\Python\\Geekfolder2") 
      
    images = [img for img in os.listdir(image_folder) 
              if img.endswith(".jpg") or
                 img.endswith(".jpeg") or
                 img.endswith("png")] 
     
    # Array images should only consider 
    # the image files ignoring others if any 
    print(images)  
  
    frame = cv2.imread(os.path.join(image_folder, images[0])) 
  
    # setting the frame width, height width 
    # the width, height of first image 
    height, width, layers = frame.shape   
    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    video = cv2.VideoWriter(video_name, fourcc, 1, (width, height))  
  
    # Appending the images to the video one by one 
    for image in images:  
        video.write(cv2.imread(os.path.join(image_folder, image)))  
      
    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    video.release()  # releasing the video generated 
  
  
# Calling the generate_video function 
generate_video() 




# ~ images = [img for img in os.listdir(image_folder) if img.endswith(".JPG")]
# ~ frame = cv2.imread(os.path.join(image_folder, images[0]))
# ~ height, width, layers = frame.shape

# ~ video = cv2.VideoWriter(video_name, 0, 1, (width,height))

# ~ i = 0
# ~ for image in images:
    # ~ video.write(cv2.imread(os.path.join(image_folder, image)))
    # ~ #i+=2
    # ~ #if i > 10: break;

# ~ cv2.destroyAllWindows()
# ~ video.release()










# ~ for filename in glob.glob('/home/tyoung/Pictures/wedding/*.JPG'):
    # ~ print(filename)
    # ~ img = cv2.imread(filename)
    # ~ height, width, layers = img.shape
    # ~ size = (width,height)
    # ~ break;
    
    
# ~ out1 = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, size)

# ~ i = 0
# ~ for filename in glob.glob('/home/tyoung/Pictures/wedding/*.JPG'):
    # ~ print(filename)
    # ~ img = cv2.imread(filename)
    # ~ height, width, layers = img.shape
    # ~ size = (width,height)
    # ~ for i in range(240):
       # ~ out1.write(img)
    # ~ i += 1
    # ~ if i > 0: break;

## ~ for i in range(len(img_array)):
## ~     out1.write(img_array[i])
    
# ~ out1.release()


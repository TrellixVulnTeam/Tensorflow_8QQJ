#!/usr/bin/env python
# coding: utf-8

# # Object Detection Demo
# Welcome to the object detection inference walkthrough!  This notebook will walk you step by step through the process of using a pre-trained model to detect objects in an image. Make sure to follow the [installation instructions](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/installation.md) before you start.

# # Imports

# In[2]:


import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
import cv2

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt

from PIL import Image

# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')


# ## Env setup

# In[3]:


# This is needed to display the images.
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Object detection imports
# Here are the imports from the object detection module.

# In[4]:


from utils import label_map_util

from utils import visualization_utils as vis_util


# # Model preparation 

# ## Variables
# 
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_FROZEN_GRAPH` to point to a new .pb file.  
# 
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# In[5]:


# What model to download.

#http://download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_2018_01_28.tar.gz
#http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz
MODEL_NAME = 'faster_rcnn_resnet101_coco_2018_01_28'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'


# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')


# ## Download Model



# In[9]:


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


# # Detection

# In[10]:


# For the sake of simplicity we will use only 2 images:
# image1.jpg
# image2.jpg
# If you want to test the code with your images, just add path to the images to the TEST_IMAGE_PATHS.
#PATH_TO_TEST_IMAGES_DIR = 'test_images'
#TEST_IMAGE_PATHS = [ os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3) ]


PATH_TO_TEST_IMAGES_DIR = 'Analysis/Image/testing/image_02/0005'

TEST_IMAGE_PATHS = [f for f in os.listdir(PATH_TO_TEST_IMAGES_DIR) if os.path.isfile(os.path.join(PATH_TO_TEST_IMAGES_DIR, f)) and f.endswith('.png')]
TEST_IMAGE_PATHS= sorted(TEST_IMAGE_PATHS)
frame = cv2.imread(os.path.join(PATH_TO_TEST_IMAGES_DIR, TEST_IMAGE_PATHS[0]))
height, width, layers = frame.shape


VIDEO_PATH_DIR = 'Analysis/Video'
VIDEO_NAME = '0005.avi'

fourcc =  cv2.VideoWriter_fourcc('M','J','P','G') # Be sure to use lower case
video = cv2.VideoWriter(os.path.join(VIDEO_PATH_DIR, VIDEO_NAME), fourcc, 10, (width,height))
#file_list = [f for f in glob.glob("*.jpg")]

#TEST_IMAGE_PATHS=os.path.join(PATH_TO_TEST_IMAGES_DIR, file_list)


    
    
    
# Size, in inches, of the output images.
IMAGE_SIZE = (height/2, width/2)






    # In[21]:


run_start_time=time.time()


i=1
for image in TEST_IMAGE_PATHS:

    image_path = os.path.join(PATH_TO_TEST_IMAGES_DIR, image)
    frame = cv2.imread(image_path)

    video.write(frame) # Write out frame to video
    i=i+1
    cv2.imshow('video',frame)
    if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
        break
    
    
video.release()
cv2.destroyAllWindows()
print("Frame: " +str(i)+ "  -- Average Runtime: "+str((time.time()-run_start_time)/i)+"s")

print("Total Duration: {0:.2f}s".format(time.time()-run_start_time))






import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
from skimage import data
from skimage.color import rgb2hsv
from scipy.stats import kurtosis, skew
from skimage.feature import greycomatrix, greycoprops
import colorsys
from matplotlib.colors import hsv_to_rgb
import pickle



props = ['contrast', 'homogeneity', 'energy', 'correlation']

def evaluation(features):
  loaded_model = pickle.load(open("finalized_model.sav", 'rb'))
  y_pred = loaded_model.predict(features)
  print(y_pred)
  return y_pred


def patternScore(neighborhood):
    m_sum = 0
    m_sum = neighborhood[0,0] + neighborhood[0,1] + neighborhood[1,0] + neighborhood[1,1]
    if(m_sum == 3):
        return float(7.0/8.0)
    elif(m_sum == 0):
        return 0
    elif(m_sum == 1):
        return float(1.0/4.0)
    elif(m_sum == 4):
        return 1
    else:
        if(neighborhood[0][1] == neighborhood[0][0]):
            return .5
        elif(neighborhood[1][0] == neighborhood[0][0]):
            return .5
        else:
            return .75

def neighbors(im, i, j, d=1):
    im = np.array(im).astype(int)
    top_left = im[i-d:i+d, j-d:j+d]
    top_right = im[i-d:i+d, j:j+d+1]
    bottom_left = im[i:i+d+1, j-d:j+d]
    bottom_right = im[i:i+d+1, j:j+d+1]
    pattern = (patternScore(top_left) + patternScore(top_right) + patternScore(bottom_left) + patternScore(bottom_right))
    return pattern

def bwarea(img):
    d = 1
    area = 0
    for i in range(1,img.shape[0]-1):
        for j in range(1,img.shape[1]-1):
            area += neighbors(img,i,j)
    return area

def getMean(array):
  array= np.array(array)
  array_mean= array[np.nonzero(array)].mean()
  return array_mean

def glcm(img,features):
    glcm1 = greycomatrix(img,distances=[1], angles=[0])
    glcm2 = greycomatrix(img, distances=[1], angles=[np.pi/4], levels=256,
                            symmetric=True, normed=True)
    glcm3 = greycomatrix(img, distances=[1], angles=[np.pi/2], levels=256,
                            symmetric=True, normed=True)
    glcm4 = greycomatrix(img, distances=[1], angles=[np.pi*3/4], levels=256,
                            symmetric=True, normed=True)
    for f in props:
      features.append(greycoprops(glcm1,f)[0][0])
      features.append(greycoprops(glcm2,f)[0][0])
      features.append(greycoprops(glcm3,f)[0][0])
      features.append(greycoprops(glcm4,f)[0][0])

def texture_feature_extraction(bgr_img,hsv_img,features):
  img_grey = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
  cv2.imwrite('../Frontend/src/assets/greyImage.jpg', img_grey)
  cv2.imshow('grey',img_grey)

  h,s,v= cv2.split(hsv_img)

  glcm(img_grey,features)
  glcm(h,features)
  glcm(s,features)
  glcm(v,features)
  """(thresh, blackAndWhiteImage) = cv2.threshold(img_grey, 72, 255, cv2.THRESH_BINARY)
  cv2.imshow('',blackAndWhiteImage)
  area= bwarea(blackAndWhiteImage)
  features.append(area)
  """
  #print(features)
  #df_test= pd.DataFrame([])
  #df_test.
  #print(df_test)

  print(features)
  #df_test.append(features)
  features= np.array(features)
  features2= features.reshape(1,-1)
  print(features2)
  #print(df_test.iloc[0:])
  y_pred= evaluation(features2)
  #print(len(features))
  #feature_list.append(features)
  #print(feature_list)

  return y_pred

def color_feature_extraction(img):
  features=[]
  bgr_img= img
  hsv_img= cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
  lab_img= cv2.cvtColor(bgr_img,cv2.COLOR_BGR2LAB)

  b, g, r = cv2.split(bgr_img)
  h,s,v= cv2.split(hsv_img)
  l, a, b = cv2.split(lab_img)

  cv2.imshow('bg2',bgr_img)

  cv2.imshow('hsv',hsv_img)
  cv2.imwrite('../Frontend/src/assets/hsv.jpg', hsv_img)

  cv2.imshow('lab',lab_img)
  cv2.imwrite('../Frontend/src/assets/lab.jpg', lab_img)

  bgr_mean= getMean(bgr_img)
  hsv_mean= getMean(hsv_img)
  lab_mean= getMean(lab_img)

  std= np.std([x for x in bgr_img[np.nonzero(bgr_img)] ])

  kur= kurtosis(bgr_img[np.nonzero(bgr_img)])
  #print("Kurtosis:",kur)
  sk= skew(bgr_img[np.nonzero(bgr_img)])
  #print("Skewness:",sk)
  features.append(bgr_mean)
  features.append(hsv_mean)
  features.append(lab_mean)
  features.append(std)
  features.append(kur)
  features.append(sk)

  y_pred= texture_feature_extraction(bgr_img,hsv_img,features)
  return y_pred

def green_region_removal(img):
  rgb_img = img
  #print (type(rgb_img))
  #print(rgb_img)

  #print('Rbg Shape:')
  #print(rgb_img.shape)
  hsv_img = rgb2hsv(rgb_img)

  #print('Hsv Shape:')
  #print(hsv_img.shape)
  hue_img = hsv_img[:, :, 0]
  value_img = hsv_img[:, :, 2]
  sat_img = hsv_img[:,:,1]

  #print(hue_img)
  #print('Sat Shape:')
  #print(sat_img.shape)

  #fig, (#axis0, #axis1, #axis2) = plt.subplots(ncols=3, #figsize=(8, 2))

  #print('Rbg Shape:')
  #print(rgb_img.shape)

  #axis0.imshow('',rgb_img)
  #axis0.set_title("RGB image")
  #axis0.#axis('off')

  #axis0.imshow('',hsv_img)
  #axis0.set_title("HSV image")
  #axis0.#axis('off')

  #axis1.imshow('',hue_img, cmap='hsv')
  #axis1.set_title("Hue channel")
  #axis1.#axis('off')

  #axis2.imshow('',value_img)
  #axis2.set_title("Value channel")
  #axis2.#axis('off')

  #axis2.imshow('',sat_img)
  #axis2.set_title("Saturation c")
  #axis2.#axis('off')


  #fig.tight_layout()

  binary_img = ((0.56) <= hue_img) |  (hue_img <= (0.295))
  #print('bin Shape:')
  #print(binary_img.shape)
  #print(binary_img)

  #print('Rbg Shape:')
  #print(rgb_img.shape)

  #fig, (#axis0, #axis1) = plt.subplots(ncols=2, #figsize=(8, 3))

  #axis0.hist(hue_img.ravel(), 512)

  #axis0.set_title("Histogram of the Saturation channel with threshold")
  #axis0.axvline(x=sat_threshold, color='r', linestyle='dashed', linewidth=2)


  #axis0.set_xbound(0, 0.12)
  #axis1.imshow('',binary_img)

  #axis1.set_title("Sat-thresholded image")
  #axis1.#axis('off')

  #fig.tight_layout()
  """
  white_img = np.ones((250, 766, 3))
  white_img = white_img*255
  cv2.imwrite('/content/white_img.jpg', white_img)

  white_img[:,:,0] = np.logical_and(binary_img, white_img[:,:,0])
  white_img[:,:,1] = np.logical_and(binary_img, white_img[:,:,1])
  white_img[:,:,2] = np.logical_and(binary_img, white_img[:,:,2])
  cv2.imwrite('/content/bw_img.jpg', white_img)

"""
  rgb_img[:,:,0] = (np.minimum(binary_img, rgb_img[:,:,0]/255.0))*255
  rgb_img[:,:,1] = (np.minimum(binary_img, rgb_img[:,:,1]/255.0))*255
  rgb_img[:,:,2] = (np.minimum(binary_img, rgb_img[:,:,2]/255.0))*255
  cv2.imwrite('../Frontend/src/assets/greenRegion.jpg', rgb_img)
  y_pred= color_feature_extraction(rgb_img)
  return y_pred

def diesease_segmentation(img):

  frame = img

  #Convert BGR to HSV
  hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

  #define range of color of disease(usually shades of brown) in HSV
  lower_brown = np.array([5,100,100])
  upper_brown = np.array([25,255,255])

  #checking colors taken using plt function
  lo_square = np.full((10, 10, 3), lower_brown, dtype=np.uint8) / 255.0
  do_square = np.full((10, 10, 3), upper_brown, dtype=np.uint8) / 255.0

  """
  plt.subplot(1, 2, 1)
  plt.imshow(hsv_to_rgb(do_square))
  plt.subplot(1, 2, 2)
  plt.imshow(hsv_to_rgb(lo_square))
  plt.show()
  """

  #Threshold the HSV image to get only brown(disease-type) colors
  mask = cv2.inRange(hsv, lower_brown, upper_brown)
  
  #Bitwise-AND mask and original image
  res = cv2.bitwise_and(frame,frame, mask= mask)
  cv2.imwrite('../Frontend/src/assets/diseaseSegmented.jpg', res)
  y_pred= green_region_removal(res)
  return y_pred

def background_removal(img):

  rgb_img = img
  cv2.imwrite('../Frontend/src/assets/originalImage.jpg', rgb_img)
  #print (type(rgb_img))
  #print(rgb_img)

  #print('Rbg Shape:')
  #print(rgb_img.shape)
  hsv_img = rgb2hsv(rgb_img)

  #print('Hsv Shape:')
  #print(hsv_img.shape)
  hue_img = hsv_img[:, :, 0]

  value_img = hsv_img[:, :, 2]
  sat_img = hsv_img[:,:,1]
  #print(hue_img)
  #print('Sat Shape:')
  #print(sat_img.shape)

  #fig, (#axis0, #axis1, #axis2) = plt.subplots(ncols=3, #figsize=(8, 2))

  #print('Rbg Shape:')
  #print(rgb_img.shape)

  #axis0.imshow('',rgb_img)
  #axis0.set_title("RGB image")
  #axis0.#axis('off')

  #axis0.imshow('',hsv_img)
  #axis0.set_title("HSV image")
  #axis0.#axis('off')

  #axis1.imshow('',hue_img, cmap='hsv')
  #axis1.set_title("Hue channel")
  #axis1.#axis('off')

  #axis2.imshow('',value_img)
  #axis2.set_title("Value channel")
  #axis2.#axis('off')

  #axis2.imshow('',sat_img)
  #axis2.set_title("Saturation c")
  #axis2.#axis('off')


  #fig.tight_layout()

  sat_threshold = 0.28
  binary_img = sat_img > sat_threshold
  #print('bin Shape:')
  #print(binary_img.shape)

  #print('Rbg Shape:')
  #print(rgb_img.shape)

  #fig, (#axis0, #axis1) = plt.subplots(ncols=2, #figsize=(8, 3))

  #axis0.hist(sat_img.ravel(), 512)

  #axis0.set_title("Histogram of the Saturation channel with threshold")
  #axis0.axvline(x=sat_threshold, color='r', linestyle='dashed', linewidth=2)


  #axis0.set_xbound(0, 0.12)
  #axis1.imshow('',binary_img)

  #axis1.set_title("Sat-thresholded image")
  #axis1.#axis('off')

  #fig.tight_layout()

  rgb_img[:,:,0] = (np.minimum(binary_img, rgb_img[:,:,0]/255.0))*255
  rgb_img[:,:,1] = (np.minimum(binary_img, rgb_img[:,:,1]/255.0))*255
  rgb_img[:,:,2] = (np.minimum(binary_img, rgb_img[:,:,2]/255.0))*255
  #cv2.imshow('bg',rgb_img)
  cv2.imwrite('../Frontend/src/assets/backgroundRemovedImage.jpg', rgb_img)
  y_pred= diesease_segmentation(rgb_img)
  return y_pred

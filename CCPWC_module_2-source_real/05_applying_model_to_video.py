# -*- coding: utf-8 -*-
"""05_Apply-model-to-Video.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XVe0bweyC6W8dySvzfufF5AR7PN2i5mA

# 05. Actual Use : Violence detection for .mp4 video file

# Imports
"""

import cv2 # openCV 4.5.1
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import time

from skimage.io import imread
from skimage.transform import resize
from PIL import Image, ImageFont, ImageDraw # add caption by using custom font

from collections import deque

"""# 05-A. Load Model Files
* **`base_model`** : MobileNet
* **`model`** : trained LSTM model file. `210512_MobileNet_model_epoch100.h5`

## 1. base_model : MobileNet
"""

base_model=keras.applications.mobilenet.MobileNet(input_shape=(160, 160, 3),
                                                  include_top=False,
                                                  weights='imagenet', classes=2)

"""## 2. model : trained LSTM model(.h5)"""

model=keras.models.load_model('210512_MobileNet_model_epoch100.h5')

"""# 05-B. Define functions

## 1. Function : video_reader()
* Load video file >> Scaling, Resizing >> Transform to Numpy array >> return Numpy array
"""

def video_reader(cv2, filename):
    """Load 1 video file. Next, read each frame image and resize as (fps, 160, 160, 3) shape and return frame Numpy array."""

    frames=np.zeros((30, 160, 160, 3), dtype=np.float) #> (fps, img size, img size, RGB)

    i=0
    print(frames.shape)
    vid=cv2.VideoCapture(filename) # read frame img from video file.

    if vid.isOpened():
        grabbed, frame=vid.read()
    else:
        grabbed=False

    frm=resize(frame,(160, 160, 3))
    frm=np.expand_dims(frm, axis=0)

    if(np.max(frm)>1):
        frm=frm/255.0 # Scaling
    frames[i][:]=frm
    i+=1
    print('Reading Video')

    while i<30:
        grabbed, frame=vid.read()
        frm=resize(frame, (160, 160, 3))
        frm=np.expand_dims(frm, axis=0)
        if(np.max(frm)>1):
            frm=frm/255.0
        frames[i][:]=frm
        i+=1

    return frames

"""## 2. Function : create_pred_imgarr()
* Extract features of each frame img by using base_model(MobileNet)
* Reshape features Numpy array to insert LSTM model
"""

def create_pred_imgarr(base_model, video_frm_ar):
    """Insert base_model(MobileNet) and result of video_reader() function.
    This function extract features from each frame img by using base_model.
    And reshape Numpy array to insert LSTM model : (1, 30, 25600)"""
    video_frm_ar_dim=np.zeros((1, 30, 160, 160, 3), dtype=np.float)
    video_frm_ar_dim[0][:][:]=video_frm_ar #> (1, 30, 160, 160, 3)

    # Extract features from each frame img by using base_model(MobileNet)
    pred_imgarr=base_model.predict(video_frm_ar)
    # Reshape features array : (1, fps, 25600)
    pred_imgarr=pred_imgarr.reshape(1, pred_imgarr.shape[0], 5*5*1024)

    return pred_imgarr #> ex : (1, 30, 25600)

"""## 3. Function : pred_fight()
* Distinguish Violence(Fight) / Non-Violence(NonFight)
* Insert reshaped-features-array to trained LSTM model
"""

def pred_fight(model, pred_imgarr, acuracy=0.9):
    """If accuracy>=input value(ex:0.9), return (Violence)'True'. else, return 'False'.
    ::model:: trained LSTM model (We already load .h5 file in the above.)
    ::pred_imgarr:: (1, 30, 25600) shaped Numpy array. Extracted features.
    ::accuracy:: default value is 0.9"""

    pred_test=model.predict(pred_imgarr) #> Violence(Fight) : [0,1]. Non-Violence(NonFight) : [1,0]

    if pred_test[0][1] >= acuracy:
        return True, pred_test[0][1] #> True, Probability of Violence

    else:
        return False, pred_test[0][1] #> False, Probability of Violence

"""## 4. Check above functions doing well

### 1) Load any video File
"""

video_file='Fight_itwill_210506_01.mp4'

"""### 2) Check function's operation"""

video_frm_ar=video_reader(cv2, video_file)

pred_imgarr=create_pred_imgarr(base_model, video_frm_ar)
pred_imgarr.shape

preds=pred_fight(model, pred_imgarr, 0.9)
preds #> (Violence True or False, Probability of Violence)

"""# 05-C. Define all-in-one function
* It contains `video_reader()`, `create_pred_imgarr()`, `pred_fight()` as all-in-one.
* Input : 1 Video file
* Output : Violence True or False / Probability of Violence

## 1. Define detect_violence()
"""

def detect_violence(video):
    """ It contains video_reader(), create_pred_imgarr(), pred_fight() function as all-in-one.
    ::video:: video file (.mp4, .avi, ...)

    video_reader() : Read each frame img by using openCV. Resize Numpy array
    create_pred_imgarr() : Extract features from frame img array by using base model(MobileNet)
    pred_fight() : Decide Violence True or False by using trained LSTM model"""

    video_frm_ar=video_reader(cv2, video)
    pred_imgarr=create_pred_imgarr(base_model, video_frm_ar)

    time1=int(round(time.time()*1000))

    f, precent=pred_fight(model, pred_imgarr, acuracy=0.65)

    time2=int(round(time.time()*1000))

    result={'Violence': f, #> True(Violence), False(Non-Violence)
            'Violence Estimation': str(precent), # Probability of Violence
            'Processing Time' : str(time2-time1)}

    return result

"""## 2. Test function: detect_violence()"""

video_file='Fight_itwill_210506_01.mp4'
detect_violence(video_file)

"""# 05-D. Add caption & Save output video file
* **`Add Captions on video file`**
    * Violence True or False
    * Probability of violence
* **`View & Save output video`**

## 1. Setting : Input path & Output path
* **`input_path`** : input video file
* **`output_path`** : You'll save output video file in output_path.
"""

input_path='Fight_itwill_210506_05.mp4'

output_path=f'{input_path}+output.mp4'

"""## 2. Distinguish Violence True or False & Add caption on Video file"""

vid=cv2.VideoCapture(input_path)
fps=vid.get(cv2.CAP_PROP_FPS) # recognize frames per secone(fps) of input_path video file.
print(f'fps : {fps}') # print fps.

writer=None
(W, H)=(None, None)
i=0 # number of seconds in video = The number of times that how many operated while loop .
Q=deque(maxlen=128)

video_frm_ar=np.zeros((1, int(fps), 160, 160, 3), dtype=np.float) #frames
frame_counter=0 # frame number in 1 second. 1~30
frame_list=[]
preds=None
maxprob=None

#. While loop : Until the end of input video, it read frame, extract features, predict violence True or False.
# ----- Reshape & Save frame img as (30, 160, 160, 3) Numpy array  -----
while True:
    frame_counter+=1
    grabbed, frm=vid.read() # read each frame img. grabbed=True, frm=frm img. ex: (240, 320, 3)

    if not grabbed:
        print('There is no frame. Streaming ends.')
        break

    if W is None or H is None: # W: width, H: height of frame img
        (H, W)=frm.shape[:2]

    output=frm.copy() # It is necessary for streaming captioned output video, and to save that.

    frame=resize(frm, (160, 160, 3)) #> Resize frame img array to (160, 160, 3)
    frame_list.append(frame) # Append each frame img Numpy array : element is (160, 160, 3) Numpy array.

    if frame_counter>=fps: # fps=30 et al
        #. ----- we'll predict violence True or False every 30 frame -----
        #. ----- Insert (1, 30, 160, 160, 3) Numpy array to LSTM model ---
        #. ----- We'll renew predict result caption on output video every 1 second. -----
        # 30-element-appended list -> Transform to Numpy array -> Predict -> Initialize list (repeat)
        frame_ar=np.array(frame_list, dtype=np.float16) #> (30, 160, 160, 3)
        frame_list=[] # Initialize frame list when frame_counter is same or exceed 30, after transforming to Numpy array.

        if(np.max(frame_ar)>1):
            frame_ar=frame_ar/255.0 # Scaling RGB value in Numpy array

        pred_imgarr=base_model.predict(frame_ar) #> Extract features from each frame img by using MobileNet. (30, 5, 5, 1024)
        pred_imgarr_dim=pred_imgarr.reshape(1, pred_imgarr.shape[0], 5*5*1024)#> (1, 30, 25600)

        preds=model.predict(pred_imgarr_dim) #> (True, 0.99) : (Violence True or False, Probability of Violence)
        print(f'preds:{preds}')
        Q.append(preds)

        # Predict Result : Average of Violence probability in last 5 second
        if i<5:
            results=np.array(Q)[:i].mean(axis=0)
        else:
            results=np.array(Q)[(i-5):i].mean(axis=0)

        print(f'Results = {results}') #> ex : (0.6, 0.650)

        maxprob=np.max(results) #> Select Maximum Probability
        print(f'Maximum Probability : {maxprob}')
        print('')

        rest=1-maxprob # Probability of Non-Violence
        diff=maxprob-rest # Difference between Probability of Violence and Non-Violence's
        th=100

        if diff>0.80:
            th=diff # ?? What is supporting basis?

        frame_counter=0 #> Initialize frame_counter to 0
        i+=1 #> 1 second elapsed

        # When frame_counter>=30, Initialize frame_counter to 0, and repeat above while loop.

    # ----- Setting caption option of output video -----
    # Renewed caption is added every 30 frames(if fps=30, it means 1 second.)
    font1=ImageFont.truetype('fonts/Raleway-ExtraBold.ttf', int(0.05*W)) # font option
    font2=ImageFont.truetype('fonts/Raleway-ExtraBold.ttf', int(0.1*W)) #font option

    if preds is not None and maxprob is not None:
        if (preds[0][1])<th : #> if violence probability < th, Violence=False (Normal, Green Caption)
            text1_1='Normal'
            text1_2='{:.2f}%'.format(100-(maxprob*100))
            img_pil=Image.fromarray(output)
            draw=ImageDraw.Draw(img_pil)
            draw.text((int(0.025*W), int(0.025*H)), text1_1, font=font1, fill=(0, 255, 0, 0))
            draw.text((int(0.025*W), int(0.095*H)), text1_2, font=font2, fill=(0, 255, 0, 0))
            output=np.array(img_pil)

        else : #> if violence probability > th, Violence=True (Violence Alert!, Red Caption)
            text2_1='Violence Alert!'
            text2_2='{:.2f}%'.format(maxprob*100)
            img_pil=Image.fromarray(output)
            draw=ImageDraw.Draw(img_pil)
            draw.text((int(0.025*W), int(0.025*H)), text2_1, font=font1, fill=(0, 0, 255, 0))
            draw.text((int(0.025*W), int(0.095*H)), text2_2, font=font2, fill=(0, 0, 255, 0))
            output=np.array(img_pil)

    # Save captioned video file by using 'writer'
    if writer is None:
        fourcc=cv2.VideoWriter_fourcc(*'DIVX')
        writer=cv2.VideoWriter(output_path, fourcc, 30, (W, H), True)

    cv2.imshow('This is output', output) # View output in new Window.
    writer.write(output) # Save output in output_path

    key=cv2.waitKey(round(1000/fps)) # time gap of frame and next frame
    if key==27: # If you press ESC key, While loop will be breaked and output file will be saved.
        print('ESC is pressed. Video recording ends.')
        break

print('Video recording ends. Release Memory.') # Output file will be saved.
writer.release()
vid.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
from threading import Timer  
import time

# times = 0

# def onTime():
#     print(times)
#     global times
#     times = 0
#     t=Timer(1,onTime) 
#     t.start()

frame = None
def onClick(event,x,y,flags,params):
    inframe = frame
    if(event == cv2.EVENT_LBUTTONDOWN):
        if(inframe is not None):
            blue = inframe[y,x,0]
            green = inframe[y,x,1]
            red = inframe[y,x,2]
            #print('x:%s,y:%s' % (x,y))
            print('red:%s, green:%s, blue:%s' % (red,green,blue))

def onSingle(event,x,y,flags,params):
    inframe = params
    if(event == cv2.EVENT_LBUTTONDOWN):
        if(inframe is not None):
            print(inframe[y,x])


lowThreshold = 0
max_lowThreshold = 100
ratio = 3
kernel_size = 3

a=0

def setLow(lowT):
    a = lowT

try:
    capture=cv2.VideoCapture(0)
except e:
    print(e)
#cv2.createTrackbar('Min threshold','Video',lowThreshold, max_lowThreshold, setLow)

level = 230
misc_scale = 70
isGet, frame = capture.read()
cv2.namedWindow('Video')
cv2.setMouseCallback('Video',onClick)
# t=Timer(1,onTime)  
# t.start()

while isGet:
    # edges = cv2.Canny(frame, 80, 150, apertureSize = 3)
    # times +=1
    frame_int = np.array(frame,int)
    frame_top_b = np.clip(np.sign(frame_int-level),0,1)
    frame_top_sum_a  = 3 - frame_top_b.sum(axis=2)
    frame_top_single = frame_top_sum_a/2 - np.clip(frame_top_sum_a-2,0,1)

    frame_btm_b = np.clip(np.sign(frame_int-level+misc_scale),0,1)
    frame_btm_sum_a  = 3 - frame_btm_b.sum(axis=2)
    frame_btm_single = frame_btm_sum_a/2 - np.clip(frame_btm_sum_a-2,0,1)

    frame_single = np.ceil((frame_top_single+frame_btm_single)/2)

    frame_single_m = np.zeros(frame.shape)
    frame_single_m[:,:,0]=frame_single
    frame_single_m[:,:,1]=frame_single
    frame_single_m[:,:,2]=frame_single
    frame_cov = frame_single_m * frame_top_b *255# frame_cov = np.array(frame_single_m * frame_top_b *255,dtype=np.uint8)
    frame_cov = np.array((frame_cov[:480-1,:640-1,:]+frame_cov[1:,1:,:])/2,dtype=np.uint8)
    # cv2.imshow('cov',frame_cov)
    # cv2.imshow('Video',frame)
    # cv2.imshow('edge',edges)
#   gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#   CannyThreshold(a)
    key = cv2.waitKey(10)
    if key == ord('s'):
        cv2.imwrite('screenshot.bmp', frame)
    elif key == ord('q'):
        cv2.destroyAllWindows()
        break

    isGet, frame = capture.read()

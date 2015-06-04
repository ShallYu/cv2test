import cv2
import numpy as np

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

try:
    capture=cv2.VideoCapture(0)
except e:
    print(e)
#cv2.createTrackbar('Min threshold','Video',lowThreshold, max_lowThreshold, setLow)

level = 250
isGet, frame = capture.read()
cv2.setMouseCallback('Video',onClick)

    # edges = cv2.Canny(frame, 80, 150, apertureSize = 3)

    # frame_int = np.array(frame,int)
    # frame_b = np.clip(np.sign(frame_int-level),0,1)
    # frame_sum_a  = 3 - frame_b.sum(axis=2)
    # frame_single = np.array(frame_sum_a/2 - np.clip(frame_sum_a-2,0,1),dtype=np.uint8)
    # frame_single_m = np.zeros(frame.shape)
    # frame_single_m[:,:,0]=frame_single
    # frame_single_m[:,:,1]=frame_single
    # frame_single_m[:,:,2]=frame_single
    # frame_cov = frame_single_m * frame_b *230
    # cv2.imshow('cov',frame_cov)
frame = frame.argmax(axis=0)
cv2.imshow('Video',frame)
key=cv2.waitKey()
if key=='q':
    cv2.destoryAllWindows()
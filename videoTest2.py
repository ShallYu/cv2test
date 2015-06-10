import cv2
import numpy as np
# from threading import Timer  
import socket

# times = 0

# def onTime():
#     print(times)
#     global times
#     times = 0
#     t=Timer(1,onTime) 
#     t.start()

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost",12345))
server.listen(1)
connection, address = server.accept()

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

bili = 0.45
low_level = 10
isGet, frame = capture.read()
cv2.namedWindow('Video')
cv2.setMouseCallback('Video',onClick)
# t=Timer(1,onTime)  
# t.start()


while isGet:
    # edges = cv2.Canny(frame, 80, 150, apertureSize = 3)
    # times +=1
    frame_single = np.zeros(frame.shape,dtype=float)
    frame_int = np.array(frame,int)+low_level
    frame_level = frame_int.sum(axis=2)
    
    frame_single[:,:,0] = frame_int[:,:,0] -frame_level * (bili+0.16)
    frame_single[:,:,1] = frame_int[:,:,1] -frame_level * (bili+0.09)
    frame_single[:,:,2] = frame_int[:,:,2] -frame_level * bili
    
    frame_single = np.clip(frame_single,0,255)
    # frame_single = np.array(frame_single,dtype=np.uint8)
    # frame_single_b = np.clip(frame_single,0,1)
    max_x = frame_single.sum(axis=0).argmax(axis=0)
    max_y = frame_single.sum(axis=1).argmax(axis=0)
    print(max_y)
    global r,g,b
    b_axis=np.array([max_x[0],max_y[0]])
    g_axis=np.array([max_x[1],max_y[1]])
    r_axis=np.array([max_x[2],max_y[2]])
    c_axix=b_axis+g_axis/2
    b_axix-=c_axis
    g_axix-=c_axis
    r_axix-=c_axis
    z_bg = -b_axis*g_axis
    z_rb = -r_axis*b_axis
    z_rg = -r_axis*g_axis
    z_all = sqrt(z_bg*z_rb*z_rg)
    z_b=z_all/z_rg
    z_g=z_all/z_rb
    z_r=z_all/z_bf
    print("%3d,%3d,%3d" % (z_b,z_g,z_r))
    # print("x:%3d, y:%3d" % (max_x[1],max_y[1]))
    # frame_cov = frame_single_b * 233
    # frame_cov = np.array(frame_single_m * frame_top_b *255,dtype=np.uint8)
    # frame_cov = np.array((frame_cov[:480-1,:640-1,:]+frame_cov[1:,1:,:])/2,dtype=np.uint8)
    cv2.imshow('cov',frame_single)
    cv2.imshow('Video',frame)
    try:
        connection.send("%3d,%3d" % (b_axis[0],b_axis[1]))
    except Exception,e:
        server.close()
        print(e)
        break
    # cv2.imshow('edge',edges)
    #   gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #   CannyThreshold(a)
    key = cv2.waitKey(10)
    if key == ord('s'):
        cv2.imwrite('screenshot.bmp', frame)
        cv2.imwrite('result.bmp',frame_single)
    elif key == ord('q'):
        cv2.destroyAllWindows()
        break

    isGet, frame = capture.read()

#!/usr/bin/python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from random import random
import numpy as np
import socket
import threading

str = None
port = '12345'
coord = [0,0,0,0,0,0]
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("localhost",12345))
mutex = threading.Lock()
max_axis_c = 0
max_axis=0
times = 0
str = client.recv(7)

def receivestr():
        global str
        global client
        str = client.recv(23)
        while(str):
                str = client.recv(23)

t1 = threading.Thread(target=receivestr)


point = np.array([2.5,1.0,1.0])
step=0.1
target=3*np.array([random(),random(),random()])
def IdleFunc():
        global point
        for i in range(3):
                if(fabs(point[i]-target[i])<=step):
                        target[i]=3*random()+0.2
        point+=0.1*(np.abs(target-point)/(target-point))
        drawFunc()
def reshape(w,h):
   glViewport(0,0, w,h)
   glMatrixMode (GL_PROJECTION)
   glLoadIdentity ()
   gluPerspective(60.0,w/h, 1.0, 20.0)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   gluLookAt (5.0, 5.0, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0)

def drawFunc():
        global coord
        global mutex
        global str
        mutex.acquire(1)
        if(len(str)==23):
            coord = str.split(',')
            mutex.release()
            coord = np.array(coord,dtype=int)
        b_axis = np.array(coord[0:2])
        g_axis = np.array(coord[2:4])
        r_axis = np.array(coord[4:6])

        c_axis=(b_axis+g_axis)/2
        b_axis_c = np.linalg.norm(b_axis - c_axis)
        g_axis_c = np.linalg.norm(g_axis - c_axis)
        r_axis_c = np.linalg.norm(r_axis - c_axis)
        # mod_b=np.linalg.norm(b_axis_c)
        # theta_bg = asin(b_axis_c[1]*1.0/mod_b)
        # x_mat = np.array([[cos(theta_bg),cos(theta_bg)],[-sin(theta_bg),sin(theta_bg)]])
        # r_axis_c2 = np.dot(r_axis_c,x_mat)
        # g_axis_c2=np.dot(g_axis_c,x_mat)
        # b_axis_c2=np.dot(b_axis_c,x_mat)
        # print(theta_bg)
        sum_axis = (b_axis+g_axis+r_axis)/3
        global times
        global max_axis
        if (times<=20):
            max_axis += b_axis_c+r_axis_c+g_axis_c
            times+=1
        else:
            global max_axis_c
            times = 0
            max_axis_c = max_axis/10
            max_axis=0
        print(max_axis_c)
        X=r_axis[0]*7.0/640
        Y=max_axis_c*7.0/400-4
        Z=7-r_axis[1]*7.0/480
        
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f (0.4, 0.8, 1.0)
        glLoadIdentity()
        gluLookAt(9.0,9.0,9.0,  0.0,0.0,0.0,  0.0,0.0,1.0)
        glBegin(GL_LINES)
        glVertex3f(0.0,0.0,0.0)
        glVertex3f(5.0,0.0,0.0)

        glVertex3f(0.0,0.0,0.0)
        glVertex3f(0.0,5.0,0.0)
        for i in range(41):
                glVertex3f(0.5*i-10,-10.0,0.0)
                glVertex3f(0.5*i-10,10.0,0.0)
        for i in range(41):
                glVertex3f(-10.0,0.5*i-10,0.0)
                glVertex3f(10.0,0.5*i-10,0.0)
        glVertex3f(0.0,0.0,0.0)
        glVertex3f(0.0,0.0,5.0)
        glColor3f(1.0,1.0,0.0)
        glEnd()

        glTranslatef(X,Y,Z)
        glutWireCube(2)
        # glutWireSphere(float(X),20,20)
        glRotatef(150,1.0,1.0,0.8)
        glutSolidCone(0.1,0.6,10,8)
        glutSwapBuffers()

def processNormalKeys(key,x,y):
    if key == GLUT_KEY_F1:
        print ('q')
        client.close()
        exit()
def processMouse(button,state,x,y):
    if(state == GLUT_DOWN):
        if(button == GLUT_LEFT_BUTTON):
            print('%d,%d' % (x,y))


def main():
        try:
                t1.start()
                glutInit()
                glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
                glutInitWindowSize(600, 600)
                glutCreateWindow("First")
                glutReshapeFunc(reshape)
                glutDisplayFunc(drawFunc)
                glutIdleFunc(IdleFunc)
                glutSpecialFunc(processNormalKeys)
                glutMouseFunc(processMouse)
                glEnable(GL_DEPTH_TEST)
                glDepthFunc(GL_LESS)
                print("InLoop")
                glutMainLoop()
        except Exception,e:
                print e

main()
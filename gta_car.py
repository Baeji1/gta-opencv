import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import pressKey, releaseKey, W, A, S, D

def maxValues(s):
    count = {}
    m = 0
    mm = 0
    try:
        for i in s:
            count[i] = 0    
        for i in s:
            z = count[i]
            z += 1
            count[i] = z
        m = 0
        mm = 0
        for i in count:
            if count[i] == max(count.values()):
                m = i
                break
        count.pop(m)
        for i in count:
            if count[i] == max(count.values()):
                mm = i
                break
    except:
        pass
    return m,mm

def slopes(a):
    s = []
##    print 'lines', a
    try:
        for i in a[0]:
            x = [i[0],i[2]]
            y = [600-i[1],600-i[3]]
            try:
                s.append(float(y[1]-y[0])/(x[1]-x[0]))
            except:
                s.append('inf')
        for i in range(len(s)):
            try:
                s[i] = float("{0:.2f}".format(s[i]))
            except:
                pass
    except:
        pass
    return s

def draw_lines(img,lines):
    try:
        for coord in lines[0]:
            cv2.line(img,(coord[0],coord[1]), (coord[2],coord[3]), [255,255,255],1)
    except:
        pass


def draw_lanes(img,lines):
##    print lines
    s = slopes(lines)
    m,mm = maxValues(s)
##    print 'slopes', m, mm
    try:
        for i in range(len(lines[0])):
            if s[i] == m or s[i] == mm:
##                print 'DRAWING'
                x = [lines[0][i][0],lines[0][i][2]]
                y = [lines[0][i][1],lines[0][i][3]]
                print x,y
                cv2.line(img,(x[0],y[0]),(x[1],y[1]),[0,255,0],3)
    except:
        pass
    return m,mm

def straight():
    pressKey(W)
    releaseKey(A)
    releaseKey(D)

def left():
    pressKey(A)
    releaseKey(D)
    releaseKey(A)

def right():
    pressKey(D)
    releaseKey(A)
    releaseKey(D)

def roi(img,vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vertices,255)
    masked_img = cv2.bitwise_and(img,mask)
    return masked_img

def process_img(original_screen):
    processed_img = cv2.cvtColor(original_screen, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1 = 200, threshold2 = 300)
    processed_img = cv2.GaussianBlur(processed_img,(5,5),0)
##    vertices = np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,500]])
    vertices = np.array([[0,500],[0,200],[300,130],[450,130],[800,200],[800,500]])
    processed_img = roi(processed_img, [vertices])
    lines = cv2.HoughLinesP(processed_img,1,np.pi/180,180,np.array([]),100,5)
##    draw_lines(processed_img,lines)
    m,mm = draw_lanes(original_screen,lines)
    return processed_img,m,mm

last_time = time.time()
##time.sleep(3)
pressKey(W)
while(True):
    screen = np.array(ImageGrab.grab(bbox=(0,40,800,640)))
    new_screen,m,mm = process_img(screen)
    print time.time()-last_time
    last_time = time.time()
    screen = cv2.cvtColor(screen,cv2.COLOR_BGR2RGB)
##    cv2.imshow('window', new_screen)
    cv2.imshow('lanes',screen)

    if m>0 and mm>0:
        right()
    elif m<0 and mm<0:
        left()
    else:
        straight()

##    cv2.imshow('window2', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25)  & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

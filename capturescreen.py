#! encoding=utf-8
# author      :max
# date        :2018/2/22
# description :yinyangshiwaigua based on image process



import time
import win32api
import win32gui
import win32con
import random
from ctypes import *



import cv2
import numpy as np
from PIL import Image
from PIL import ImageGrab
# 每抓取一次屏幕需要的时间约为1s,如果图像尺寸小一些效率就会高一些

global winsize  # the size of the whole window
winsize = {"length": 0, "width": 0}
global Rect  # the postion of the rectangle
Rect = ()

def clickLeftCur(x,y):
    """move the mouse"""
    windll.user32.SetCursorPos(int(x),int(y))
    """模拟鼠标左键单击，第一个参数表示先按下，然后放开，后面两个参数表示相当于上一次的鼠标偏移量"""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def mouse_absolute(x,y,x2,y2):
    SW=1920
    SH=1080
    windll.user32.SetCursorPos(x, y)    #鼠标移动到
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)    #左键按下
    time.sleep(0.2)
    mw = int(x2 * 65535 / SW)
    mh = int(y2 * 65535 / SH)
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE + win32con.MOUSEEVENTF_MOVE, mw, mh, 0, 0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)




def getWinHandle():
    appname = 'BlueStacks App Player'
    appclass = 'BS2CHINAUI'
    return win32gui.FindWindow(appclass, appname)


def getWindetail():
    """get the detail of the whole window"""
    global winsize
    global Rect
    hwnd = getWinHandle()
    Rect = win32gui.GetWindowRect(hwnd)
    winsize['length'] = abs(Rect[0] - Rect[2])
    winsize['width'] = abs(Rect[1] - Rect[3])


# 输入灰度图，返回hash
def getHash(image):
    avreage = np.mean(image)
    hash = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] > avreage:
                hash.append(1)
            else:
                hash.append(0)
    return hash

# 计算图片的汉明距离
def Hamming_distance(hash1, hash2):
    num = 0
    for index in range(len(hash1)):
        if hash1[index] != hash2[index]:
            num += 1
    return num


def classify_pHash(gray1, gray2):
    gray1 = cv2.resize(gray1, (32, 32))
    gray2 = cv2.resize(gray2, (32, 32))
    # 将灰度图转为浮点型，再进行dct变换
    dct1 = cv2.dct(np.float32(gray1))
    dct2 = cv2.dct(np.float32(gray2))
    # 取左上角的8*8，这些代表图片的最低频率
    # 这个操作等价于c++中利用opencv实现的掩码操作
    # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
    dct1_roi = dct1[0:8, 0:8]
    dct2_roi = dct2[0:8, 0:8]
    hash1 = getHash(dct1_roi)
    hash2 = getHash(dct2_roi)
    return Hamming_distance(hash1, hash2)

def oudistance(image1,image2):
    """计算两张图片插值并且判断是否为相同图片"""
    sum = 0
    size = image1.shape
    #直接计算两张图片的差值，并求和
    for i in range(size[0]-1):
        for j in range(size[1]-1):
            if image1[i,j]>image2[i,j]:
                sum = sum + image1[i,j]-image2[i,j]
            else:
                sum = sum + image2[i, j] - image1[i, j]

    return sum



def PIL2MAT_Resize(image):
    """将图片转换成mat类并且对图片尺寸进行重定义并进行灰度操作"""
    img = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, (640, 360))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def endCheck(winlib):
    """检测当前战斗是否已经结束，判断画面是否已经静止不动，
    """
    winiconsize=(331,166)#胜利图标设计
    size=winlib.shape
    timesum=0
    print "攻打中"
    global Rect
    while True:
        #每4秒刷新一次，判断画面是否已经结束，直接计算欧式距离
        startimg = ImageGrab.grab(bbox=Rect)
        startimg = cv2.cvtColor(np.asarray(startimg), cv2.COLOR_RGB2BGR)
        roiImg = startimg[740:740+size[0]-10,788:788+size[1]]
        roiImg = cv2.resize(roiImg,winiconsize)
        roiImg = cv2.cvtColor(roiImg, cv2.COLOR_BGR2GRAY)
        time.sleep(4)
        timesum=timesum+4
        if oudistance(winlib,roiImg) < 100000 :
            print '回合结束'
            return 0
        else:
            pass
        if timesum > 120:
            print '当前战斗出现误检测，退出重新刷新'
            return 1





def experenceGet():
    #刷怪
    getWindetail()

    #相关按钮的位置坐标
    space={'x':780,'y':750}
    buttonStart={'x':960,'y':520}
    buttonBack = {'x': 67, 'y': 95}
    buttonConform = {'x': 1164, 'y': 608}
    buttonSeek = {'x': 1420, 'y': 808}

    # 预加载boss和小怪的对比模型
    bosslib = cv2.imread('boss.jpg',0)
    monsterlib = cv2.imread('monster.jpg',0)
    winlib = cv2.imread('win.jpg',0)  #图片尺寸 331*166

    #开始选择
    clickLeftCur(buttonStart['x'], buttonStart['y'])
    time.sleep(3)
    clickLeftCur(buttonSeek['x'], buttonSeek['y'])


    while True:
        time.sleep(5)
        start=time.time()
        img = ImageGrab.grab(bbox=Rect)
        # # 将图像转换为opencv模式，并按比例缩小图片的尺寸
        image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        image = cv2.resize(image, (640, 360))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        # 使用霍夫变换检测图像中所有的攻击圆形

        circles1 = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1,
                                    5, param1=100, param2=30, minRadius=10, maxRadius=40)

        # 防止出现屏幕上没有小怪的情况
        try:
            circles = circles1[0, :, :]
        except:
            print '当前屏幕没有小怪'
            clickLeftCur(1920/2+100, 1080/2)
            continue




        monsterFlag=0 #标记检测到的圆形中是否存在小怪
        error = 0     #标记出错
        bossmark = 0  #标记是否是boss战

        # 获取圆形的矩形框坐标,并将图片截取出来
        for circle in circles:
            if circle[2]>17 and circle[2]<25:
                roiImg = image[int(circle[1] - circle[2]):int(circle[1] + circle[2]),
                         int(circle[0] - circle[2]):int(circle[0 ] + circle[2])]

                # 将截取的图片与图片库图片进行比较，判断是否为战斗目标，并判断小怪和首领
                roiImg = cv2.resize(roiImg, (40, 40))
                print circle  # 打印圆形
                #计算选中的区域与标准图片库图片的汉明距离
                ouboss = oudistance(roiImg,bosslib)
                oumonster = oudistance(roiImg,monsterlib)
                print ouboss,oumonster
                hashboss = classify_pHash(roiImg,bosslib)
                hashmonster=classify_pHash(roiImg,monsterlib)
                #计算两个汉明距离，只有当距离之和小于50时，认为是攻击目标，同时距离相等，按小怪处理
                #每次检测只对一个小怪进行攻击
                if hashboss + hashmonster < 50 and ouboss <100000 and oumonster < 100000:
                    monsterFlag = 1 #表示当前回合存在小怪
                    print hashboss,hashmonster
                    if  abs(oumonster-ouboss)<10000:
                        print '回合开始，攻击boss'
                        bossmark=1
                    else:
                        print '回合开始，攻击小怪'
                        bossmark=0

                    clickLeftCur(int(circle[0]) * 3, int(circle[1]) * 3)
                    end=time.time()
                    print end-start
                    time.sleep(3)
                    error=endCheck(winlib)
                    time.sleep(3)
                    clickLeftCur(space['x'], space['y'])
                    break
                else:
                    pass


            else:
                pass

        #判断所有的圆形中是否存在小怪
        if monsterFlag==1:
            pass
        else:
            print '当前屏幕没有小怪'
            clickLeftCur(1920/2+100, 1080/2)

        if bossmark==1  or error == 1:
            time.sleep(3)
            clickLeftCur(buttonBack['x'],buttonBack['y'])
            time.sleep(3)
            clickLeftCur(buttonConform['x'], buttonConform['y'])
            time.sleep(8)
            clickLeftCur(buttonStart['x'], buttonStart['y'])
            time.sleep(3)
            clickLeftCur(buttonSeek['x'], buttonSeek['y'])
        else:
            pass




experenceGet()


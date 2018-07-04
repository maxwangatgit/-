#!encoding=utf-8
# auther: 		maxwang
# date:   		2018/2/1
# description:   yinyangshigua


import time
import win32api
import win32gui
import random
from ctypes import *

import win32con



global winsize  # the size of the whole window
winsize = {"length": 0, "width": 0}
global Rect  # the postion of the rectangle
Rect = ()

global TIMES
TIMES=9

def clickLeftCur(x,y):
    """move the mouse"""
    windll.user32.SetCursorPos(int(x),int(y))
    """模拟鼠标左键单击，第一个参数表示先按下，然后放开，后面两个参数表示相当于上一次的鼠标偏移量"""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)






def getCurPos():
    """get the postion of the cursor """
    return win32gui.GetCursorPos()


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
    print hwnd









def clickButtonRefrash():
    global Rect
    global winsize

    # the first step is refresh the process :the button refrash
    # calculate the postion of button refarash
    buttonrefrashx = ((1600 - 290) / float(1600)) * winsize['length']+Rect[0]
    buttonrefrashy = ((61+617) / float(900)) * winsize['width']+Rect[1]
    #click refrash button
    clickLeftCur(buttonrefrashx, buttonrefrashy)
    time.sleep(2)
    #click sure button
    buttonSurex = ((1600 - 652) / float(1600)) * winsize['length']+Rect[0]
    buttonSurey = ((61+480) / float(900)) * winsize['width']+Rect[1]
    clickLeftCur(buttonSurex, buttonSurey)
    print "刷新成功"
    time.sleep(4)#等待刷新界面


def clickFight():
    global Rect
    global winsize
    global TIMES
    # 向右移动或向下移动的偏移量百分比
    deviationx=float(430)/1600
    deviationy=float(160)/900
    # 选中单个后点击突破按钮的偏移量
    buttonAttackDeviationx=float(100)/1600
    buttonAttackDeviationy=float(227)/900
    # 第一个突破的中心坐标
    startx=int((1600-1231)/float(1600)*winsize['length']+Rect[0])
    starty=int((134+61)/float(900)*winsize['width']+Rect[1])

    #打算突破顺序，防止被检测是挂
    fightorder=[1,2,3,4,5,6,7,8,9]
    random.shuffle(fightorder)
    print fightorder
    for i in range(0,9):

        #点击突破目标
        print '当前正在攻打结界',fightorder[i]
        if fightorder[i]%3 !=0: #如果是三的整数倍，就需要另外计算
            presentchoosex=startx + ((fightorder[i]%3)-1)*deviationx*winsize['length']
            presentchoosey = starty + fightorder[i] / 3 * deviationy * winsize['width']
        else:
            presentchoosex=startx +2*deviationx*winsize['length']
            presentchoosey=starty + (fightorder[i]/3-1)*deviationy*winsize['width']
        print presentchoosex,presentchoosey
        clickLeftCur(presentchoosex,presentchoosey)
        time.sleep(2)

        #点击进攻按钮
        print "开始攻打"
        clickLeftCur(presentchoosex + buttonAttackDeviationx*winsize['length']
                     , presentchoosey + buttonAttackDeviationy*winsize['width'] )
        #固定战斗时常
        time.sleep(120)

        #结束战斗点击空白,考虑物品领取，每突破三个额外奖励
        spacex=(1600-450)/float(1600)*winsize['length']+Rect[0]
        spacey = (700 + 61) / float(900) * winsize['width'] + Rect[1]
        clickLeftCur(spacex,spacey)
        time.sleep(3)
        clickLeftCur(spacex, spacey)
        time.sleep(3)
        clickLeftCur(spacex, spacey)
        time.sleep(3)
        clickLeftCur(spacex, spacey)
        time.sleep(3)
        print "当前回合结束"
        TIMES=TIMES-1
        print "剩余突破券",TIMES
        if TIMES==0:
            print "突破券已用完，攻打结束"
            exit(0)

def breakEnchantmen():
    """breakEnchantmen """
    global TIMES
    getWindetail()
    while TIMES!=0:
        #先刷新进度，后进行结界攻打
        clickButtonRefrash()
        clickFight()

if __name__=='__main__':
    breakEnchantmen()
    # while  True:
    #     time.sleep(0.5)
    #     print getCurPos()




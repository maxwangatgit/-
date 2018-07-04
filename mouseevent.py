#!encoding=utf-8
# auther: 		maxwang
# date:   		2018/2/4
# description:   结界突破外挂


import time
import win32api
import win32gui
import random
from ctypes import *

import win32con


def clickLeftCur(x,y):
    """move the mouse"""
    windll.user32.SetCursorPos(int(x),int(y))
    """模拟鼠标左键单击，第一个参数表示先按下，然后放开，后面两个参数表示相当于上一次的鼠标偏移量"""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |win32con.MOUSEEVENTF_LEFTUP , 0, 0)


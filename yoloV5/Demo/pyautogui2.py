import time
import pyautogui
import pynput
from pynput.mouse import Listener
from threading import Thread

# mouse = pynput.mouse.Controller()
# # lock_mode = False
# with pynput.mouse.Events() as events:
#     while True:
#         time.sleep(0.5)
#         it = next(events)
#         while it is not None and not isinstance(it, pynput.mouse.Events.Click): #鼠标移动  和 不是被点击 就迭代
#             it = next(events)
#             print("移动中")
#
#         while it is not None and isinstance(it, pynput.mouse.Events.Click): #and it.pressed  是被按下
#             it = next(events)
#             print("左键被按下")
#         print("程序")
#
#
# def on_move(x, y):
#     if x:
#         print('正在移动',x,y)
#     else:
#         print("停止移动")
#
# def move_Listener():
#     with Listener(on_move=on_move) as listener:
#         listener.join()
#
#
# Thread(target=move_Listener).start()

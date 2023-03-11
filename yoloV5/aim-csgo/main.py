import sys
sys.path.append('D:\Py_Project\yoloV5')
# import math
import time
import torch
# from grabscreen import grab_screen_mss
import numpy as np
from utils.general import non_max_suppression, scale_boxes, xyxy2xywh
from utils.augmentations import letterbox
import pynput
from pynput.mouse import Listener
# from mouse_controler import lock
from models.common import DetectMultiBackend
from threading import Thread
from SendInput import mouse_xy,mouse_xy_d
from utils.torch_utils import smart_inference_mode
from mss import mss
import cv2
# from PositionalPID import PID  #位置式
from IncrementalPID import PID   #增量式
# from simple_pid import PID

mouse = pynput.mouse.Controller()
lock_mode = False  #程序开启
mouse_move = False  #鼠标移动情况

conf_thres = 0.7  # 置信度
iou_thres = 0.05  # 交并比
# 截图相关参数-------------
x, y = 2560, 1440  # 截图范围size
x, y = 2880, 1800  # 截图范围size
x_c, y_c = 320, 320  # 截图大小
x_c, y_c = 640, 640  # 截图大小
k = x_c/2            #计算移动距离时用 减去截图大小的一半
move_P = 1.668
x1, y1, x2, y2 = int(x / 2 - x_c / 2), int(y / 2 - x_c / 2), int(x / 2 + x_c / 2), int(y / 2 + x_c / 2)
#kP=0.5, kI=0.09, kD=0.1  #kP=0.81, kI=0.22, kD=0.19  #kP=0.2,kI=0.03,kD=0.28 #kP=0.6,kI=0.03, kD=0.1
#kp = 0.9; ki = 0.088; kd = 0.114
#kP = 0.5 kI = 0.113 kD = 0.102
#kp = 0.7; ki = 0.255; kd = 0.2
#P=0.81, I=0.22, D=0.19
#P = 0.774 I = 0.428 D = 0.2

#引用的pid
#kp = 0.8; ki = 0.026; kd = 0.01
#kp = 0.453; ki = 0.03; kd = 0.001
# kp = 0.612; ki = 0.529; kd = 0
# pidx = PID(kp, ki, kd, setpoint=0, sample_time=0.001, output_limits=(-k, k))
# pidy = PID(kp, ki, kd, setpoint=0, sample_time=0.001, output_limits=(-k, k))

#kp = 0.865; ki = 0.059; kd = 0.108 还行
#kp = 0.73; ki = 0.263; kd = 0  基本够用
#kp = 0.75; ki = 0.308; kd = 0  可以
#kp = 0.75; ki = 0.318; kd = 0.058
#自己写的pid
kp = 0.75; ki = 0.318; kd = 0.058
add = True  #调参（PID）
pidx = PID(P=kp, I=ki, D=kd, max_m=x_c/2)
pidy = PID(P=kp, I=ki, D=kd, max_m=x_c/2)

def open_click(x, y, button, pressed):
    global lock_mode,pidx,pidy
    if pressed and button == pynput.mouse.Button.right:
        lock_mode = not lock_mode
        print('lock mode', 'on' if lock_mode else 'off')
        #开关一次后初始化pid
        if lock_mode == True:
            pidx = PID(P=kp, I=ki, D=kd, max_m=x_c / 2)
            pidy = PID(P=kp, I=ki, D=kd, max_m=x_c / 2)
            # pidx = PID(kp, ki, kd, setpoint=0, sample_time=0.001, output_limits=(-k, k))
            # pidy = PID(kp, ki, kd, setpoint=0, sample_time=0.001, output_limits=(-k, k))

            print("PID 初始化")
    # elif not pressed and button == pynput.mouse.Button.middle:
    #     lock_mode = False
    #     print("关闭")

def open_listener():
    with Listener(on_click=open_click) as listener:
        listener.join()

"""
如果鼠标移动，判断程序是否开启，and 鼠标移动默认是否为False： 是：改变mouse_move值为T，程序暂停0.001秒
"""
def on_move(x, y):
    global mouse_move, lock_mode
    if lock_mode == True and mouse_move == False:
        mouse_move = True

def move_Listener():
    with Listener(on_move=on_move) as listener:
            listener.join()


#PID调参函数  P   I   K
def Key_press(key):
    global kp,ki,kd,add,pidx,pidy
    try:
        if key.char == "=":
            print("当前为 + ")
            add = True
        if key.char == "-":
            print("当前为 -")
            add = False
        if add == True:
            if key.char == 'p':
                kp = round(kp + 0.001,4)
                print("P + 0.01, 当前 P ：",kp)

                pidx = PID(P=kp, I=ki, D=kd)
                pidy = PID(P=kp, I=ki, D=kd)
            elif key.char == "i":
                ki = round(ki + 0.001,4)
                print("i + 0.01, 当前 i ：", ki)
                pidx = PID(P=kp, I=ki, D=kd)
                pidy = PID(P=kp, I=ki, D=kd)
            elif key.char == 'k':
                kd = round(kd + 0.001,4)
                print("d + 0.01, 当前 d ：", kd)
                pidx = PID(P=kp, I=ki, D=kd)
                pidy = PID(P=kp, I=ki, D=kd)
        if add == False:
            if key.char == 'p':
                kp = round(kp - 0.001,4)
                print("P - 0.01, 当前 P ：",kp)
                pidx = PID(P=kp, I=ki, D=kd)
                pidy = PID(P=kp, I=ki, D=kd)
            elif key.char == "i":
                ki = round(ki - 0.001,4)
                print("i - 0.01, 当前 i ：", ki)
                pidx = PID(P=kp, I=ki, D=kd)
                pidy = PID(P=kp, I=ki, D=kd)
            elif key.char == 'k':
                kd = round(kd - 0.001,4)
                print("d - 0.01, 当前 d ：", kd)
                pidx = PID(P=kp, I=ki, D=kd)
                pidy = PID(P=kp, I=ki, D=kd)
    except:
        pass

def on_press():
    with pynput.keyboard.Listener(on_press=Key_press) as listener:
        listener.join()




@smart_inference_mode()
def run():


    # re_x, re_y = 640, 640  # 显示size
    # ------------------------------
    # PID係數可調整
    # PID(P, I, D)
    # P: 加快系統反映。輸出值較快，但越大越不穩定
    # I: 積分。用於穩定誤差
    # D: 微分。提高系統的動態性能
    # 以下為個人使用參數可供參考
    # pidx = PID(P=p, I=i, D=d)   #P=0.5, I=0.09, D=0.1  #P=0.81, I=0.22, D=0.19  #P=0.2,I=0.03,D=0.28 #P=0.6,I=0.03, D=0.1
    # pidy = PID(P=p, I=i, D=d) #P=0.6, I=0.1, D=0.4
    # ----------------------------------------------

    ## 加载模型
    # weights = r'E:\Pycharm\Python_Projects\yolov5\aim-csgo\model\best_csgo.engine'
    weights = r'D:\Py_Project\yoloV5\aim-csgo\model\best_csgo.pt'
    # weights = r"E:\Pycharm\Python_Projects\yolov5\csgo2w8.engine"
    # weights=r'E:\Pycharm\Python_Projects\yolov5\aim-csgo\model\csgo_28600p_20ep_5n_5.0_4lab.wts'
    imgsz = 640
    device = torch.device('cpu')
    print("device ", device)

    # model = DetectMultiBackend(weights, device=device, dnn=False, data=False, fp16=True)
    model = DetectMultiBackend(weights, device=device, dnn=False, data=False, fp16=False)
    stride = model.stride
    # model.warmup(imgsz=(1 if pt or model.triton else 1, 3, *imgsz))  # warmup
    # -----------------

    global lock_mode,mouse_move
    global pidx, pidy
    MSS = mss()        #生成截图类
    while True:

        t0 = time.time()
        if lock_mode == False: #判断程序是否开启
            time.sleep(0.1)
            continue
        else:
            if mouse_move == True:  #判断鼠标是否在移动
                mouse_move = False
                time.sleep(0.001)
                continue
        # print("判断用时:",time.time()-t0)

        # img0 = grab_screen_mss(monitor=(x1, y1, x2, y2))  # 截图  region范围  截图用时 20ms 以内
        img0 = MSS.grab((x1, y1, x2, y2))
        img0 = np.array(img0)  # 转换成numpy数组
        img0 = cv2.cvtColor(img0, cv2.COLOR_BGRA2BGR)

        # t1 = time.time()
        # img0 = cv2.resize(img0,(re_x, re_y))
        im = letterbox(img0, imgsz, stride=stride)[0]
        im = im.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        im = np.ascontiguousarray(im)  # contiguous
        im = torch.from_numpy(im).to(model.device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        # t1 = time.time()
        pred = model(im, augment=False, visualize=False)
        """更改了non_max_suppression一点内容"""
        pred = non_max_suppression(pred, conf_thres=conf_thres, iou_thres=iou_thres, agnostic=False,
                                   im=im.shape[2:], img0=img0.shape, k=k)
        # print("推理用时", time.time() - t1)

        if len(pred):
            tag = pred[0]
            # print("tag:" , tag)
            if tag == 0 or tag == 2:
                #PID移动-------------start
                x = int(round(pidx.SetStepSignal((pred[1] - k) * move_P)))
                y = int(round(pidy.SetStepSignal((pred[2] - k) * move_P)))  #int((target_info[2] - k) * move_P)
                mouse_xy(x, y)
                # mouse_xy_d(x, y)

                time.sleep(0.001)
                # print("输入x:", (pred[1] - k) * move_P, "输入y：", (pred[2] - k) * move_P)
                # print("实际移动x:", x, "y:", y)
                #PID移动-------------end

                # # PID移动-------------start  引用
                # # print("输入x:", (pred[1] - k) * move_P,"输入y：", (pred[2] - k) * move_P)
                # # xx = -pidx((pred[1] - k) * move_P)
                # # yy = -pidy((pred[2] - k) * move_P)
                # x = round(-pidx((pred[1] - k) * move_P))
                # y = round(-pidy((pred[2] - k) * move_P))  # int((target_info[2] - k) * move_P)
                # # print("输出x:", xx, "y:", yy)
                # # print("实际移动x:", x, "y:", y)
                # mouse_xy(x, y)
                # # PID移动-------------end

                # #正常移动--------------start
                # mouse_xy(int(((target_info[1] - k) * move_P)), int((target_info[2] - k) * move_P))
                # time.sleep(0.001)
                # #正常移动----------end
                # print("移动数据x:",int((pred[1] - k) * move_P),"y:",int((pred[2] - k) * move_P))
            elif tag == 1 or tag == 3:
                #PID移动-------------start
                x = int(round(pidx.SetStepSignal((pred[1] - k) * move_P)))
                y = int(round(pidy.SetStepSignal((pred[2] - 4/10 * pred[4] - k) * move_P))) #int((target_info[2] - 4/10 * target_info[4] - k) * move_P)
                mouse_xy(x, y)
                # mouse_xy_d(x, y)
                time.sleep(0.001)
                # print("输入x:", (pred[1] - k) * move_P, "输入y：", (pred[2] - 4 / 10 * pred[4] - k) * move_P)
                # print("实际移动x:", x, "y:", y)
                # PID移动-------------end

                # # PID移动-------------start  引用
                # # print("输入x:", (pred[1] - k) * move_P,"输入y：", (pred[2] - 4 / 10 * pred[4] - k) * move_P)
                # # xx = -pidx((pred[1] - k) * move_P)
                # # yy = -pidy((pred[2] - 4 / 10 * pred[
                # #     4] - k) * move_P)
                # x = round(-pidx((pred[1] - k) * move_P))
                # y = round(-pidy((pred[2] - 4 / 10 * pred[
                #     4] - k) * move_P))  # int((target_info[2] - 4/10 * target_info[4] - k) * move_P)
                # # print("输出x:", xx, "y:", yy)
                # # print("实际移动x:", x, "y:", y)
                # mouse_xy(x, y)
                # # PID移动-------------end

                # # 正常移动--------------start
                # mouse_xy(int(((target_info[1] - k) * move_P)), int((target_info[2] - 4/10 * target_info[4] - k) * move_P))
                # time.sleep(0.001)
                # # 正常移动----------end
                # print("移动数据x:", int((pred[2] - 4/10 * pred[4] - k) * move_P), "y:", int((pred[2] - k) * move_P))
        #     # time.sleep(1)
        #     # time.sleep(0.001)
        #     print("当前 PID值 P =", kp, "I =", ki, "D =",kd , "pidx.LastError:" ,pidx.LastError ,"pidx.Error:",pidx.Error,"pidx.LastLastError",pidx.LastLastError)
            # print("当前 PID值 P =", kp, "I =", ki, "D =", kd)

            print("程序用时:", time.time()-t0, "FPS:", round(1/(time.time()-t0)))

                    # print("height" , target_info[4],"\n")w

                    # time.sleep(0.01)
        #         for i, det in enumerate(aims):  # 可视化框
        #             _, x_center, y_center, width, hight = det
        #             x_center, width = re_x * float(x_center), re_x * float(width)
        #             y_center, hight = re_y * float(y_center), re_y * float(hight)
        #             top_left = (int(x_center - width / 2), int(y_center - hight / 2))
        #             bottom_right = (int(x_center + width / 2), int(y_center + hight / 2))
        #             color = (0, 255, 0) # RGB
        #             cv2.rectangle(img0, top_left, bottom_right, color, thickness=3)
        #
        #
        #
        # #可视化框
        # cv2.namedWindow("csgo-detect",cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("csgo-detect", re_x, re_y)
        # cv2.imshow("csgo-detect",img0)
        # hwnd = win32gui.FindWindow(None , 'csgo-detect')
        # CVRECT = cv2.getWindowImageRect('csgo-detect')
        # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     cv2.destroyAllWindows()
        #     break


if __name__ == "__main__":
    mouse_listener = Thread(target=open_listener).start()
    move_Listener = Thread(target=move_Listener).start()
    # add_PID = Thread(target=on_press).start()
    run()


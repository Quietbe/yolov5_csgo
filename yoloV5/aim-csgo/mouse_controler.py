# import pydirectinput
# import time
# import pyautogui as pg
from SendInput import mouse_xy


x_b = 1.64
y_b = 1.67

def lock(aims, x, y, pidx='', pidy=''):
    # mouse_pos_x, mouse_pos_y = mouse.position  # 获得当前鼠标位子
    mouse_pos_x, mouse_pos_y = x / 2, y / 2
    dist_list = []
    for det in aims:
        _, x_c, y_c, _, _ = det
        dist = (x * float(x_c) - mouse_pos_x) ** 2 + (y * float(y_c) - mouse_pos_y) ** 2  #计算距离信息
        dist_list.append(dist)

    det = aims[dist_list.index(min(dist_list))]   # 获得最近的对象det

    tag, x_center, y_center, width, height = det  #计算中心位置
    tag = int(tag)
    x_center, width = x * float(x_center), x * float(width)
    y_center, height = y * float(y_center), y * float(height)
    # xx = int(x_center - x/2)
    # yy = int(y_center - y/2)
    # if xx**2+yy**2 > 10:
    if tag == 0 or tag == 2:
        # x 1.638  y 1.67
        mouse_xy(round(-pidx(int((x_center - x/2) * x_b))), round(int((y_center - y/2) * y_b ))) #pid
        # mouse_xy(int((x_center - x / 2) * x_b), int((y_center - y / 2) * y_b))
        # time.sleep(0.5)
        # pg.click()
        # moveR(int((x_center - x / 2) * x_b), int((y_center - y / 2) * y_b))
        # print("移动了一次x ",x_center - x/2, 'y', int(y_center - y/2))

    elif tag == 1 or tag == 3:
        # mouse_xy(round(-pidx(int((x_center - x/2) * x_b ))), round(int((y_center - 4 / 10 * height -y/2) * y_b )))  #pid
        mouse_xy(int((x_center - x / 2) * x_b), int((y_center - 4 / 10 * height - y / 2) * y_b))
        # time.sleep(0.5)
        # pg.click()

        # moveR(int((x_center - x / 2) * x_b), int((y_center - 1 / 6 * height - y / 2) * y_b))
        # print("移动了一次x ", int(x_center - x/2), 'y', int(y_center - 1 / 6 * height -y/2))


# import csv
# f = csv.reader(open("dd_csvs/ak47.csv",encoding="utf-8"))
# list = []
#
# for i in f:
#     list.append(i)
# print(list)

import csv
from threading import Thread
import pynput
import time
from SendInput import mouse_xy

def recoil_control():
    f = csv.reader(open("dd_csvs/ak47.csv", encoding="utf-8"))
    ak_recoil = []
    for i in f:
        ak_recoil.append(i)
    ak_recoil[0][0] = '0'
    ak_recoil = [[float(i) for i in x] for x in ak_recoil]
    print(ak_recoil)
    k = -1
    mouse = pynput.mouse.Controller()
    flag = 0
    recoil_mode = False  # mouse.button.x1
    with pynput.mouse.Events() as events:
        for event in events:
            if isinstance(event,pynput.mouse.Events.Click):
                if event.button == event.button.left:
                    if event.pressed:
                        flag = 1
                    else:
                        flag = 0
                if event.button == event.button.middle and event.pressed:
                    recoil_mode = not recoil_mode
                    print("recoil mode", "on" if recoil_mode else "off")
            if flag and recoil_mode:
                i = 0
                a = next(events)
                while True:
                    # print(ak_recoil[i])
                    t0 = time.time()
                    mouse_xy(round(ak_recoil[i][0] * k), round(ak_recoil[i][1] * k))
                    print(i,"移动中x:", -ak_recoil[i][0], "y:", -ak_recoil[i][1], "time:", ak_recoil[i][2])
                    i += 1
                    if i == 30:
                        break
                    if a is not None and isinstance(a, pynput.mouse.Events.Click) and a.button == a.button.left \
                            and not a.pressed:
                        break
                    a = next(events)
                    while a is not None and not isinstance(a, pynput.mouse.Events.Click):
                        a = next(events)
                    tt = (ak_recoil[i-1][2] / 1000)-(time.time()-t0)
                    try:
                        time.sleep(tt)
                    except:pass
                    print("sleep:", tt)
                flag = 0

if __name__ == '__main__':

    # t = Thread(target=recoil_control)
    # t.start()
    # t.join()

    n = 55
    k = n //10
    print(k)
from PositionalPID import PID

# pidx = PID(P=0.2, I=0.03, D=0.28)
# #P=0.5, I=0.09, D=0.1  7
# #P=0.2, I=0.03, D=0.28   2
# #
# x = 300
# n = 0
# PIDOutput = 0
#
# while True:
#     n += 1
#     x = int(x - PIDOutput)
#     print("传入参数:", x)
#     PIDOutput = int(pidx.SetStepSignal(x))
#     # PIDOutput = int(pidx.PIDOutput)
#     print("移动参数", PIDOutput)
#     SystemOutput = pidx.SystemOutput
#     LastSystemOutput = pidx.LastSystemOutput
#     PIDErrAdd = pidx.PIDErrAdd
#     LastError = pidx.LastError
#     print(n, ": PIDOutput:", PIDOutput, "PIDErrAdd:", PIDErrAdd, "LastError", LastError, "SystemOutput:", SystemOutput,
#           "LastSystemOutput:", LastSystemOutput)
#     if PIDOutput == 0:break
#     if n > 100:break

#------------------------------------------------------------------------------------------------------



#PID 增量式
from IncrementalPID import PID

pidx = PID(P=0.8, I=0.1, D=0.1)
#P=0.5, I=0.09, D=0.1  7
#P=0.2, I=0.03, D=0.28   2
#
x = 300
n = 0
PIDOutput = 0

while True:
    n += 1
    x = int(x - PIDOutput)
    # print("传入参数:", x)
    PIDOutput = int(pidx.SetStepSignal(x))
    # PIDOutput = int(pidx.PIDOutput)
    # print("移动参数", PIDOutput)

    SystemOutput = pidx.SystemOutput
    LastSystemOutput = pidx.LastSystemOutput
    LastLastError = pidx.LastError
    LastError = pidx.Error
    print(n, ": PIDOutput:", PIDOutput,"Error:",pidx.Error, "LastLastError:", LastLastError, "LastError", LastError, "SystemOutput:", SystemOutput,
          "LastSystemOutput:", LastSystemOutput)
    if PIDOutput == 0:break
    # if n > 3:pidx(0)
    if n > 100:break


# #键盘监听Demo
# p = 0.8; i = 0.01; k = 0
# add = True
# import pynput
# from threading import Thread
# def Key_press(key):
#     global p,i,k,add
#     try:
#         if key.char == "=":
#             print("当前为 + ")
#             add = True
#         if key.char == "-":
#             print("当前为 -")
#             add = False
#         if add == True:
#             if key.char == 'p':
#                 p = round(p + 0.01,3)
#                 print("P + 0.01, 当前 P ：",p)
#             elif key.char == "i":
#                 i = round(i + 0.01,3)
#                 print("i + 0.01, 当前 i ：", i)
#             elif key.char == 'k':
#                 k = round(k + 0.01,3)
#                 print("d + 0.01, 当前 d ：", k)
#         if add == False:
#             if key.char == 'p':
#                 p = round(p - 0.01,3)
#                 print("P - 0.01, 当前 P ：",p)
#             elif key.char == "i":
#                 i = round(i - 0.01,3)
#                 print("i - 0.01, 当前 i ：", i)
#             elif key.char == 'k':
#                 k = round(k - 0.01,3)
#                 print("d - 0.01, 当前 d ：", k)
#     except:
#         pass
#
#
#
# def on_press():
#     with pynput.keyboard.Listener(on_press=Key_press) as listener:
#         listener.join()
#
# Thread(target=on_press).start()







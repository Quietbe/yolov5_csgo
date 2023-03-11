#位置式PID系统
class PositionalPID:
    def __init__(self, P: float, I: float, D: float):
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.PIDOutput = 0.0  # PID控制器输出
        self.SystemOutput = 0.0  # 系统输出值
        self.LastSystemOutput = 0.0  # 系统的上一次输出

        self.PIDErrAdd = 0.0
        self.ResultValueBack = 0.0
        self.Error = 0.0
        self.LastError = 0.0


    def SetStepSignal(self, StepSignal):
        self.Error = StepSignal - self.SystemOutput

        KpWork  = self.Kp * self.Error
        KiWork = self.Ki* self.PIDErrAdd
        KdWork = self.Kd * (self.Error - self.LastError)
        self.PIDOutput = KpWork + KiWork + KdWork
        self.PIDErrAdd += self.Error
        self.LastError = self.Error
        return self.PIDOutput
        # 以一阶惯性环节为例子演示控制效果

    def SetInertiaTime(self, IntertiaTime, SampleTime):
        self.SystemOutput = (IntertiaTime * self.LastSystemOutput + SampleTime * self.PIDOutput) / (
                    SampleTime + IntertiaTime)
        self.LastSystemOutput = self.SystemOutput


def PID(P = float, I = float, D = float):
    Positional = PositionalPID(P=P, I=I ,D=D)
    return Positional




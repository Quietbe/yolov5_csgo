#增量式PID系统
class IncrementalPID:
    def __init__(self, P:float ,I:float ,D:float ,max_m:float):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        self.max_m = max_m

        self.PIDOutput =0.0         #PID控制器输出
        self.SystemOutput = 0.0     #系统输出值
        self.LastSystemOutput = 0.0 #系统的上一次输出

        self.Error = 0.0
        self.LastError = 0.0
        self.LastLastError = 0.0

    #设置PID控制器参数
    def SetStepSignal(self,StepSignal):
        self.Error = StepSignal - self.SystemOutput
        #计算增量
        IncrementalValue = self.Kp*(self.Error - self.LastError)\
            + self.Ki * self.Error +self.Kd *(self.Error -2*self.LastError +self.LastLastError)
        #计算输出
        self.PIDOutput += IncrementalValue

        # if self.PIDOutput > self.max_m:self.PIDOutput=self.max_m
        # if self.PIDOutput < -self.max_m:self.PIDOutput=-self.max_m

        self.LastLastError = self.LastError
        self.LastError = self.Error
        return self.PIDOutput

    #以一阶惯性环节为例子演示控制效果
    def SetInertiaTime(self,IntertiaTime,SampleTime):
        self.SystemOutput = (IntertiaTime*self.LastSystemOutput + SampleTime *self.PIDOutput)/(SampleTime + IntertiaTime)
        self.LastSystemOutput = self.SystemOutput

def PID(P:float, I:float, D:float,max_m = 320):
    Incremental = IncrementalPID(P=P, I=I,D=D, max_m=max_m)
    return Incremental
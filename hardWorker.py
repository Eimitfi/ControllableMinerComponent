from gc import collect
from multiprocessing.connection import wait
from marshal import loads
from types import FunctionType
from ctypes import CDLL, c_uint32,c_uint64, RTLD_GLOBAL
#add ps util for resources usage, cpu affinity and cpu niceness

class HardWorker:
#funny story, the placeholder one
    def sendnonce(self,placeholder):
        self.monitor.send(self.nonce[:])
    def sendhigherlimit(self,placeholder):
        self.monitor.send(self.higherLimit[:])
    def sendlowerlimit(self,placeholder):
        self.monitor.send(self.lowerLimit[:])
    def sendtarget(self,placeholder):
        self.monitor.send(self.target[:])
    def sendnetheader(self,placeholder):
        self.monitor.send(self.netheader[:])
    def sendsecondaryname(self,placeholder):
        self.monitor.send(self.secondary.__name__)
    def sendprimaryname(self,placeholder):
        self.monitor.send(self.primary.__name__)
    def sendsequentialexecuting(self,placeholder):
        self.monitor.send(self.executing.__name__)
    def sendautostart(self,placeholder):
        self.monitor.send(self.autostart)

    def __init__(self):
        self.secondary = lambda arg1 : 0
        self.secondary.__name__ = 'donothing'
        self.secondaryinput = lambda arg1: 0

        self.higherLimit:int = [2 ** 32]
        self.lowerLimit:int = [-1]

        self.nonce = (c_uint64 * 1)()
        self.target = (c_uint32 * 8)()
        self.netheader = (c_uint32 * 19)()

        self.nonce[:] = self.lowerLimit[:]
        
        self.garlic = CDLL('./cLib/isValid.so',mode=RTLD_GLOBAL).isValid
        self.primary = lambda self: self.garlic(self.nonce,self.target,self.netheader)
        self.primary.__name__ = "garlicoin step"

        self.stopprimary = lambda self: self.nonce[:] == self.higherLimit[:]
        self.isprimaryinput = lambda self :  type(self.inp) == type([]) and (len(self.inp) == 19 or len(self.inp) == 8) and type(self.inp[0]) == type(1)
        self.getprimarysolution = lambda self: self.nonce[:]

        self.autostart = True

    def primaryinput(self,placeholder):
        if len(self.inp) == 19:
            self.netheader[:] = self.inp[:]
            if self.autostart:
                self.execute = self.primary
                self.nonce[:] = self.lowerLimit[:]
        if len(self.inp) == 8:
            self.target[:] = self.inp[:]

    def autoclean(self, placeholder):
        del self.target
        self.listen.remove(self.input)
        self.input.close()
        del self.netheader
        del self.myprimary
        del self.primary
        collect()

    def launch(self,InputFunction,OutputFunction,Monitor,Control):
        self.output = OutputFunction
        self.input = InputFunction
        self.monitor = Monitor
        self.control = Control
        
        self.listen = [self.control,self.input]

        self.execute = self.secondary

        while True:
            if self.execute == self.primary and self.stopprimary(self):
                self.execute = self.secondary
            if self.execute(self) == 1:
                try:
                    self.output.send(self.getprimarysolution(self))
                except ValueError as closed:
                    self.autoclean(self)

            self.ready_read = wait(self.listen,0)

            if len(self.ready_read) > 0:
                if self.control in self.ready_read:
                    try:
                        FunctionType(loads(self.control.recv()), {}, "")(self)
                    except Exception as e:
                        self.monitor.send(e)
                if self.input in self.ready_read:
                    self.inp = self.input.recv()
                    if self.isprimaryinput(self):
                        self.primaryinput(self)
                    else:
                        self.secondaryinput(self)

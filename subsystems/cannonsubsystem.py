from commands2 import SubsystemBase
from ctre import WPI_VictorSPX
from wpilib import Solenoid
import wpilib
from wpilib import AnalogInput
import constants

def map(pressureinput: float, voltmin: float, voltmax: float, pressuremin: float, pressuremax: float) -> None:
    return (pressureinput - pressuremin) * ((voltmax - voltmin) / (pressuremax - pressuremin)) + voltmin

class CannonSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.launchSolonoid = WPI_VictorSPX(constants.kCannonLaunchVictorDeviceID)
        self.fillSolonoid = Solenoid(constants.kPCMCannonCanID, constants.kCannonFillPCMID)
        self.pressure = AnalogInput(constants.kCannonPressureAnalogInput)

        self.fillSolonoid.set(False)
        self.launchSolonoid.set(0.0)

    def close(self) -> None:
        """close all the solonoids"""
        self.fillSolonoid.set(False)
        self.launchSolonoid.set(0.0)
        print(self.map(self.pressure.getVoltage(), constants.kVoltageOutMin,  constants.kVoltageOutMax, constants.kPressureInMin, constants.kPressureInMax))
        # print("CLOSING")

    def fill(self) -> None:
        """begins filling staging tank"""
        # self.launchSolonoid.set(
        #     Relay.Value.kOff
        # )  #ensure air doesnt just flow out the end without being stored
        self.launchSolonoid.set(0.0)
        self.fillSolonoid.set(True)
        print(self.fillSolonoid.get())
        print("FILLING")

    def launch(self) -> None:
        self.fillSolonoid.set(False)
        self.launchSolonoid.set(1.0)
        print(self.launchSolonoid.get())

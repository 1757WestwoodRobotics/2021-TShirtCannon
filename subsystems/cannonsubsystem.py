from enum import Enum, auto
from commands2 import SubsystemBase
from ctre import WPI_VictorSPX
from wpilib import Solenoid, PneumaticsModuleType, AnalogInput, SmartDashboard
import constants


def map(
    pressureinput: float,
    voltmin: float,
    voltmax: float,
    pressuremin: float,
    pressuremax: float,
) -> None:
    return (pressureinput - pressuremin) * (
        (voltmax - voltmin) / (pressuremax - pressuremin)
    ) + voltmin


class CannonSubsystem(SubsystemBase):
    class State(Enum):
        Closed = 0
        Filling = 1
        Launching = 2

    def periodic(self) -> None:
        SmartDashboard.putNumber(constants.kCannonStateKey, self.state.value)
        SmartDashboard.putNumber(constants.kPressureKey, self.getPressure())

    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.launchSolonoid = WPI_VictorSPX(constants.kCannonLaunchVictorDeviceID)
        self.fillSolonoid = Solenoid(
            constants.kPCMCannonCanID,
            PneumaticsModuleType.CTREPCM,
            constants.kCannonFillPCMID,
        )
        self.pressure = AnalogInput(constants.kCannonPressureAnalogInput)

        self.fillSolonoid.set(False)
        self.launchSolonoid.set(0.0)
        self.state = CannonSubsystem.State.Closed

    def getPressure(self) -> float:
        return map(
            self.pressure.getVoltage(),
            constants.kVoltageOutMin,
            constants.kVoltageOutMax,
            constants.kPressureInMin,
            constants.kPressureInMax,
        )

    def close(self) -> None:
        """close all the solonoids"""
        self.fillSolonoid.set(False)
        self.launchSolonoid.set(0.0)
        self.state = CannonSubsystem.State.Closed
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
        self.state = CannonSubsystem.State.Filling

    def launch(self) -> None:
        self.fillSolonoid.set(False)
        self.launchSolonoid.set(1.0)
        print(self.launchSolonoid.get())
        self.state = CannonSubsystem.State.Launching

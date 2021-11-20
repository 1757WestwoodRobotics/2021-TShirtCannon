from commands2 import SubsystemBase
from wpilib import Relay
import wpilib
import constants


class CannonSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.launchSolonoid = Relay(constants.kCannonLaunchSpikePWMID)
        self.fillSolonoid = Relay(constants.kCannonFillSpikePWMID)

        self.fillSolonoid.set(Relay.Value.kOff)
        self.launchSolonoid.set(Relay.Value.kOn)

    def close(self) -> None:
        """close all the solonoids"""
        self.fillSolonoid.set(Relay.Value.kOff)
        self.launchSolonoid.set(Relay.Value.kOn)
        # print("CLOSING")

    def fill(self) -> None:
        """begins filling staging tank"""
        # self.launchSolonoid.set(
        #     False
        # )  #ensure air doesnt just flow out the end without being stored
        self.fillSolonoid.set(Relay.Value.kOff if self.fillSolonoid.get() ==
                              Relay.Value.kOn else Relay.Value.kOn)
        print(self.fillSolonoid.get())
        print("FILLING")

    def launch(self) -> None:
        self.launchSolonoid.set(Relay.Value.kOff if self.launchSolonoid.get(
        ) == Relay.Value.kOn else Relay.Value.kOn)
        print(self.launchSolonoid.get())

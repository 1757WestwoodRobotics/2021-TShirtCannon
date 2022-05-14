from commands2 import CommandBase
from subsystems.lightsubsystem import LightSubsystem


class PulseLight(CommandBase):
    def __init__(
        self, light: LightSubsystem, pulseInterval: int, squareOutput: bool
    ) -> None:
        CommandBase.__init__(self)
        self.light = light
        self.pulseInterval = pulseInterval  # interval between each pulse

        self.setBrightness = lambda x: self.light.light.set(
            x**x if squareOutput else x
        )  # yay inline functions

        self.rising = True
        self.setName(__class__.__name__)

    def execute(self) -> None:
        self.setBrightness(
            bright := (  # set and reture for future use
                self.light.light.get()
                + (self.rising * 2 - 1)
                * (self.pulseInterval / 40)  # convert bool (0 or 1) to range of -1,1
            )
        )  # 40 because 1 pulse = 1 up and 1 down

        if bright <= 0 or bright >= 1:
            self.rising = not self.rising
        # print("Starting")

    def end(self, interrupted: bool) -> None:
        self.light.light.set(0.0)  # turn off when done
        # print("ending")

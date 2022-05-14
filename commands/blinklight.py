from subsystems.lightsubsystem import LightSubsystem
from commands2 import CommandBase


class BlinkLight(CommandBase):
    def __init__(self, light: LightSubsystem, amount: int, interval: int) -> None:
        CommandBase.__init__(self)
        self.repeatAmount = amount
        self.light = light
        self.interval = interval

        self.timer = 0  # track ms since start

        self.setName(__class__.__name__)
        self.addRequirements([self.light])

        self.on = False

    def execute(self) -> None:
        # ASSUME 20MS BETWEEN EACH ITERATION OF BEING CALLED
        # !!! DO NOT CHANDE INTERVAL OF ROBOT !!!
        self.timer += 20

        if self.timer > self.interval:
            if self.on:  # epsilon
                self.light.light.set(0.0)
                self.repeatAmount -= 1
            else:
                self.light.light.set(1.0)
            self.on = not self.on
            self.timer = self.timer % self.interval  # if go over take the remainder

    def isFinished(self) -> bool:
        return (not self.on) and (self.repeatAmount < 0) and (self.timer - 0.1 <= 0)

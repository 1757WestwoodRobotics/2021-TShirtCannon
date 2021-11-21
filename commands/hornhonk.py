import typing
from subsystems.hornsubsystem import HornSubsystem
from commands2 import CommandBase


class HornHonk(CommandBase):
    def __init__(self, horn: HornSubsystem, amount: typing.Callable[[], float]) -> None: 
        CommandBase.__init__(self)
        self.horn = horn
        self.hornStrength = amount

        self.hornOutput = lambda strength: self.horn.horn.set(strength)

        self.setName(__class__.__name__)
        self.addRequirements([self.horn])

    def execute(self) -> None:

        self.horn.horn.set(self.hornOutput())

    def end(self, interrupted: bool) -> None:
        self.horn.horn.set(0.0)

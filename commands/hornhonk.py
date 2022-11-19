from subsystems.hornsubsystem import HornSubsystem
from commands2 import CommandBase


class HornHonk(CommandBase):
    def __init__(self, horn: HornSubsystem) -> None:
        CommandBase.__init__(self)
        self.horn = horn

        self.hornOutput = lambda strength: self.horn.horn.set(strength)

        self.setName(__class__.__name__)
        self.addRequirements([self.horn])

    def execute(self) -> None:
        self.hornOutput(1.0)

    def end(self, interrupted: bool) -> None:
        self.hornOutput(0.0)

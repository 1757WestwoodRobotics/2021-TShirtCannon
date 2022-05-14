from enum import Enum, auto
from subsystems.cannonsubsystem import CannonSubsystem
from commands2 import CommandBase


class SetCannon(CommandBase):
    class Mode(Enum):
        Off = auto()
        Fill = auto()
        Launch = auto()

    def __init__(self, cannon: CannonSubsystem, mode: Mode) -> None:
        CommandBase.__init__(self)
        self.setName(__class__.__name__)
        self.cannon = cannon
        self.mode = mode
        self.addRequirements([self.cannon])

        self.funcs = {
            SetCannon.Mode.Off: self.cannon.close,
            SetCannon.Mode.Fill: self.cannon.fill,
            SetCannon.Mode.Launch: self.cannon.launch,
        }

        self.isFinished = lambda: True

    def execute(self) -> None:
        self.funcs[self.mode]()

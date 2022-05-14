from subsystems.lightsubsystem import LightSubsystem
import typing
from commands2 import CommandBase


class RelayControl(CommandBase):
    def __init__(
        self, controller: LightSubsystem, controlPercent: typing.Callable[[], float]
    ) -> None:
        CommandBase.__init__(self)
        self.control = controller
        self.controlPercentCommand = controlPercent

        self.setOutputPercent = lambda percent: self.control.light.set(percent)

        self.addRequirements([self.control])
        self.setName(__class__.__name__)

    def execute(self) -> None:
        self.setOutputPercent(self.controlPercentCommand())

    def end(self, interrupted: bool) -> None:
        self.setOutputPercent(0.0)

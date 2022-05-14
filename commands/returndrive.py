import typing
from typing import Tuple
from commands2 import CommandBase
from subsystems.drivesubsystem import DriveSubsystem
from math import sqrt


class ReturnDrive(CommandBase):
    def __init__(
        self,
        drive: DriveSubsystem,
        scaler: typing.Callable[[], float],
        rotation: typing.Callable[[], float],
    ) -> None:
        CommandBase.__init__(self)
        self.setName(__class__.__name__)

        self.drive = drive
        self.scaler = scaler
        self.rotation = rotation

        self.addRequirements([self.drive])
        self.setName(__class__.__name__)

    def Deadband(self, input: float, deadband: float) -> float:
        if abs(input) <= deadband:
            return 0
        else:
            return input

    def normalize(self, x: float, y: float) -> Tuple[float, float]:
        length = sqrt(pow(x, 2) + pow(y, 2))

        if length == 0:
            return 0, 0
        elif length <= 1:
            return x, y
        return x / length, y / length

    def getDirection(self) -> Tuple[float, float]:

        returnPos = self.drive.returnPos
        currentPos = self.drive.odometry.getPose()

        xDelta = currentPos.X() - returnPos.X()
        yDelta = currentPos.Y() - returnPos.Y()

        return self.normalize(float(xDelta * -1), float(yDelta * -1))

    def execute(self) -> None:

        deadband = 0.1

        self.drive.arcadeDriveWithFactors(
            self.Deadband(self.getDirection()[0], deadband) * self.scaler(),
            self.Deadband(self.getDirection()[1], deadband) * self.scaler(),
            self.rotation() * -1,
            DriveSubsystem.CoordinateMode.FieldRelative,
        )

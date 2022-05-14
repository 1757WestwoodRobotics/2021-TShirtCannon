import typing
from commands2 import CommandBase
from subsystems.drivesubsystem import DriveSubsystem
from networktables import NetworkTables


class DefaultDrive(CommandBase):
    def __init__(
        self,
        drive: DriveSubsystem,
        forward: typing.Callable[[], float],
        sideways: typing.Callable[[], float],
        rotation: typing.Callable[[], float],
    ) -> None:
        CommandBase.__init__(self)
        self.setName(__class__.__name__)

        self.drive = drive
        self.forward = forward
        self.sideways = sideways
        self.rotation = rotation

        self.addRequirements([self.drive])
        self.setName(__class__.__name__)

    def execute(self) -> None:
        NetworkTables.getTable("limelight").putNumber("ledMode", 1)
        self.drive.arcadeDriveWithFactors(
            self.forward(),
            self.sideways(),
            self.rotation(),
            DriveSubsystem.CoordinateMode.RobotRelative,
        )

from commands2 import CommandBase
from wpimath.geometry._geometry import Pose2d

from subsystems.drivesubsystem import DriveSubsystem


class ResetDrive(CommandBase):
    def __init__(self, drive: DriveSubsystem) -> None:
        CommandBase.__init__(self)
        self.setName(__class__.__name__)
        self.drive = drive
        self.addRequirements(drive)

    def initialize(self) -> None:
        print("Command: {}".format(self.getName()))
        self.drive.returnPos = self.drive.shiftPoint(self.drive.returnPos, self.drive.odometry.getPose())

    def execute(self) -> None:
        self.drive.resetSwerveModules()

    def end(self, interrupted: bool) -> None:
        print("... DONE")

    def isFinished(self) -> bool:
        return True

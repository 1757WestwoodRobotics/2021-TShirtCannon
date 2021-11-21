from commands2 import CommandBase
from subsystems.drivesubsystem import DriveSubsystem
from networktables import NetworkTable

class TargetDrive(CommandBase):
    def __init__(self, drive: DriveSubsystem, table: NetworkTable) -> None:
        CommandBase.__init__(self)

        self.drive = drive
        self.table = table

        self.addRequirements([self.drive])
        self.setName(__class__.__name__)

    def execute(self) -> None:
        if not self.table.getNumber('ty'):
            #rotate in place slowly
            self.table.putNumber("ledMode", 2)
            self.drive.arcadeDriveWithFactors(0, 0, 0.25, DriveSubsystem.CoordinateMode.RobotRelative)
        else:
            #get distance of object from center (tx) rotate towards it
            #move to object, scale speed based on how close objeect is (based on target size, ta)
            pass
    def end(self) -> None:
        self.table.putNumber("ledMode", 1)
from commands2 import CommandBase
from subsystems.cameracontroller import CameraSubsystem
from subsystems.drivesubsystem import DriveSubsystem
from networktables import NetworkTable

class TargetDrive(CommandBase):
    def __init__(self, drive: DriveSubsystem, table: NetworkTable, camera: CameraSubsystem) -> None:
        CommandBase.__init__(self)

        self.drive = drive
        self.table = table
        self.camera = camera

        self.addRequirements([self.drive])
        self.setName(__class__.__name__)

    def Deadband(self, input: float, deadband: float) -> float:
        if abs(input) <= deadband:
            return 0
        else:
            return input

    def execute(self) -> None:

        #set camera level to ground 
        #alternate solution: find PWM value and hard set
        pitch = self.table.getNumberArray("camtran")[4]
        self.camera.setCameraRotation(0, self.camera.upDown.get() + self.Deadband(pitch * -1, 0.1))

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
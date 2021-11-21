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
        pitch = self.table.getNumberArray("camtran", [0, 0, 0, 0, 0, 0])[4]
        self.camera.setCameraRotation(0, self.camera.upDown.get() + self.Deadband(pitch * -1, 0.1))

        if not self.table.getNumber('ty', 0):
            #blink limelight
            self.table.putNumber("ledMode", 2)
            
            #rotate in place slowly
            self.drive.arcadeDriveWithFactors(0, 0, 0.25, DriveSubsystem.CoordinateMode.RobotRelative)
        else:
            #TODO: compensate for latency, adjust scaling and deadband
            
            #set limelight on
            self.table.putNumber("ledMode", 3)

            #get distance of object from center (tx), scale rotation based on how far object from center -27 to 27 degrees
            xDistance = self.table.getNumber("tx", 0)
            rotation = self.Deadband(xDistance/5, 0.1)

            #move to object, scale speed based on how close object is and on how much it needs to rotate (based on target size, ta, and distance from center, tx)
            speedScale = 1 - abs(xDistance)/27
            objSize = self.table.getNumber("ta", 100)
            speed = min(1, self.Deadband(25/objSize * speedScale, 0.5))
            self.drive.arcadeDriveWithFactors(speed, 0, rotation, DriveSubsystem.CoordinateMode.RobotRelative)

    def end(self, interrupted: bool) -> None:
        #turn off limelight
        self.table.putNumber("ledMode", 1)
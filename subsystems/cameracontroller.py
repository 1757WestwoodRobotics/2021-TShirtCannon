from commands2 import SubsystemBase
from wpilib import PWMMotorController, RobotBase
import constants


class CameraSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.leftRight = PWMMotorController(
            "Camera X",
            constants.kPWMCameraSwerveLeftRight
            if RobotBase.isReal()
            else constants.kPWMCameraSimSwerveLeftRight,
        )
        self.upDown = PWMMotorController(
            "Camera Y",
            constants.kPWMCameraSwerveUpDown
            if RobotBase.isReal()
            else constants.kPWMCameraSimSwerveUpDown,
        )

        self.leftRight.setInverted(constants.kPWMCameraLeftRightInverted)
        self.upDown.setInverted(constants.kPWMCameraUpDownInverted)

    def setCameraRotation(self, x: float, y: float):
        self.leftRight.set(x)
        self.upDown.set(y)

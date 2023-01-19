from commands2 import CommandBase
from wpilib import SmartDashboard

from subsystems.armsubsystem import ArmSubsystem

import constants


class SetArmPosition(CommandBase):
    def __init__(self, arm: ArmSubsystem) -> None:
        CommandBase.__init__(self)
        self.setName(__class__.__name__)
        self.arm = arm
        self.addRequirements([self.arm])

    def execute(self) -> None:
        self.armAngle = SmartDashboard.getNumber(constants.kArmTargetDegreesKey, 550)
        self.arm.setArmAngle(self.armAngle)

    def end(self, _interrupted: bool) -> None:
        print("SUSSY ENDING (no imposters)s")
        SmartDashboard.putBoolean(constants.kArmMovingOnKey, False)
    
    def isFinished(self) -> bool:
        # if (
        #     (x:= abs(
        #         (
        #             self.arm.armMotor.getSelectedSensorPosition()
        #             - self.arm.convertToEncoderTicks(self.armAngle)
        #         )
        #     ))
        #     < constants.kArmPositionThreshold
        # ) :
        #     print("SIS")
        #     return True
        # print(x)
        return False

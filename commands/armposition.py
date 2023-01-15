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
        armAngle = SmartDashboard.getNumber(constants.kArmTargetDegreesKey, 550)
        self.arm.setArmAngle(armAngle)

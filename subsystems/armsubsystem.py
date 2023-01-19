from wpilib import SmartDashboard
from ctre import ControlMode
from util.ctrecheck import ctreCheckError
from util.simfalcon import createMotor
import constants
from commands2 import SubsystemBase


class ArmSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)
        self.setName(__class__.__name__)
        self.armMotor = createMotor(constants.kArmMotorID)
        if not ctreCheckError(
            "configFactoryDefault",
            self.armMotor.configFactoryDefault(
                constants.kConfigurationTimeoutLimit
            ),
        ):
            return
        if not ctreCheckError(
            "config_kP",
            self.armMotor.config_kP(
                constants.kArmMotorPIDSlot,
                constants.kArmMotorPGain,
                constants.kConfigurationTimeoutLimit,
            ),
        ):
            return
        if not ctreCheckError(
            "config_kI",
            self.armMotor.config_kI(
                constants.kArmMotorPIDSlot,
                constants.kArmMotorIGain,
                constants.kConfigurationTimeoutLimit,
            ),
        ):
            return
        if not ctreCheckError(
            "config_kD",
            self.armMotor.config_kD(
                constants.kArmMotorPIDSlot,
                constants.kArmMotorDGain,
                constants.kConfigurationTimeoutLimit,
            ),
        ):
            return
        if not ctreCheckError(
            "config_Invert",
            self.armMotor.setInverted(constants.kArmMotorInversion),
        ):
            return
        self.armMotor.configReverseSoftLimitThreshold(
            constants.kArmSafeDistanceEncoderTicks
        )
        self.armMotor.configReverseSoftLimitEnable(True)
    
    def convertToEncoderTicks(self, degrees) -> int:
        encoderTicks = (degrees * constants.kTalonEncoderPulsesPerRevolution * constants.kArmGearRatio * constants.kArmPulleyRatio) / (constants.kDegeersPerRevolution)
        return encoderTicks


    def setArmAngle(self, degrees) -> None:
        encoderTicks = self.convertToEncoderTicks(degrees)
        self.armMotor.set(
            ControlMode.Position, encoderTicks
        )
    
    def periodic(self) -> None:
        SmartDashboard.putNumber(
            constants.kArmEncoderTicksKey,
            self.armMotor.getSelectedSensorPosition(),
        )
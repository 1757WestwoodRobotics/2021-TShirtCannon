from commands2 import SubsystemBase
from ctre import WPI_TalonSRX
import constants


class HornSubsystem(SubsystemBase):
    def __init__(self) -> None:
        SubsystemBase.__init__(self)

        self.horn = WPI_TalonSRX(constants.kHornControllerDeviceID)
    
    

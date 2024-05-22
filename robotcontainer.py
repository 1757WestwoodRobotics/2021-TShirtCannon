from wpilib import Compressor, PneumaticsModuleType
from commands.absoluterelativedrive import AbsoluteRelativeDrive
from commands.blinklight import BlinkLight
from commands2 import ParallelCommandGroup
from commands.hornhonk import HornHonk
from commands.pulselight import PulseLight
from commands.setcannon import SetCannon
from subsystems.cannonsubsystem import CannonSubsystem
from subsystems.hornsubsystem import HornSubsystem
from subsystems.lightsubsystem import LightSubsystem
import wpilib

import commands2
import commands2.button
from commands.varyoutput import RelayControl

import constants

from commands.complexauto import ComplexAuto
from commands.drivedistance import DriveDistance
from commands.fieldrelativedrive import FieldRelativeDrive
from commands.resetdrive import ResetDrive

from commands.returndrive import ReturnDrive

from commands.setreturn import SetReturn

from subsystems.drivesubsystem import DriveSubsystem

from operatorinterface import OperatorInterface
from util.helpfultriggerwrappers import ModifiableJoystickButton


class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:

        # The operator interface (driver controls)
        self.operatorInterface = OperatorInterface()

        # The robot's subsystems
        self.drive = DriveSubsystem()
        self.cannon = CannonSubsystem()
        self.light = LightSubsystem()
        self.horn = HornSubsystem()
        # self.log = SystemLogSubsystem()

        # compressor
        self.compressor = Compressor(
            constants.kPCMCannonCanID, PneumaticsModuleType.CTREPCM
        )

        # horn
        # self.light = wpilib.(constants.kHornPWMPinLocation)
        # self.light2 = wpilib.Spark(constants.kHorn2PWMPinLocation)
        # self.light.setRaw(65535) #turn off horn by default
        # self.light2.setRaw(65535)
        # Autonomous routines
        # A simple auto routine that drives forward a specified distance, and then stops.

        self.simpleAuto = DriveDistance(
            constants.kAutoDriveDistance,
            constants.kAutoDriveSpeedFactor,
            DriveDistance.Axis.X,
            self.drive,
        )

        # A complex auto routine that drives forward, right, back, left
        self.complexAuto = ComplexAuto(self.drive)

        # Chooser
        self.chooser = wpilib.SendableChooser()

        # Add commands to the autonomous command chooser
        self.chooser.setDefaultOption("Simple Auto", self.simpleAuto)
        self.chooser.addOption("Complex Auto", self.complexAuto)

        # Put the chooser on the dashboard
        wpilib.SmartDashboard.putData("Autonomous", self.chooser)

        self.configureButtonBindings()

        self.drive.setDefaultCommand(
            FieldRelativeDrive(
                self.drive,
                self.operatorInterface.chassisControls.forwardsBackwards,
                self.operatorInterface.chassisControls.sideToSide,
                self.operatorInterface.chassisControls.rotationX,
            )
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        ModifiableJoystickButton(
            self.operatorInterface.coordinateModeControl
        ).whileHeld(
            FieldRelativeDrive(
                self.drive,
                self.operatorInterface.chassisControls.forwardsBackwards,
                self.operatorInterface.chassisControls.sideToSide,
                self.operatorInterface.chassisControls.rotationX,
            )
        )

        ModifiableJoystickButton(self.operatorInterface.resetSwerveControl).whenPressed(
            ResetDrive(self.drive)
        )

        ModifiableJoystickButton(self.operatorInterface.fillCannon).whenPressed(
            SetCannon(self.cannon, SetCannon.Mode.Fill)
        )

        ModifiableJoystickButton(self.operatorInterface.launchCannon).whenPressed(
            SetCannon(self.cannon, SetCannon.Mode.Launch)
        )

        ModifiableJoystickButton(
            self.operatorInterface.returnPositionInput
        ).whenPressed(SetReturn(self.drive))

        ModifiableJoystickButton(self.operatorInterface.closeValves).whenPressed(
            SetCannon(self.cannon, SetCannon.Mode.Off)
        )

        ModifiableJoystickButton(self.operatorInterface.returnModeControl).whileHeld(
            ParallelCommandGroup(
                ReturnDrive(
                    self.drive,
                    self.operatorInterface.chassisControls.rotationX,
                ),
                BlinkLight(self.light, 1, 100),
            )
        )

        ModifiableJoystickButton(
            self.operatorInterface.pulseTheLights
        ).toggleWhenPressed(ParallelCommandGroup(PulseLight(self.light, 500, False)))

        ModifiableJoystickButton(self.operatorInterface.hornControl).whileHeld(
            HornHonk(self.horn)
        )

        ModifiableJoystickButton(self.operatorInterface.lightControl).whileHeld(
            RelayControl(self.light, lambda: 1.0)
        )

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()

from wpilib import Compressor
from wpilib._wpilib import PneumaticsModuleType
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
from commands.rotatecamera import RotateCamera

import constants

from commands.complexauto import ComplexAuto
from commands.drivedistance import DriveDistance
from commands.defaultdrive import DefaultDrive
from commands.fieldrelativedrive import FieldRelativeDrive
from commands.resetdrive import ResetDrive
from subsystems.cameracontroller import CameraSubsystem

from commands.returndrive import ReturnDrive

from commands.setreturn import SetReturn

from subsystems.drivesubsystem import DriveSubsystem

from operatorinterface import OperatorInterface


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
        self.camera = CameraSubsystem()
        self.cannon = CannonSubsystem()
        self.light = LightSubsystem()
        self.horn = HornSubsystem()

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
            DefaultDrive(
                self.drive,
                self.operatorInterface.chassisControls.forwardsBackwards,
                self.operatorInterface.chassisControls.sideToSide,
                self.operatorInterface.chassisControls.rotation,
            )
        )

        self.camera.setDefaultCommand(
            RotateCamera(
                self.camera,
                self.operatorInterface.cameraControls.leftRight,
                self.operatorInterface.cameraControls.upDown,
            )
        )

        # self.cannon.setDefaultCommand(
        #     SetCannon(self.cannon, SetCannon.Mode.Off))
        self.light.setDefaultCommand(
            RelayControl(self.light, self.operatorInterface.lightControl)
        )

        self.horn.setDefaultCommand(
            HornHonk(self.horn, self.operatorInterface.hornControl)
        )

    def configureButtonBindings(self):
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """
        commands2.button.JoystickButton(
            *self.operatorInterface.coordinateModeControl
        ).whileHeld(
            FieldRelativeDrive(
                self.drive,
                self.operatorInterface.chassisControls.forwardsBackwards,
                self.operatorInterface.chassisControls.sideToSide,
                self.operatorInterface.chassisControls.rotation,
            )
        )

        commands2.button.JoystickButton(
            *self.operatorInterface.resetSwerveControl
        ).whenPressed(ResetDrive(self.drive))

        commands2.button.JoystickButton(*self.operatorInterface.fillCannon).whenPressed(
            SetCannon(self.cannon, SetCannon.Mode.Fill)
        )

        commands2.button.JoystickButton(
            *self.operatorInterface.launchCannon
        ).whenPressed(SetCannon(self.cannon, SetCannon.Mode.Launch))

        commands2.button.POVButton(
            *self.operatorInterface.returnPositionInput
        ).whenPressed(SetReturn(self.drive))

        commands2.button.JoystickButton(
            *self.operatorInterface.closeValves
        ).whenPressed(SetCannon(self.cannon, SetCannon.Mode.Off))

        commands2.button.POVButton(*self.operatorInterface.returnModeControl).whileHeld(
            ParallelCommandGroup(
                ReturnDrive(
                    self.drive,
                    self.operatorInterface.scaler,
                    self.operatorInterface.chassisControls.rotation,
                ),
                BlinkLight(self.light, 1, 100),
            )
        )

        commands2.button.POVButton(
            *self.operatorInterface.pulseTheLights
        ).toggleWhenPressed(ParallelCommandGroup(PulseLight(self.light, 500, False)))

        # commands2.button.JoystickButton(
        #     *self.operatorInterface.honkControl
        # ).whileHeld(HornHonk(self.light2))

    def getAutonomousCommand(self) -> commands2.Command:
        return self.chooser.getSelected()

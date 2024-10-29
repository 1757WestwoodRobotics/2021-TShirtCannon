from os import path
from wpilib import Joystick, RobotBase, Preferences

import typing
import json

import constants
from subsystems.cannonsubsystem import map_range

AnalogInput = typing.Callable[[], float]


def Deadband(input: AnalogInput, deadband: float) -> AnalogInput:
    """take a function and reture a function which if below a threshold returns 0"""

    def withDeadband() -> float:
        value = input()
        if abs(value) <= deadband:
            return 0
        else:
            return value

    return withDeadband


def Abs(input: AnalogInput) -> AnalogInput:
    """takes a function and returns the absolute value of that function"""

    def absolute() -> float:
        inp = input()
        return -1 * inp if inp < 0 else inp

    return absolute


def Invert(input: AnalogInput) -> AnalogInput:
    """inverts the output of a function"""

    def invert() -> float:
        return -1 * input()

    return invert


class CameraControl:
    """class to contain the data related to controlling a camera"""

    def __init__(self, leftRight: AnalogInput, upDown: AnalogInput):
        self.leftRight = leftRight
        self.upDown = upDown


class HornControl:
    def __init__(self, amount: AnalogInput) -> None:
        self.amount = amount


class HolonomicInput:
    """class containing 3 axis of motion that make a system holonomic
    all values are functions"""

    def __init__(
        self,
        forwardsBackwards: AnalogInput,
        sideToSide: AnalogInput,
        rotationX: AnalogInput,
        rotationY: AnalogInput,
    ) -> None:
        self.forwardsBackwards = forwardsBackwards
        self.sideToSide = sideToSide
        self.rotationX = rotationX
        self.rotationY = rotationY


class OperatorInterface:
    """
    The controls that the operator(s)/driver(s) interact with
    """

    def __init__(self) -> None:

        with open(
            path.join(path.dirname(path.realpath(__file__)), "controlInterface.json"),
            "r",
        ) as file:
            controlScheme = json.load(
                file
            )  # get the generau control scheme defined in controlInterface.json

        with open(
            path.join(path.dirname(path.realpath(__file__)), "controlInterface.json"),
            "r",
            encoding="utf-8",
        ) as file:
            controlScheme = json.load(file)

        controllerNumbers = set([0, 1, 2, 3, 4, 5])  # set ensures no duplicates
        print(f"Looking for controllers: {controllerNumbers} ...")

        controllers = {}

        self.prefs = Preferences

        for control in controlScheme:
            binding = controlScheme[control]
            self.prefs.setInt(control + " controller", binding[0])
            if "Button" in binding[1].keys():
                self.prefs.setInt(control + " button", binding[1]["Button"])
            elif "Axis" in binding[1].keys():
                self.prefs.setInt(control + " axis", binding[1]["Axis"])

        for num in controllerNumbers:
            controller = Joystick(num)
            print(
                f"Found Controller {num}:{controller.getName()}\n\tAxis: {controller.getAxisCount()}\n\tButtons: {controller.getButtonCount()}\n\tPoV Hats: {controller.getPOVCount()}"
            )
            controllers[num] = controller

        def getButtonBindingOfName(
            name: str,
        ) -> typing.Callable[[], typing.Tuple[Joystick, int]]:
            return lambda: (
                controllers[self.prefs.getInt(name + " controller")],
                self.prefs.getInt(name + " button"),
            )

        def getAxisBindingOfName(name: str) -> AnalogInput:
            return lambda: controllers[
                self.prefs.getInt(name + " controller")
            ].getRawAxis(self.prefs.getInt(name + " axis"))

        self.returnPositionInput = getButtonBindingOfName("returnPositionInput")
        self.returnModeControl = getButtonBindingOfName("returnModeControl")
        self.pulseTheLights = getButtonBindingOfName("pulseTheLights")

        self.fillCannon = getButtonBindingOfName("fillCannon")
        self.launchCannon = getButtonBindingOfName("launchCannon")
        self.closeValves = getButtonBindingOfName("closeValves")

        self.coordinateModeControl = getButtonBindingOfName("coordinateModeControl")
        self.resetSwerveControl = getButtonBindingOfName("resetSwerveControl")

        self.lightControl = getButtonBindingOfName("lightControl")
        self.hornControl = getButtonBindingOfName("hornControl")

        self.chassisControls = HolonomicInput(  # drive controls, allows for any directional movement and rotation
            Invert(  # forwards / backwards
                Deadband(
                    getAxisBindingOfName("forwardsBackwards"),
                    constants.kXboxJoystickDeadband,
                )
            ),
            Invert(  # left / right
                Deadband(
                    getAxisBindingOfName("leftRight"),
                    constants.kXboxJoystickDeadband,
                )
            ),
            Invert(
                Deadband(  # rotational X movement
                    getAxisBindingOfName("rotationX"),
                    constants.kXboxJoystickDeadband,
                )
            ),
            Invert(
                Deadband(  # rotational Y movement
                    getAxisBindingOfName("rotationY"),
                    constants.kXboxJoystickDeadband,
                )
            ),
        )

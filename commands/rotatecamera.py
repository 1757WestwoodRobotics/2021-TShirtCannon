import typing
from commands2 import CommandBase

from subsystems.cameracontroller import CameraSubsystem


class RotateCamera(CommandBase):
    def __init__(
        self,
        camera: CameraSubsystem,
        leftRight: typing.Callable[[], float],
        upDown: typing.Callable[[], float],
    ) -> None:
        CommandBase.__init__(self)
        self.setName(__class__.__name__)

        self.camera = camera
        self.leftRight = leftRight
        self.upDown = upDown

        self.addRequirements([self.camera])
        self.setName(__class__.__name__)

    def execute(self) -> None:
        self.camera.setCameraRotation(self.leftRight(), self.upDown())

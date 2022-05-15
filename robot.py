#!/usr/bin/env python3

from os import environ, path
import typing

from networktables import NetworkTables
import wpilib
import commands2

from robotcontainer import RobotContainer

import constants

import asyncio
import json
import time
from foxglove_websocket import run_cancellable
from foxglove_websocket.server import FoxgloveServer, FoxgloveServerListener
from foxglove_websocket.types import ChannelId

from util.convenietmath import get_quaternion_from_euler


class MentorBot(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run

    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """

        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomousCommand:
            self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()


async def foxglove():
    print("initialization of foxglove...")

    class Listener(FoxgloveServerListener):
        def on_subscribe(self, server: FoxgloveServer, channel_id: ChannelId):
            print("First client subscribed to", channel_id)

        def on_unsubscribe(self, server: FoxgloveServer, channel_id: ChannelId):
            print("Last client unsubscribed from", channel_id)

    async with FoxgloveServer("0.0.0.0", 8765, "Robot Server") as server:
        serv_var = environ.get("SERVER")
        NetworkTables.initialize(
            server=serv_var if serv_var != None else "roborio-1757-frc.local"
        )
        table = NetworkTables.getTable("/SmartDashboard") if environ.get("SERVER") != None else wpilib.SmartDashboard
        server.set_listener(Listener())
        robot_pose = await server.add_channel(
            {
                "topic": "/robot_pose",
                "encoding": "json",
                "schemaName": "geometry_msgs/PoseStamped",
            }
        )

        cannon_state = await server.add_channel(
            {
                "topic": "/cannon_state",
                "encoding": "json",
                "schemaName": "CannonState",
                "schema": json.dumps(
                    {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number"},
                            "pressure": {"type": "number"},
                        },
                    }
                ),
            }
        )

        markers = await server.add_channel(
            {
                "topic": "/markers",
                "encoding": "json",
                "schemaName": "visualization_msgs/MarkerArray",
            }
        )

        while True:
            await asyncio.sleep(0.01)
            [x, y, theta] = table.getNumberArray(
                constants.kRobotPoseArrayKeys, [0, 0, 0]
            )

            rot = get_quaternion_from_euler(0, 0, theta)
            await server.send_message(
                robot_pose,
                time.time_ns(),
                json.dumps(
                    {
                        "header": {
                            "seq": 0,
                            "stamp": {
                                "sec": int(time.time()),
                                "nsec": time.time_ns() % 1000,
                            },
                            "frame_id": "base_link",
                        },
                        "pose": {
                            "position": {"x": x, "y": y, "z": 0},
                            "orientation": {
                                "x": rot[0],
                                "y": rot[1],
                                "z": rot[2],
                                "w": rot[3],
                            },
                        },
                    }
                ).encode("utf8"),
            )

            await server.send_message(
                cannon_state,
                time.time_ns(),
                json.dumps(
                    {
                        "value": table.getNumber(constants.kCannonStateKey, 0),
                        "pressure": table.getNumber(constants.kPressureKey, 0),
                    }
                ).encode("utf8"),
            )

            await server.send_message(
                markers,
                time.time_ns(),
                json.dumps(
                    {
                        "markers": [
                            {
                                "header": {
                                    "seq": 1,
                                    "stamp": {
                                        "sec": int(time.time()),
                                        "nsec": time.time_ns() % 1000,
                                    },
                                    "frame_id": "base_link",
                                },
                                "ns": "base_link",
                                "id": 1,
                                "type": 1,
                                "action": 0,
                                "pose": {
                                    "position": {"x": 54 / 4, "y": 27 / 4, "z": -0.25},
                                    "orientation": {
                                        "x": 0,
                                        "y": 0,
                                        "z": 0,
                                        "w": 1,
                                    },
                                },
                                "scale": {
                                    "x": 54/2,
                                    "y": 27/2,
                                    "z": 0.5,
                                },
                                "color": {
                                    "r": 1,
                                    "g": 0,
                                    "b": 0,
                                    "a": 0.5,
                                },
                                "lifetime": 1,
                                "frame_locked": False,
                            }
                        ]
                    }
                ).encode("utf8"),
            )


async def run_async():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, wpilib.run, MentorBot)


async def run_all():
    await asyncio.wait([run_async(), foxglove()])


if __name__ == "__main__":
    if environ.get("FOXGLOVE") != None:
        run_cancellable(foxglove())
    elif environ.get("ALL") != None:
        run_cancellable(run_all())
    else:
        wpilib.run(MentorBot)

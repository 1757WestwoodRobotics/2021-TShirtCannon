from math import sin, tau, floor, cos
from wpimath.geometry import Rotation2d


def optimizeAngle(currentAngle: Rotation2d, targetAngle: Rotation2d) -> Rotation2d:
    currentAngle = currentAngle.radians()

    closestFullRotation = (
        floor(abs(currentAngle / tau)) * (-1 if currentAngle < 0 else 1) * tau
    )

    currentOptimalAngle = targetAngle.radians() + closestFullRotation - currentAngle

    potentialNewAngles = [
        currentOptimalAngle,
        currentOptimalAngle - tau,
        currentOptimalAngle + tau,
    ]  # closest other options

    deltaAngle = tau  # max possible error, a full rotation!
    for potentialAngle in potentialNewAngles:
        if abs(deltaAngle) > abs(potentialAngle):
            deltaAngle = potentialAngle

    return Rotation2d(deltaAngle + currentAngle)


def get_quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.

    Input
      :param roll: The roll (rotation around x-axis) angle in radians.
      :param pitch: The pitch (rotation around y-axis) angle in radians.
      :param yaw: The yaw (rotation around z-axis) angle in radians.

    Output
      :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) - cos(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)
    qy = cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * cos(
        pitch / 2
    ) * sin(yaw / 2)
    qz = cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) - sin(roll / 2) * sin(
        pitch / 2
    ) * cos(yaw / 2)
    qw = cos(roll / 2) * cos(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * sin(
        pitch / 2
    ) * sin(yaw / 2)

    return [qx, qy, qz, qw]

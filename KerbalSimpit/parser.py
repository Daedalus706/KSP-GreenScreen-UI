from KerbalSimpit.const import *
from KerbalSimpit.message_structs import *

import struct


def parse_message(message_type:bytes, message:list[bytes]):
    try:
        match message_type:
            case OutboundPackets.ALTITUDE_MESSAGE:
                sealevel_altitude = struct.unpack('f', bytes(message[:4]))[0]
                surface_altitude = struct.unpack('f', bytes(message[4:]))[0]
                return AltitudeMessage(sealevel_altitude, surface_altitude)
            
            case OutboundPackets.VELOCITY_MESSAGE:
                orbital_velocity = struct.unpack('f', bytes(message[:4]))[0]
                surface_velocity = struct.unpack('f', bytes(message[4:8]))[0]
                vertical_velocity = struct.unpack('f', bytes(message[8:]))[0]
                return VelocityMessage(orbital_velocity, surface_velocity, vertical_velocity)

            case OutboundPackets.ORBIT_MESSAGE:
                eccentricity: float = struct.unpack('f', bytes(message[:4]))[0]
                semiMajorAxis: float = struct.unpack('f', bytes(message[4:8]))[0]
                inclination: float = struct.unpack('f', bytes(message[8:12]))[0]
                longAscendingNode: float = struct.unpack('f', bytes(message[12:16]))[0]
                argPeriapsis: float = struct.unpack('f', bytes(message[16:20]))[0]
                trueAnomaly: float = struct.unpack('f', bytes(message[20:24]))[0]
                meanAnomaly: float = struct.unpack('f', bytes(message[24:28]))[0]
                period: float = struct.unpack('f', bytes(message[28:]))[0]
                return OrbitInfoMessage(eccentricity, semiMajorAxis, inclination, longAscendingNode, argPeriapsis, trueAnomaly, meanAnomaly, period)
            
            case OutboundPackets.ROTATION_DATA_MESSAGE:
                heading: float = struct.unpack('f', bytes(message[:4]))[0]
                pitch: float = struct.unpack('f', bytes(message[4:8]))[0]
                roll: float = struct.unpack('f', bytes(message[8:12]))[0]
                orbitalVelocityHeading: float = struct.unpack('f', bytes(message[12:16]))[0]
                orbitalVelocityPitch: float = struct.unpack('f', bytes(message[16:20]))[0]
                surfaceVelocityHeading: float = struct.unpack('f', bytes(message[20:24]))[0]
                surfaceVelocityPitch: float = struct.unpack('f', bytes(message[24:]))[0]
                return VesselPointingMessage(heading, pitch, roll, orbitalVelocityHeading, orbitalVelocityPitch, surfaceVelocityHeading, surfaceVelocityPitch)
            
            case OutboundPackets.CAGSTATUS_MESSAGE:
                return CagStatusMessage(message)
            
            case OutboundPackets.LF_MESSAGE:
                total:float = struct.unpack('f', bytes(message[:4]))[0]
                available:float = struct.unpack('f', bytes(message[4:]))[0]
                return ResourceMessage(total, available)
            
            case OutboundPackets.THROTTLE_CMD_MESSAGE:
                throttle:int = struct.unpack('H', bytes(message[:2]))[0]
                return ThrottleMessage(throttle)

            case _:
                raise ValueError(f"Unhandled message type: {message_type}, {message}")
            
    except Exception as e:
        print("Error in parse_message:", e)
from dataclasses import dataclass
from KerbalSimpit.const import FligthStatusFlags, AtmoConditionsFlags

@dataclass
class AltitudeMessage:
    sealevel: float
    surface: float

@dataclass
class ApsidesMessage:
    periapsis: float
    apoapsis: float

@dataclass
class ApsidesTimeMessage:
    periapsis: int  # Seconds to periapsis
    apoapsis: int   # Seconds to apoapsis

@dataclass
class OrbitInfoMessage:
    eccentricity: float
    semiMajorAxis: float
    inclination: float
    longAscendingNode: float
    argPeriapsis: float
    trueAnomaly: float
    meanAnomaly: float
    period: float

class FlightStatusMessage:
    def __init__(self,
                 flightStatusFlags: int,
                 vesselSituation: int,
                 currentTWIndex: int,
                 crewCapacity: int,
                 crewCount: int,
                 commNetSignalStrenghPercentage: int,
                 currentStage: int,
                 vesselType: int
                 ) -> None:
        self.flightStatusFlags = flightStatusFlags
        self.vesselSituation = vesselSituation
        self.currentTWIndex = currentTWIndex
        self.crewCapacity = crewCapacity
        self.crewCount = crewCount
        self.commNetSignalStrenghPercentage = commNetSignalStrenghPercentage
        self.currentStage = currentStage
        self.vesselType = vesselType

    def isInFlight(self) -> bool:
        return self.flightStatusFlags & FligthStatusFlags.FLIGHT_IN_FLIGHT != 0
    
    def isInEVA(self):
         return self.flightStatusFlags & FligthStatusFlags.FLIGHT_IS_EVA != 0
    
    def isRecoverable(self) -> bool:
        return self.flightStatusFlags & FligthStatusFlags.FLIGHT_IS_RECOVERABLE != 0
    
    def isInAtmoTW(self) -> bool:
        return self.flightStatusFlags & FligthStatusFlags.FLIGHT_IS_ATMO_TW != 0
    
    def getControlLevel(self) -> bool:
        """ Returns the current control level. 0 for no control, 1 for partially unmanned, 2 for partially manned, 3 for full control. """
        return ((self.flightStatusFlags >> 4) & 3) != 0
    
    def hasTarget(self) -> bool:
        return self.flightStatusFlags & FligthStatusFlags.FLIGHT_HAS_TARGET != 0


class AtmoConditionsMessage:
    def __init__(self,
                 atmoCharacteristics:int,
                 airDensity:float,
                 temperature:float,
                 pressure:float
                 ) -> None:
        self.atmoCharacteristics = atmoCharacteristics
        self.airDensity = airDensity
        self.temperature = temperature
        self.pressure = pressure 

    def hasAtmosphere(self) -> bool:
        return self.atmoCharacteristics & AtmoConditionsFlags.HAS_ATMOSPHERE != 0
    
    def hasOxygen(self) -> bool:
        return self.atmoCharacteristics & AtmoConditionsFlags.HAS_OXYGEN != 0

    def isVesselInAtmosphere(self) -> bool:
        return self.atmoCharacteristics & AtmoConditionsFlags.IS_IN_ATMOSPHERE != 0


@dataclass
class ResourceMessage:
    total: float
    available: float

@dataclass
class VelocityMessage:
    orbital: float
    surface: float
    vertical: float

@dataclass
class AirspeedMessage:
    IAS: float
    mach: float
    gForce: float


@dataclass
class VesselPointingMessage:
    heading: float
    pitch: float
    roll: float
    orbitalVelocityHeading: float
    orbitalVelocityPitch: float
    surfaceVelocityHeading: float
    surfaceVelocityPitch: float

class CagStatusMessage:
    def __init__(self, status:list[bytes]) -> None:
        self.status = status
    
    def is_action_activated(self, i:int) -> bool:
        return self.status[i//8] & 1<<(i%8) != 0
    
@dataclass
class ThrottleMessage:
    throttle: int
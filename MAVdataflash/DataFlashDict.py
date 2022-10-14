import polars as pl

__dtypes__ = {
    "a": pl.Utf8,
    "b": pl.Int64,
    "B": pl.Int64,
    "h": pl.Int64,
    "H": pl.Int64,
    "i": pl.Int64,
    "I": pl.Int64,
    "f": pl.Float64,
    "n": pl.Utf8,
    "N": pl.Utf8,
    "Z": pl.Utf8,
    "c": pl.Float64,
    "C": pl.Float64,
    "e": pl.Float64,
    "E": pl.Float64,
    "L": pl.Float64,
    "d": pl.Float64,
    "M": pl.Int64,
    "q": pl.Int64,
    "Q": pl.Int64,
    "DT": pl.Datetime(time_unit = "ms")
}

# dict of units of each column [Extract from FMTU]
__dunits__ = {
    '-': "" ,              # no units e.g. Pi, or a string
    '?': "UNKNOWN" ,       # Units which haven't been worked out yet....
    'A': "A" ,             # Ampere
    'a': "Ah" ,            # Ampere hours
    'd': "deg" ,           # of the angular variety, -180 to 180
    'b': "B" ,             # bytes
    'k': "deg/s" ,         # degrees per second. Degrees are NOT SI, but is some situations more user-friendly than radians
    'D': "deglatitude" ,   # degrees of latitude
    'e': "deg/s/s" ,       # degrees per second per second. Degrees are NOT SI, but is some situations more user-friendly than radians
    'E': "rad/s" ,         # radians per second
    'G': "Gauss" ,         # Gauss is not an SI unit, but 1 tesla = 10000 gauss so a simple replacement is not possible here
    'h': "degheading" ,    # 0.? to 359.?
    'i': "A.s" ,           # Ampere second
    'J': "W.s" ,           # Joule (Watt second)
    #  'l': "l" ,          # litres
    'L': "rad/s/s" ,       # radians per second per second
    'm': "m" ,             # metres
    'n': "m/s" ,           # metres per second
    #  'N', "N" ,          # Newton
    'o': "m/s/s" ,         # metres per second per second
    'O': "degC" ,          # degrees Celsius. Not SI, but Kelvin is too cumbersome for most users
    '%': "%" ,             # percent
    'S': "satellites" ,    # number of satellites
    's': "sec" ,             # seconds
    'q': "rpm" ,           # rounds per minute. Not SI, but sometimes more intuitive than Hertz
    'r': "rad" ,           # radians
    'U': "deglongitude" ,  # degrees of longitude
    'u': "ppm" ,           # pulses per minute
    'v': "V" ,             # Volt
    'P': "Pa" ,            # Pascal
    'w': "Ohm" ,           # Ohm
    'W': "Watt" ,          # Watt
    'X': "W.h" ,           # Watt hour
    'Y': "us" ,            # pulse width modulation in microseconds
    'z': "Hz" ,            # Hertz
    '#': "instance"        # (e.g.)Sensor instance number
}

# dict of multiplier of each column [Extract from FMTU]  
__dmultiplier__ = {
    '-': 1 ,       # no multiplier e.g. a string
    '?': 1 ,       # multipliers which haven't been worked out yet....
# <leave a gap here, just in case....>
    '2': 1e2 ,
    '1': 1e1 ,
    '0': 1e0 ,
    'A': 1e-1 ,
    'B': 1e-2 ,
    'C': 1e-3 ,
    'D': 1e-4 ,
    'E': 1e-5 ,
    'F': 1e-6 ,
    'G': 1e-7 ,
    'I': 1e-9 ,
# <leave a gap here, just in case....>
    '!': 3.6 , # (ampere*second => milliampere*hour) and (km/h => m/s)
    '/': 3600 , # (ampere*second => ampere*hour)
}

__event_id__ =  {
    10: "ARMED",
    11: "DISARMED",
    15: "AUTO_ARMED",
    17: "LAND_COMPLETE_MAYBE",
    18: "LAND_COMPLETE",
    28: "NOT_LANDED",
    19: "LOST_GPS",
    21: "FLIP_START",
    22: "FLIP_END",
    25: "SET_HOME",
    26: "SET_SIMPLE_ON",
    27: "SET_SIMPLE_OFF",
    29: "SET_SUPERSIMPLE_ON",
    30: "AUTOTUNE_INITIALISED",
    31: "AUTOTUNE_OFF",
    32: "AUTOTUNE_RESTART",
    33: "AUTOTUNE_SUCCESS",
    34: "AUTOTUNE_FAILED",
    35: "AUTOTUNE_REACHED_LIMIT",
    36: "AUTOTUNE_PILOT_TESTING",
    37: "AUTOTUNE_SAVEDGAINS",
    38: "SAVE_TRIM",
    39: "SAVEWP_ADD_WP",
    41: "FENCE_ENABLE",
    42: "FENCE_DISABLE",
    43: "ACRO_TRAINER_OFF",
    44: "ACRO_TRAINER_LEVELING",
    45: "ACRO_TRAINER_LIMITED",
    46: "GRIPPER_GRAB",
    47: "GRIPPER_RELEASE",
    49: "PARACHUTE_DISABLED",
    50: "PARACHUTE_ENABLED",
    51: "PARACHUTE_RELEASED",
    52: "LANDING_GEAR_DEPLOYED",
    53: "LANDING_GEAR_RETRACTED",
    54: "MOTORS_EMERGENCY_STOPPED",
    55: "MOTORS_EMERGENCY_STOP_CLEARED",
    56: "MOTORS_INTERLOCK_DISABLED",
    57: "MOTORS_INTERLOCK_ENABLED",
    58: "ROTOR_RUNUP_COMPLETE",
    59: "ROTOR_SPEED_BELOW_CRITICAL",
    60: "EKF_ALT_RESET",
    61: "LAND_CANCELLED_BY_PILOT",
    62: "EKF_YAW_RESET",
    63: "AVOIDANCE_ADSB_ENABLE",
    64: "AVOIDANCE_ADSB_DISABLE",
    65: "AVOIDANCE_PROXIMITY_ENABLE",
    66: "AVOIDANCE_PROXIMITY_DISABLE",
    67: "GPS_PRIMARY_CHANGED",
    71: "ZIGZAG_STORE_A",
    72: "ZIGZAG_STORE_B",
    73: "LAND_REPO_ACTIVE",
    74: "STANDBY_ENABLE",
    75: "STANDBY_DISABLE",
    80: "FENCE_FLOOR_ENABLE",
    81: "FENCE_FLOOR_DISABLE",
    85: "EK3_SOURCES_SET_TO_PRIMARY",
    86: "EK3_SOURCES_SET_TO_SECONDARY",
    87: "EK3_SOURCES_SET_TO_TERTIARY",
    90: "IRSPEED_PRIMARY_CHANGED",
    163: "SURFACED",
    164: "NOT_SURFACED",
    165: "BOTTOMED",
    166: "NOT_BOTTOMED"
}